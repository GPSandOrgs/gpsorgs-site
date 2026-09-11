import html
LOGO = """<svg viewBox="0 0 34 34" aria-hidden="true"><circle cx="17" cy="17" r="15.5" fill="none" stroke="#1d2624" stroke-width="1.4"/><circle cx="17" cy="17" r="9.5" fill="none" stroke="#2f5d6b" stroke-width="1.2"/><circle cx="17" cy="17" r="4" fill="#4f6b52"/><path d="M17 1.5v6M17 26.5v6M1.5 17h6M26.5 17h6" stroke="#1d2624" stroke-width="1.2"/></svg>"""
NAV = [("/","Home"),("/committee","Committee"),("/events","Events"),("/resources","Resources"),("/join","Join")]
def navhtml(fname):
    out=[]
    for h,t in NAV:
        cur = ' aria-current="page"' if h==('/' if fname=='index.html' else '/'+fname[:-5]) else ''
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
  <a class="brand" href="/">%s<span><span class="name">GPS <span>&amp;</span> Orgs</span><span class="tag">Geography · Place · Space · Organisations</span></span></a>
  <nav class="main" aria-label="Main">%s</nav>
</div></header>
<main class="wrap">
%s
</main>
<footer class="site"><div class="wrap">
  <div>GPS &amp; Orgs Community · Geography, Place, Space and Organisations</div>
  <div><a href="/join">Join the mailing list</a></div>
</div></footer>
</body>
</html>
""" % (html.escape(title), html.escape(desc), LOGO, navhtml(fname), body)
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
  <h2>What this is</h2>
  <p>Research on organisations and geography, place and space runs in many conversations at once: organisational space and spatial practice, proximity and the built environment, place and meaning, cities and regions, infrastructure, distributed and virtual work. They use different vocabularies, work at different scales, and reach well beyond management and organisation studies into architecture, urban planning, geography and sociology. Often they do not meet.</p>
  <p>This community exists to connect them. It grew out of conversations at EGOS and the Academy of Management and took shape at a first event at UCL School of Management on 7 September 2026. It is early, deliberately open, and will be shaped by the people who join it.</p>
</section>
<section class="band">
  <div class="grid">
    <div class="card"><h3>Meet</h3><p>Events that bring people together around the work: a day, a seminar, a walk. <a href="/events">See events</a>.</p></div>
    <div class="card"><h3>Read</h3><p>A growing set of readings, calls and related communities. <a href="/resources">Resources</a>.</p></div>
    <div class="card"><h3>Belong</h3><p>The mailing list is the front door for now. <a href="/join">Join</a>.</p></div>
  </div>
</section>
""")
pages["committee.html"] = ("Committee", "The steering committee and representatives of the GPS & Orgs Community.", """
<section class="page-title"><h1>Committee</h1><p class="lede">The people keeping the community moving.</p></section>
<section class="band">
  <h2>Steering committee</h2>
  <p class="muted">To be announced.</p>
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
      <p class="small muted">Organised by Jen Rhymer (UCL), Alessandra Migliore (Politecnico di Milano) and Santi Furnari (Bayes Business School).</p>
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
    <div class="card"><h3>Related conversations</h3><p>Some of the existing conversations this community builds on:</p><p>EGOS Standing Working Group 07, Organizations and Place-Based Communities<br>The AOM PDW series on Organisational Spaces<br>RGCS, the Research Group on Collaborative Spaces, and its annual symposium</p></div>
    <div class="card"><h3>From our events</h3><p class="placeholder">Slides, notes and summaries from community events, starting with 7 September 2026. Coming soon.</p></div>
  </div>
</section>
""")
pages["join.html"] = ("Join", "Join the GPS & Orgs Community mailing list.", """
<section class="page-title"><h1>Join</h1><p class="lede">For now, the community lives on its mailing list. Sign up to hear about events, calls and what members are working on.</p></section>
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
for f,(t,d,b) in pages.items():
    open(f,"w").write(page(f,t,b,d))
print("pages:", ", ".join(pages))
