// Cloudflare Pages Function: POST /api/join
// Appends one row to signups.csv in this repo via the GitHub contents API.
// Needs a Pages secret GITHUB_TOKEN (fine-grained, this repo only, Contents: read and write).
// Success -> redirect to /joined. Problem -> redirect to /join-problem.

const REPO = "jrhy7/gpsorgs-site";
const FILE = "signups.csv";
const HEADER = "timestamp,name,email,affiliation,interests\n";

function csv(v) {
  const s = String(v ?? "").replace(/\r?\n/g, " ").trim();
  return /[",]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}
function b64encode(str) { return btoa(unescape(encodeURIComponent(str))); }
function b64decode(str) { return decodeURIComponent(escape(atob(str.replace(/\n/g, "")))); }

export async function onRequestPost({ request, env }) {
  const back = (path) => Response.redirect(new URL(path, request.url).toString(), 303);
  let form;
  try { form = await request.formData(); } catch { return back("/join-problem"); }

  // honeypot: real people never see or fill this field
  if (form.get("website")) return back("/joined");

  const name = (form.get("name") || "").toString().trim();
  const email = (form.get("email") || "").toString().trim();
  const affiliation = (form.get("affiliation") || "").toString().trim();
  const interests = (form.get("interests") || "").toString().trim();
  if (!name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || !form.get("consent")) return back("/join-problem");
  if (!env.GITHUB_TOKEN) return back("/join-problem");

  const api = `https://api.github.com/repos/${REPO}/contents/${FILE}`;
  const headers = {
    "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
    "Accept": "application/vnd.github+json",
    "User-Agent": "gpsorgs-join-form",
    "X-GitHub-Api-Version": "2022-11-28",
  };
  const row = [new Date().toISOString(), name, email, affiliation, interests].map(csv).join(",") + "\n";

  // read, append, write; retry once if the file changed underneath us
  for (let attempt = 0; attempt < 2; attempt++) {
    let sha = null, content = HEADER;
    const get = await fetch(api, { headers });
    if (get.status === 200) {
      const j = await get.json();
      sha = j.sha;
      content = b64decode(j.content);
      if (!content.endsWith("\n")) content += "\n";
    } else if (get.status !== 404) {
      return back("/join-problem");
    }
    const body = {
      message: `Signup: ${name}`,
      content: b64encode(content + row),
      ...(sha ? { sha } : {}),
    };
    const put = await fetch(api, { method: "PUT", headers, body: JSON.stringify(body) });
    if (put.ok) return back("/joined");
    if (put.status !== 409 && put.status !== 422) return back("/join-problem");
  }
  return back("/join-problem");
}
