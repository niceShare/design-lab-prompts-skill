#!/usr/bin/env python3
"""Query the offline Design Lab prompt catalog using only Python's standard library."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any


DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "references" / "catalog.json"

CATEGORY_ALIASES = {
    "saas": ["saas", "tool", "tools", "dashboard", "b2b", "工具", "仪表盘"],
    "portfolio": ["portfolio", "resume", "designer", "作品集", "简历", "设计师"],
    "ecom": ["ecommerce", "e-commerce", "shop", "store", "retail", "电商", "商城", "商店"],
    "blog": ["blog", "content", "media", "publication", "博客", "内容", "媒体"],
    "game": ["game", "gaming", "entertainment", "游戏", "娱乐"],
    "wellness": ["wellness", "health", "fitness", "meditation", "健康", "养生", "健身", "冥想"],
    "fintech": ["fintech", "finance", "bank", "trading", "金融", "银行", "交易"],
    "edu": ["education", "learning", "school", "course", "教育", "学习", "课程"],
    "food": ["food", "restaurant", "dining", "cafe", "餐饮", "美食", "餐厅", "咖啡"],
    "fashion": ["fashion", "streetwear", "beauty", "时尚", "潮牌", "美妆"],
    "aitech": ["ai", "tech", "developer", "api", "artificial intelligence", "科技", "开发者", "人工智能"],
    "culture": ["culture", "art", "museum", "gallery", "文化", "艺术", "博物馆", "画廊"],
}


class CatalogError(RuntimeError):
    """Raised for catalog loading or lookup failures."""


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold().strip()
    return re.sub(r"[\s_/]+", " ", value)


def contains_term(haystack: str, term: str) -> bool:
    """Match Latin aliases as tokens and CJK aliases as substrings."""
    needle = normalize(term)
    if re.fullmatch(r"[a-z0-9-]+(?: [a-z0-9-]+)*", needle):
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])", haystack))
    return needle in haystack


def load_catalog(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CatalogError(f"Catalog not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CatalogError(f"Catalog is not valid JSON: {path}: {exc}") from exc
    if data.get("schema_version") != "1.0.0" or not isinstance(data.get("styles"), list):
        raise CatalogError(f"Unsupported or malformed catalog: {path}")
    return data


def aliases(style: dict[str, Any]) -> list[str]:
    return [style["id"], style["name"]["en"], style["name"]["zh"]]


def resolve_style(styles: list[dict[str, Any]], query: str) -> dict[str, Any]:
    wanted = normalize(query)
    for style in styles:
        if wanted in {normalize(alias) for alias in aliases(style)}:
            return style

    choices = {normalize(alias): f"{style['id']} ({style['name']['en']} / {style['name']['zh']})"
               for style in styles for alias in aliases(style)}
    matches = difflib.get_close_matches(wanted, list(choices), n=5, cutoff=0.45)
    suffix = f" Closest: {', '.join(choices[item] for item in matches)}." if matches else ""
    raise CatalogError(f"Unknown style: {query}.{suffix}")


def language_payload(style: dict[str, Any], language: str) -> tuple[str, bool]:
    if language == "en" and not style["prompts"]["en"]:
        return "zh", True
    return language, False


def localized(style: dict[str, Any], field: str, language: str) -> Any:
    payload = style[field]
    if isinstance(payload, dict):
        value = payload.get(language)
        if value in (None, [], ""):
            return payload.get("zh")
        return value
    return payload


def prompt_kind(title: str) -> str:
    normalized = normalize(title)
    if "keyword" in normalized or "关键词" in normalized:
        return "keywords"
    if "advanced" in normalized or "进阶" in normalized:
        return "advanced"
    return "basic"


def style_search_text(style: dict[str, Any], languages: list[str]) -> dict[int, str]:
    weighted: dict[int, list[str]] = {6: aliases(style), 5: [], 4: style["filters"], 3: [], 2: []}
    for language in languages:
        weighted[5].append(style["hint"].get(language) or "")
        weighted[3].append(style["description"].get(language) or "")
        weighted[3].extend(prompt["text"] for prompt in style["prompts"].get(language, []))
        weighted[2].extend(style["characteristics"].get(language, []))
        weighted[2].extend(style["dos"].get(language, []))
        weighted[2].extend(style["donts"].get(language, []))
        weighted[2].extend(color["name"].get(language) or "" for color in style["colors"])
    return {weight: normalize(" ".join(values)) for weight, values in weighted.items()}


def score_style(style: dict[str, Any], query: str, language: str) -> int:
    phrase = normalize(query)
    tokens = [token for token in re.findall(r"[\w\-]+", phrase) if len(token) > 1]
    languages = ["zh", "en"] if language == "all" else [language]
    weighted = style_search_text(style, languages)
    score = 0
    normalized_id = normalize(style["id"])
    normalized_names = [normalize(style["name"]["zh"]), normalize(style["name"]["en"])]
    for token in tokens:
        if token == normalized_id:
            score += 30
        elif any(token in name.split() for name in normalized_names):
            score += 12
    for weight, haystack in weighted.items():
        if phrase and phrase in haystack:
            score += weight * 4
        score += sum(weight * min(haystack.count(token), 3) for token in tokens)
    return score


def search_styles(catalog: dict[str, Any], query: str, language: str, limit: int) -> list[dict[str, Any]]:
    results = []
    for style in catalog["styles"]:
        score = score_style(style, query, language)
        if score:
            results.append({"score": score, "style": style})
    results.sort(key=lambda item: (-item["score"], item["style"]["order"]))
    return results[:limit]


def detect_category(description: str) -> str | None:
    haystack = normalize(description)
    scored = []
    for category, terms in CATEGORY_ALIASES.items():
        score = sum(3 if contains_term(haystack, term) else 0 for term in terms)
        if category == "aitech" and contains_term(haystack, "ai"):
            score += 4
        if score:
            scored.append((score, category))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return scored[0][1] if scored else None


def compact_style(style: dict[str, Any], language: str) -> dict[str, Any]:
    effective_language, fallback = language_payload(style, language)
    return {
        "id": style["id"],
        "name": style["name"][language],
        "name_zh": style["name"]["zh"],
        "name_en": style["name"]["en"],
        "difficulty": style["difficulty"],
        "filters": style["filters"],
        "hint": localized(style, "hint", effective_language),
        "translation_status": style["translation_status"],
        "resolved_language": effective_language,
        "fallback_to_chinese": fallback,
    }


def command_stats(catalog: dict[str, Any], args: argparse.Namespace) -> None:
    payload = {
        **catalog["stats"],
        "prompt_entries_total": catalog["stats"]["prompts_zh"] + catalog["stats"]["prompts_en"],
        "recommendation_categories": len(catalog["recommender"]["categories"]),
        "recommendation_levels": len(catalog["recommender"]["levels"]),
        "recommendation_records": sum(
            len(items)
            for levels in catalog["recommender"]["recommendations"].values()
            for items in levels.values()
        ),
        "source": catalog["source"],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"Styles: {payload['styles']} ({payload['styles_bilingual']} bilingual, {payload['styles_zh_only']} zh-only)")
    print(f"Prompts: {payload['prompts_zh']} zh + {payload['prompts_en']} en = {payload['prompt_entries_total']} entries")
    print(f"Recommender: {payload['recommendation_categories']} categories × {payload['recommendation_levels']} levels = {payload['recommendation_records']} records")
    print(f"Captured: {payload['source']['captured_at']} from {payload['source']['url']}")


def command_list(catalog: dict[str, Any], args: argparse.Namespace) -> None:
    styles = [style for style in catalog["styles"] if not args.filter or args.filter in style["filters"]]
    for style in styles:
        name = style["name"][args.lang]
        status = " [zh-only]" if style["translation_status"] == "zh-only" else ""
        print(f"{style['order']:02d}  {style['id']:<15} {name}  d{style['difficulty']}  {','.join(style['filters'])}{status}")
    print(f"\n{len(styles)} style(s)")


def command_show(catalog: dict[str, Any], args: argparse.Namespace) -> None:
    style = resolve_style(catalog["styles"], args.style)
    language, fallback = language_payload(style, args.lang)
    if args.json:
        payload = {**style, "requested_language": args.lang, "resolved_language": language, "fallback_to_chinese": fallback}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if fallback:
        print("[English source unavailable; showing original Chinese data.]\n")
    print(f"# {style['name'][language]} ({style['id']})")
    print(f"Difficulty: {style['difficulty']}/5 | Filters: {', '.join(style['filters'])}")
    print(f"Hint: {localized(style, 'hint', language)}")
    print(f"\n{localized(style, 'description', language)}")
    print("\nColors: " + ", ".join(
        f"{color['name'].get(language) or color['name']['zh']} {color['hex']}" for color in style["colors"]
    ))
    print("\nCharacteristics:")
    for item in localized(style, "characteristics", language):
        print(f"- {item}")
    print("\nPrompts:")
    for prompt in style["prompts"][language]:
        print(f"\n## {prompt['title']}\n{prompt['text']}")
    print("\nCSS:\n```css\n" + style["css"] + "\n```")
    print("\nDo:")
    for item in localized(style, "dos", language):
        print(f"- {item}")
    print("\nDon't:")
    for item in localized(style, "donts", language):
        print(f"- {item}")


def command_search(catalog: dict[str, Any], args: argparse.Namespace) -> None:
    results = search_styles(catalog, args.query, args.lang, args.limit)
    if args.json:
        print(json.dumps([
            {"score": result["score"], **compact_style(result["style"], "zh" if args.lang == "zh" else "en")}
            for result in results
        ], ensure_ascii=False, indent=2))
        return
    if not results:
        print("No matching styles.")
        return
    output_lang = "zh" if args.lang == "zh" else "en"
    for result in results:
        style = result["style"]
        info = compact_style(style, output_lang)
        print(f"{style['id']:<15} score={result['score']:<3} {info['name']} — {info['hint']}")


def command_prompt(catalog: dict[str, Any], args: argparse.Namespace) -> None:
    style = resolve_style(catalog["styles"], args.style)
    language, fallback = language_payload(style, args.lang)
    prompts = style["prompts"][language]
    if args.kind != "all":
        prompts = [prompt for prompt in prompts if prompt_kind(prompt["title"]) == args.kind]
    payload = {
        "style_id": style["id"],
        "style_name": style["name"][language],
        "requested_language": args.lang,
        "resolved_language": language,
        "fallback_to_chinese": fallback,
        "kind": args.kind,
        "prompts": prompts,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if fallback:
        print("[English source unavailable; showing original Chinese prompt.]\n")
    if not prompts:
        print(f"No {args.kind} prompt is available for {style['id']} in {language}.")
        return
    for index, prompt in enumerate(prompts):
        if len(prompts) > 1:
            print(f"## {prompt['title']}")
        print(prompt["text"])
        if index < len(prompts) - 1:
            print()


def command_recommend(catalog: dict[str, Any], args: argparse.Namespace) -> None:
    category = args.category or detect_category(args.description)
    results: list[dict[str, Any]] = []
    if category:
        items = catalog["recommender"]["recommendations"][category][str(args.level)]
        by_id = {style["id"]: style for style in catalog["styles"]}
        results = [{"style": by_id[item["style_id"]], "reason": item["reason"][args.lang], "badges": item["badges"]}
                   for item in items]
    else:
        fallback_reason = "匹配到目录字段" if args.lang == "zh" else "Matched catalog fields"
        for result in search_styles(catalog, args.description, "all", args.limit):
            results.append({"style": result["style"], "reason": fallback_reason, "badges": []})
    results = results[:args.limit]
    payload = {
        "detected_category": category,
        "creativity_level": args.level,
        "results": [
            {**compact_style(result["style"], args.lang), "reason": result["reason"], "badges": result["badges"]}
            for result in results
        ],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if category:
        category_info = next(item for item in catalog["recommender"]["categories"] if item["id"] == category)
        print(f"Category: {category_info[args.lang]} | Creativity: {args.level}/4\n")
    elif not results:
        print("No recommendation category or matching style found.")
        return
    for index, result in enumerate(payload["results"], 1):
        badges = f" [{', '.join(result['badges'])}]" if result["badges"] else ""
        print(f"{index}. {result['name']} ({result['id']}){badges}\n   {result['reason']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG, help="catalog.json path")
    subparsers = parser.add_subparsers(dest="command", required=True)

    stats_parser = subparsers.add_parser("stats", help="show snapshot coverage")
    stats_parser.add_argument("--json", action="store_true")
    stats_parser.set_defaults(handler=command_stats)

    list_parser = subparsers.add_parser("list", help="list styles")
    list_parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    list_parser.add_argument("--filter", choices=["easy", "medium", "hard", "light", "dark", "trend", "bold"])
    list_parser.set_defaults(handler=command_list)

    show_parser = subparsers.add_parser("show", help="show complete style details")
    show_parser.add_argument("style")
    show_parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    show_parser.add_argument("--json", action="store_true")
    show_parser.set_defaults(handler=command_show)

    search_parser = subparsers.add_parser("search", help="search catalog text")
    search_parser.add_argument("query")
    search_parser.add_argument("--lang", choices=["zh", "en", "all"], default="all")
    search_parser.add_argument("--limit", type=int, default=8)
    search_parser.add_argument("--json", action="store_true")
    search_parser.set_defaults(handler=command_search)

    prompt_parser = subparsers.add_parser("prompt", help="copy one style's prompts")
    prompt_parser.add_argument("style")
    prompt_parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    prompt_parser.add_argument("--kind", choices=["basic", "advanced", "keywords", "all"], default="all")
    prompt_parser.add_argument("--json", action="store_true")
    prompt_parser.set_defaults(handler=command_prompt)

    recommend_parser = subparsers.add_parser("recommend", help="recommend styles for a project")
    recommend_parser.add_argument("description")
    recommend_parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    recommend_parser.add_argument("--level", type=int, choices=range(1, 5), default=2)
    recommend_parser.add_argument("--category", choices=list(CATEGORY_ALIASES))
    recommend_parser.add_argument("--limit", type=int, default=3)
    recommend_parser.add_argument("--json", action="store_true")
    recommend_parser.set_defaults(handler=command_recommend)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "limit", 1) < 1:
        parser.error("--limit must be at least 1")
    try:
        catalog = load_catalog(args.catalog)
        args.handler(catalog, args)
    except CatalogError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
