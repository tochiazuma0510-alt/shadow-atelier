#!/usr/bin/env node
// crosscheck/check-blob-hashes.mjs -- 裁定41/便40 F5.3 + 裁定42/便41 F3.2 対応。
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
// ============================================================================
// 裁定42/便41 F3.2 対応(coverage モード・本ファイルの主眼):
//
// 旧版の穴(Sol 実測): active blob table は「載っている行」だけを検査し、
// 「載っていないファイル」の存在を一切見ていなかった。そのため
//   - 表から一行を完全に削除すると、残りが一致する限り fail-closed に
//     見えたまま静かに縮小する(取りこぼしを検出しない)。
//   - START/END を `indexOf` で最初の一組しか見ないため、二つ目の
//     active-looking table を後ろに置いても最初の marker pair しか読まない。
//   - checker 自身(crosscheck/check-blob-hashes.mjs)が表に載っておらず、
//     「照合器の bytes を束縛するものが何もない」状態だった。
//
// 本版は次の3つを追加する:
//   1. **coverage 列挙**: `crosscheck/*.mjs`・`crosscheck/*.ps1`・
//      `search/*.g`・`search/*.mjs` を実列挙し、各ファイルが
//      (a) active blob table に載っている、または
//      (b) 明示的な EXCLUDED-FILES テーブル(理由つき)に載っている
//      のいずれでもなければ INTEGRITY_STOP で止まる(取りこぼし禁止)。
//      対象ディレクトリ内に「表にも除外リストにも無いファイル」が一つでも
//      あれば fail-closed。
//   2. **marker 一意性・重複禁止**: START/END マーカーがそれぞれ文書中に
//      ちょうど一回しか出現しないことを assert する(第二の active table を
//      後置する攻撃を拒否)。active table 内の path 重複、および同じ path が
//      active table と exclusion list の両方に載っている(あいまいな二重
//      登録)ことも拒否する。
//   3. **checker 自身の自己拘束**: `crosscheck/check-blob-hashes.mjs` 自身を
//      active blob table に含め、他の全ファイルと同じ hash-object 照合の
//      対象にする。
//
// 実行: node crosscheck/check-blob-hashes.mjs

import { readFileSync, readdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const DOC = join(ROOT, 'docs/week4-K5_Rule1_impl_versions.md');

const ACTIVE_START = '<!-- ACTIVE-BLOB-TABLE-START -->';
const ACTIVE_END = '<!-- ACTIVE-BLOB-TABLE-END -->';
const EXCLUDED_START = '<!-- EXCLUDED-FILES-START -->';
const EXCLUDED_END = '<!-- EXCLUDED-FILES-END -->';

const text = readFileSync(DOC, 'utf8');

// --- marker 一意性(裁定42/便41 F3.2 要件 2 の一部): 各 marker がちょうど
// 一回だけ出現することを assert する。第二の active table / exclusion list
// を後置する攻撃(最初の marker pair だけを読んで通す旧穴)を拒否する。
function countOccurrences(haystack, needle) {
  let count = 0, idx = 0;
  while (true) {
    idx = haystack.indexOf(needle, idx);
    if (idx === -1) break;
    count++;
    idx += needle.length;
  }
  return count;
}
const markerCounts = {
  [ACTIVE_START]: countOccurrences(text, ACTIVE_START),
  [ACTIVE_END]: countOccurrences(text, ACTIVE_END),
  [EXCLUDED_START]: countOccurrences(text, EXCLUDED_START),
  [EXCLUDED_END]: countOccurrences(text, EXCLUDED_END),
};
const badMarkers = Object.entries(markerCounts).filter(([, n]) => n !== 1);
if (badMarkers.length > 0) {
  console.error('INTEGRITY_STOP: anchor markers must each appear exactly once in the document (a second table or a deleted marker would otherwise silently change what is being verified):');
  for (const [marker, n] of badMarkers) console.error(`  ${JSON.stringify(marker)}: found ${n} time(s), expected exactly 1`);
  process.exit(1);
}

const activeStartIdx = text.indexOf(ACTIVE_START);
const activeEndIdx = text.indexOf(ACTIVE_END);
if (activeStartIdx === -1 || activeEndIdx === -1 || activeEndIdx < activeStartIdx) {
  console.error(`INTEGRITY_STOP: could not find ${ACTIVE_START} / ${ACTIVE_END} anchors (or END precedes START) in ${DOC}`);
  process.exit(1);
}
const activeBlock = text.slice(activeStartIdx + ACTIVE_START.length, activeEndIdx);

const exclStartIdx = text.indexOf(EXCLUDED_START);
const exclEndIdx = text.indexOf(EXCLUDED_END);
if (exclStartIdx === -1 || exclEndIdx === -1 || exclEndIdx < exclStartIdx) {
  console.error(`INTEGRITY_STOP: could not find ${EXCLUDED_START} / ${EXCLUDED_END} anchors (or END precedes START) in ${DOC}`);
  process.exit(1);
}
const exclBlock = text.slice(exclStartIdx + EXCLUDED_START.length, exclEndIdx);

// row format (active table): | `path` | role text | `40-hex-blob-hash` |
const ROW_RE = /^\|\s*`([^`]+)`\s*\|(.*)\|\s*`([0-9a-f]{40})`\s*\|\s*$/;
const HEADER_RE = /^\|\s*path\s*\|\s*role\s*\|\s*blob hash\s*\|\s*$/;
const SEPARATOR_RE = /^\|[-\s|]+\|$/;

// row format (exclusion table): | `path` | reason |
const EXCL_ROW_RE = /^\|\s*`([^`]+)`\s*\|(.+)\|\s*$/;
const EXCL_HEADER_RE = /^\|\s*path\s*\|\s*reason\s*\|\s*$/;

// 便40 F5.3 較正で自ら実演した罠(自己反省として記録): 旧版は行が ROW_RE に
// マッチしなければ黙って読み飛ばしていた(header/separator 行のような
// "無視してよい" 行と "本当は照合すべきだが書式が崩れた" 行を区別しな
// かったため、path セル直後に注記(例: `` `path`(新設) ``)を付けた行が
// サイレントに数えられずに 34/34 と誤って報告する fail-open が実際に
// 起きた)。**本版は空行・header・separator 以外の行が ROW_RE に一致
// しなければ INTEGRITY_STOP で止まる**(照合対象の取りこぼしを黙認しない)。
const rows = [];
const unparsedLines = [];
for (const rawLine of activeBlock.split(/\r?\n/)) {
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

const exclRows = [];
const exclUnparsed = [];
for (const rawLine of exclBlock.split(/\r?\n/)) {
  const line = rawLine.trim();
  if (line.length === 0) continue;
  if (EXCL_HEADER_RE.test(line) || SEPARATOR_RE.test(line)) continue;
  const m = EXCL_ROW_RE.exec(line);
  if (m) { exclRows.push({ path: m[1], reason: m[2].trim() }); continue; }
  exclUnparsed.push(line);
}
if (exclUnparsed.length > 0) {
  console.error('INTEGRITY_STOP: excluded-files table contains line(s) that are neither header/separator nor a valid `path`|reason row:');
  for (const l of exclUnparsed) console.error(`  ${l}`);
  process.exit(1);
}
if (exclRows.some((r) => r.reason.length === 0)) {
  console.error('INTEGRITY_STOP: excluded-files table has an entry with an empty reason (exclusions must be justified, not blank)');
  process.exit(1);
}

// --- 重複禁止(裁定42/便41 F3.2 要件 2): active table 内の path 重複、
// exclusion list 内の path 重複、および同じ path が両方に載っている
// あいまいな二重登録を拒否する。行複製攻撃(同じ行を二回貼る)を検出する。
const activePaths = rows.map((r) => r.path);
const activeDupes = activePaths.filter((p, i) => activePaths.indexOf(p) !== i);
const exclPaths = exclRows.map((r) => r.path);
const exclDupes = exclPaths.filter((p, i) => exclPaths.indexOf(p) !== i);
const bothListed = activePaths.filter((p) => exclPaths.includes(p));
if (activeDupes.length > 0 || exclDupes.length > 0 || bothListed.length > 0) {
  console.error('INTEGRITY_STOP: path uniqueness violated:');
  if (activeDupes.length > 0) console.error(`  active blob table has duplicate path(s): ${JSON.stringify([...new Set(activeDupes)])}`);
  if (exclDupes.length > 0) console.error(`  excluded-files table has duplicate path(s): ${JSON.stringify([...new Set(exclDupes)])}`);
  if (bothListed.length > 0) console.error(`  path(s) listed in BOTH active table and excluded-files table (ambiguous): ${JSON.stringify([...new Set(bothListed)])}`);
  process.exit(1);
}

// --- coverage 列挙(裁定42/便41 F3.2 要件 1・主眼): crosscheck/*.mjs,
// crosscheck/*.ps1, search/*.g, search/*.mjs を実列挙し、各ファイルが
// active table か exclusion list のいずれかに載っていることを assert する。
function listExt(dir, ext) {
  return readdirSync(join(ROOT, dir))
    .filter((f) => f.endsWith(`.${ext}`))
    .map((f) => `${dir}/${f}`)
    .sort();
}
const coverageTargets = [
  ...listExt('crosscheck', 'mjs'),
  ...listExt('crosscheck', 'ps1'),
  ...listExt('search', 'g'),
  ...listExt('search', 'mjs'),
];
const knownPaths = new Set([...activePaths, ...exclPaths]);
const uncovered = coverageTargets.filter((p) => !knownPaths.has(p));
if (uncovered.length > 0) {
  console.error(`INTEGRITY_STOP: ${uncovered.length} file(s) under the coverage globs (crosscheck/*.mjs, crosscheck/*.ps1, search/*.g, search/*.mjs) are neither in the active blob table nor in the excluded-files table -- these would otherwise be silently unaccounted for:`);
  for (const p of uncovered) console.error(`  ${p}`);
  process.exit(1);
}
// 逆方向: active table / exclusion list に載っているのに coverage glob の
// 対象ディレクトリの中に実ファイルが存在しない path(=表の記述が古い、
// または削除されたファイルをまだ表からも消していない)は、少なくとも
// coverage glob が対象とする 4 拡張子については矛盾として報告する(ただし
// 証明書・文書等 coverage glob の対象外の active table 行は対象外)。
const coverageTargetSet = new Set(coverageTargets);
const isCoverageScoped = (p) => /^(crosscheck\/.*\.(mjs|ps1)|search\/.*\.(g|mjs))$/.test(p);
const staleActive = activePaths.filter((p) => isCoverageScoped(p) && !coverageTargetSet.has(p));
const staleExcl = exclPaths.filter((p) => isCoverageScoped(p) && !coverageTargetSet.has(p));
if (staleActive.length > 0 || staleExcl.length > 0) {
  console.error('INTEGRITY_STOP: table/exclusion-list entries reference coverage-scoped paths that no longer exist on disk:');
  if (staleActive.length > 0) console.error(`  active table: ${JSON.stringify(staleActive)}`);
  if (staleExcl.length > 0) console.error(`  excluded-files table: ${JSON.stringify(staleExcl)}`);
  process.exit(1);
}

console.log(`coverage: ${coverageTargets.length} file(s) under crosscheck/*.mjs, crosscheck/*.ps1, search/*.g, search/*.mjs`);
console.log(`  -> ${rows.length} in active blob table, ${exclRows.filter((r) => isCoverageScoped(r.path)).length} in excluded-files table (coverage-scoped), ${exclRows.length - exclRows.filter((r) => isCoverageScoped(r.path)).length} excluded entries outside coverage scope`);

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

console.log(`\n=== ${pass}/${pass + fail} PASS (active blob table: ${rows.length} rows; coverage: ${coverageTargets.length}/${coverageTargets.length} accounted for) ===`);
if (fail > 0) process.exitCode = 1;
