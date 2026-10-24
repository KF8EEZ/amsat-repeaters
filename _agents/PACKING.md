# Packing checklist: portable satellite setup

Tick off before leaving. Items marked (?) are not confirmed against the actual kit; fix the
list once the operator has packed it once.

## Before leaving
- [ ] Cue sheets printed (`uv run sat_cue_sheets.py --days 2 --min-el 10`), one page per pass
- [ ] Pass times checked against the site (if not Dayton, rerun with that lat/lon)
- [ ] TLEs fresh (run `uv run upcoming.py` online the same day)
- [ ] Phone/tablet has the `_output/` pass page cached for offline use (?)
- [ ] All batteries charged (radios, recorder, headlamp)

## Uplink (VHF)
- [ ] Yaesu VX-6R
- [ ] MH-57A4B speaker mic
- [ ] Spare VX-6R battery or AA case (?)
- [ ] Charger / USB cable

## Downlink (UHF)
- [ ] Alinco DJ-VX50
- [ ] Earphone (optional; not used at present, speaker is audible and gets recorded)
- [ ] Spare battery (?)
- [ ] Its own antenna

## Antenna and aiming
- [ ] Elk 2M/440L5 log-periodic
- [ ] Tripod, with the mount/clamp for the Elk
- [ ] Coax to the VX-6R, plus adapters for the connector types (?)
- [ ] Compass or phone compass app for the rise azimuth
- [ ] Marked azimuth reference (landmark or tape) so pre-aiming is quick (?)

## Audio recording
- [ ] Recorder, charged, with free storage (see `EQUIPMENT.md` for the setup question)
- [ ] Spare batteries / power bank and cable
- [ ] Windscreen
- [ ] Clip, lanyard or pocket so it needs no hands
- [ ] Recorder started before AOS and stopped after LOS, one file per pass; say the satellite
      name and local time at the start of each file

## Operating comfort
- [ ] Headlamp, ideally with red mode (night passes)
- [ ] Clipboard and pencil (backup for notes)
- [ ] Clip or weights so the cue sheet does not blow away
- [ ] Warm clothes, gloves with a free trigger finger, rain cover
- [ ] Water
- [ ] Power bank for phone

## Licence and etiquette
- [ ] Callsign (KF8EEZ) on the cue sheet; identify on each transmission
- [ ] Low power (LOW3, 2.5 W); short calls only on shared single-channel FM

## Site
- [ ] Open view to the horizon in the rise and set directions
- [ ] Away from strong local RF and metal structures
- [ ] The home LimeSDR is not part of this kit; leave it at home (TX near it overloads its front end)
