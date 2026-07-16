#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

function parseArguments(argv) {
  const positional = [];
  let capturedAt = new Date().toISOString();

  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--captured-at") {
      capturedAt = argv[index + 1];
      index += 1;
      if (!capturedAt || Number.isNaN(Date.parse(capturedAt))) {
        throw new Error("--captured-at must be a valid ISO 8601 date-time");
      }
    } else if (argument.startsWith("-")) {
      throw new Error(`Unknown option: ${argument}`);
    } else {
      positional.push(argument);
    }
  }

  if (positional.length !== 2) {
    throw new Error(
      "Usage: node extract_site_data.mjs <inline-scripts.json|inline-script.js> <catalog.json> " +
        "[--captured-at <ISO-8601>]",
    );
  }
  return { inputPath: positional[0], outputPath: positional[1], capturedAt };
}

let argumentsParsed;
try {
  argumentsParsed = parseArguments(process.argv.slice(2));
} catch (error) {
  console.error(error.message);
  process.exit(2);
}
const { inputPath, outputPath, capturedAt } = argumentsParsed;

function skipTrivia(source, start) {
  let index = start;
  while (index < source.length) {
    if (/\s/u.test(source[index])) {
      index += 1;
    } else if (source.startsWith("//", index)) {
      const newline = source.indexOf("\n", index + 2);
      index = newline < 0 ? source.length : newline + 1;
    } else if (source.startsWith("/*", index)) {
      const closing = source.indexOf("*/", index + 2);
      if (closing < 0) throw new Error(`Unterminated block comment near offset ${index}`);
      index = closing + 2;
    } else {
      break;
    }
  }
  return index;
}

function findMarker(source, marker) {
  let quote = null;
  let escaped = false;
  let lineComment = false;
  let blockComment = false;

  for (let index = 0; index < source.length; index += 1) {
    const character = source[index];
    const next = source[index + 1];

    if (lineComment) {
      if (character === "\n") lineComment = false;
      continue;
    }
    if (blockComment) {
      if (character === "*" && next === "/") {
        blockComment = false;
        index += 1;
      }
      continue;
    }
    if (quote) {
      if (escaped) {
        escaped = false;
      } else if (character === "\\") {
        escaped = true;
      } else if (character === quote) {
        quote = null;
      }
      continue;
    }
    if (character === "/" && next === "/") {
      lineComment = true;
      index += 1;
      continue;
    }
    if (character === "/" && next === "*") {
      blockComment = true;
      index += 1;
      continue;
    }
    if (character === "'" || character === '"' || character === "`") {
      quote = character;
      continue;
    }

    const previous = source[index - 1];
    const validBoundary = index === 0 || /[\s;{}]/u.test(previous);
    if (validBoundary && source.startsWith(marker, index)) return index;
  }
  return -1;
}

function findLiteral(source, marker, opening) {
  const markerIndex = findMarker(source, marker);
  if (markerIndex < 0) throw new Error(`Marker not found: ${marker}`);

  const start = skipTrivia(source, markerIndex + marker.length);
  if (source[start] !== opening) {
    throw new Error(`Expected data literal ${opening} immediately after ${marker}`);
  }

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

class LiteralParser {
  constructor(source, label) {
    this.source = source;
    this.label = label;
    this.index = 0;
  }

  error(message) {
    throw new Error(`${this.label}:${this.index}: ${message}`);
  }

  skipTrivia() {
    this.index = skipTrivia(this.source, this.index);
  }

  parse() {
    this.skipTrivia();
    const value = this.parseValue();
    this.skipTrivia();
    if (this.index !== this.source.length) this.error("Unexpected content after data literal");
    return value;
  }

  parseValue() {
    this.skipTrivia();
    const character = this.source[this.index];
    if (character === "{") return this.parseObject();
    if (character === "[") return this.parseArray();
    if (character === "\"" || character === "'" || character === "`") return this.parseString();
    if (character === "+" || character === "-" || character === "." || /[0-9]/u.test(character ?? "")) {
      return this.parseNumber();
    }
    if (/[A-Za-z_$]/u.test(character ?? "")) {
      const identifier = this.parseIdentifier();
      if (identifier === "true") return true;
      if (identifier === "false") return false;
      if (identifier === "null") return null;
      this.error(`Unsupported identifier value: ${identifier}`);
    }
    this.error(`Unsupported value starting with ${JSON.stringify(character)}`);
  }

  parseObject() {
    const result = Object.create(null);
    this.index += 1;
    this.skipTrivia();
    if (this.source[this.index] === "}") {
      this.index += 1;
      return result;
    }

    while (this.index < this.source.length) {
      this.skipTrivia();
      const character = this.source[this.index];
      let key;
      if (character === "\"" || character === "'" || character === "`") {
        key = this.parseString();
      } else if (/[A-Za-z_$]/u.test(character ?? "")) {
        key = this.parseIdentifier();
      } else if (/[0-9]/u.test(character ?? "")) {
        key = String(this.parseNumber());
      } else {
        this.error("Object keys must be strings, identifiers, or numbers");
      }
      if (Object.hasOwn(result, key)) this.error(`Duplicate object key: ${key}`);

      this.skipTrivia();
      if (this.source[this.index] !== ":") this.error(`Expected ':' after object key ${key}`);
      this.index += 1;
      result[key] = this.parseValue();
      this.skipTrivia();

      const separator = this.source[this.index];
      if (separator === "}") {
        this.index += 1;
        return result;
      }
      if (separator !== ",") this.error("Expected ',' or '}' in object literal");
      this.index += 1;
      this.skipTrivia();
      if (this.source[this.index] === "}") {
        this.index += 1;
        return result;
      }
    }
    this.error("Unterminated object literal");
  }

  parseArray() {
    const result = [];
    this.index += 1;
    this.skipTrivia();
    if (this.source[this.index] === "]") {
      this.index += 1;
      return result;
    }

    while (this.index < this.source.length) {
      if (this.source[this.index] === ",") this.error("Sparse arrays are not supported");
      result.push(this.parseValue());
      this.skipTrivia();
      const separator = this.source[this.index];
      if (separator === "]") {
        this.index += 1;
        return result;
      }
      if (separator !== ",") this.error("Expected ',' or ']' in array literal");
      this.index += 1;
      this.skipTrivia();
      if (this.source[this.index] === "]") {
        this.index += 1;
        return result;
      }
    }
    this.error("Unterminated array literal");
  }

  parseIdentifier() {
    const match = /^[A-Za-z_$][\w$]*/u.exec(this.source.slice(this.index));
    if (!match) this.error("Invalid identifier");
    this.index += match[0].length;
    return match[0];
  }

  parseNumber() {
    const match = /^[+-]?(?:0[xX][0-9a-fA-F]+|0[bB][01]+|0[oO][0-7]+|(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)/u.exec(
      this.source.slice(this.index),
    );
    if (!match) this.error("Invalid number");
    this.index += match[0].length;
    const value = Number(match[0]);
    if (!Number.isFinite(value)) this.error("Number must be finite");
    return value;
  }

  parseString() {
    const quote = this.source[this.index];
    let result = "";
    this.index += 1;

    while (this.index < this.source.length) {
      const character = this.source[this.index];
      if (character === quote) {
        this.index += 1;
        return result;
      }
      if (quote === "`" && character === "$" && this.source[this.index + 1] === "{") {
        this.error("Template interpolation is not allowed");
      }
      if (character === "\n" || character === "\r") {
        if (quote !== "`") this.error("Unescaped newline in string literal");
        result += character;
        this.index += 1;
        continue;
      }
      if (character !== "\\") {
        result += character;
        this.index += 1;
        continue;
      }

      this.index += 1;
      if (this.index >= this.source.length) this.error("Unterminated string escape");
      const escaped = this.source[this.index];
      const simpleEscapes = {
        "'": "'",
        '"': '"',
        "`": "`",
        "\\": "\\",
        b: "\b",
        f: "\f",
        n: "\n",
        r: "\r",
        t: "\t",
        v: "\v",
        0: "\0",
      };
      if (Object.hasOwn(simpleEscapes, escaped)) {
        if (escaped === "0" && /[0-9]/u.test(this.source[this.index + 1] ?? "")) {
          this.error("Legacy octal escapes are not supported");
        }
        result += simpleEscapes[escaped];
        this.index += 1;
      } else if (escaped === "x") {
        const hex = this.source.slice(this.index + 1, this.index + 3);
        if (!/^[0-9a-fA-F]{2}$/u.test(hex)) this.error("Invalid hexadecimal escape");
        result += String.fromCharCode(Number.parseInt(hex, 16));
        this.index += 3;
      } else if (escaped === "u") {
        const brace = this.source[this.index + 1] === "{";
        const end = brace ? this.source.indexOf("}", this.index + 2) : this.index + 5;
        const hex = this.source.slice(this.index + (brace ? 2 : 1), end);
        if (!/^[0-9a-fA-F]{1,6}$/u.test(hex) || (!brace && hex.length !== 4)) {
          this.error("Invalid Unicode escape");
        }
        const codePoint = Number.parseInt(hex, 16);
        if (codePoint > 0x10ffff) this.error("Unicode escape is out of range");
        result += String.fromCodePoint(codePoint);
        this.index = end + (brace ? 1 : 0);
      } else if (escaped === "\n") {
        this.index += 1;
      } else if (escaped === "\r") {
        this.index += this.source[this.index + 1] === "\n" ? 2 : 1;
      } else {
        result += escaped;
        this.index += 1;
      }
    }
    this.error("Unterminated string literal");
  }
}

function parseLiteral(literal, label) {
  return new LiteralParser(literal, label).parse();
}

function normalizePrompt(prompt) {
  return { title: prompt.t, text: prompt.x };
}

const inputText = fs.readFileSync(inputPath, "utf8");
let source = inputText;
if (inputPath.endsWith(".json")) {
  const scripts = JSON.parse(inputText);
  if (!Array.isArray(scripts)) throw new Error("JSON input must be an array of script records");
  const markers = [
    "const S =",
    "const S_EN =",
    "const P=",
    "const RECO_CATS =",
    "const RECO_LEVELS =",
    "const RECO_MAP =",
  ];
  const sourceEntry = scripts
    .filter(
      (entry) =>
        typeof entry?.text === "string" && markers.every((marker) => findMarker(entry.text, marker) >= 0),
    )
    .sort((a, b) => b.text.length - a.text.length)[0];
  if (!sourceEntry) throw new Error("No script record contains the complete Design Lab catalog markers");
  source = sourceEntry.text;
}

if (source.length < 1_000) throw new Error("No substantial inline script found");
const stylesZh = parseLiteral(findLiteral(source, "const S =", "["), "styles-zh.js");
const stylesEn = parseLiteral(findLiteral(source, "const S_EN =", "{"), "styles-en.js");
const promptsEn = parseLiteral(findLiteral(source, "const P=", "{"), "prompts-en.js");
const recommendationCategories = parseLiteral(
  findLiteral(source, "const RECO_CATS =", "["),
  "recommendation-categories.js",
);
const recommendationLevels = parseLiteral(
  findLiteral(source, "const RECO_LEVELS =", "["),
  "recommendation-levels.js",
);
const recommendationMap = parseLiteral(
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

const orphanEnglishIds = [...new Set([...Object.keys(stylesEn), ...Object.keys(promptsEn)])].filter(
  (id) => !seen.has(id),
);
if (orphanEnglishIds.length) {
  throw new Error(`English ids without Chinese styles: ${orphanEnglishIds.join(", ")}`);
}

const result = {
  schema_version: "1.0.0",
  source: {
    url: "https://design-lab-yanliu.vercel.app/",
    title: "Design Lab",
    curator: "Dreameryanyan",
    captured_at: capturedAt,
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
