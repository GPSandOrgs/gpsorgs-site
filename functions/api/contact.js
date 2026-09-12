// Cloudflare Pages Function: POST /api/contact
// Emails the message to the community inbox through Resend (secret RESEND_API_KEY).
// The topic goes in the subject in square brackets; the sender's address is set as
// reply-to so a plain reply from Gmail reaches them. Nothing is stored.
// Success -> /contacted. Problem, or no sender configured -> /contact-problem.

const TO = "gpsandorgs@gmail.com";
const FROM = "GPS & Orgs website <no-reply@gpsorgs.com>";
const TOPICS = new Set(["Announcement request", "Event idea", "Website feedback", "Member registry issue", "General enquiry"]);
const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const clean = (v, max) => String(v ?? "").replace(/\r\n?/g, "\n").trim().slice(0, max);

export async function onRequestPost({ request, env }) {
  const back = (path) => Response.redirect(new URL(path, request.url).toString(), 303);
  let form;
  try { form = await request.formData(); } catch { return back("/contact-problem"); }
  if (form.get("website")) return back("/contacted");           // honeypot

  const topic = clean(form.get("topic"), 40);
  const name = clean(form.get("name"), 200).replace(/\s+/g, " ");
  const email = clean(form.get("email"), 254);
  const message = clean(form.get("message"), 5000);
  if (!TOPICS.has(topic) || !name || !EMAIL.test(email) || !message) return back("/contact-problem");
  if (!env.RESEND_API_KEY) return back("/contact-problem");

  const text = `From: ${name} <${email}>\nTopic: ${topic}\n\n${message}\n`;
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { "Authorization": `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from: FROM, to: [TO], reply_to: email, subject: `[${topic}] from ${name} via gpsorgs.com`, text }),
  });
  return back(res.ok ? "/contacted" : "/contact-problem");
}
