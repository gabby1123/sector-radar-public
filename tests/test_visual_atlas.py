"""Validate offline schematic files and attribution for educational photographs."""
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from sector_catalog import SECTORS
from visual_atlas import ROOT, VISUAL_ATLAS, local_diagram_for


class VisualAtlasTests(unittest.TestCase):
    def test_diagrams_are_svg_and_parseable(self):
        for sector in ("pcb", "server", "packaging", "equipment", "optical"):
            with self.subTest(sector=sector):
                path = local_diagram_for(sector)
                self.assertIsNotNone(path)
                self.assertEqual(path.suffix, ".svg")
                root = ET.parse(path).getroot()
                self.assertTrue(root.tag.endswith("svg"))
                self.assertIn("viewBox", root.attrib)
                self.assertIn("NOT TO SCALE", path.read_text(encoding="utf-8"))
                self.assertIn("Designed by C", path.read_text(encoding="utf-8"))

    def test_every_photo_has_attribution_and_license(self):
        valid_ids = {s["id"] for s in SECTORS}
        self.assertTrue(set(VISUAL_ATLAS).issubset(valid_ids))
        photo_entries = {key: image for key, image in VISUAL_ATLAS.items() if image.get("photo_url")}
        self.assertEqual(set(photo_entries), {"pcb", "packaging", "optical"})
        for key, image in photo_entries.items():
            with self.subTest(sector=key):
                self.assertTrue(image["photo_url"].startswith("https://upload.wikimedia.org/"))
                self.assertTrue(image["photo_source"].startswith("https://commons.wikimedia.org/wiki/File:"))
                self.assertIn("creativecommons.org", image["photo_license_url"])
                self.assertTrue(image["photo_author"])
                self.assertTrue(image["photo_context"])
                self.assertTrue(image["investment_signals"])
                for title, question in image["investment_signals"]:
                    self.assertTrue(title and question)

    def test_photos_not_mislabeled_as_advanced_products(self):
        self.assertIn("並非 AI 伺服器", VISUAL_ATLAS["pcb"]["photo_context"])
        self.assertIn("不是已完成", VISUAL_ATLAS["packaging"]["photo_context"])
        self.assertIn("不是 CPO", VISUAL_ATLAS["optical"]["photo_context"])
        self.assertIsNone(local_diagram_for("nonexistent"))

    def test_diagrams_live_inside_repository(self):
        for entry in VISUAL_ATLAS.values():
            path = ROOT / entry["diagram"]
            self.assertEqual(path.resolve().parent, (ROOT / "assets" / "diagrams").resolve())


if __name__ == "__main__":
    unittest.main()
