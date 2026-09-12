// GET /members/verify: the code entry form (only meaningful with a pending cookie)
import { cookies, PENDING_COOKIE, codePage, redirect } from "../../lib/members.js";
export async function onRequestGet({ request }) {
  if (!cookies(request)[PENDING_COOKIE]) return redirect(request, "/register");
  return codePage({ path: "/members" });
}
