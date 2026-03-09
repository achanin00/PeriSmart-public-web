# PeriSmart Public Website Source

This folder contains the static HTML/CSS source for the PeriSmart public website.

## Files

- `index.html`
- `platform.html`
- `how-it-works.html`
- `privacy-deployment.html`
- `contact.html`
- `styles.css`
- `includes/header.html` — shared site header (injected by `includes/load.js`)
- `includes/footer.html` — shared site footer (injected by `includes/load.js`)
- `includes/load.js` — loads header and footer into each page and sets the active nav link

Pages use placeholder `<div id="site-header">` and `<div id="site-footer">`; the script runs at the end of each page to fetch and inject the shared markup. Serve the site over HTTP (e.g. `python -m http.server 8000`) so the fetch requests succeed; opening files directly with `file://` may block includes.

## Assets

Copied website assets live under `assets/` so this folder can be treated as a self-contained source tree.

## Pre-Launch Replacements

Before publishing:
- replace the placeholder contact email in `contact.html`
- replace any placeholder scheduling link if you want direct booking
- add final legal page links if available
