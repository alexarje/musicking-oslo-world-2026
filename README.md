# Musicking Technology: the reveal.js deck

English deck for Oslo World, Trekanten, 31 October 2026, in the MishMash style of the school deck of
30 October (`../../../2026-10-30-Musikk i skolen/presentation/`). Open `index.html` in a browser;
it works offline. S opens the speaker notes. Online at https://alexarje.github.io/musicking-oslo-world-2026/. The PDF beside it is the flat backup.

- `slides.html` holds the slides and notes. Edit it, then run `.venv/bin/python tools/assemble.py`,
  which wraps it in the school deck's styles and scripts (`index-school.html`) to give `index.html`.
- `tools/make_figs.py` draws every figure as stacked SVG layers: the musicking quadrant and its
  overlays (axes, links between all four corners, AI and technology in the middle),
  product and process, 4E cognition and embodied and social.
- `tools/palette.py` holds the sunrise palette (light fills for figures and page styles, strong colours for the section openers); `assemble.py` maps the inherited MishMash colours to it.
- `tools/make_qr.py` writes the QR code to the open-access book at MIT Press.
- `tools/build_pdf.py` rebuilds the PDF (it writes to the first *.pdf in the folder);
  `tools/notes_sheet.py` writes `../notes.md`.
- Intro figure and photos from the EDM deck of 29 October; new English UiO logo trimmed from
  `photos/logos/UiO/ny logo/03_uio_full_logo_eng_pos[1].png`; Sound Actions cover from
  `writing/0-SoundActions/cover pics/jensenius.actionspng.png`.
- Pushing to `main` deploys to GitHub Pages (`.github/workflows/pages.yml`).
