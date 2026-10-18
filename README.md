# amsat-repeaters

Pass planning and printable cue sheets for two-way FM amateur satellite contacts
(SO-50, LilacSat-2, the ISS repeater) from Dayton, OH (KF8EEZ).

Split out of the `sstv-iss` repo (ARISS SSTV reception and LimeSDR measurements);
that repo keeps the SDR work.

```sh
uv sync
uv run upcoming.py                       # passes in the next 48 h
uv run upcoming.py --from 2026-10-19T04:00 --to 2026-10-19T07:00
export QUARTO_PYTHON=$PWD/.venv/bin/python
uv run sat_cue_sheets.py --days 2 --min-el 10      # one-page PDFs in data/cue_sheets/
quarto render reports/index.qmd                    # upcoming-pass page in _output/
```

One-time Quarto setup: `uv run python -m ipykernel install --user --name amsat-repeaters`
(Quarto 1.10+ and its Typst support are needed for the PDFs).

Agents: start with `_agents/README.md`.
