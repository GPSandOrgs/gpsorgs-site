// Cloudflare Pages Function: POST /api/join
// Stores one signup in the D1 database bound as SIGNUPS (see wrangler.toml).
// Success -> redirect to /joined. Problem -> redirect to /join-problem.
// A repeat signup with the same email is treated as success and not stored twice.

const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const clean = (v, max) => String(v ?? "").replace(/\s+/g, " ").trim().slice(0, max);

export async function onRequestPost({ request, env }) {
  const back = (path) => Response.redirect(new URL(path, request.url).toString(), 303);
  let form;
  try { form = await request.formData(); } catch { return back("/join-problem"); }

  // honeypot: real people never see or fill this field
  if (form.get("website")) return back("/joined");

  const name = clean(form.get("name"), 200);
  const email = clean(form.get("email"), 254);
  const affiliation = clean(form.get("affiliation"), 300);
  const interests = clean(form.get("interests"), 2000);
  if (!name || !EMAIL.test(email) || !form.get("consent")) return back("/join-problem");
  if (!env.SIGNUPS) return back("/join-problem");

  try {
    await env.SIGNUPS.prepare(
      "INSERT OR IGNORE INTO signups (ts, name, email, affiliation, interests, consent) VALUES (?, ?, ?, ?, ?, 1)"
    ).bind(new Date().toISOString(), name, email, affiliation, interests).run();
  } catch {
    return back("/join-problem");
  }
  return back("/joined");
}
