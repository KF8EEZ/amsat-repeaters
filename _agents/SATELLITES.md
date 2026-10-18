# Satellites

Downlink frequencies are on 70 cm; uplinks on 2 m. From the AMSAT live FM table
(https://www.amsat.org/live-fm-satellites). Availability is not guaranteed; check
the AMSAT status pages and the Dayton pass list before relying on any of them.

| Satellite | NORAD | Uplink MHz | Uplink tone | Downlink MHz |
|---|---|---|---|---|
| SO-50 | 27607 | 145.850 | 67.0 Hz (after arming) | 436.795 |
| LilacSat-2 | 40908 | 144.350 | none | 437.200 |
| ISS repeater | 25544 | 145.990 | 67.0 Hz | 437.800 |

The code's single source for these is `SATS` in `sat_cue_sheets.py`
(`LISTEN_ONLY` in `upcoming.py` lists downlink-only watch targets: HADES-SA 436.875
NORAD 68446, RS95S 436.950 NORAD 67291, TEVEL2-1 436.400 NORAD 63217).

## Operating notes
- **SO-50:** must be armed. Send a ~2 s carrier with 74.4 Hz tone, then talk at 67.0 Hz. The
  timer runs about 10 min, so arm just after rise and re-arm if it drops. Single-channel FM:
  short calls only. Radio tone changes are on the cue sheet.
- **LilacSat-2:** FM transponder planned for 24 h starting about 22:00 UTC (18:00 EDT) on
  Mondays, Wednesdays and Fridays. AMSAT says flexible and subject to change
  (https://www.amsat.org/two-way-satellites/lilacsat-2-cas-3h/). Outside that it may send a
  telemetry beacon on 437.200. Expect silence on Sunday/Tuesday/Thursday/Saturday daytime.
- **ISS repeater:** availability varies; silent when the crew uses the radio for other modes.
  ISS-SSTV on 437.550 is a separate receive-only matter (ARISS series starts 2026-10-22).
- **Doppler:** ladder is for 5 kHz steps. TX = nominal minus Doppler, RX = nominal plus
  Doppler (error up to 2.5 kHz from rounding). Rows are every 30 s.
- **Not included:** PO-101 downlinks on 145.900 (437.500 is an uplink, may be failing), SO-124
  decayed, HADES-ICM has no TLE. HADES-SA is SSDV FSK (not FM), listen-only.
