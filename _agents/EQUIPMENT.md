# Equipment and cue sheets

## Radios
- **Uplink: Yaesu VX-6R** with MH-57A4B speaker mic. Low power (LOW3, 2.5 W). VHF.
  Manual: `data/manuals/VX-6R_E_EH021M217_2101E-QS.pdf` (the full operating manual despite the
  "QS" name). Settings are Set Mode items (FUNC/W, then 0 to enter).
- **Downlink: Alinco DJ-VX50** (UHF). Manual: `data/manuals/DJ-VX50HE_HT_manual.pdf` (scanned,
  two manual pages per PDF page). Menu: FUNC, then 8, UP/DOWN to the number, dial for the value,
  FUNC to confirm, ESC to exit. Defaults are on manual p.24.
- **Antennas:** hand-aimed Elk 2M/440L5 log-periodic on a tripod for the uplink (8.7 dBi at 2 m,
  estimated 74 deg beamwidth, the gray zone on the sky plot). Aim: point AT the satellite,
  pre-aim at the rise azimuth, follow the ladder, slant 45 deg. The Alinco uses its own antenna.
- The home LimeSDR is a separate system in the sstv-iss repo, with a Comet GI990NMO mobile
  antenna (7.7 dBi at UHF, terrestrial-focused pattern). Keep the TX radio and antenna well away
  from it (front-end overload).

## Audio recorder (planned)
The operator wants a recorder to capture every contact so nothing has to be written down
in the moment. Model not chosen yet. The operator currently uses no earpiece: the DJ-VX50
speaker is audible and the VX-6R speaker mic is used for speaking. So one recorder placed near
the operator and the Alinco speaker should capture both the downlink and the operator's voice
(simplest plan; try it first). Caveat: the Alinco speaker also feeds the VX-6R mic when the
operator is keyed, so keep the speaker volume modest and the Alinco away from the mic. Fallbacks
if the audio is poor: a Y-splitter from the Alinco earphone jack into the recorder's line-in, or
a small lav mic on the operator into a two-input recorder. Whatever is chosen must not need a
free hand. Start/stop is handled per pass (see `PACKING.md`). Contact times then come from the
recording, so the "roughly to the minute" log in `TODO.md` can be filled from the audio.

## What the cue sheets contain
One page per pass (Typst PDF via Quarto): header (times, peak, azimuths), TX/RX frequency,
30 s ladder (time, TX, RX, az, el), sky plot with the satellite's track, then two columns of radio
settings, satellite notes and general reminders. Code paths:
- `SATS`, `GENERAL`, `rx_radio(info)` and `tx_radio(info)` in `sat_cue_sheets.py`.
- `reports/sat-cue-sheet.qmd` lays it out; values are passed with `-P` (needs papermill).
- Escape `\ # * _ $ @ < ` ~` in text that goes into Typst (`esc()` in the template).
- Keep each radio's rows to ~13 lines at 8 pt or the sheet spills to a second page.
  Check with `pdfinfo` after changes.

## Verified vs. unverified
- Menu numbers and key sequences come straight from the manuals. They were not bench-tested
  on the radios. If the operator reports a sequence that does not work, fix it in
  `rx_radio`/`tx_radio` and regenerate.
- DJ-VX50 menu 19 SQL: default is 9 and the manual says 0-9; the sheet says start at 1-2.
  Confirm direction (lower = more open) on the radio.
