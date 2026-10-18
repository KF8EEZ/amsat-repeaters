"""Pass prediction helpers: TLE cache, pass finder, Doppler.

find_passes and doppler_khz are copied from the sstv-iss repo (cue_sheets.py,
iss_passes.py) so this repo stands alone.
"""
import urllib.request
from datetime import timedelta
from pathlib import Path

import numpy as np
from skyfield.api import EarthSatellite

ROOT = Path(__file__).resolve().parent
TLE_DIR = ROOT / "data" / "tle"
TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?CATNR={}&FORMAT=tle"
C_KM_S = 299792.458


def refresh_tle(norad):
    """Fetch the TLE from Celestrak into data/tle/<norad>.tle; fall back to the cache."""
    TLE_DIR.mkdir(parents=True, exist_ok=True)
    path = TLE_DIR / f"{norad}.tle"
    try:
        with urllib.request.urlopen(TLE_URL.format(norad), timeout=15) as r:
            text = r.read().decode()
        if "\n1 " in "\n" + text:
            path.write_text(text)
    except Exception:
        if not path.exists():
            raise
    return path


def load_sat(norad, ts):
    lines = [ln.strip() for ln in refresh_tle(norad).read_text().splitlines() if ln.strip()]
    l1 = next(ln for ln in lines if ln.startswith("1 "))
    l2 = next(ln for ln in lines if ln.startswith("2 "))
    return EarthSatellite(l1, l2, str(norad), ts)


def doppler_khz(sat, site, t, freq_mhz):
    """Doppler shift in kHz (positive = received frequency is above nominal)."""
    topo = (sat - site).at(t)
    pos = topo.position.km
    vel = topo.velocity.km_per_s
    range_rate = np.sum(pos * vel, axis=0) / np.sqrt(np.sum(pos**2, axis=0))
    return -freq_mhz * 1e3 * range_rate / C_KM_S


def find_passes(sat, site, ts, start, days, min_el, end_time=None):
    """Yield (rise, peak, setting, max_el_deg, az_rise_deg, az_set_deg).

    Passes are bounded by the 10 degree horizon search; min_el filters on the peak.
    end_time: optional tz-aware datetime; passes rising at or after it are skipped.
    """
    end = start + timedelta(days=days)
    t0, t1 = ts.from_datetime(start), ts.from_datetime(end)
    times, events = sat.find_events(site, t0, t1, altitude_degrees=10.0)
    cur = {}
    for t, e in zip(times, events):
        cur[e] = t
        if e != 2 or not {0, 1}.issubset(cur):
            continue
        rise, peak, setting = cur[0], cur[1], cur[2]
        cur = {}
        if end_time is not None and rise.utc_datetime() >= end_time:
            continue
        alt, _, _ = (sat - site).at(peak).altaz()
        if alt.degrees < min_el:
            continue
        _, az_r, _ = (sat - site).at(rise).altaz()
        _, az_s, _ = (sat - site).at(setting).altaz()
        yield rise, peak, setting, alt.degrees, az_r.degrees, az_s.degrees
