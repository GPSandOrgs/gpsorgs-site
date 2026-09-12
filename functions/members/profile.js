// GET /members/profile: edit form for a signed-in member
import { currentUser, profilePage, redirect } from "../../lib/members.js";
export async function onRequestGet({ request, env }) {
  const user = await currentUser(request, env);
  if (!user) return redirect(request, "/members");
  if (!user.member) return redirect(request, "/register");
  return profilePage({ path: "/members/profile", user });
}
