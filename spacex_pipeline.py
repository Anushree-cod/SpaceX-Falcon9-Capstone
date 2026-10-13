"""Utilities for the SpaceX Falcon 9 capstone."""
from __future__ import annotations
import requests
import pandas as pd

BASE_URL = "https://api.spacexdata.com/v4"

def get_json(endpoint: str, timeout: int = 30):
    """Fetch one public SpaceX API endpoint and return parsed JSON."""
    response = requests.get(f"{BASE_URL}/{endpoint.lstrip('/')}", timeout=timeout)
    response.raise_for_status()
    return response.json()

def collect_launch_table() -> pd.DataFrame:
    """Retrieve launches and enrich with rocket, launchpad, payload, and core metadata."""
    launches = get_json("launches")
    rockets = {x["id"]: x for x in get_json("rockets")}
    pads = {x["id"]: x for x in get_json("launchpads")}
    payloads = {x["id"]: x for x in get_json("payloads")}
    cores = {x["id"]: x for x in get_json("cores")}

    rows = []
    for launch in launches:
        core_links = launch.get("cores") or []
        first_core = core_links[0] if core_links else {}
        core_id = first_core.get("core")
        core_obj = cores.get(core_id, {}) if core_id else {}
        rocket = rockets.get(launch.get("rocket"), {})
        pad = pads.get(launch.get("launchpad"), {})
        payload_ids = launch.get("payloads") or []
        payload_objs = [payloads[p] for p in payload_ids if p in payloads]
        rows.append({
            "flight_number": launch.get("flight_number"),
            "name": launch.get("name"),
            "date_utc": launch.get("date_utc"),
            "date_precision": launch.get("date_precision"),
            "success": launch.get("success"),
            "upcoming": launch.get("upcoming"),
            "rocket_name": rocket.get("name"),
            "rocket_type": rocket.get("type"),
            "launchpad_name": pad.get("name"),
            "launchpad_full_name": pad.get("full_name"),
            "launchpad_locality": pad.get("locality"),
            "launchpad_region": pad.get("region"),
            "latitude": pad.get("latitude"),
            "longitude": pad.get("longitude"),
            "payload_count": len(payload_objs),
            "payload_mass_kg": sum((p.get("mass_kg") or 0) for p in payload_objs),
            "orbit": "; ".join(sorted({p.get("orbit") or "Unknown" for p in payload_objs})),
            "customer": "; ".join(sorted({c for p in payload_objs for c in (p.get("customers") or [])})),
            "core_serial": core_obj.get("serial"),
            "core_reused": first_core.get("reused"),
            "landing_attempt": first_core.get("landing_attempt"),
            "landing_success": first_core.get("landing_success"),
            "landing_type": first_core.get("landing_type"),
            "landing_vehicle": first_core.get("landpad"),
            "reused": launch.get("cores", [{}])[0].get("reused") if launch.get("cores") else None,
            "details": launch.get("details"),
            "webcast": launch.get("links", {}).get("webcast"),
            "article": launch.get("links", {}).get("article"),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df["date_utc"] = pd.to_datetime(df["date_utc"], errors="coerce", utc=True)
        df["launch_year"] = df["date_utc"].dt.year
        df["launch_month"] = df["date_utc"].dt.month
    return df

def build_landing_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Keep rows with known landing outcomes and create a numeric target."""
    out = df.copy()
    out["landing_success"] = out["landing_success"].map({True: 1, False: 0})
    out = out[out["landing_success"].notna()].copy()
    out["landing_success"] = out["landing_success"].astype(int)
    out = out[out["upcoming"] != True]
    return out
