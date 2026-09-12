// POST /api/members/delete: a member removes their own profile and all their sessions
import { currentUser, redirect, clearCookie, SESSION_COOKIE } from "../../../lib/members.js";
export async function onRequestPost({ request, env }) {
  const user = await currentUser(request, env);
  if (!user) return redirect(request, "/");
  await env.SIGNUPS.batch([
    env.SIGNUPS.prepare("DELETE FROM members WHERE email = ?").bind(user.email),
    env.SIGNUPS.prepare("DELETE FROM sessions WHERE email = ?").bind(user.email),
  ]);
  return redirect(request, "/", [clearCookie(SESSION_COOKIE)]);
}
