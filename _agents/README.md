# Agent guide: amsat-repeaters

Read these in order:

1. `PROJECT.md`: goal, operator, station, standing rules.
2. `SATELLITES.md`: frequencies, tones, procedures and status of each satellite.
3. `EQUIPMENT.md`: radios, antennas, and how the cue sheets are built.
4. `PACKING.md`: checklist for taking the setup out.
5. `TODO.md`: open work.

Code: `passes.py` (TLE cache, pass finder, Doppler), `sat_cue_sheets.py`
(satellite table, per-radio settings, PDF generation), `upcoming.py` (CLI pass list),
`reports/sat-cue-sheet.qmd` (Typst template, one PDF per pass),
`reports/index.qmd` (upcoming-pass page). Manuals are in `data/manuals/`.
