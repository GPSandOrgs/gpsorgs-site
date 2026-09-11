GPS & Orgs Community site (gpsorgs.com). Static HTML, one shared stylesheet in assets/site.css, no build step. Deployed by Cloudflare Pages from this repo: build command empty, output directory `/`.

Pages: index, committee, events, resources, join. Placeholders are marked in italics (class "placeholder"). The join form has no target yet (see data-note on the form).

Join form: `functions/api/join.js` appends each signup to `signups.csv` in this repo through the GitHub API. Requires the Pages secret `GITHUB_TOKEN` (fine-grained token, this repo only, Contents read and write). The Drive file `GPS Orgs Community/mailing-list.csv` is the working list; sync from `signups.csv`.
