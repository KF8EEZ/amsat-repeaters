# TODO

- Regenerate cue sheets for the coming days: `uv run sat_cue_sheets.py --days 2 --min-el 10`,
  copy `data/cue_sheets/sat_*.pdf` into `_output/data/cue_sheets/`, re-render
  `reports/index.qmd`, commit.
- After each attempted contact, ask the operator for approximate transmit times and what they
  heard; keep a log (`data/contacts.csv` is a good place; not created yet).
- Compare the operator's times with the SDR bursts (data in sstv-iss `data/sats/`, burst search in
  `sdr_report.py` there) to see whether the repeater relayed the uplink.
- A local 70 cm repeater test (e.g. K8MCA 444.250 out / 449.250 in, tone 123.0) would check the
  whole chain without Doppler or sharing: key the VX-6R/DJ-VX50 into it while the SDR records.
- Optional: ICS calendar export of passes; pass filter by horizon mask (needs the sstv-iss
  empirical mask); LilacSat-2 window marker on the pass list (see `lilacsat_scheduled` in
  sstv-iss `sdr_report.py`).
- No git remote yet; ask before creating one or pushing.
