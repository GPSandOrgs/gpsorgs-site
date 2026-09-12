// GET /members: the registry for signed-in members with a profile; the sign-in form otherwise.
import { page, esc, html } from "../../lib/shell.js";
import { currentUser, emailPage, signedBar, redirect } from "../../lib/members.js";

const BADGE = { steering: ["★", "Steering committee"], representative: ["◆", "Representative"] };
function card(m, viewerIsSteering) {
  const b = BADGE[m.badge];
  const lines = [m.affiliation, m.role, m.location].filter(Boolean).map(esc);
  const email = (!m.email_private || viewerIsSteering) ? `<div class="mail-line"><a href="mailto:${esc(m.email)}">${esc(m.email)}</a>${m.email_private ? ' <span class="muted small">(private, visible to the committee)</span>' : ""}</div>` : "";
  const remove = viewerIsSteering ? `<form method="post" action="/api/members/remove" class="remove" onsubmit="return confirm('Remove ${esc(m.name).replace(/'/g, "\\'")} from the registry?')"><input type="hidden" name="id" value="${m.id}"><button type="submit" class="linkbtn muted small">Remove</button></form>` : "";
  return `<div class="member"><div class="who">${esc(m.name)}${b ? ` <span class="badge ${m.badge}" title="${b[1]}">${b[0]}</span>` : ""}</div>${lines.length ? `<div class="where">${lines.join(" · ")}</div>` : ""}${email}${m.interests ? `<p class="interests">${esc(m.interests)}</p>` : ""}${remove}</div>`;
}
export async function onRequestGet({ request, env }) {
  const user = await currentUser(request, env);
  if (!user) return emailPage({ path: "/members", register: false });
  if (!user.member) return redirect(request, "/register");
  const { results } = await env.SIGNUPS.prepare(
    "SELECT m.id, m.name, m.email, m.email_private, m.affiliation, m.role, m.location, m.interests, b.badge FROM members m LEFT JOIN badges b ON b.email = m.email ORDER BY m.name COLLATE NOCASE").all();
  const steering = user.badge === "steering";
  const saved = new URL(request.url).searchParams.has("saved");
  const body = `
<section class="page-title"><h1>Member registry</h1><p class="lede">Who is in the community, what they work on and where. Visible to signed-in members only.</p></section>
<section class="band">
  ${saved ? '<div class="alert ok" role="status">Your profile is saved.</div>' : ""}
  <p class="small muted">${results.length} member${results.length === 1 ? "" : "s"} · <span class="badge steering">★</span> steering committee · <span class="badge representative">◆</span> representative</p>
  <div class="registry">${results.map(m => card(m, steering)).join("")}</div>
</section>`;
  return html(page({ path: "/members", title: "Member registry", desc: "GPS & Orgs Community member registry", bar: signedBar(user), body }));
}
