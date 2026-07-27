// version-event preflight lint v2(便 50 F8.1 → 便 51 F5.3/F9.2/F9.3 反映・裁定 61)
// v2 の変更: ①裸の b / 型再融合の token 追加 ②走査対象に provenance/CLAIMS.md ③allowlist を
// 行単位キーワードから「打消し(~~)+RETRACTED blockquote 範囲」の block 型へ ④triage record
// (search/preflight-triage.json・normalized line hash 束縛)— 全 hit が有効 disposition を
// 持つときのみ exit 0。本文が変わると hash が失効し triage は自動無効(便 51 F9.3)。
// 使い方: node search/version-event-preflight-lint.mjs [--triage] <file...>
import fs from 'fs';
import crypto from 'crypto';

const DEFAULT_FILES = [
  'docs/week4-BFC攻略_opus_v2.md',
  'docs/amendment_5prime_draft.md',
  'docs/week4-TB4導出_opus_v1.md',
  'provenance/CLAIMS.md',
];
const TRIAGE_PATH = 'search/preflight-triage.json';

const TOKENS = [
  { id: 'unadjusted',        re: /未調整|要調整/ },
  { id: 'stale-v1-status',   re: /現在は v1|現在は\s*`?659a9570/ },
  { id: 'stale-provenance',  re: /残るのは[^\n]{0,40}provenance/ },
  { id: 'unversioned-bundle', re: /THEOREM-ANTECEDENT-Rcyc(?!\/)|FALSIFIER-ANTECEDENT-BFC(?!\/)/ },
  { id: 'old-b-names',       re: /b_\{?\(8\.1\)\}?|b_\{\\rm TB4\}|b_TB4/ },
  { id: 'untyped-t-eps',     re: /(?<!\\bar\s{0,3})(?<!\\bar\{)t\\varepsilon/ },
  // v2: 裸の b(数式中の指数・添字としての単独 b。b_{\rm op}/b_{\rm cmp}/\hat b/b_i 等の typed 形は除外)
  { id: 'naked-b',           re: /\\kappa\^b(?![_\\{a-zA-Z])|\\xi\^\{?\s*b\s*\}?(?![_a-zA-Z])|\{bk\}|\^\{bk\}|で定めた \$b\$|\\zeta_M\^\{?bk/ },
  // v2: 型再融合(b_op/link-free 宣言系と ε^{-1}=:b の同居パターン)
  { id: 're-fusion',         re: /=\s*\\varepsilon\^\{-1\}[^\n]{0,20}=:\s*b(?![_])|b\s*:=\s*\\varepsilon\^\{-1\}(?![^\n]*b_\{\\rm (?:op|cmp)\})/ },
  { id: 'unconditional',     re: /無条件(?![^\n]{0,60}(root-link-free|ではなく|ではない|と書いた|と呼んだ|と呼んでよいのは))/ },
];

function lineHash(s) { return crypto.createHash('sha1').update(s.replace(/\s+/g, ' ').trim()).digest('hex').slice(0, 16); }

let triage = {};
try { triage = JSON.parse(fs.readFileSync(TRIAGE_PATH, 'utf8')); } catch {}

const args = process.argv.slice(2).filter(a => a !== '--triage');
const writeTriage = process.argv.includes('--triage');
const files = args.length ? args : DEFAULT_FILES;

let open = 0, dispositioned = 0;
const newTriage = {};
for (const f of files) {
  const lines = fs.readFileSync(f, 'utf8').split('\n');
  // block 型 allowlist: RETRACTED を含む blockquote 開始から、その blockquote が切れるまで
  const allowed = new Array(lines.length).fill(false);
  let inRetractedBox = false;
  lines.forEach((line, i) => {
    if (/RETRACTED|【履歴】/.test(line) && /^\s*>/.test(line)) inRetractedBox = true;
    if (inRetractedBox && !/^\s*>/.test(line) && line.trim() !== '') inRetractedBox = false;
    if (inRetractedBox) allowed[i] = true;
    if (/~~[^~]+~~/.test(line)) allowed[i] = true;           // 打消し引用
    if (/^\|\s*\*\*[A-Z]+\d+\*\*\s*\|/.test(line)) allowed[i] = true; // 変更履歴表の行(U5/G1/V18/H1/A15 等)
  });
  const hits = [];
  lines.forEach((line, i) => {
    if (allowed[i]) return;
    for (const t of TOKENS) if (t.re.test(line)) hits.push({ line: i + 1, token: t.id, text: line.slice(0, 110), fp: lineHash(line) });
  });
  console.log(`## ${f}: ${hits.length} hit(s)`);
  for (const h of hits) {
    const key = `${f}::${h.fp}::${h.token}`;
    const d = triage[key];
    if (d && d.disposition) { dispositioned++; console.log(`  L${h.line} [${h.token}] (triaged: ${d.disposition}) ${h.text.slice(0, 70)}`); }
    else { open++; console.log(`  L${h.line} [${h.token}] OPEN ${h.text}`); }
    if (writeTriage && !d) newTriage[key] = { file: f, line: h.line, token: h.token, text: h.text, disposition: '', reviewer: '' };
  }
}
if (writeTriage && Object.keys(newTriage).length) {
  fs.writeFileSync(TRIAGE_PATH, JSON.stringify({ ...triage, ...newTriage }, null, 2));
  console.log(`triage 雛形を ${TRIAGE_PATH} に追記(disposition 記入後に再実行)`);
}
console.log(open === 0
  ? `PREFLIGHT_LINT_CLEAN(open 0 / triaged ${dispositioned})`
  : `PREFLIGHT_LINT_OPEN_HITS: ${open}(triaged ${dispositioned}・司令塔 disposition 記入まで版イベント発火不可)`);
process.exit(open === 0 ? 0 : 1);
