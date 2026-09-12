// POST /api/members/remove: steering committee removes a profile (bogus or inappropriate accounts)
import { currentUser, redirect } from "../../../lib/members.js";
export async function onRequestPost({ request, env }) {
  const user = await currentUser(request, env);
  if (!user || user.badge !== "steering") return redirect(request, "/members");
  let form; try { form = await request.formData(); } catch { return redirect(request, "/members"); }
  const id = parseInt(form.get("id"), 10);
  if (!Number.isInteger(id)) return redirect(request, "/members");
  const target = await env.SIGNUPS.prepare("SELECT email FROM members WHERE id = ?").bind(id).first();
  if (target && target.email !== user.email) {
    await env.SIGNUPS.batch([
      env.SIGNUPS.prepare("DELETE FROM members WHERE id = ?").bind(id),
      env.SIGNUPS.prepare("DELETE FROM sessions WHERE email = ?").bind(target.email),
    ]);
    console.log("member removed by", user.email, ":", target.email);
  }
  return redirect(request, "/members");
}
