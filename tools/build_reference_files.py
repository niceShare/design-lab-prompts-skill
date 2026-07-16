#!/usr/bin/env python3
"""Validate the normalized catalog and generate deterministic skill references."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def calculate_stats(styles: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "styles": len(styles),
        "styles_bilingual": sum(style["translation_status"] == "complete" for style in styles),
        "styles_zh_only": sum(style["translation_status"] == "zh-only" for style in styles),
        "prompts_zh": sum(len(style["prompts"]["zh"]) for style in styles),
        "prompts_en": sum(len(style["prompts"]["en"]) for style in styles),
    }


def recommendation_count(catalog: dict[str, Any]) -> int:
    return sum(
        len(items)
        for levels in catalog["recommender"]["recommendations"].values()
        for items in levels.values()
    )


def validate(catalog: dict[str, Any]) -> None:
    if catalog.get("schema_version") != "1.0.0":
        fail("schema_version must be 1.0.0")

    source = catalog.get("source")
    if not isinstance(source, dict):
        fail("source must be an object")
    required_source_strings = (
        "url", "title", "curator", "captured_at", "extraction", "inline_source_sha256",
    )
    if any(not isinstance(source.get(field), str) or not source[field] for field in required_source_strings):
        fail("source provenance fields must be non-empty strings")
    if not source["url"].startswith("https://"):
        fail("source url must use HTTPS")
    try:
        datetime.fromisoformat(source["captured_at"].replace("Z", "+00:00"))
    except ValueError:
        fail("source captured_at must be an ISO 8601 date-time")
    source_hash = source["inline_source_sha256"]
    if len(source_hash) != 64 or any(character not in "0123456789abcdef" for character in source_hash):
        fail("source inline_source_sha256 must be a lowercase SHA-256 digest")
    if not isinstance(source.get("inline_source_characters"), int) or source["inline_source_characters"] < 1:
        fail("source inline_source_characters must be a positive integer")

    styles = catalog.get("styles")
    if not isinstance(styles, list) or not styles:
        fail("styles must be a non-empty array")
    if any(not isinstance(style, dict) for style in styles):
        fail("every style must be an object")
    ids = [style.get("id") for style in styles]
    if any(not isinstance(style_id, str) or not style_id for style_id in ids):
        fail("every style must have a non-empty string id")
    if len(set(ids)) != len(ids):
        fail("style ids must be unique")

    for expected_order, style in enumerate(styles, 1):
        if style.get("order") != expected_order:
            fail(f"style order mismatch at {style.get('id')}")
        for field in (
            "name", "difficulty", "filters", "description", "characteristics", "colors", "css", "hint",
            "prompts", "dos", "donts", "translation_status",
        ):
            if field not in style:
                fail(f"{style['id']} is missing {field}")
        for field in ("name", "description", "characteristics", "hint", "prompts", "dos", "donts"):
            if not isinstance(style[field], dict):
                fail(f"{style['id']} has an invalid {field} object")
        if (
            not style["name"].get("zh")
            or not style["name"].get("en")
            or not style["description"].get("zh")
            or not style["characteristics"].get("zh")
            or not style["hint"].get("zh")
            or not style["prompts"].get("zh")
            or not style["dos"].get("zh")
            or not style["donts"].get("zh")
            or not style["colors"]
            or not isinstance(style["css"], str)
            or not style["css"]
        ):
            fail(f"{style['id']} lacks required Chinese data")
        if not isinstance(style["difficulty"], int) or not 1 <= style["difficulty"] <= 5:
            fail(f"{style['id']} difficulty must be an integer from 1 to 5")
        if not isinstance(style["filters"], list) or not all(
            isinstance(value, str) and value for value in style["filters"]
        ):
            fail(f"{style['id']} filters must be non-empty strings")
        if not isinstance(style["colors"], list):
            fail(f"{style['id']} colors must be an array")
        for color in style["colors"]:
            if (
                not isinstance(color, dict)
                or not isinstance(color.get("hex"), str)
                or not color["hex"]
                or not isinstance(color.get("name"), dict)
                or not color["name"].get("zh")
            ):
                fail(f"{style['id']} has a malformed palette entry")
        for language in ("zh", "en"):
            if not isinstance(style["prompts"].get(language), list):
                fail(f"{style['id']} has an invalid {language} prompt list")
            for prompt in style["prompts"].get(language, []):
                if not prompt.get("title") or not prompt.get("text"):
                    fail(f"{style['id']} has an empty {language} prompt")
        expected_status = "complete" if style["prompts"]["en"] else "zh-only"
        if style.get("translation_status") != expected_status:
            fail(f"{style['id']} has inconsistent translation_status")
        if expected_status == "complete":
            for field in ("description", "characteristics", "hint", "dos", "donts"):
                if not style[field].get("en"):
                    fail(f"{style['id']} is marked complete but lacks English {field}")

    computed_stats = calculate_stats(styles)
    if catalog.get("stats") != computed_stats:
        fail(f"catalog stats do not match contents: expected {computed_stats!r}, got {catalog.get('stats')!r}")

    recommender = catalog.get("recommender")
    if not isinstance(recommender, dict):
        fail("recommender must be an object")
    categories = recommender.get("categories")
    levels_metadata = recommender.get("levels")
    recommendations = recommender.get("recommendations")
    if not isinstance(categories, list) or not categories:
        fail("recommender categories must be a non-empty array")
    if not isinstance(levels_metadata, list) or not levels_metadata:
        fail("recommender levels must be a non-empty array")
    if not isinstance(recommendations, dict):
        fail("recommender recommendations must be an object")

    if any(not isinstance(item, dict) for item in categories):
        fail("every recommender category must be an object")
    category_ids = [item.get("id") for item in categories]
    if any(not category_id for category_id in category_ids) or len(set(category_ids)) != len(category_ids):
        fail("recommender category ids must be non-empty and unique")
    if set(recommendations) != set(category_ids):
        fail("recommender category metadata and recommendation keys do not match")

    if any(not isinstance(item, dict) for item in levels_metadata):
        fail("every recommender level must be an object")
    raw_level_ids = [item.get("id") for item in levels_metadata]
    if any(level_id is None for level_id in raw_level_ids):
        fail("recommender level ids must be present")
    level_ids = [str(level_id) for level_id in raw_level_ids]
    if len(set(level_ids)) != len(level_ids):
        fail("recommender level ids must be unique")

    known_ids = set(ids)
    for category, levels in recommendations.items():
        if not isinstance(levels, dict) or set(levels) != set(level_ids):
            fail(f"{category} recommendation levels do not match level metadata")
        for level, items in levels.items():
            if not isinstance(items, list) or not items:
                fail(f"{category}/{level} must have at least one recommendation")
            if any(not isinstance(item, dict) for item in items):
                fail(f"{category}/{level} recommendation entries must be objects")
            recommended_ids = [item.get("style_id") for item in items]
            if len(set(recommended_ids)) != len(recommended_ids):
                fail(f"{category}/{level} contains duplicate styles")
            for item in items:
                style_id = item.get("style_id")
                if style_id not in known_ids:
                    fail(f"recommendation references unknown style {style_id!r}")
                reason = item.get("reason")
                if not isinstance(reason, dict) or not reason.get("zh") or not reason.get("en"):
                    fail(f"{category}/{level}/{style_id} lacks a bilingual reason")
                if not isinstance(item.get("badges"), list):
                    fail(f"{category}/{level}/{style_id} badges must be an array")


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
        f"- Translation: {catalog['stats']['styles_bilingual']} bilingual; "
        f"{catalog['stats']['styles_zh_only']} Chinese-only.",
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
        "recommendation_records": recommendation_count(catalog),
        "files": {name: {"sha256": sha256(references / name), "bytes": (references / name).stat().st_size}
                  for name in tracked},
    }
    write_text(references / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(
        {**catalog["stats"], "recommendation_records": recommendation_count(catalog)},
        ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
