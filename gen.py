import html
LOGO = """<svg viewBox="0 0 34 34" aria-hidden="true"><circle cx="17" cy="17" r="15.5" fill="none" stroke="#1e2528" stroke-width="1.4"/><circle cx="17" cy="17" r="9.5" fill="none" stroke="#3d5a68" stroke-width="1.2"/><circle cx="17" cy="17" r="4" fill="#b0553a"/><path d="M17 1.5v6M17 26.5v6M1.5 17h6M26.5 17h6" stroke="#1e2528" stroke-width="1.2"/></svg>"""
NAV = [("index.html","Home"),("committee.html","Committee"),("events.html","Events"),("resources.html","Resources"),("join.html","Join")]
def navhtml(fname):
    out=[]
    for h,t in NAV:
        cur = ' aria-current="page"' if h==fname else ''
        out.append('<a href="%s"%s>%s</a>' % (h,cur,t))
    return "".join(out)
def page(fname, title, body, desc):
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s · GPS &amp; Orgs Community</title>
<meta name="description" content="%s">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<header class="site"><div class="wrap">
  <a class="brand" href="index.html">%s<span><span class="name">GPS <span>&amp;</span> Orgs</span><span class="tag">Geography · Place · Space · Organisations</span></span></a>
  <nav class="main" aria-label="Main">%s</nav>
</div></header>
<main class="wrap">
%s
</main>
<footer class="site"><div class="wrap">
  <div>GPS &amp; Orgs Community · Geography, Place, Space and Organisations</div>
  <div><a href="join.html">Join the mailing list</a> · <a href="mailto:hello@gpsorgs.com">hello@gpsorgs.com</a></div>
</div></footer>
</body>
</html>
""" % (html.escape(title), html.escape(desc), LOGO, navhtml(fname), body)
pages = {}
pages["index.html"] = ("Home", "A community of researchers exploring organisations in relation to geography, place and space.", """
<section class="hero">
  <div class="kicker">A research community</div>
  <h1>Organisations, in place.</h1>
  <p class="lede">A community of researchers exploring how organisations are shaped by, and shape, the geographies, places and spaces they inhabit.</p>
  <div class="actions"><a class="btn accent" href="join.html">Join the mailing list</a><a class="btn" href="events.html">Events</a></div>
</section>
<hr class="rule">
<section class="band">
  <h2>What this is</h2>
  <p>We are an interdisciplinary group of academic researchers working at the meeting point of organisation studies and the spatial disciplines: geography, urban studies, architecture, the sociology of place. Our shared question is how the where of organising matters: the buildings, cities, regions, landscapes and digital spaces in which organisations take form.</p>
  <p>The community began with a one day event at UCL School of Management on 7 September 2026, <em>Space, Place, Geography and Organisations: Exploring Connections</em>, and grew out of conversations at EGOS and the Academy of Management. It is early, deliberately open, and shaped by whoever turns up.</p>
</section>
<section class="band">
  <div class="grid">
    <div class="card"><h3>Meet</h3><p>Events that bring people together around the work: a day, a seminar, a walk. <a href="events.html">See events</a>.</p></div>
    <div class="card"><h3>Read</h3><p>A growing set of readings, calls and related communities. <a href="resources.html">Resources</a>.</p></div>
    <div class="card"><h3>Belong</h3><p>The mailing list is the front door for now. <a href="join.html">Join</a>.</p></div>
  </div>
</section>
""")
pages["committee.html"] = ("Committee", "The steering committee and representatives of the GPS & Orgs Community.", """
<section class="page-title"><h1>Committee</h1><p class="lede">The people keeping the community moving.</p></section>
<section class="band">
  <h2>Steering committee</h2>
  <div class="people">
    <div class="person"><div class="who">Jen Rhymer</div><div class="where">UCL School of Management</div><div class="role">Steering</div></div>
    <div class="person"><div class="who placeholder">Name to add</div><div class="where placeholder">Institution</div><div class="role">Steering</div></div>
    <div class="person"><div class="who placeholder">Name to add</div><div class="where placeholder">Institution</div><div class="role">Steering</div></div>
    <div class="person"><div class="who placeholder">Name to add</div><div class="where placeholder">Institution</div><div class="role">Steering</div></div>
  </div>
  <h2>Representatives</h2>
  <p class="muted">Representatives are the community's points of contact at their institutions and disciplines.</p>
  <div class="people">
    <div class="person"><div class="who placeholder">Name to add</div><div class="where placeholder">Institution</div><div class="role">Representative</div></div>
    <div class="person"><div class="who placeholder">Name to add</div><div class="where placeholder">Institution</div><div class="role">Representative</div></div>
    <div class="person"><div class="who placeholder">Name to add</div><div class="where placeholder">Institution</div><div class="role">Representative</div></div>
    <div class="person"><div class="who placeholder">Name to add</div><div class="where placeholder">Institution</div><div class="role">Representative</div></div>
    <div class="person"><div class="who placeholder">Name to add</div><div class="where placeholder">Institution</div><div class="role">Representative</div></div>
    <div class="person"><div class="who placeholder">Name to add</div><div class="where placeholder">Institution</div><div class="role">Representative</div></div>
  </div>
  <p class="small muted" style="margin-top:28px">Want to represent your institution? <a href="join.html">Get in touch</a>.</p>
</section>
""")
pages["events.html"] = ("Events", "Upcoming and past events of the GPS & Orgs Community.", """
<section class="page-title"><h1>Events</h1><p class="lede">Where the community meets.</p></section>
<section class="band">
  <h2>Upcoming</h2>
  <p class="muted">The next event will be announced to the mailing list first. <a href="join.html">Join</a> to hear about it.</p>
  <h2>Past</h2>
  <div class="event">
    <div class="when">7 Sept 2026<small>Full day</small></div>
    <div>
      <h3>Space, Place, Geography and Organisations: Exploring Connections</h3>
      <div class="where">UCL School of Management, London</div>
      <p>The founding meeting. A day of talks, discussion and an academic workshop bringing together researchers from organisation studies and the spatial disciplines to map shared questions and set the community in motion.</p>
    </div>
  </div>
</section>
""")
pages["resources.html"] = ("Resources", "Readings, calls and related communities for research on organisations, geography, place and space.", """
<section class="page-title"><h1>Resources</h1><p class="lede">A working shelf, added to as the community grows.</p></section>
<section class="band">
  <div class="grid">
    <div class="card"><h3>Readings</h3><p class="placeholder">A short starter list of foundational and recent work at the intersection of organisations and space, place and geography. Coming soon.</p></div>
    <div class="card"><h3>Calls and tracks</h3><p class="placeholder">Conference sub-themes, special issues and workshops relevant to the community, including at EGOS and the Academy of Management. Coming soon.</p></div>
    <div class="card"><h3>Related communities</h3><p class="placeholder">Groups, networks and seminar series we are in conversation with. Coming soon.</p></div>
    <div class="card"><h3>From our events</h3><p class="placeholder">Slides, notes and summaries from community events, starting with 7 September 2026. Coming soon.</p></div>
  </div>
  <p class="small muted" style="margin-top:32px">Have something to add? <a href="mailto:hello@gpsorgs.com">Send it our way</a>.</p>
</section>
""")
pages["join.html"] = ("Join", "Join the GPS & Orgs Community mailing list.", """
<section class="page-title"><h1>Join</h1><p class="lede">For now, the community lives on its mailing list. Sign up to hear about events, calls and what members are working on.</p></section>
<section class="band">
  <form class="join" action="#" method="post" data-note="Form target not yet connected. Set action to the mailing list endpoint.">
    <div class="field"><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
    <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="affiliation">Institution or affiliation</label><input id="affiliation" name="affiliation" type="text" autocomplete="organization"></div>
    <div class="field"><label for="interests">What are you working on? <span class="muted">(optional)</span></label><textarea id="interests" name="interests" rows="3"></textarea></div>
    <div class="field"><label class="check"><input type="checkbox" name="consent" required><span>I would like to receive occasional emails from the GPS &amp; Orgs Community. Unsubscribe any time.</span></label></div>
    <button class="btn accent" type="submit">Join the mailing list</button>
    <p class="hint" style="margin-top:14px">Prefer email? Write to <a href="mailto:hello@gpsorgs.com">hello@gpsorgs.com</a>.</p>
  </form>
</section>
""")
for f,(t,d,b) in pages.items():
    open(f,"w").write(page(f,t,b,d))
print("pages:", ", ".join(pages))
