// POST /api/members/verify: check the code, open a session, send to profile or registry
import { oneLine, finishSignIn, createSession, codePage, redirect, clearCookie, PENDING_COOKIE, now } from "../../../lib/members.js";
export async function onRequestPost({ request, env }) {
  let form; try { form = await request.formData(); } catch { return redirect(request, "/register"); }
  const code = oneLine(form.get("code"), 6).replace(/\D/g, "");
  const r = await finishSignIn(env, request, code);
  if (r.error) return r.restart ? redirect(request, "/register", [clearCookie(PENDING_COOKIE)]) : codePage({ path: "/members", error: r.error });
  const session = await createSession(env, r.email);
  const member = await env.SIGNUPS.prepare("SELECT id FROM members WHERE email = ?").bind(r.email).first();
  if (member) await env.SIGNUPS.prepare("UPDATE members SET last_login = ? WHERE email = ?").bind(now(), r.email).run();
  return redirect(request, member ? "/members" : "/register", [session, clearCookie(PENDING_COOKIE)]);
}
