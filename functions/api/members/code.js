// POST /api/members/code: take an email, send a code, set the pending cookie
import { EMAIL_RE, oneLine, startSignIn, emailPage, redirect } from "../../../lib/members.js";
export async function onRequestPost({ request, env }) {
  let form; try { form = await request.formData(); } catch { return redirect(request, "/register"); }
  if (form.get("website")) return redirect(request, "/members/verify");   // honeypot: pretend
  const email = oneLine(form.get("email"), 254).toLowerCase();
  const register = (request.headers.get("referer") || "").includes("/register");
  if (!EMAIL_RE.test(email)) return emailPage({ path: register ? "/register" : "/members", register, error: "Please enter a valid email address.", email });
  const r = await startSignIn(env, email);
  if (r.error) return emailPage({ path: register ? "/register" : "/members", register, error: r.error, email });
  return redirect(request, "/members/verify", [r.cookie]);
}
