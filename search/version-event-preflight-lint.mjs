// version-event preflight lint(便 50 F8.1・裁定 59 採用)
// 版イベント直前に、現役本文へ残ってはならない token を fail-closed で走査する。
// 履歴・撤回文脈(RETRACTED / 撤回 / 【履歴】/ 変更履歴表の行)は allowlist。
// 使い方: node search/version-event-preflight-lint.mjs <file...>   (無指定なら既定 3 文書)
// exit 0 = クリーン / exit 1 = 要検分 hit あり(hit は司令塔が個別判定)
import fs from 'fs';

const DEFAULT_FILES = [
  'docs/week4-BFC攻略_opus_v2.md',
  'docs/amendment_5prime_draft.md',
  'docs/week4-TB4導出_opus_v1.md',
];

const TOKENS = [
  { id: 'unadjusted',       re: /未調整|要調整/ },
  { id: 'stale-v1-status',  re: /現在は v1|現在は\s*`?659a9570/ },
  { id: 'stale-provenance', re: /残るのは[^\n]{0,40}provenance|残るのは[^\n]{0,40}束縛/ },
  { id: 'unversioned-bundle', re: /THEOREM-ANTECEDENT-Rcyc(?!\/)|FALSIFIER-ANTECEDENT-BFC(?!\/)/ },
  { id: 'old-b-names',      re: /b_\{?\(8\.1\)\}?|b_\{\\rm TB4\}|b_TB4/ },
  { id: 'untyped-t-eps',    re: /(?<!\\bar\s{0,3})(?<!\\bar\{)t\\varepsilon|t\s*\\cdot\s*\\varepsilon(?![^\n]*\\bar)/ },
  { id: 'unconditional',    re: /無条件(?![^\n]*root-link-free)/ },
];

const ALLOW = /RETRACTED|撤回|【履歴】|変更履歴|差分一覧|旧文引用|←\s*旧|v2\.\d+ まで/;
const TABLE_HISTORY = /^\|\s*\*\*(?:[A-Z]\d+|[UVGERS]\d+|R\d+)\*\*\s*\|/; // 変更履歴表の行(U5/G1/V18/E2 等)

let totalHits = 0;
for (const f of process.argv.length > 2 ? process.argv.slice(2) : DEFAULT_FILES) {
  const lines = fs.readFileSync(f, 'utf8').split('\n');
  const hits = [];
  lines.forEach((line, i) => {
    if (ALLOW.test(line) || TABLE_HISTORY.test(line)) return;
    for (const t of TOKENS) {
      if (t.re.test(line)) hits.push({ line: i + 1, token: t.id, text: line.slice(0, 120) });
    }
  });
  console.log(`## ${f}: ${hits.length} hit(s)`);
  for (const h of hits) console.log(`  L${h.line} [${h.token}] ${h.text}`);
  totalHits += hits.length;
}
console.log(totalHits === 0 ? 'PREFLIGHT_LINT_CLEAN' : `PREFLIGHT_LINT_HITS: ${totalHits}(司令塔検分が必要 — 版イベント発火不可)`);
process.exit(totalHits === 0 ? 0 : 1);
