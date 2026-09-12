// GET /register: email step for newcomers; profile form once signed in; existing members go to edit.
import { currentUser, emailPage, profilePage, redirect } from "../lib/members.js";
export async function onRequestGet({ request, env }) {
  const user = await currentUser(request, env);
  if (!user) return emailPage({ path: "/register", register: true });
  if (user.member) return redirect(request, "/members/profile");
  return profilePage({ path: "/register", user });
}
