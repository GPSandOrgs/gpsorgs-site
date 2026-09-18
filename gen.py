import html, re, hashlib, sys
FULL = "--full" in sys.argv   # the working copy: the readings page with every reference in place
CSSV = hashlib.sha1(open("assets/site.css","rb").read()).hexdigest()[:8]   # changes whenever the stylesheet does, so browsers never keep a stale copy

import urllib.parse
def scholarize(block):
    """Append a Google Scholar search link to every reference in a readings block, keyed on the title."""
    def link(m):
        li = m.group(1)
        t = re.search(r"\(\d{4}[a-z]?\)\. (.+?[.?!]) <em>", li)        # article: title before the journal (may end in ? or !)
        if not t: t = re.search(r"\(\d{4}[a-z]?\)\. <em>(.+?)</em>", li)  # book: title is the italic part
        if not t: return m.group(0)
        title = html.unescape(re.sub(r"<[^>]+>", "", t.group(1))).rstrip(".")
        title = title.replace("\u201c", "").replace("\u201d", "")   # curly quotes inside a title break the phrase search
        q = urllib.parse.quote_plus('"' + title + '"')
        return '<li>%s <a class="scholar" href="https://scholar.google.com/scholar?q=%s" target="_blank" rel="noopener">Google Scholar</a></li>' % (li, q)
    return re.sub(r"<li>(.*?)</li>", link, block, flags=re.S)
def in_development(block):
    """The public readings page while the list is still being put together: keep every heading
    and its descriptive line, drop the references themselves, and say the list is coming."""
    return re.sub(r"<ul>.*?</ul>", '<p class="placeholder">List in development.</p>', block, flags=re.S)
LOGO = """<svg viewBox="0 0 34 34" aria-hidden="true"><circle cx="17" cy="17" r="15.5" fill="none" stroke="#1d2624" stroke-width="1.4"/><circle cx="17" cy="17" r="9.5" fill="none" stroke="#2f5d6b" stroke-width="1.2"/><circle cx="17" cy="17" r="4" fill="#4f6b52"/><path d="M17 1.5v6M17 26.5v6M1.5 17h6M26.5 17h6" stroke="#1d2624" stroke-width="1.2"/></svg>"""
NAV = [
    ("/", "Home", None),
    ("Members", None, [("/committee", "Committee"), ("/members", "Member registry")]),
    ("/events", "Events", None),
    ("Resources", None, [("/resources", "Community"), ("/readings", "Readings"), ("/teaching", "Teaching")]),
    ("Join", None, [("/join", "Mailing list"), ("/register", "Register as a member")]),
]
def navhtml(fname):
    here = '/' if fname == 'index.html' else '/' + fname[:-5]
    out = []
    for a, b, kids in NAV:
        if kids is None:
            cur = ' aria-current="page"' if a == here else ''
            out.append('<a href="%s"%s>%s</a>' % (a, cur, b))
        else:
            inside = any(h == here for h, _ in kids)
            items = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == here else '', t) for h, t in kids)
            out.append('<details class="menu"%s><summary%s>%s</summary><div class="drop">%s</div></details>'
                       % (' open' if False else '', ' class="current"' if inside else '', a, items))
    return "".join(out)
# the contact address is assembled by script so it is not sitting in the page source for scrapers
MAILJS = """<script>
document.querySelectorAll('a.mail').forEach(function(a){var u=a.dataset.u,d=a.dataset.d;a.href='mailto:'+u+'@'+d;if(!a.textContent.trim())a.textContent=u+'@'+d;});
document.querySelectorAll('details.menu').forEach(function(d){d.addEventListener('toggle',function(){if(d.open)document.querySelectorAll('details.menu').forEach(function(o){if(o!==d)o.open=false;});});});
document.addEventListener('click',function(e){if(!e.target.closest('details.menu'))document.querySelectorAll('details.menu').forEach(function(o){o.open=false;});});
</script>"""
TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · GPS &amp; Orgs Community</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="/assets/site.css?v={cssv}">
</head>
<body>
<header class="site"><div class="wrap">
  <a class="brand" href="/">{logo}<span><span class="name">GPS <span>&amp;</span> Orgs</span><span class="tag">Geography · Place · Space · Organisations</span></span></a>
  <nav class="main" aria-label="Main">{nav}</nav>
</div></header>
{bar}
<main class="wrap">
{body}
</main>
<footer class="site"><div class="wrap">
  <div>GPS &amp; Orgs Community · Geography, Place, Space and Organisations</div>
  <div><a href="/join">Join the mailing list</a> · <a href="/contact">Contact us</a></div>
</div></footer>
{script}
</body>
</html>
"""
def fill(tpl, **kw):
    kw.setdefault("cssv", CSSV)
    for k, v in kw.items(): tpl = tpl.replace("{" + k + "}", v)
    return tpl
WORKING_BAR = '<div class="signed"><div class="wrap"><span>Working copy of the site, kept for the steering committee. The readings page here carries the full reference list; the public site at <a href="https://gpsorgs.com">gpsorgs.com</a> does not yet.</span></div></div>'
def page(fname, title, body, desc):
    return fill(TEMPLATE, title=html.escape(title), desc=html.escape(desc), logo=LOGO, nav=navhtml(fname), bar=WORKING_BAR if FULL else "", body=body, script=MAILJS)

# lib/shell.js: the same template and navigation for pages rendered by Functions
import json
SHELL_JS = r"""// GENERATED by gen.py. Do not edit by hand: change gen.py and re-run it.
export const LOGO = %s;
export const NAV = %s;
export const MAILJS = %s;
const TEMPLATE = %s.replace("{cssv}", %s);
export function esc(s) { return String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
export function navhtml(here) {
  return NAV.map(([a, b, kids]) => {
    if (!kids) return `<a href="${a}"${a === here ? ' aria-current="page"' : ''}>${b}</a>`;
    const inside = kids.some(([h]) => h === here);
    const items = kids.map(([h, t]) => `<a href="${h}"${h === here ? ' aria-current="page"' : ''}>${t}</a>`).join("");
    return `<details class="menu"><summary${inside ? ' class="current"' : ''}>${a}</summary><div class="drop">${items}</div></details>`;
  }).join("");
}
export function page({ path, title, desc, body, bar = "" }) {
  const vals = { title: esc(title), desc: esc(desc), logo: LOGO, nav: navhtml(path), bar, body, script: MAILJS };
  return TEMPLATE.replace(/\{(title|desc|logo|nav|bar|body|script)\}/g, (_, k) => vals[k]);
}
export function html(body, status = 200, headers = {}) {
  return new Response(body, { status, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", ...headers } });
}
""" % (json.dumps(LOGO), json.dumps(NAV), json.dumps(MAILJS), json.dumps(TEMPLATE), json.dumps(CSSV))
import os
os.makedirs("lib", exist_ok=True)
open("lib/shell.js", "w").write(SHELL_JS)
pages = {}
pages["index.html"] = ("Home", "A community of researchers exploring organisations in relation to geography, place and space.", """
<section class="hero">
  <div class="kicker">A research community</div>
  <h1>Connecting geography, place, space and organisations.</h1>
  <p class="lede">A community of researchers whose work meets where organisations and the spatial disciplines overlap, and who want those conversations to talk to one another.</p>
  <div class="actions"><a class="btn accent" href="/join">Join the mailing list</a><a class="btn" href="/events">Events</a></div>
</section>
<hr class="rule">
<section class="band">
  <h2>About us</h2>
  <p>Research on organisations and geography, place and space runs in many conversations at once: organisational space and spatial practice, proximity and the built environment, place and meaning, cities and regions, infrastructure, distributed and virtual work. They use different vocabularies, work at different scales, and reach well beyond management and organisation studies into architecture, urban planning, geography and sociology. Often they do not meet.</p>
  <p>This community exists to connect them. It grew out of conversations at EGOS and the Academy of Management and took shape at a first event at UCL School of Management on 7 September 2026. It is early, deliberately open, and will be shaped by the people who join it.</p>
</section>
<section class="band">
  <div class="grid">
    <div class="card"><h3>Meet</h3><p>Events that bring people together around the work: a day, a seminar, a walk. <a href="/events">See events</a>.</p></div>
    <div class="card"><h3>Read</h3><p>A growing set of readings, calls and related communities. <a href="/resources">Resources</a>.</p></div>
    <div class="card"><h3>Belong</h3><p>Join the <a href="/join">mailing list</a> to hear from us, or <a href="/register">register as a member</a> to appear in the member registry.</p></div>
  </div>
</section>
""")
pages["committee.html"] = ("Committee", "The steering committee and representatives of the GPS & Orgs Community.", """
<section class="page-title"><h1>Committee</h1><p class="lede">The people keeping the community moving.</p></section>
<section class="band">
  <h2>Steering committee</h2>
  <div class="people">
    <div class="person"><div class="who">Alessandra Migliore</div><div class="where">Politecnico di Milano</div></div>
    <div class="person"><div class="who">Santi Furnari</div><div class="where">Bayes Business School</div></div>
    <div class="person"><div class="who">Jen Rhymer</div><div class="where">UCL School of Management</div></div>
  </div>
  <p class="muted" style="margin-top:22px">The steering committee is growing. Further members will be announced as the community takes shape.</p>
  <h2>Representatives</h2>
  <p class="muted">Representatives will be the community's points of contact at their institutions and across disciplines. To be announced.</p>
</section>
""")
pages["events.html"] = ("Events", "Upcoming and past events of the GPS & Orgs Community.", """
<section class="page-title"><h1>Events</h1><p class="lede">Where the community meets.</p></section>
<section class="band">
  <h2>Upcoming</h2>
  <p class="muted">The next event will be announced to the mailing list first. <a href="/join">Join</a> to hear about it.</p>
  <h2>Past</h2>
  <div class="event">
    <div class="when">7 Sept 2026<small>Full day</small></div>
    <div>
      <h3>Space, Place, Geography and Organisations: Exploring Connections</h3>
      <div class="where">UCL School of Management, London</div>
      <p>The first meeting. A day bringing together researchers from organisation studies and the spatial disciplines: a panel mapping the research areas, roundtables on a shared phenomenon, a panel on methods and data sources, and a closing session on future research agendas and the community itself.</p>
      <figure class="photo">
        <img src="/assets/2026-09-07-first-meeting-900.jpg" srcset="/assets/2026-09-07-first-meeting-900.jpg 900w, /assets/2026-09-07-first-meeting-1800.jpg 1800w" sizes="(max-width: 600px) 92vw, 670px" width="900" height="365" loading="lazy" alt="Researchers seated around tables in a top-floor room at UCL School of Management, listening to a speaker at the lectern, with the London skyline through the windows.">
      </figure>
      <p class="small muted">Organised by Jen Rhymer (UCL), Alessandra Migliore (Politecnico di Milano) and Santi Furnari (Bayes Business School).</p>
    </div>
  </div>
</section>
""")
pages["resources.html"] = ("Community", "Announcements, calls and related networks for research on organisations, geography, place and space.", """
<section class="page-title"><h1>Community</h1><p class="lede">A shared noticeboard for the community. Announcements and calls are posted as they come in. The <a href="/readings">reading list</a> has its own page.</p>
<nav class="subnav" aria-label="On this page"><a href="#announcements">Announcements</a><a href="#calls">Calls and tracks</a><a href="#networks">Related networks</a></nav></section>

<section class="band" id="announcements">
  <h2>Announcements</h2>
  <p class="muted">Related events, workshops, seminars and opportunities that members want the community to know about, whether or not we are involved in organising them. Newest first.</p>
  <div class="notice-list">
    <div class="notice empty"><div class="when">&nbsp;</div><div><p class="placeholder">Nothing posted yet. The first announcements will appear here after the community's next call for items.</p></div></div>
  </div>
</section>

<section class="band" id="calls">
  <h2>Calls and tracks</h2>
  <p class="muted">Conference sub-themes, professional development workshops, special issues and calls for papers relevant to the community, with their deadlines.</p>
  <div class="notice-list">
    <div class="notice empty"><div class="when">&nbsp;</div><div><p class="placeholder">No open calls listed yet.</p></div></div>
  </div>
</section>

<section class="band" id="networks">
  <h2>Related networks</h2>
  <p class="muted">Existing conversations this community builds on and stays in touch with.</p>
  <ul class="linklist">
    <li><strong><a href="https://www.egos.org/SWGs/SWG-07">EGOS Standing Working Group 07</a></strong>, Organizations and Place-Based Communities (2025 to 2028). Sub-themes at the annual EGOS Colloquium.</li>
    <li><strong>AOM PDW series on Organisational Spaces</strong>. Professional development workshops at the Academy of Management annual meeting.</li>
    <li><strong><a href="https://rgcs-owee.org/">RGCS</a></strong>, the Research Group on Collaborative Spaces, and its annual symposium.</li>
    <li><strong><a href="https://www.twrnetwork.org">TWR Network</a></strong>, the Transdisciplinary Workplace Research network: scholars and practitioners across disciplines working on workplaces and wellbeing, with a biennial conference.</li>
  </ul>
</section>
""")
# The full reading list: the master copy, and the place to add new references. While the list
# is still being put together the public page shows only the headings and their descriptive
# lines; `python3 gen.py --full` builds the working copy, with every reference in place.
READINGS_SHELVES = """
<section class="band" id="readings">
  <h3 class="shelf-cat">Areas</h3>
  <div class="shelf">
    <div class="shelf-item"><h3>Organisational space and spatial practice</h3><p>Space as experienced, practised and socially produced, including how organisational power relations take material form.</p><ul><li>Migliore, A., Rossi-Lamastra, C. and Tagliaro, C. (2025). Home vs office: Does workspace design influence where academics conduct their research? <em>Research Policy</em>.</li><li>Stephenson, K. A., Kuismin, A., Putnam, L. L. and Sivunen, A. (2020). Process studies of organizational space. <em>Academy of Management Annals</em>.</li><li>De Vaujany, F. X. and Vaast, E. (2014). If these walls could talk: The mutual construction of organizational space and legitimacy. <em>Organization Science</em>.</li><li>Furnari, S. (2014). Interstitial spaces: Microinteraction settings and the genesis of new practices between institutional fields. <em>Academy of Management Review</em>.</li><li>Taylor, S. and Spicer, A. (2007). Time for space: A narrative review of research on organizational spaces. <em>International Journal of Management Reviews</em>.</li></ul></div>
    <div class="shelf-item"><h3>Proximity, microgeography and the built environment</h3><p>Enclosures, barriers, layout and ambient surroundings that shape interaction and behaviour.</p><ul><li>Lee, S. and Sosa, M. E. (2025). Spaces for creativity: Unconventional workspaces and divergent thinking. <em>Management Science</em>.</li><li>Oyedeji, B. A., Ko, Y. H. and Lee, S. (2025). Physical work environments: An integrative review and agenda for future research. <em>Journal of Management</em>.</li><li>Roche, M. P., Oettl, A. and Catalini, C. (2024). Proximate (co-)working: Knowledge spillovers and social interactions. <em>Management Science</em>.</li><li>Elsbach, K. D. and Pratt, M. G. (2007). The physical environment in organizations. <em>Academy of Management Annals</em>.</li></ul></div>
    <div class="shelf-item"><h3>Place, meaning and identity</h3><p>Spaces made meaningful through experience, attachment, narrative and collective interpretation.</p><ul><li>Wright, A. L., Irving, G., Zafar, A. and Reay, T. (2023). The role of space and place in organizational and institutional change: A systematic review of the literature. <em>Journal of Management Studies</em>.</li><li>Aversa, P., Furnari, S. and Jenkins, M. (2022). The primordial soup: Exploring the emotional microfoundations of cluster genesis. <em>Organization Science</em>.</li><li>Cartel, M., Kibler, E. and Dacin, M. T. (2022). Unpacking &ldquo;sense of place&rdquo; and &ldquo;place-making&rdquo; in organization studies: A toolkit for place-sensitive research. <em>The Journal of Applied Behavioral Science</em>.</li><li>Nash, L. (2020). Performing place: A rhythmanalysis of the City of London. <em>Organization Studies</em>.</li><li>Cresswell, T. (2004). <em>Place: A Short Introduction</em>. Blackwell.</li><li>Gieryn, T. F. (2000). A space for place in sociology. <em>Annual Review of Sociology</em>.</li></ul></div>
    <div class="shelf-item"><h3>Cities, regions and neighbourhoods</h3><p>Local communities, cities, regions and ecosystems that shape organisational practices, opportunities and outcomes.</p><ul><li>Hwang, J. and Yoon, H. (2026). Shifting and persisting neighborhood hierarchies: Immigrant influx and the gentrification of Black neighborhoods in the twenty-first century. <em>Sociological Perspectives</em>.</li><li>Brandtner, C. and Su&aacute;rez, D. (2021). The structure of city action: Institutional embeddedness and sustainability practices in U.S. cities. <em>American Review of Public Administration</em>.</li><li>Gagliardi, L. and Iammarino, S. (2018). Innovation in risky markets: Ownership and location advantages in the UK regions. <em>Journal of Economic Geography</em>.</li><li>Marquis, C. and Battilana, J. (2009). Acting globally but thinking locally? The enduring influence of local communities on organizations. <em>Research in Organizational Behavior</em>.</li></ul></div>
    <div class="shelf-item"><h3>Infrastructure and meso-geography</h3><p>Material and connective systems that enable, organise and constrain activity across places and scales.</p><ul><li>Dutta, S., Armanios, D. E. and Desai, J. D. (2021). Beyond spatial proximity: The impact of enhanced spatial connectedness from new bridges on entrepreneurship. <em>Organization Science</em>.</li><li>Roche, M. P. (2020). Taking innovation to the streets: Microgeography, physical structure, and innovation. <em>The Review of Economics and Statistics</em>.</li></ul></div>
    <div class="shelf-item"><h3>Distributed and virtual spaces</h3><p>Organising across dispersed, hybrid and digitally mediated spaces, shaped by technologies and changing patterns of presence and mobility.</p><ul><li>Leonardi, P. M. (2021). COVID-19 and the new technologies of organizing: Digital exhaust, digital footprints, and artificial intelligence in the wake of remote work. <em>Journal of Management Studies</em>.</li><li>Mazmanian, M., Orlikowski, W. J. and Yates, J. (2013). The autonomy paradox: The implications of mobile email devices for knowledge professionals. <em>Organization Science</em>.</li></ul></div>
  </div>
  <h3 class="shelf-cat">Methods</h3>
  <div class="shelf">
    <div class="shelf-item"><h3>Space syntax</h3><p>Analysing the configuration of buildings and cities to show how spatial layout shapes movement, encounter and interaction.</p><ul><li>Sailer, K. and McCulloh, I. (2012). Social networks and spatial configuration: How office layouts drive social interaction. <em>Social Networks</em>.</li><li>Hillier, B. (1996). <em>Space is the Machine: A Configurational Theory of Architecture</em>. Cambridge University Press.</li><li>Hillier, B. and Hanson, J. (1984). <em>The Social Logic of Space</em>. Cambridge University Press.</li></ul></div>
    <div class="shelf-item"><h3 class="placeholder">Further methods to add</h3><p class="placeholder">Mapping and GIS, ethnographies of place, spatial network analysis, and more, as members contribute.</p></div>
  </div>
</section>
"""
READINGS_LEDE_FULL = """A starter shelf, organised by the provisional map of research conversations drawn up at the 7 September event. The map is a working device, not a taxonomy; the boundaries are exactly what the community is here to question."""
READINGS_LEDE = """The provisional map of research conversations drawn up at the 7 September event. The map is a working device, not a taxonomy; the boundaries are exactly what the community is here to question. The readings that will sit under each heading are being put together now, and members will be asked to contribute: if there is work you think belongs on this shelf, including your own, <a href="/contact">tell us</a>."""
pages["readings.html"] = (
    "Readings",
    "A map of research conversations on organisations, geography, place and space. The reading list under each heading is in development."
      if not FULL else
    "A starter reading list on organisations, geography, place and space, organised by research conversation.",
    '<section class="page-title"><h1>Readings</h1><p class="lede">%s</p></section>\n%s\n'
      % (READINGS_LEDE_FULL if FULL else READINGS_LEDE,
          scholarize(READINGS_SHELVES) if FULL else in_development(READINGS_SHELVES)))
pages["teaching.html"] = ("Teaching", "Teaching resources on organisations, geography, place and space.", """
<section class="page-title"><h1>Teaching</h1><p class="lede">Cases, syllabi, exercises and materials for teaching organisations through geography, place and space.</p></section>
<section class="band"><p class="placeholder">Nothing here yet. This page will grow as members share what they teach with. If you have something to contribute, <a href="/contact">get in touch</a>.</p></section>
""")
pages["join.html"] = ("Join", "Join the GPS & Orgs Community mailing list.", """
<section class="page-title"><h1>Join the mailing list</h1><p class="lede">Sign up to hear about events, calls and what members are working on. If you would also like other members to be able to find you, <a href="/register">register as a member</a>.</p></section>
<section class="band">
  <form class="join" action="/api/join" method="post">
    <div style="position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden" aria-hidden="true"><label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
    <div class="field"><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
    <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="affiliation">Institution or affiliation</label><input id="affiliation" name="affiliation" type="text" autocomplete="organization"></div>
    <div class="field"><label for="interests">What are you working on? <span class="muted">(optional)</span></label><textarea id="interests" name="interests" rows="3"></textarea></div>
    <div class="field"><label class="check"><input type="checkbox" name="consent" required><span>I would like to receive occasional emails from the GPS &amp; Orgs Community. Unsubscribe any time.</span></label></div>
    <button class="btn accent" type="submit">Join the mailing list</button>
  </form>
</section>
""")
pages["joined.html"] = ("You're on the list", "Thanks for joining the GPS & Orgs Community mailing list.", """
<section class="page-title"><h1>You're on the list.</h1><p class="lede">Thank you. You will hear from us when there is something worth hearing about: an event, a call, a conversation starting.</p>
<div class="actions"><a class="btn" href="/">Back to the front page</a><a class="btn" href="/events">Events</a></div></section>
""")
pages["join-problem.html"] = ("Something went wrong", "The sign up could not be saved.", """
<section class="page-title"><h1>That did not go through.</h1><p class="lede">Something stopped the sign up from saving. Please check the name and email fields and try again in a moment.</p>
<div class="actions"><a class="btn accent" href="/join">Try again</a></div></section>
""")
pages["contact.html"] = ("Contact", "Contact the GPS & Orgs Community.", """
<section class="page-title"><h1>Contact us</h1><p class="lede">Announcements you would like shared, ideas for events, feedback on the site, or anything else. Messages go to the steering committee.</p></section>
<section class="band">
  <form class="join" action="/api/contact" method="post">
    <div style="position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden" aria-hidden="true"><label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
    <div class="field"><label for="topic">What is it about?</label><select id="topic" name="topic" required>
      <option value="">Choose one</option>
      <option>Announcement request</option>
      <option>Event idea</option>
      <option>Website feedback</option>
      <option>Member registry issue</option>
      <option>General enquiry</option>
    </select></div>
    <div class="field"><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
    <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required><div class="hint">So we can reply. Not stored anywhere else.</div></div>
    <div class="field"><label for="message">Message</label><textarea id="message" name="message" rows="6" required></textarea></div>
    <button class="btn accent" type="submit">Send</button>
  </form>
  <p class="small muted" style="margin-top:22px">You can also write to us directly at <a class="mail" data-u="hello" data-d="gpsorgs.com"></a>.</p>
</section>
""")
pages["contacted.html"] = ("Message sent", "Your message to the GPS & Orgs Community was sent.", """
<section class="page-title"><h1>Thank you.</h1><p class="lede">Your message is on its way to the steering committee. We reply to everything, though not always quickly.</p>
<div class="actions"><a class="btn" href="/">Back to the front page</a></div></section>
""")
pages["contact-problem.html"] = ("Something went wrong", "The message could not be sent.", """
<section class="page-title"><h1>That did not go through.</h1><p class="lede">Something stopped the message from sending. Please check the fields and try again in a moment, or email us directly at <a class="mail" data-u="hello" data-d="gpsorgs.com"></a>.</p>
<div class="actions"><a class="btn accent" href="/contact">Try again</a></div></section>
""")
for f,(t,d,b) in pages.items():
    open(f,"w").write(page(f,t,b,d))
print("pages:", ", ".join(pages))
