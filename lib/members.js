// Member registry helpers: cookies, sessions, sign-in codes, forms.
// Sessions: the cookie holds a random token, the database its sha256. Codes: six digits,
// fifteen minutes, five attempts, three per email per hour. Sent through Resend.
import { page, esc, html } from "./shell.js";

export const SESSION_COOKIE = "gps_session";
export const PENDING_COOKIE = "gps_pending";
const SESSION_DAYS = 365, CODE_MINUTES = 15, CODE_ATTEMPTS = 5, CODES_PER_HOUR = 3;
const FROM = "GPS & Orgs Community <no-reply@gpsorgs.com>";
export const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

export const now = () => new Date().toISOString();
const plus = (ms) => new Date(Date.now() + ms).toISOString();
export const clean = (v, max) => String(v ?? "").replace(/\r\n?/g, "\n").trim().slice(0, max);
export const oneLine = (v, max) => clean(v, max).replace(/\s+/g, " ");

export function cookies(request) {
  const out = {};
  for (const part of (request.headers.get("cookie") || "").split(";")) {
    const i = part.indexOf("="); if (i > 0) out[part.slice(0, i).trim()] = decodeURIComponent(part.slice(i + 1).trim());
  }
  return out;
}
export function setCookie(name, value, maxAge) {
  return `${name}=${encodeURIComponent(value)}; Path=/; Max-Age=${maxAge}; HttpOnly; Secure; SameSite=Lax`;
}
export const clearCookie = (name) => setCookie(name, "", 0);

export function redirect(request, path, setCookies = []) {
  const h = new Headers({ Location: new URL(path, request.url).toString() });
  for (const c of setCookies) h.append("Set-Cookie", c);
  return new Response(null, { status: 303, headers: h });
}

export async function sha256(s) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, "0")).join("");
}
export function randomToken(bytes = 32) {
  const a = crypto.getRandomValues(new Uint8Array(bytes));
  return btoa(String.fromCharCode(...a)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
export function randomCode() {
  const n = crypto.getRandomValues(new Uint32Array(1))[0] % 1000000;
  return String(n).padStart(6, "0");
}

// Who is asking? null, or { email, member (may be null), badge (may be null), sessionHash }
export async function currentUser(request, env) {
  const raw = cookies(request)[SESSION_COOKIE];
  if (!raw) return null;
  const sessionHash = await sha256(raw);
  const s = await env.SIGNUPS.prepare("SELECT email, expires FROM sessions WHERE token_hash = ?").bind(sessionHash).first();
  if (!s || s.expires < now()) return null;
  const member = await env.SIGNUPS.prepare("SELECT * FROM members WHERE email = ?").bind(s.email).first();
  const b = await env.SIGNUPS.prepare("SELECT badge FROM badges WHERE email = ?").bind(s.email).first();
  return { email: s.email, member: member || null, badge: b ? b.badge : null, sessionHash };
}
export async function createSession(env, email) {
  const token = randomToken();
  await env.SIGNUPS.prepare("INSERT INTO sessions (token_hash, email, created, expires) VALUES (?, ?, ?, ?)")
    .bind(await sha256(token), email, now(), plus(SESSION_DAYS * 864e5)).run();
  return setCookie(SESSION_COOKIE, token, SESSION_DAYS * 86400);
}

export async function sendEmail(env, { to, subject, text, replyTo }) {
  if (!env.RESEND_API_KEY) return false;
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from: FROM, to: [to], subject, text, ...(replyTo ? { reply_to: replyTo } : {}) }),
  });
  if (!res.ok) console.log("resend error", res.status, (await res.text()).slice(0, 300));
  return res.ok;
}

// Start a sign-in: store a code for this email, send it, return the pending cookie (or an error string)
export async function startSignIn(env, email) {
  const recent = await env.SIGNUPS.prepare("SELECT COUNT(*) AS n FROM login_codes WHERE email = ? AND created > ?")
    .bind(email, plus(-36e5)).first();
  if (recent.n >= CODES_PER_HOUR) return { error: "Too many codes requested for this address in the last hour. Please try again later." };
  await env.SIGNUPS.prepare("DELETE FROM login_codes WHERE expires < ?").bind(now()).run();
  const token = randomToken(), code = randomCode();
  await env.SIGNUPS.prepare("INSERT INTO login_codes (token, email, code_hash, attempts, created, expires) VALUES (?, ?, ?, 0, ?, ?)")
    .bind(token, email, await sha256(token + code), now(), plus(CODE_MINUTES * 6e4)).run();
  const sent = await sendEmail(env, {
    to: email, subject: `Your GPS & Orgs sign-in code: ${code}`,
    text: `Your sign-in code for the GPS & Orgs Community member registry is:\n\n    ${code}\n\nIt expires in ${CODE_MINUTES} minutes. If you did not ask for it, you can ignore this email.\n\nhttps://gpsorgs.com/members\n`,
  });
  if (!sent) return { error: "The code could not be emailed just now. Please try again in a moment." };
  return { cookie: setCookie(PENDING_COOKIE, token, CODE_MINUTES * 60) };
}
// Check a code against the pending cookie. Returns { email } or { error }
export async function finishSignIn(env, request, code) {
  const token = cookies(request)[PENDING_COOKIE];
  if (!token) return { error: "That sign-in has expired. Please request a new code.", restart: true };
  const row = await env.SIGNUPS.prepare("SELECT * FROM login_codes WHERE token = ?").bind(token).first();
  if (!row || row.expires < now()) return { error: "That code has expired. Please request a new one.", restart: true };
  if (row.attempts >= CODE_ATTEMPTS) return { error: "Too many wrong attempts. Please request a new code.", restart: true };
  if ((await sha256(token + code)) !== row.code_hash) {
    await env.SIGNUPS.prepare("UPDATE login_codes SET attempts = attempts + 1 WHERE token = ?").bind(token).run();
    return { error: "That code is not right. Check the email and try again." };
  }
  await env.SIGNUPS.prepare("DELETE FROM login_codes WHERE token = ?").bind(token).run();
  return { email: row.email };
}

// ---------- shared page fragments ----------
export function signedBar(user) {
  if (!user) return "";
  const who = user.member ? esc(user.member.name) : esc(user.email);
  return `<div class="signed"><div class="wrap"><span>Signed in as <strong>${who}</strong></span><span class="links">${user.member ? '<a href="/members">Registry</a><a href="/members/profile">Edit profile</a>' : '<a href="/register">Finish registering</a>'}<form method="post" action="/api/members/signout"><button type="submit" class="linkbtn">Sign out</button></form></span></div></div>`;
}
const errorBox = (e) => e ? `<div class="alert" role="alert">${esc(e)}</div>` : "";

export function emailPage({ path, register, error, email = "" }) {
  const title = register ? "Register as a member" : "Member registry";
  const lede = register
    ? "Members get a profile in the member registry, where other members can find them and see what they work on. Start with your email: we will send a six digit code to confirm it, then you fill in your profile."
    : "The registry is visible to members only. Enter the email you registered with and we will send a six digit code to sign you in. Not a member yet? The same form registers you.";
  return html(page({ path, title, desc: title, body: `
<section class="page-title"><h1>${title}</h1><p class="lede">${lede}</p></section>
<section class="band">${errorBox(error)}
  <form class="join" method="post" action="/api/members/code">
    <div style="position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden" aria-hidden="true"><label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
    <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required value="${esc(email)}"></div>
    <button class="btn accent" type="submit">Send me a code</button>
    <p class="small muted" style="margin-top:16px">No password to remember. Once you are signed in on a device you stay signed in, and on a new device you just ask for another code.</p>
  </form>
</section>` }));
}
export function codePage({ path, error }) {
  return html(page({ path, title: "Check your email", desc: "Enter your sign-in code", body: `
<section class="page-title"><h1>Check your email.</h1><p class="lede">We have sent a six digit code. Enter it below within fifteen minutes.</p></section>
<section class="band">${errorBox(error)}
  <form class="join" method="post" action="/api/members/verify">
    <div class="field"><label for="code">Code</label><input id="code" name="code" class="code" type="text" inputmode="numeric" pattern="[0-9]{6}" maxlength="6" autocomplete="one-time-code" required autofocus></div>
    <button class="btn accent" type="submit">Sign in</button>
    <p class="small muted" style="margin-top:16px">Nothing arrived? Check spam, or <a href="/register">request a new code</a>.</p>
  </form>
</section>` }));
}
export function profilePage({ path, user, error }) {
  const m = user.member || {}; const isNew = !user.member;
  const v = (k) => esc(m[k] ?? "");
  const checked = (b) => b ? " checked" : "";
  return html(page({ path, title: isNew ? "Your profile" : "Edit your profile", desc: "Member profile", bar: signedBar(user), body: `
<section class="page-title"><h1>${isNew ? "Your profile" : "Edit your profile"}</h1><p class="lede">${isNew ? "Nearly there. This is what other members will see about you." : "Change anything below and save."}</p></section>
<section class="band">${errorBox(error)}
  <form class="join" method="post" action="/api/members/profile">
    <div class="field"><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name" required value="${v("name")}"></div>
    <div class="field"><label for="email">Email</label><input id="email" type="email" value="${esc(user.email)}" disabled><div class="hint">This is the address you sign in with. To change it, contact us.</div></div>
    <div class="field"><label class="check"><input type="checkbox" name="email_private"${checked(isNew ? true : m.email_private)}><span>Keep my email private. Other members will not see it; only the steering committee can.</span></label></div>
    <div class="field"><label for="affiliation">Institution or affiliation</label><input id="affiliation" name="affiliation" type="text" autocomplete="organization" value="${v("affiliation")}"></div>
    <div class="field"><label for="role">Role <span class="muted">(for example PhD student, lecturer, practitioner)</span></label><input id="role" name="role" type="text" autocomplete="organization-title" value="${v("role")}"></div>
    <div class="field"><label for="location">Where are you based? <span class="muted">(city or country)</span></label><input id="location" name="location" type="text" value="${v("location")}"></div>
    <div class="field"><label for="interests">Research interests</label><textarea id="interests" name="interests" rows="4">${v("interests")}</textarea></div>
    <div class="field"><label class="check"><input type="checkbox" name="mailing"${checked(isNew)}><span>Add me to the general mailing list for occasional community emails.</span></label></div>
    <div class="field"><label class="check"><input type="checkbox" name="volunteer"><span>I am willing to volunteer: helping with events, the website or the community's running.</span></label></div>
    ${isNew ? `<div class="field"><label class="check"><input type="checkbox" name="ack" required><span>I understand that my profile is visible to other signed-in members of the community, that I can edit or delete it at any time, and that accounts which are inappropriate or not genuine will be deleted.</span></label></div>` : ""}
    <button class="btn accent" type="submit">${isNew ? "Create my profile" : "Save"}</button>
  </form>
  ${isNew ? "" : `<form method="post" action="/api/members/delete" style="margin-top:36px" onsubmit="return confirm('Delete your profile and sign out? This cannot be undone.')"><button type="submit" class="btn danger">Delete my profile</button></form>`}
</section>` }));
}
