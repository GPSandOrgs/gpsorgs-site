// POST /api/members/profile: create or update the signed-in member's profile; feed the mailing lists
import { currentUser, clean, oneLine, profilePage, redirect, now } from "../../../lib/members.js";
export async function onRequestPost({ request, env }) {
  const user = await currentUser(request, env);
  if (!user) return redirect(request, "/register");
  let form; try { form = await request.formData(); } catch { return redirect(request, "/register"); }
  const isNew = !user.member;
  const name = oneLine(form.get("name"), 200);
  const p = {
    affiliation: oneLine(form.get("affiliation"), 300), role: oneLine(form.get("role"), 200),
    location: oneLine(form.get("location"), 200), interests: clean(form.get("interests"), 2000),
    email_private: form.get("email_private") ? 1 : 0,
  };
  if (!name) return profilePage({ path: isNew ? "/register" : "/members/profile", user, error: "Please give your name." });
  if (isNew && !form.get("ack")) return profilePage({ path: "/register", user, error: "Please tick the box confirming you understand how your profile is shown." });
  const t = now();
  if (isNew) {
    await env.SIGNUPS.prepare("INSERT INTO members (email, name, affiliation, role, location, interests, email_private, created, updated, last_login) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
      .bind(user.email, name, p.affiliation, p.role, p.location, p.interests, p.email_private, t, t, t).run();
  } else {
    await env.SIGNUPS.prepare("UPDATE members SET name = ?, affiliation = ?, role = ?, location = ?, interests = ?, email_private = ?, updated = ? WHERE email = ?")
      .bind(name, p.affiliation, p.role, p.location, p.interests, p.email_private, t, user.email).run();
  }
  // mailing lists: ticking adds; unticking never removes (removal is handled by the committee)
  if (form.get("mailing") || form.get("volunteer")) {
    await env.SIGNUPS.prepare("INSERT OR IGNORE INTO signups (ts, name, email, affiliation, interests, consent, volunteer) VALUES (?, ?, ?, ?, ?, 1, 0)")
      .bind(t, name, user.email, p.affiliation, p.interests).run();
  }
  if (form.get("volunteer")) await env.SIGNUPS.prepare("UPDATE signups SET volunteer = 1 WHERE lower(email) = ?").bind(user.email).run();
  return redirect(request, "/members?saved");
}
