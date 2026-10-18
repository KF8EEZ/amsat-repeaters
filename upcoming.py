#!/usr/bin/env python3
"""List upcoming passes of the two-way FM satellites (and listen-only ones).

    uv run upcoming.py                                   # next 48 h, >= 10 deg
    uv run upcoming.py --from 2026-10-19T04:00 --to 2026-10-19T07:00
    uv run upcoming.py --sats ISS SO-50 --min-el 20
    uv run upcoming.py --two-way

Times are local (--tz). Naive --from/--to values are read as local time.
"""
import argparse
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from skyfield.api import load, wgs84

from passes import find_passes, load_sat
from sat_cue_sheets import SATS

# Downlink-only targets (no uplink to use); same data as the SDR repo's recorder.
LISTEN_ONLY = {
    "HADES-SA": dict(norad=68446, down=436.875, note="FSK 200/800 baud SSDV"),
    "RS95S": dict(norad=67291, down=436.950, note=""),
    "TEVEL2-1": dict(norad=63217, down=436.400, note="9600 bps BPSK beacon"),
}


def upcoming(start, end, min_el=10.0, sats=None, two_way_only=False, lat=39.76, lon=-84.19, elev=225):
    """Return [(rise, peak, set, max_el, az_r, az_s, name, info)] sorted by rise (tz-aware UTC)."""
    ts = load.timescale()
    site = wgs84.latlon(lat, lon, elev)
    table = {**{n: dict(i, two_way=True) for n, i in SATS.items()},
             **({} if two_way_only else {n: dict(i, two_way=False) for n, i in LISTEN_ONLY.items()})}
    out = []
    for name, info in table.items():
        if sats and name not in sats:
            continue
        sat = load_sat(info["norad"], ts)
        # search a little early so a pass already in progress at `start` is not lost
        for r, p, s, el, az_r, az_s in find_passes(sat, site, ts, start - timedelta(minutes=20),
                                                  (end - start).total_seconds() / 86400 + 0.03, min_el):
            ru, su = r.utc_datetime(), s.utc_datetime()
            if su >= start and ru <= end:
                out.append((ru, p.utc_datetime(), su, el, az_r, az_s, name, info))
    return sorted(out, key=lambda x: x[0])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="t0", help="ISO start (default now)")
    ap.add_argument("--to", dest="t1", help="ISO end (default start + --hours)")
    ap.add_argument("--hours", type=float, default=48)
    ap.add_argument("--min-el", type=float, default=10)
    ap.add_argument("--sats", nargs="*")
    ap.add_argument("--two-way", action="store_true", help="skip listen-only satellites")
    ap.add_argument("--tz", default="America/New_York")
    args = ap.parse_args()
    tz = ZoneInfo(args.tz)

    def parse(v):
        d = datetime.fromisoformat(v)
        return (d if d.tzinfo else d.replace(tzinfo=tz)).astimezone(timezone.utc)

    start = parse(args.t0) if args.t0 else datetime.now(timezone.utc)
    end = parse(args.t1) if args.t1 else start + timedelta(hours=args.hours)
    rows = upcoming(start, end, args.min_el, args.sats, args.two_way)
    if not rows:
        print("No passes.")
    for r, p, s, el, az_r, az_s, name, info in rows:
        rl, sl = r.astimezone(tz), s.astimezone(tz)
        mode = f"TX {info['up']:.3f} / RX {info['down']:.3f}" if info["two_way"] else f"listen {info['down']:.3f}"
        print(f"{rl:%a %m/%d %H:%M}-{sl:%H:%M} {name:10s} {el:3.0f}° {(s - r).total_seconds() / 60:4.1f} min "
              f"{az_r:3.0f}->{az_s:3.0f}  {mode}")


if __name__ == "__main__":
    main()
