"""Strictly allowlisted public-data adapter for Sector Radar.

Never import/read raw research_notes, deep_dive_notes, explorer_company_notes,
forum memos, secrets, or internal workspaces here. Only pre-reviewed
projections in data/public_memos.json are eligible for public display. All fields exposed to the
public entrypoint are individually selected, never passed through wholesale.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC_JSON_FILES = {
    "latest": "data/latest.json",  # Public-market-derived price snapshot
    "profiles": "data/company_profiles.json",  # TWSE / TPEx issuer disclosures
    "revenue": "data/company_revenue.json",  # MOPS monthly disclosures
    "quarters": "data/quarterly_financials.json",  # Reported FinMind quarterly history
    "memos": "data/public_memos.json",  # Independently exported, field-projected public summaries
}
EXTRA_RESEARCH_CODES = {"6456": "GIS-KY", "7873": "瑞峰半導體"}


def _read_public_json(root, key):
    """Only preapproved locations can be opened, even if callers pass bad keys."""
    if key not in PUBLIC_JSON_FILES:
        raise ValueError("This data source is not approved for the public app")
    path = Path(root) / PUBLIC_JSON_FILES[key]
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError, TypeError):
        return {}


def load_public_snapshots(root=ROOT):
    """Read only public-market data; no proprietary analyst notes or memos."""
    return {key: _read_public_json(root, key) for key in PUBLIC_JSON_FILES}


def _number(value):
    try:
        parsed = float(value)
        return parsed if math.isfinite(parsed) else None
    except (ValueError, TypeError):
        return None


def _records(value):
    return value if isinstance(value, list) else []


def public_company_labels(snapshots):
    """Company code -> name, using the public universe and two research-only names."""
    names = {}
    for row in _records(snapshots.get("latest", {}).get("universe")):
        if not isinstance(row, dict):
            continue
        code, name = str(row.get("code") or "").strip(), str(row.get("name") or "").strip()
        if code.isdigit() and name:
            names[code] = name
    for code, name in EXTRA_RESEARCH_CODES.items():
        names.setdefault(code, name)
    return names


def public_sector_rows(snapshots):
    """Expose only price-derived public sector aggregates."""
    fields = ("sector", "count", "median_r20", "mean_discovery_score",
              "mean_momentum_score", "flow_coverage")
    rows = []
    for value in _records(snapshots.get("latest", {}).get("sectors")):
        if isinstance(value, dict) and value.get("sector"):
            rows.append({key: value.get(key) for key in fields})
    return rows


def public_stock_rows(snapshots):
    """Expose a small explicit projection, never raw repository records."""
    fields = ("code", "name", "sector", "close", "price_date", "r5", "r20",
              "rs20", "discovery_score", "momentum_score", "stage")
    rows = []
    for value in _records(snapshots.get("latest", {}).get("stocks")):
        if isinstance(value, dict) and str(value.get("code", "")).isdigit():
            rows.append({key: value.get(key) for key in fields})
    return rows


def _lookup(mapping, code):
    return mapping.get(str(code), {}) if isinstance(mapping, dict) else {}


def public_company_record(snapshots, code):
    """Whitelist issuer facts, monthly revenue and published quarter metrics."""
    code = str(code)
    names = public_company_labels(snapshots)
    universe = _records(snapshots.get("latest", {}).get("universe"))
    basic = next((r for r in universe if isinstance(r, dict)
                  and str(r.get("code")) == code), {})
    p = _lookup(snapshots.get("profiles", {}).get("profiles"), code)
    r = _lookup(snapshots.get("revenue", {}).get("stocks"), code)
    q = _lookup(snapshots.get("quarters", {}).get("stocks"), code)
    allowed_quarters = []
    for raw in _records(q.get("quarters")):
        if not isinstance(raw, dict) or not raw.get("period"):
            continue
        allowed_quarters.append({
            "period": str(raw["period"]),
            "eps": _number(raw.get("eps")),
            "gross_margin": _number(raw.get("gross_margin")),
            "operating_margin": _number(raw.get("operating_margin")),
            "revenue_yoy_pct": _number(raw.get("revenue_yoy_pct")),
            "gross_margin_yoy_pp": _number(raw.get("gross_margin_yoy_pp")),
            "eps_yoy_delta": _number(raw.get("eps_yoy_delta")),
        })
    return {
        "code": code,
        "name": names.get(code, "未知公司"),
        "sector": str(basic.get("sector") or "未納入行情觀察"),
        "market": str(basic.get("market") or "—"),
        "official_name": p.get("name_official"),
        "official_source": p.get("source_url"),
        "official_updated": p.get("last_success_at"),
        "listing_date": p.get("listing_date"),
        "shares_outstanding": _number(p.get("issued_common_shares_raw")),
        "revenue_period": r.get("period"),
        "revenue_mom_pct": _number(r.get("revenue_mom_pct")),
        "revenue_yoy_pct": _number(r.get("revenue_yoy_pct")),
        "revenue_ytd_yoy_pct": _number(r.get("ytd_yoy_pct")),
        "revenue_source": r.get("source_url"),
        "revenue_updated": r.get("last_success_at"),
        "quarter_updated": q.get("last_success_at"),
        "quarters": sorted(allowed_quarters, key=lambda item: item["period"])[-8:],
    }


def public_memo_records(snapshots):
    """Published research abstracts only; never disclose raw private records."""
    raw = snapshots.get("memos", {})
    source = raw.get("companies", {}) if isinstance(raw, dict) else {}
    if not isinstance(source, dict):
        return {}
    allowed = public_company_labels(snapshots)
    text_fields = ("business", "thesis", "catalyst", "risk", "confidence")
    deep_fields = ("research_position", "earnings_engine", "key_metric_focus",
                   "potential_bottleneck", "bear_case", "source_qualification",
                   "prepared_on")
    result = {}
    for code, item in source.items():
        if code not in allowed or not isinstance(item, dict):
            continue
        manual = item.get("manual")
        deep = item.get("deep")
        if not isinstance(manual, dict) and not isinstance(deep, dict):
            continue
        m = ({**{field: str(manual.get(field) or "") for field in text_fields},
              "questions": [str(v) for v in manual.get("questions", []) if isinstance(v, str)][:8]}
             if isinstance(manual, dict) else None)
        d = None
        if isinstance(deep, dict):
            scenario = deep.get("scenario_2027") or {}
            d = {
                **{field: str(deep.get(field) or "") for field in deep_fields},
                "verification": [str(v) for v in deep.get("verification", [])
                                 if isinstance(v, str)][:8],
                "scenario_2027": {
                    "framework": str(scenario.get("framework") or ""),
                    "sensitivity": str(scenario.get("sensitivity") or ""),
                    "missing_inputs": [str(v) for v in scenario.get("missing_inputs", [])
                                       if isinstance(v, str)][:8],
                },
            }
        result[code] = {"code": code, "name": allowed[code], "manual": m, "deep": d}
    return result
