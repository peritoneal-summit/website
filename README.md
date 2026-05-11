# Peritoneal Summit — peritoneal-summit.com

Source code for the 2nd Peritoneal Summit website (Spiez, 8–10 September 2027).
Built with [Quarto](https://quarto.org), deployed to <https://peritoneal-summit.com>.

The site is currently in **Save the Date** mode. Registration opens September 2026.

## Edit and publish

The repo is maintained solo by the lead organizer. Edits happen either locally (Quarto + VS Code) or directly in the github.com web editor. Every push to `main` triggers `.github/workflows/publish.yml`, which renders the Quarto site and deploys it to GitHub Pages within ~1–2 minutes.

## Page layout

```
index.qmd            Home / Save the Date hero
program.qmd          Provisional 3-day structure, themes
speakers.qmd         Organizing committee + (TBD) keynote speakers
abstracts.qmd        Submission info (opens spring 2027)
registration.qmd     Provisional packages, Ticketino link (TBD)
venue.qmd            Spiez logistics, accommodation
contact.qmd          Organizer contact details
past/2025.qmd        Archive of the 1st Summit (Pontresina, January 2025)
```

## Tech

- Theme: light (Bootswatch `flatly`) with custom SCSS overlay (`theme-summit.scss`)
- Font: system sans-serif stack
- Deploy: GitHub Pages via Actions flow (not a `gh-pages` branch)
- Domain: `peritoneal-summit.com` via the `CNAME` file at repo root
- Registration backend: Ticketino (external, linked from `registration.qmd`)

## License

MIT for code, CC BY 4.0 for content — see [LICENSE](LICENSE).
