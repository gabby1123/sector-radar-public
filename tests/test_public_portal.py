"""Public portal regression tests: enforce the publication boundary without a network."""
import json
import tempfile
import unittest
from pathlib import Path

from public_data import (
    PUBLIC_JSON_FILES, _read_public_json, load_public_snapshots,
    public_company_labels, public_company_record, public_sector_rows,
    public_stock_rows,
)


class PublicPortalTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        for name in PUBLIC_JSON_FILES.values():
            (self.root / name).parent.mkdir(parents=True, exist_ok=True)
        self.fixture = {
            "latest": {
                "price_asof": "2026-10-08",
                "universe": [{"code": "2368", "name": "金像電", "sector": "PCB", "market": "TW"}],
                "stocks": [{"code": "2368", "name": "金像電", "sector": "PCB",
                            "close": 120, "r20": 10, "stage": "強勢",
                            "private_strategy": "DO-NOT-EXPOSE"}],
                "sectors": [{"sector": "PCB", "count": 1,
                             "mean_momentum_score": 60, "internal_signal": "SECRET"}],
            },
            "profiles": {"profiles": {"2368": {
                "name_official": "金像電子(股)公司", "source_url": "https://twse.example/",
                "secret_company_note": "PRIVATE-NOTE",
            }}},
            "revenue": {"stocks": {"2368": {
                "period": "2026-09", "revenue_yoy_pct": 35,
                "secret_revenue_note": "RESTRICTED",
            }}},
            "quarters": {"stocks": {"2368": {
                "quarters": [{"period": "2026Q2", "eps": 3.2, "gross_margin": 22,
                              "internal_target_price": 200}],
            }}},
        }
        for key, filename in PUBLIC_JSON_FILES.items():
            (self.root / filename).write_text(
                json.dumps(self.fixture[key], ensure_ascii=False), encoding="utf-8")
        (self.root / "data" / "research_notes.json").write_text(
            '{"secret":"INTERNAL MEMO"}', encoding="utf-8")

    def test_only_approved_data_files_are_loadable(self):
        with self.assertRaises(ValueError):
            _read_public_json(self.root, "../data/research_notes.json")
        with self.assertRaises(ValueError):
            _read_public_json(self.root, "research_notes")
        data = load_public_snapshots(self.root)
        self.assertEqual(set(data), set(PUBLIC_JSON_FILES))
        self.assertNotIn("INTERNAL MEMO", repr(data))

    def test_public_fields_never_include_source_private_fields(self):
        data = load_public_snapshots(self.root)
        stocks = public_stock_rows(data)
        sectors = public_sector_rows(data)
        company = public_company_record(data, "2368")
        for item in (stocks[0], sectors[0], company, company["quarters"][0]):
            text = repr(item)
            for secret in ("DO-NOT-EXPOSE", "SECRET", "PRIVATE-NOTE",
                           "RESTRICTED", "internal_target_price"):
                self.assertNotIn(secret, text)
        self.assertEqual(company["quarters"][0]["eps"], 3.2)
        self.assertEqual(company["revenue_yoy_pct"], 35)

    def test_public_navigation_has_nonpriced_research_codes(self):
        names = public_company_labels(load_public_snapshots(self.root))
        self.assertEqual(names["6456"], "GIS-KY")
        self.assertEqual(names["7873"], "瑞峰半導體")
        extra = public_company_record(load_public_snapshots(self.root), "7873")
        self.assertFalse(extra["quarters"])
        self.assertIsNone(extra["revenue_yoy_pct"])

    def test_public_entrypoint_does_not_import_private_app_or_memos(self):
        source = (Path(__file__).resolve().parents[1] / "public_app.py").read_text(encoding="utf-8")
        # This is a static warning test; publication safety also relies on the
        # allowlist and deploying this separate entrypoint, not private app.py.
        self.assertNotIn("from fundamental_dashboard import", source)
        self.assertNotIn("import company_research", source)
        self.assertNotIn("read_text(encoding=", source.replace('diagram.read_text(encoding=', ''))

    def test_missing_public_snapshot_is_handled(self):
        (self.root / PUBLIC_JSON_FILES["quarters"]).unlink()
        data = load_public_snapshots(self.root)
        self.assertEqual(data["quarters"], {})
        self.assertEqual(public_company_record(data, "2368")["quarters"], [])


if __name__ == "__main__":
    unittest.main()
