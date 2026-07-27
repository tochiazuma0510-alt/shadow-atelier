#!/usr/bin/env node
// crosscheck/check-blob-hashes.mjs -- 裁定41/便40 F5.3 対応。
//
// 目的: docs/week4-K5_Rule1_impl_versions.md の「単一 active blob table」
// (§9.9・<!-- ACTIVE-BLOB-TABLE-START/END --> で囲まれたセクション)を
// パースし、各行の `path` に対して実際に `git hash-object <path>` を実行して
// 記載された blob hash と一致することを検査する。Sol 便40 F5.3 の指摘
// (「active blob table を一つに限定し、全 path を git hash-object と自動
// 照合する小型 checker を置く」)への対応。
//
// この checker は文書の一貫性だけを検査するものであり、GAP/node の
// 探索器・照合器の分離とは無関係(ES(7) の「探索器と照合器の分離」規律の
// 対象外 -- ここでの「照合」は文書の自己整合性チェックであって、数学的な
// crosscheck ではない)。
//
// 実行: node crosscheck/check-blob-hashes.mjs

import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const DOC = join(ROOT, 'docs/week4-K5_Rule1_impl_versions.md');

const START = '<!-- ACTIVE-BLOB-TABLE-START -->';
const END = '<!-- ACTIVE-BLOB-TABLE-END -->';

const text = readFileSync(DOC, 'utf8');
const startIdx = text.indexOf(START);
const endIdx = text.indexOf(END);
if (startIdx === -1 || endIdx === -1 || endIdx < startIdx) {
  console.error(`INTEGRITY_STOP: could not find ${START} / ${END} anchors in ${DOC}`);
  process.exit(1);
}
const block = text.slice(startIdx + START.length, endIdx);

// row format: | `path` | role text | `40-hex-blob-hash` |
const ROW_RE = /^\|\s*`([^`]+)`\s*\|(.*)\|\s*`([0-9a-f]{40})`\s*\|\s*$/;
const HEADER_RE = /^\|\s*path\s*\|\s*role\s*\|\s*blob hash\s*\|\s*$/;
const SEPARATOR_RE = /^\|[-\s|]+\|$/;

// 便40 F5.3 較正で自ら実演した罠(自己反省として記録): 旧版は行が ROW_RE に
// マッチしなければ黙って読み飛ばしていた(header/separator 行のような
// "無視してよい" 行と "本当は照合すべきだが書式が崩れた" 行を区別しな
// かったため、path セル直後に注記(例: `` `path`(新設) ``)を付けた行が
// サイレントに数えられずに 34/34 と誤って報告する fail-open が実際に
// 起きた)。**本版は空行・header・separator 以外の行が ROW_RE に一致
// しなければ INTEGRITY_STOP で止まる**(照合対象の取りこぼしを黙認しない)。
const rows = [];
const unparsedLines = [];
for (const rawLine of block.split(/\r?\n/)) {
  const line = rawLine.trim();
  if (line.length === 0) continue;
  if (HEADER_RE.test(line) || SEPARATOR_RE.test(line)) continue;
  const m = ROW_RE.exec(line);
  if (m) { rows.push({ path: m[1], role: m[2].trim(), hash: m[3] }); continue; }
  unparsedLines.push(line);
}

if (unparsedLines.length > 0) {
  console.error('INTEGRITY_STOP: active blob table contains line(s) that are neither header/separator nor a valid `path`|role|`hash` row -- these would otherwise be silently skipped:');
  for (const l of unparsedLines) console.error(`  ${l}`);
  process.exit(1);
}

if (rows.length === 0) {
  console.error('INTEGRITY_STOP: active blob table block parsed to zero rows (anchor markers present but no matching rows -- check row format)');
  process.exit(1);
}

let pass = 0, fail = 0;
for (const { path, hash } of rows) {
  let actual;
  try {
    actual = execFileSync('git', ['hash-object', path], { cwd: ROOT, encoding: 'utf8' }).trim();
  } catch (e) {
    console.log(`[FAIL] ${path}: git hash-object failed -- ${e.message}`);
    fail++;
    continue;
  }
  if (actual === hash) {
    console.log(`[PASS] ${path}: ${actual}`);
    pass++;
  } else {
    console.log(`[FAIL] ${path}: doc says ${hash}, git hash-object says ${actual}`);
    fail++;
  }
}

console.log(`\n=== ${pass}/${pass + fail} PASS (active blob table: ${rows.length} rows) ===`);
if (fail > 0) process.exitCode = 1;
