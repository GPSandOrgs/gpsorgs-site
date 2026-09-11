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
      <p class="small muted">Organised by Jen Rhymer (UCL), Alessandra Migliore (Politecnico di Milano) and Santi Furnari (Bayes Business School).</p>
    </div>
  </div>
</section>
""")
pages["resources.html"] = ("Resources", "Announcements, calls, readings and related networks for research on organisations, geography, place and space.", """
<section class="page-title"><h1>Resources</h1><p class="lede">A shared noticeboard and shelf for the community. Announcements and calls are posted as they come in; the reading list grows as members add to it.</p>
<nav class="subnav" aria-label="On this page"><a href="#announcements">Announcements</a><a href="#calls">Calls and tracks</a><a href="#readings">Readings</a><a href="#networks">Related networks</a></nav></section>

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

<section class="band" id="readings">
  <h2>Readings</h2>
  <p class="muted">A starter shelf, organised by the provisional map of research conversations drawn up at the 7 September event. The map is a working device, not a taxonomy; the boundaries are exactly what the community is here to question.</p>
  <h3 class="shelf-cat">Areas</h3>
  <div class="shelf">
    <div class="shelf-item"><h3>Organisational space and spatial practice</h3><p>Space as experienced, practised and socially produced, including how organisational power relations take material form.</p><ul><li>Taylor, S. and Spicer, A. (2007). Time for space: A narrative review of research on organizational spaces. <em>International Journal of Management Reviews</em>.</li></ul></div>
    <div class="shelf-item"><h3>Proximity, microgeography and the built environment</h3><p>Enclosures, barriers, layout and ambient surroundings that shape interaction and behaviour.</p><ul><li>Elsbach, K. D. and Pratt, M. G. (2007). The physical environment in organizations. <em>Academy of Management Annals</em>.</li></ul></div>
    <div class="shelf-item"><h3>Place, meaning and identity</h3><p>Spaces made meaningful through experience, attachment, narrative and collective interpretation.</p><ul><li>Gieryn, T. F. (2000). A space for place in sociology. <em>Annual Review of Sociology</em>.</li><li>Cresswell, T. (2004). <em>Place: A Short Introduction</em>. Blackwell.</li></ul></div>
    <div class="shelf-item"><h3>Cities, regions and neighbourhoods</h3><p>Local communities, cities, regions and ecosystems that shape organisational practices, opportunities and outcomes.</p><ul><li>Marquis, C. and Battilana, J. (2009). Acting globally but thinking locally? The enduring influence of local communities on organizations. <em>Research in Organizational Behavior</em>.</li></ul></div>
    <div class="shelf-item"><h3>Infrastructure and meso-geography</h3><p>Material and connective systems that enable, organise and constrain activity across places and scales.</p><ul><li class="placeholder">Starter references to be added.</li></ul></div>
    <div class="shelf-item"><h3>Distributed and virtual spaces</h3><p>Organising across dispersed, hybrid and digitally mediated spaces, shaped by technologies and changing patterns of presence and mobility.</p><ul><li>Mazmanian, M., Orlikowski, W. J. and Yates, J. (2013). The autonomy paradox: The implications of mobile email devices for knowledge professionals. <em>Organization Science</em>.</li><li>Leonardi, P. M. (2021). COVID-19 and the new technologies of organizing: Digital exhaust, digital footprints, and artificial intelligence in the wake of remote work. <em>Journal of Management Studies</em>.</li></ul></div>
  </div>
  <h3 class="shelf-cat">Methods</h3>
  <div class="shelf">
    <div class="shelf-item"><h3>Space syntax</h3><p>Analysing the configuration of buildings and cities to show how spatial layout shapes movement, encounter and interaction.</p><ul><li>Hillier, B. and Hanson, J. (1984). <em>The Social Logic of Space</em>. Cambridge University Press.</li><li>Hillier, B. (1996). <em>Space is the Machine: A Configurational Theory of Architecture</em>. Cambridge University Press.</li><li>Sailer, K. and McCulloh, I. (2012). Social networks and spatial configuration: How office layouts drive social interaction. <em>Social Networks</em>.</li></ul></div>
    <div class="shelf-item"><h3 class="placeholder">Further methods to add</h3><p class="placeholder">Mapping and GIS, ethnographies of place, spatial network analysis, and more, as members contribute.</p></div>
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
