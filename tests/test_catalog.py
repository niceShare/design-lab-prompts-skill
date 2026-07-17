from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "design-lab-prompts"
REFERENCES = SKILL / "references"
CATALOG_PATH = REFERENCES / "catalog.json"
CLI = SKILL / "scripts" / "query_prompts.py"
EXTRACTOR = ROOT / "tools" / "extract_site_data.mjs"
GENERATOR = ROOT / "tools" / "build_reference_files.py"


def load_generator_module():
    spec = importlib.util.spec_from_file_location("build_reference_files", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load generator: {GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def style_array_fixture(description: str = '"安全说明"') -> str:
    return f"""[
      {{
        id: "safe", cn: "安全风格", name: "Safe Style", diff: 1, f: ["easy"],
        desc: {description}, chars: ["清晰"], colors: ["#ffffff"], cnames: ["白色"],
        css: "color: #111;", hint: "保持清晰", prompts: [{{t: "基础", x: "安全 prompt"}}],
        dos: ["保持清晰"], donts: ["不要混乱"],
      }},
    ]"""


def extractor_fixture(
    style_expression: str | None = None,
    description: str = '"安全说明"',
    styles_en: str | None = None,
) -> str:
    source_style = style_expression or style_array_fixture(description)
    english_styles = styles_en or (
        '{safe: {desc: "Safe description", chars: ["Clear"], '
        'dos: ["Stay clear"], donts: ["Avoid clutter"]}}'
    )
    return f"""
      const S = {source_style};
      const S_EN = {english_styles};
      const P={{safe: {{cnames: ["White"], hint: "Stay clear", prompts: [{{t: "Basic", x: "Safe prompt"}}]}}}};
      const RECO_CATS = [{{id: "saas", icon: "S", zh: "工具", en: "Tools"}}];
      const RECO_LEVELS = [{{id: 1, label: "标准", desc: "安全"}}];
      const RECO_MAP = {{saas: {{1: [["safe", "安全理由", "Safe reason", ["safe"]]]}}}};
      /* {"padding" * 180} */
    """


class ExtractorTests(unittest.TestCase):
    def run_extractor(
        self,
        source: str | list[dict[str, str]],
        captured_at: str = "2025-01-02T03:04:05Z",
    ) -> tuple[subprocess.CompletedProcess[str], dict]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            is_json = isinstance(source, list)
            source_path = Path(temporary_directory) / ("inline.json" if is_json else "inline.js")
            output_path = Path(temporary_directory) / "catalog.json"
            source_text = json.dumps(source, ensure_ascii=False) if is_json else source
            source_path.write_text(source_text, encoding="utf-8")
            result = subprocess.run(
                [
                    "node",
                    str(EXTRACTOR),
                    str(source_path),
                    str(output_path),
                    "--captured-at",
                    captured_at,
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            payload = json.loads(output_path.read_text(encoding="utf-8")) if output_path.exists() else {}
            return result, payload

    def test_plain_data_literals_are_extracted(self) -> None:
        result, payload = self.run_extractor(extractor_fixture())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload["stats"]["styles"], 1)
        self.assertEqual(payload["styles"][0]["id"], "safe")

    def test_executable_style_expression_is_rejected(self) -> None:
        result, _ = self.run_extractor(extractor_fixture(f"(() => {style_array_fixture()})()"))
        self.assertNotEqual(result.returncode, 0)

    def test_template_interpolation_is_rejected(self) -> None:
        result, _ = self.run_extractor(extractor_fixture(description="`unsafe ${1 + 1}`"))
        self.assertNotEqual(result.returncode, 0)

    def test_capture_time_is_supplied_by_the_caller(self) -> None:
        captured_at = "2025-01-02T03:04:05Z"
        result, payload = self.run_extractor(extractor_fixture(), captured_at=captured_at)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload["source"]["captured_at"], captured_at)

    def test_json_input_selects_the_script_with_catalog_markers(self) -> None:
        scripts = [
            {"text": extractor_fixture()},
            {"text": "/* unrelated but longer */" + "x" * 5_000},
        ]
        result, payload = self.run_extractor(scripts)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload["styles"][0]["id"], "safe")

    def test_markers_inside_comments_are_ignored(self) -> None:
        decoy = style_array_fixture().replace('id: "safe"', 'id: "decoy"', 1)
        source = f"/* const S = {decoy} */\n{extractor_fixture()}"
        result, payload = self.run_extractor(source)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload["styles"][0]["id"], "safe")

    def test_orphan_english_metadata_is_rejected(self) -> None:
        styles_en = """{
          safe: {desc: "Safe", chars: ["Clear"], dos: ["Do"], donts: ["Don't"]},
          orphan: {desc: "Orphan", chars: ["Unknown"], dos: ["Do"], donts: ["Don't"]},
        }"""
        result, _ = self.run_extractor(extractor_fixture(styles_en=styles_en))
        self.assertNotEqual(result.returncode, 0)


class GeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator_module()
        cls.catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    def updated_catalog(self) -> dict:
        catalog = copy.deepcopy(self.catalog)
        added_style = copy.deepcopy(catalog["styles"][-1])
        added_style["order"] = len(catalog["styles"]) + 1
        added_style["id"] = "future-style"
        added_style["name"] = {"zh": "未来风格", "en": "Future Style"}
        catalog["styles"].append(added_style)
        catalog["stats"]["styles"] += 1
        catalog["stats"]["styles_zh_only"] += 1
        catalog["stats"]["prompts_zh"] += len(added_style["prompts"]["zh"])
        return catalog

    def test_updated_snapshot_is_validated_by_its_own_contents(self) -> None:
        self.generator.validate(self.updated_catalog())

    def test_style_index_uses_snapshot_translation_counts(self) -> None:
        index = self.generator.generate_index(self.updated_catalog())
        self.assertIn("67 bilingual; 11 Chinese-only", index)

    def test_recommendation_count_is_computed_from_records(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["recommender"]["recommendations"]["saas"]["1"].pop()
        self.assertEqual(self.generator.recommendation_count(catalog), 143)

    def test_missing_source_provenance_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        del catalog["source"]["inline_source_sha256"]
        with self.assertRaises(SystemExit):
            self.generator.validate(catalog)

    def test_malformed_palette_entry_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["styles"][0]["colors"][0]["hex"] = ""
        with self.assertRaises(SystemExit):
            self.generator.validate(catalog)


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


class DocumentationTests(unittest.TestCase):
    def test_public_readme_has_open_source_onboarding_and_prominent_notice(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("https://design-lab-yanliu.vercel.app/", readme)
        self.assertIn("unofficial, independent open-source learning project", readme)
        self.assertIn("solely for study, research, design analysis, and non-commercial exchange", readme)
        self.assertIn("README.zh-CN.md", readme)
        self.assertIn("Quick start", readme)
        self.assertIn("CONTRIBUTING.md", readme)
        self.assertIn("SECURITY.md", readme)
        self.assertIn("AUDIT.md", readme)
        self.assertIn("ATTRIBUTION.md", readme)
        self.assertIn("NOTICE.md", readme)

    def test_open_source_community_documents_are_present(self) -> None:
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("Pull request checklist", contributing)
        self.assertIn("Updating the source snapshot", contributing)
        self.assertIn("Report a vulnerability", security)
        self.assertIn("security/advisories/new", security)

    def test_attribution_is_bilingual_and_explicit(self) -> None:
        attribution = (ROOT / "ATTRIBUTION.md").read_text(encoding="utf-8")
        self.assertIn("参考来源", attribution)
        self.assertIn("Reference source", attribution)
        self.assertIn("Curated by Dreameryanyan", attribution)
        self.assertIn("仅供学习、研究、设计分析和非商业交流使用", attribution)
        self.assertIn("solely for study, research, design analysis, and non-commercial exchange", attribution)

    def test_notice_separates_code_license_from_upstream_content(self) -> None:
        notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
        self.assertIn("MIT License 仅适用于本仓库原创的软件代码和原创项目文档", notice)
        self.assertIn("不包含在 MIT 授权中", notice)
        self.assertIn("No affiliation, partnership, sponsorship, endorsement", notice)
        self.assertIn("does not cover upstream prompt text", notice)

    def test_skill_preserves_source_credit_for_shared_outputs(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("https://design-lab-yanliu.vercel.app/", skill)
        self.assertIn("Curated by Dreameryanyan", skill)
        self.assertIn("Treat copied Design Lab prompts and metadata as upstream reference content", skill)

    def test_skill_keeps_provenance_notices_out_of_generated_ui(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Keep attribution in repository documentation or external delivery notes", skill)
        self.assertIn("Never add source credit, attribution copy, unofficial-project disclaimers, or prompt labels", skill)
        self.assertNotIn("Original Design Lab prompt", skill)
        self.assertNotIn("For public or shared outputs, state that the design direction references Design Lab", skill)


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

    def test_short_ai_alias_does_not_match_inside_retail(self) -> None:
        payload = json.loads(
            self.run_cli("recommend", "retail landing page", "--lang", "en", "--json").stdout
        )
        self.assertEqual(payload["detected_category"], "ecom")

    def test_search_fallback_reason_uses_requested_language(self) -> None:
        payload = json.loads(
            self.run_cli("recommend", "glassmorphism", "--lang", "zh", "--json").stdout
        )
        self.assertIsNone(payload["detected_category"])
        self.assertGreater(len(payload["results"]), 0)
        self.assertEqual(payload["results"][0]["reason"], "匹配到目录字段")

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
