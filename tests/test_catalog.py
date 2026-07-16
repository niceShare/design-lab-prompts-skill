from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "design-lab-prompts"
REFERENCES = SKILL / "references"
CATALOG_PATH = REFERENCES / "catalog.json"
CLI = SKILL / "scripts" / "query_prompts.py"


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    def test_snapshot_counts_are_exact(self) -> None:
        self.assertEqual(
            self.catalog["stats"],
            {
                "styles": 77,
                "styles_bilingual": 67,
                "styles_zh_only": 10,
                "prompts_zh": 174,
                "prompts_en": 144,
            },
        )
        self.assertEqual(self.catalog["source"]["inline_source_characters"], 294111)
        self.assertRegex(self.catalog["source"]["inline_source_sha256"], r"^[0-9a-f]{64}$")

    def test_style_ids_and_required_fields_are_complete(self) -> None:
        styles = self.catalog["styles"]
        self.assertEqual(len({style["id"] for style in styles}), 77)
        self.assertEqual([style["order"] for style in styles], list(range(1, 78)))
        for style in styles:
            self.assertTrue(style["description"]["zh"], style["id"])
            self.assertTrue(style["prompts"]["zh"], style["id"])
            self.assertTrue(style["colors"], style["id"])
            self.assertTrue(style["css"], style["id"])
            self.assertTrue(style["dos"]["zh"], style["id"])
            self.assertTrue(style["donts"]["zh"], style["id"])

    def test_translation_gap_is_explicit(self) -> None:
        zh_only = [style["id"] for style in self.catalog["styles"] if style["translation_status"] == "zh-only"]
        self.assertEqual(
            zh_only,
            ["cream", "grain", "editorialsaas", "ambient", "spec", "ascii", "victorian", "atomic", "zine", "halftone"],
        )
        for style in self.catalog["styles"]:
            if style["id"] in zh_only:
                self.assertEqual(style["prompts"]["en"], [])

    def test_recommender_matrix_is_complete(self) -> None:
        recommender = self.catalog["recommender"]
        self.assertEqual(len(recommender["categories"]), 12)
        self.assertEqual(len(recommender["levels"]), 4)
        known_ids = {style["id"] for style in self.catalog["styles"]}
        records = []
        for levels in recommender["recommendations"].values():
            self.assertEqual(set(levels), {"1", "2", "3", "4"})
            for items in levels.values():
                self.assertEqual(len(items), 3)
                records.extend(items)
        self.assertEqual(len(records), 144)
        self.assertTrue(all(record["style_id"] in known_ids for record in records))

    def test_every_prompt_is_present_in_generated_markdown(self) -> None:
        prompt_books = {
            "zh": (REFERENCES / "prompts-zh.md").read_text(encoding="utf-8"),
            "en": (REFERENCES / "prompts-en.md").read_text(encoding="utf-8"),
        }
        for style in self.catalog["styles"]:
            for language in ("zh", "en"):
                for prompt in style["prompts"][language]:
                    self.assertIn(prompt["text"], prompt_books[language], f"{style['id']} {language}")

    def test_manifest_hashes_match_files(self) -> None:
        manifest = json.loads((REFERENCES / "manifest.json").read_text(encoding="utf-8"))
        for name, metadata in manifest["files"].items():
            path = REFERENCES / name
            self.assertEqual(path.stat().st_size, metadata["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), metadata["sha256"])


class CliTests(unittest.TestCase):
    def run_cli(self, *args: str, expected_code: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=SKILL,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, expected_code, result.stderr or result.stdout)
        return result

    def test_stats_json(self) -> None:
        payload = json.loads(self.run_cli("stats", "--json").stdout)
        self.assertEqual(payload["styles"], 77)
        self.assertEqual(payload["prompt_entries_total"], 318)
        self.assertEqual(payload["recommendation_records"], 144)

    def test_show_resolves_localized_name(self) -> None:
        payload = json.loads(self.run_cli("show", "玻璃拟态", "--lang", "en", "--json").stdout)
        self.assertEqual(payload["id"], "glass")
        self.assertEqual(payload["resolved_language"], "en")
        self.assertFalse(payload["fallback_to_chinese"])

    def test_chinese_only_style_falls_back_visibly(self) -> None:
        result = self.run_cli("prompt", "cream", "--lang", "en", "--kind", "basic")
        self.assertIn("English source unavailable", result.stdout)
        self.assertIn("Cream SaaS 风格", result.stdout)

    def test_source_recommender_is_used(self) -> None:
        payload = json.loads(
            self.run_cli("recommend", "AI developer dashboard", "--lang", "en", "--level", "3", "--json").stdout
        )
        self.assertEqual(payload["detected_category"], "aitech")
        self.assertEqual([item["id"] for item in payload["results"]], ["terminal", "kinetic", "neo"])

    def test_search_finds_glassmorphism(self) -> None:
        payload = json.loads(self.run_cli("search", "frosted glass", "--lang", "en", "--json").stdout)
        self.assertGreater(len(payload), 0)
        self.assertEqual(payload[0]["id"], "glass")

    def test_trend_filter_has_expected_count(self) -> None:
        result = self.run_cli("list", "--filter", "trend")
        self.assertTrue(result.stdout.rstrip().endswith("38 style(s)"))

    def test_unknown_style_returns_actionable_error(self) -> None:
        result = self.run_cli("show", "glassmorph", expected_code=2)
        self.assertIn("Unknown style", result.stderr)
        self.assertIn("glass", result.stderr)


if __name__ == "__main__":
    unittest.main()
