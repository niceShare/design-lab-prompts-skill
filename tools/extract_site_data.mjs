#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import crypto from "node:crypto";

const [inputPath, outputPath] = process.argv.slice(2);

if (!inputPath || !outputPath) {
  console.error("Usage: node extract_site_data.mjs <inline-scripts.json> <catalog.json>");
  process.exit(2);
}

function findLiteral(source, marker, opening) {
  const markerIndex = source.indexOf(marker);
  if (markerIndex < 0) throw new Error(`Marker not found: ${marker}`);

  const start = source.indexOf(opening, markerIndex + marker.length);
  if (start < 0) throw new Error(`Opening ${opening} not found after ${marker}`);

  const pairs = { "{": "}", "[": "]", "(": ")" };
  const stack = [];
  let quote = null;
  let escaped = false;
  let lineComment = false;
  let blockComment = false;

  for (let i = start; i < source.length; i += 1) {
    const ch = source[i];
    const next = source[i + 1];

    if (lineComment) {
      if (ch === "\n") lineComment = false;
      continue;
    }
    if (blockComment) {
      if (ch === "*" && next === "/") {
        blockComment = false;
        i += 1;
      }
      continue;
    }
    if (quote) {
      if (escaped) {
        escaped = false;
      } else if (ch === "\\") {
        escaped = true;
      } else if (ch === quote) {
        quote = null;
      }
      continue;
    }
    if (ch === "/" && next === "/") {
      lineComment = true;
      i += 1;
      continue;
    }
    if (ch === "/" && next === "*") {
      blockComment = true;
      i += 1;
      continue;
    }
    if (ch === "'" || ch === '"' || ch === "`") {
      quote = ch;
      continue;
    }
    if (pairs[ch]) {
      stack.push(ch);
      continue;
    }
    const expectedOpening = Object.keys(pairs).find((key) => pairs[key] === ch);
    if (expectedOpening) {
      const actualOpening = stack.pop();
      if (actualOpening !== expectedOpening) {
        throw new Error(`Unbalanced literal near offset ${i}`);
      }
      if (stack.length === 0) return source.slice(start, i + 1);
    }
  }

  throw new Error(`Unterminated literal after ${marker}`);
}

function evaluateLiteral(literal, label) {
  return vm.runInNewContext(`(${literal})`, Object.create(null), {
    filename: label,
    timeout: 1_000,
  });
}

function normalizePrompt(prompt) {
  return { title: prompt.t, text: prompt.x };
}

const inputText = fs.readFileSync(inputPath, "utf8");
let source = inputText;
if (inputPath.endsWith(".json")) {
  const scripts = JSON.parse(inputText);
  const sourceEntry = scripts
    .filter((entry) => typeof entry.text === "string")
    .sort((a, b) => b.text.length - a.text.length)[0];
  source = sourceEntry?.text ?? "";
}

if (source.length < 1_000) throw new Error("No substantial inline script found");
const stylesZh = evaluateLiteral(findLiteral(source, "const S =", "["), "styles-zh.js");
const stylesEn = evaluateLiteral(findLiteral(source, "const S_EN =", "{"), "styles-en.js");
const promptsEn = evaluateLiteral(findLiteral(source, "const P=", "{"), "prompts-en.js");
const recommendationCategories = evaluateLiteral(
  findLiteral(source, "const RECO_CATS =", "["),
  "recommendation-categories.js",
);
const recommendationLevels = evaluateLiteral(
  findLiteral(source, "const RECO_LEVELS =", "["),
  "recommendation-levels.js",
);
const recommendationMap = evaluateLiteral(
  findLiteral(source, "const RECO_MAP =", "{"),
  "recommendation-map.js",
);

const seen = new Set();
const styles = stylesZh.map((style, index) => {
  if (seen.has(style.id)) throw new Error(`Duplicate style id: ${style.id}`);
  seen.add(style.id);

  const english = stylesEn[style.id];
  const englishPrompts = promptsEn[style.id];
  return {
    order: index + 1,
    id: style.id,
    name: { zh: style.cn, en: style.name },
    difficulty: style.diff,
    filters: style.f,
    translation_status: english && englishPrompts ? "complete" : "zh-only",
    description: { zh: style.desc, en: english?.desc ?? null },
    characteristics: { zh: style.chars, en: english?.chars ?? [] },
    colors: style.colors.map((hex, colorIndex) => ({
      hex,
      name: {
        zh: style.cnames[colorIndex] ?? null,
        en: englishPrompts?.cnames?.[colorIndex] ?? null,
      },
    })),
    css: style.css,
    hint: { zh: style.hint, en: englishPrompts?.hint ?? null },
    prompts: {
      zh: style.prompts.map(normalizePrompt),
      en: englishPrompts?.prompts?.map(normalizePrompt) ?? [],
    },
    dos: { zh: style.dos, en: english?.dos ?? [] },
    donts: { zh: style.donts, en: english?.donts ?? [] },
  };
});

const orphanEnglishIds = Object.keys(promptsEn).filter((id) => !seen.has(id));
if (orphanEnglishIds.length) {
  throw new Error(`English prompt ids without Chinese styles: ${orphanEnglishIds.join(", ")}`);
}

const result = {
  schema_version: "1.0.0",
  source: {
    url: "https://design-lab-yanliu.vercel.app/",
    title: "Design Lab",
    curator: "Dreameryanyan",
    captured_at: "2026-07-16T17:29:57+08:00",
    extraction: "current rendered page inline JavaScript",
    inline_source_characters: source.length,
    inline_source_sha256: crypto.createHash("sha256").update(source).digest("hex"),
    note: "Search-engine cache advertised 67 styles; the current page source contains 77.",
  },
  stats: {
    styles: styles.length,
    styles_bilingual: styles.filter((style) => style.translation_status === "complete").length,
    styles_zh_only: styles.filter((style) => style.translation_status === "zh-only").length,
    prompts_zh: styles.reduce((sum, style) => sum + style.prompts.zh.length, 0),
    prompts_en: styles.reduce((sum, style) => sum + style.prompts.en.length, 0),
  },
  recommender: {
    categories: recommendationCategories,
    levels: recommendationLevels,
    recommendations: Object.fromEntries(
      Object.entries(recommendationMap).map(([category, levels]) => [
        category,
        Object.fromEntries(
          Object.entries(levels).map(([level, items]) => [
            level,
            items.map(([styleId, reasonZh, reasonEn, badges]) => ({
              style_id: styleId,
              reason: { zh: reasonZh, en: reasonEn },
              badges,
            })),
          ]),
        ),
      ]),
    ),
  },
  styles,
};

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify(result.stats));
