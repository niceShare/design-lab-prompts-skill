#!/usr/bin/env python3
"""Validate the normalized catalog and generate deterministic skill references."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


EXPECTED_STATS = {
    "styles": 77,
    "styles_bilingual": 67,
    "styles_zh_only": 10,
    "prompts_zh": 174,
    "prompts_en": 144,
}


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def validate(catalog: dict[str, Any]) -> None:
    if catalog.get("schema_version") != "1.0.0":
        fail("schema_version must be 1.0.0")
    if catalog.get("stats") != EXPECTED_STATS:
        fail(f"unexpected stats: {catalog.get('stats')!r}")

    styles = catalog.get("styles")
    if not isinstance(styles, list) or len(styles) != EXPECTED_STATS["styles"]:
        fail("styles array is missing or has the wrong length")
    ids = [style.get("id") for style in styles]
    if len(set(ids)) != len(ids):
        fail("style ids are not unique")

    zh_count = 0
    en_count = 0
    for expected_order, style in enumerate(styles, 1):
        if style.get("order") != expected_order:
            fail(f"style order mismatch at {style.get('id')}")
        for field in ("name", "description", "characteristics", "colors", "css", "hint", "prompts", "dos", "donts"):
            if field not in style:
                fail(f"{style['id']} is missing {field}")
        if not style["description"]["zh"] or not style["prompts"]["zh"] or not style["colors"]:
            fail(f"{style['id']} lacks required Chinese data")
        for language in ("zh", "en"):
            for prompt in style["prompts"][language]:
                if not prompt.get("title") or not prompt.get("text"):
                    fail(f"{style['id']} has an empty {language} prompt")
        zh_count += len(style["prompts"]["zh"])
        en_count += len(style["prompts"]["en"])

    if (zh_count, en_count) != (EXPECTED_STATS["prompts_zh"], EXPECTED_STATS["prompts_en"]):
        fail(f"prompt totals do not match: zh={zh_count}, en={en_count}")

    categories = catalog.get("recommender", {}).get("categories", [])
    recommendations = catalog.get("recommender", {}).get("recommendations", {})
    if len(categories) != 12 or set(recommendations) != {item["id"] for item in categories}:
        fail("recommender categories are incomplete")
    recommendation_count = 0
    for category, levels in recommendations.items():
        if set(levels) != {"1", "2", "3", "4"}:
            fail(f"{category} does not have four recommendation levels")
        for level, items in levels.items():
            if len(items) != 3:
                fail(f"{category}/{level} does not have three recommendations")
            for item in items:
                if item["style_id"] not in ids:
                    fail(f"recommendation references unknown style {item['style_id']}")
                recommendation_count += 1
    if recommendation_count != 144:
        fail(f"expected 144 recommendations, got {recommendation_count}")


def escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def generate_index(catalog: dict[str, Any]) -> str:
    difficulty = Counter(style["difficulty"] for style in catalog["styles"])
    filters = Counter(tag for style in catalog["styles"] for tag in style["filters"])
    lines = [
        "# Design Lab style index",
        "",
        f"Snapshot: `{catalog['source']['captured_at']}` · {catalog['stats']['styles']} styles · "
        f"{catalog['stats']['prompts_zh']} Chinese prompts · {catalog['stats']['prompts_en']} English prompts.",
        "",
        "## Distribution",
        "",
        "- Difficulty: " + ", ".join(f"{level}/5 = {difficulty[level]}" for level in sorted(difficulty)),
        "- Filters: " + ", ".join(f"{tag} = {filters[tag]}" for tag in sorted(filters)),
        "- Translation: 67 bilingual; 10 Chinese-only.",
        "",
        "## Styles",
        "",
        "| # | ID | English | 中文 | Difficulty | Filters | Prompts zh/en | Translation |",
        "|---:|---|---|---|---:|---|---:|---|",
    ]
    for style in catalog["styles"]:
        lines.append(
            f"| {style['order']} | `{style['id']}` | {escape_table(style['name']['en'])} | "
            f"{escape_table(style['name']['zh'])} | {style['difficulty']} | "
            f"{', '.join(style['filters'])} | {len(style['prompts']['zh'])}/{len(style['prompts']['en'])} | "
            f"{style['translation_status']} |"
        )
    return "\n".join(lines) + "\n"


def generate_prompt_book(catalog: dict[str, Any], language: str) -> str:
    language_name = "Chinese" if language == "zh" else "English"
    lines = [
        f"# Design Lab prompts — {language_name}",
        "",
        f"Source snapshot: <{catalog['source']['url']}> at `{catalog['source']['captured_at']}`.",
        "Prompt wording is preserved from the captured source.",
        "",
    ]
    missing = []
    for style in catalog["styles"]:
        prompts = style["prompts"][language]
        if not prompts:
            missing.append(style)
            continue
        lines.extend([
            f"## {style['order']:02d}. {style['name'][language]} (`{style['id']}`)",
            "",
            f"> {style['hint'][language]}",
            "",
        ])
        for prompt in prompts:
            lines.extend([f"### {prompt['title']}", "", prompt["text"], ""])
    if missing:
        lines.extend([
            "## Styles without English source prompts",
            "",
            "The captured source exposes these styles in Chinese only; no translation was invented:",
            "",
        ])
        lines.extend(f"- `{style['id']}` — {style['name']['en']} / {style['name']['zh']}" for style in missing)
        lines.append("")
    return "\n".join(lines)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 3:
        fail("usage: build_reference_files.py <catalog.json> <skill-directory>")
    source_path = Path(sys.argv[1]).resolve()
    skill_dir = Path(sys.argv[2]).resolve()
    references = skill_dir / "references"
    repository_root = skill_dir.parents[1]
    version_path = repository_root / "VERSION"
    source_notes = references / "source-notes.md"
    if not version_path.exists():
        fail(f"repository version file is missing: {version_path}")
    if not source_notes.exists():
        fail(f"source notes must exist before generation: {source_notes}")

    catalog = json.loads(source_path.read_text(encoding="utf-8"))
    validate(catalog)
    write_text(references / "catalog.json", json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    write_text(references / "style-index.md", generate_index(catalog))
    write_text(references / "prompts-zh.md", generate_prompt_book(catalog, "zh"))
    write_text(references / "prompts-en.md", generate_prompt_book(catalog, "en"))

    tracked = ["catalog.json", "style-index.md", "prompts-zh.md", "prompts-en.md", "source-notes.md"]
    manifest = {
        "version": version_path.read_text(encoding="utf-8").strip(),
        "schema_version": catalog["schema_version"],
        "source": catalog["source"],
        "stats": catalog["stats"],
        "recommendation_records": 144,
        "files": {name: {"sha256": sha256(references / name), "bytes": (references / name).stat().st_size}
                  for name in tracked},
    }
    write_text(references / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({**catalog["stats"], "recommendation_records": 144}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
