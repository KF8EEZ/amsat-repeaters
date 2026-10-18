#!/usr/bin/env python3
"""One-page printable cue sheets for two-way FM satellite passes.

Each ladder row carries both an uplink (TX) and a downlink (RX) frequency,
Doppler-corrected and rounded to a 5 kHz step, plus the satellite's tone/arming notes.
Rendered by Quarto from reports/sat-cue-sheet.qmd, one PDF per pass.

Usage:
    uv run sat_cue_sheets.py --start 2026-10-17T07:00 --days 0.6 --min-el 20
    uv run sat_cue_sheets.py --sats SO-50 LilacSat-2 --days 2

TLEs are cached in data/tle/<norad>.tle and refreshed from Celestrak when possible
(passes.py).
"""
import argparse
import shutil
import subprocess
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from skyfield.api import load, wgs84

from passes import doppler_khz, find_passes, load_sat

ROOT = Path(__file__).resolve().parent
STEP_S = 30

# Frequencies from the AMSAT live FM table (amsat.org/live-fm-satellites) and
# the LilacSat-2 page; availability is NOT guaranteed.
SATS = {
    "SO-50": dict(
        norad=27607, up=145.850, down=436.795, tone="67.0 Hz CTCSS", ctcss=67.0, arm=74.4,
        notes=["ARM FIRST: 2 s carrier with 74.4 Hz tone, then switch to 67.0 Hz. "
               "The timer runs about 10 min, so arm just after rise (re-arm if it drops).",
               "Single-channel FM: short calls, no long conversations."]),
    "LilacSat-2": dict(
        norad=40908, up=144.350, down=437.200, tone="no tone", ctcss=None, arm=None,
        notes=["FM transponder planned for 24 h from ~22:00 UTC Mon/Wed/Fri "
               "(AMSAT: flexible, subject to change).",
               "Listen on the downlink first; a telemetry beacon may be heard when the transponder is off."]),
    "ISS": dict(
        norad=25544, up=145.990, down=437.800, tone="67.0 Hz CTCSS", ctcss=67.0, arm=None,
        notes=["ISS FM repeater availability varies (check the AMSAT / ARISS status pages).",
               "If the crew is using the station radio for other modes it will be silent."]),
}
GENERAL = [
    ("Identify", "KF8EEZ, short calls; low power. Keep both radios and the TX antenna well away from the SDR"),
    ("Two radios", "Yaesu VX-6R + MH-57A4B speaker mic = uplink TX (log-periodic); Alinco DJ-VX50 = downlink RX. "
                   "Use an earphone on the Alinco so its speaker doesn't feed the speaker mic"),
    ("Aim (log-periodic)", "point AT satellite: pre-aim at rise Az, follow the Az/El ladder; slant 45°"),
]


def rx_radio(info):
    """Alinco DJ-VX50 downlink receive settings (menu numbers: DJ-VX50 manual pp.22-24).

    Menu items are listed in numerical order so they can be stepped through in sequence.
    """
    digits = " ".join(f"{info['down']:.3f}".replace(".", ""))
    return [
        ("Menu access", "FUNC, then 8, UP/DOWN to the menu number, dial = value, FUNC = confirm, ESC = exit"),
        ("Frequency", f"VFO mode: key in digits, e.g. {info['down']:.3f} = {digits}; the dial then retunes for Doppler"),
        ("Menu 01 R-CDC", "OFF (default): a tone squelch would mute the downlink"),
        ("Menu 03 STEP", "5K (default is 10K), so each dial click is one ladder step"),
        ("Menu 04 W/N", "WIDE (default)"),
        ("Menu 17 SAVE", "OFF (default is ON): battery saver can clip weak openings"),
        ("Menu 19 SQL", "start at 1-2 (default 9 is tight); raise only if noise is constant"),
        ("Menu 20 REPEAT", "OFF (default), and FUNC 4 until no offset is shown: simplex"),
        ("Keypad lock", "FUNC, then hold #; the dial still retunes, and PTT stays untouched on this radio"),
        ("Audio", "Earphone, volume up enough to hear a weak FM carrier"),
    ]


def tx_radio(info):
    """Yaesu VX-6R + MH-57A4B uplink settings (Set Mode items: VX-6R operating manual).

    Direct key sequences first, then the Set Mode items in numerical order.
    """
    if info["ctcss"] is None:
        tone = ("Tone", "none: [F/W] then [MODE(SPS) SQ TYP], dial until no TONE shows, PTT to save")
    else:
        tone = ("Tone", f"[F/W] then [MODE(SPS) SQ TYP], dial to TONE (not T SQL), PTT to save; "
                        f"[F/W] then [2(CODE)], dial to {info['ctcss']:.1f} Hz, press [2(CODE)] to save")
    rows = [
        ("Set Mode access", "[F/W] then [0(SET)], dial to the item, [0(SET)] to edit, dial = value, PTT = save"),
        ("Frequency", f"VHF band, VFO: key in digits for {info['up']:.3f}; the dial retunes for Doppler"),
        tone,
        ("Power", "[F/W] then [7(LK)TXPO] cycles HIGH / LOW3 (2.5 W) / LOW2 (1 W) / LOW1; use LOW3"),
        ("Set Mode 1 APO", "OFF"),
        ("Set Mode 4 ARS", "OFF"),
        ("Set Mode 6 BCLO", "OFF, so PTT is never blocked by the downlink"),
        ("Set Mode 27 HLF.DEV", "OFF: full deviation"),
        ("Set Mode 37 MCGAIN", "LVL 5, adjust to your voice on the speaker mic"),
        ("Set Mode 51 RPT", "SIMP (simplex); shortcut [F/W] [6(RPT)]"),
        ("Set Mode 67 TOT", "1 min (default 3)"),
        ("Set Mode 70 TXSAVE", "OFF"),
        ("Do not", "tap [7(LK)TXPO] alone: it turns on the Internet DTMF beep at every TX"),
    ]
    if info["arm"]:
        rows.append(("Arming tone", f"set tone to {info['arm']:.1f} Hz (as above) and key 2 s, "
                                    f"then set {info['ctcss']:.1f} Hz and talk"))
    return rows


def r5(mhz):
    return round(mhz * 1000 / 5) * 5 / 1000


def sat_ladder(sat, site, ts, rise, setting, up_mhz, down_mhz, step_s=STEP_S):
    """[(time, el, az, tx_mhz, rx_mhz), ...] every step_s while above the horizon."""
    rows, t0, t1, s = [], rise.utc_datetime(), setting.utc_datetime(), 0
    while t0 + timedelta(seconds=s) <= t1:
        tt = ts.from_datetime(t0 + timedelta(seconds=s))
        alt, az, _ = (sat - site).at(tt).altaz()
        if alt.degrees >= 0:
            d_up = float(doppler_khz(sat, site, tt, up_mhz))
            d_dn = float(doppler_khz(sat, site, tt, down_mhz))
            rows.append((t0 + timedelta(seconds=s), alt.degrees, az.degrees,
                         r5(up_mhz - d_up / 1e3), r5(down_mhz + d_dn / 1e3)))
        s += step_s
    return rows


def render(name, rise, peak, setting, el, az_r, az_s, args, out_path):
    bare = f".satcue_tmp_{uuid.uuid4().hex}.pdf"
    cmd = ["quarto", "render", "reports/sat-cue-sheet.qmd",
           "-P", f"sat_name:{name}",
           "-P", f"rise_iso:{rise.utc_datetime().isoformat()}",
           "-P", f"peak_iso:{peak.utc_datetime().isoformat()}",
           "-P", f"set_iso:{setting.utc_datetime().isoformat()}",
           "-P", f"max_el:{el}", "-P", f"az_r:{az_r}", "-P", f"az_s:{az_s}",
           "-P", f"lat:{args.lat}", "-P", f"lon:{args.lon}", "-P", f"elev:{args.elev}",
           "-P", f"tz_name:{args.tz}", "-P", f"beamwidth_deg:{args.beamwidth}",
           "--output", bare]
    try:
        subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)
    finally:
        for png in (ROOT / "reports").glob(".satskyplot_*.png"):
            png.unlink()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(ROOT / bare, out_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sats", nargs="*", default=list(SATS), choices=list(SATS))
    ap.add_argument("--lat", type=float, default=39.76)
    ap.add_argument("--lon", type=float, default=-84.19)
    ap.add_argument("--elev", type=float, default=225)
    ap.add_argument("--tz", default="America/New_York")
    ap.add_argument("--start", help="ISO 8601; naive = local --tz (default now)")
    ap.add_argument("--days", type=float, default=1)
    ap.add_argument("--min-el", type=float, default=20)
    ap.add_argument("--beamwidth", type=float, default=74.0,
                    help="antenna half-power beamwidth for the gray sky-plot zone (Elk 2M/440L5: 8.7 dBi at 2 m)")
    ap.add_argument("--out-dir", type=Path, default=Path("data/cue_sheets"))
    args = ap.parse_args()

    tz = ZoneInfo(args.tz)
    start = datetime.fromisoformat(args.start) if args.start else datetime.now(timezone.utc)
    if start.tzinfo is None:
        start = start.replace(tzinfo=tz)
    ts = load.timescale()
    site = wgs84.latlon(args.lat, args.lon, args.elev)
    out = []
    for name in args.sats:
        sat = load_sat(SATS[name]["norad"], ts)
        for rise, peak, setting, el, az_r, az_s in find_passes(sat, site, ts, start, args.days, args.min_el):
            path = args.out_dir / f"sat_{name}_{rise.astimezone(tz):%Y%m%d_%H%M}.pdf"
            render(name, rise, peak, setting, el, az_r, az_s, args, path)
            out.append((rise, name, el, path))
    if not out:
        print("No qualifying passes.")
    for rise, name, el, path in sorted(out):
        print(f"{rise.astimezone(tz):%a %m/%d %H:%M} {name:10s} {el:3.0f}°  -> {path}")


if __name__ == "__main__":
    main()
