// POST /api/members/signout
import { currentUser, redirect, clearCookie, SESSION_COOKIE } from "../../../lib/members.js";
export async function onRequestPost({ request, env }) {
  const user = await currentUser(request, env);
  if (user) await env.SIGNUPS.prepare("DELETE FROM sessions WHERE token_hash = ?").bind(user.sessionHash).run();
  return redirect(request, "/", [clearCookie(SESSION_COOKIE)]);
}
