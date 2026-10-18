# Project: two-way FM satellite contacts (Dayton, OH)

## Goal
Make contacts through FM satellite repeaters and plan for them. The operator is a
licensed amateur (KF8EEZ) who transmits on VHF and monitors the 70 cm downlink.
Tooling here predicts passes, prints one-page cue sheets (Doppler-corrected TX and RX
frequencies, azimuth/elevation, radio settings), and lists upcoming passes.

- Location: 39.76 N, -84.19 W, 225 m. Time zone America/New_York (all printed times local).
- This repo was split from `~/proj/sstv-iss` (ARISS SSTV + LimeSDR). That repo keeps the
  SDR recorder and report; do not move that work here. Cue sheet and pass-planning code was
  copied here and is now maintained here (the sstv-iss copy is not synced).

## Standing rules
- The operator transmits; agents never do. Do not suggest transmitting in ways that
  break licence rules; keep calls short, low power, identify with the callsign.
- No attribution lines (Co-Authored-By etc.) in commit messages. Use `git commit -F file`
  when a message contains backticks.
- Commit `_output/` after rendering (rendered reports and cue-sheet PDF copies are browsable
  from GitHub). Raw/generated files in `data/cue_sheets/` and `data/tle/` stay out of git.
- Render needs `QUARTO_PYTHON=$PWD/.venv/bin/python`; the Jupyter kernel is `amsat-repeaters`.
- Remote: `origin` = git@github.com:KF8EEZ/amsat-repeaters.git. Push only when asked.
- Cue sheets must stay one page each. Menu items on the sheets are listed in numerical
  order so the operator can step through them.

## Operator preferences learned so far
- One hand is on the antenna tripod; the other handles the radios (Doppler tuning, speaking).
  Do not add steps that need more hands. Aim plan stays the original: pre-aim at the rise
  azimuth, follow the Az/El ladder (the operator is fixing the tripod mechanically).
- The channel is shared with other hams, so a keying schedule is impractical. Contact
  timing is logged by the operator afterwards (roughly to the minute).
- Low-elevation passes are preferred for tests: the home SDR's antenna favors the horizon.
  Generate sheets down to 10 deg peak elevation.
- Uplink radio is the Yaesu VX-6R with an MH-57A4B speaker mic (easier to speak into);
  downlink radio is the Alinco DJ-VX50 with an earphone (so its speaker does not feed the mic).

## Findings from the SDR (sstv-iss repo, 2026-10-16/18)
A LimeSDR at the same site watched downlinks 435.85-438.35 MHz on TLE-scheduled windows.
- The ISS repeater (437.800) showed weak narrowband bursts (6-10 dB, ~4% of rows) tracking the
  predicted Doppler line on three passes (05:02, 06:37, 13:08 EDT on 10/17), including passes
  before the operator transmitted: other stations or the ISS itself were active.
- The operator's own attempt on 10/17 13:08 produced broken audio on the downlink. Unclear
  whether anyone heard the uplink. Strongest audio mid-pass.
- Not seen: SO-50 (including the 08:59 pass), LilacSat-2 (outside its FM window), HADES-SA,
  RS95S, TEVEL2-1, ISS-SSTV (series starts 2026-10-22).
- The SDR cannot see the 2 m uplink (145 MHz). Only repeater retransmissions on 70 cm.
