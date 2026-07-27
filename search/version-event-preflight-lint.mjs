// version-event preflight lint v3(便 52 F5.4/F7-5/F9 反映・裁定 63)
// v3 の変更(v2 比):
//  ① version-event-manifest.json を入力正本にし、artifact header の版・CLAIMS 行の必須 token・
//     certificate の input_doc 束縛を equality 照合(F9.1 — 「scan した≠同期した」の機械化)
//  ② naked-b 検出を拡張(裸の b=1・「ε の mod n 還元が b」型の再融合説明)
//  ③ triage 検証の fail-closed 化: disposition は closed enum 接頭辞・reviewer 非空・
//     orphan(現 hit に対応しない record)は 0 でなければ FAIL(F9.3)
//  ④ receipt を search/preflight-receipt.json に出力(source_commit・digest・件数・verdict)
// 使い方: node search/version-event-preflight-lint.mjs [--triage] [--prune-orphans] [file...]
import fs from 'fs';
import crypto from 'crypto';
import { execSync } from 'child_process';

const MANIFEST_PATH = 'search/version-event-manifest.json';
const TRIAGE_PATH = 'search/preflight-triage.json';
const RECEIPT_PATH = 'search/preflight-receipt.json';
const DISPOSITION_ENUM = ['scoped-usage', 'local-declaration', 'history-table', 'meta-mention', 'correct-conditional', 'lesson-quote', 'lesson-definition', 'negated-or-lesson', 'math-usage', 'reviewed-legitimate'];

const TOKENS = [
  { id: 'unadjusted',        re: /未調整|要調整/ },
  { id: 'stale-v1-status',   re: /現在は v1|現在は\s*`?659a9570/ },
  { id: 'stale-provenance',  re: /残るのは[^\n]{0,40}provenance/ },
  { id: 'unversioned-bundle', re: /THEOREM-ANTECEDENT-Rcyc(?!\/)|FALSIFIER-ANTECEDENT-BFC(?!\/)/ },
  { id: 'old-b-names',       re: /b_\{?\(8\.1\)\}?|b_\{\\rm TB4\}|b_TB4/ },
  { id: 'untyped-t-eps',     re: /(?<!\\bar\s{0,3})(?<!\\bar\{)t\\varepsilon/ },
  { id: 'naked-b',           re: /\\kappa\^b(?![_\\{a-zA-Z])|\\xi\^\{?\s*b\s*\}?(?![_a-zA-Z])|\{bk\}|\^\{bk\}|で定めた \$b\$|\\zeta_M\^\{?bk/ },
  { id: 'naked-b-eq1',       re: /(?<![_{\\a-zA-Z])b\s*=\s*1(?![0-9])(?![^\n]*b_\{\\rm (?:op|cmp)\})(?![^\n]*b_(?:op|cmp))/ },
  { id: 're-fusion',         re: /=\s*\\varepsilon\^\{-1\}[^\n]{0,20}=:\s*b(?![_])|b\s*:=\s*\\varepsilon\^\{-1\}(?![^\n]*b_\{\\rm (?:op|cmp)\})/ },
  { id: 're-fusion-modM',    re: /単位[^\n]{0,12}\\?varepsilon[^\n]{0,12}の\s*mod\s*\d+\s*還元/ },
  { id: 'unconditional',     re: /無条件(?![^\n]{0,60}(root-link-free|ではなく|ではない|と書いた|と呼んだ|と呼んでよいのは))/ },
];

const lineHash = s => crypto.createHash('sha1').update(s.replace(/\s+/g, ' ').trim()).digest('hex').slice(0, 16);
const sha256 = f => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');

const argv = process.argv.slice(2);
const writeTriage = argv.includes('--triage');
const pruneOrphans = argv.includes('--prune-orphans');
const fileArgs = argv.filter(a => !a.startsWith('--'));

const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
let triage = {}; try { triage = JSON.parse(fs.readFileSync(TRIAGE_PATH, 'utf8')); } catch {}

let failures = [];

// ① manifest equality 照合
const artifactReceipts = [];
for (const a of manifest.artifacts) {
  const head = fs.readFileSync(a.path, 'utf8').split('\n')[0];
  const ok = new RegExp(a.header_re).test(head);
  if (!ok) failures.push(`VERSION-IDENTITY: ${a.path} の 1 行目が declared ${a.declared_version} と不一致`);
  artifactReceipts.push({ path: a.path, sha256: sha256(a.path), declared_version: a.declared_version, header_ok: ok });
}
const claimsText = fs.readFileSync('provenance/CLAIMS.md', 'utf8');
const claimsReceipts = [];
for (const c of manifest.claims) {
  const row = claimsText.split('\n').find(l => l.startsWith(`| ${c.row_id} |`)) || '';
  const missing = c.must_contain.filter(t => !row.includes(t));
  if (missing.length) failures.push(`CLAIMS-SYNC: ${c.row_id} に必須 token 欠落: ${missing.join(' / ')}`);
  claimsReceipts.push({ row_id: c.row_id, ok: missing.length === 0, row_hash: lineHash(row) });
}
const cert = JSON.parse(fs.readFileSync(manifest.certificate.path, 'utf8'));
const certOk = cert.provenance.input_doc_path === manifest.certificate.input_doc_path
  && cert.provenance.input_doc_sha256 === artifactReceipts.find(r => r.path === manifest.certificate.input_doc_path)?.sha256;
if (!certOk) failures.push('CERT-BINDING: certificate の input_doc 束縛が現物 digest と不一致(再束縛が必要)');

// ② token 走査(v2 と同じ block 型 allowlist)
const files = fileArgs.length ? fileArgs : [...manifest.artifacts.map(a => a.path), 'provenance/CLAIMS.md'];
let open = 0, dispositioned = 0;
const activeKeys = new Set();
const newTriage = {};
for (const f of files) {
  const lines = fs.readFileSync(f, 'utf8').split('\n');
  const allowed = new Array(lines.length).fill(false);
  let inBox = false;
  lines.forEach((line, i) => {
    if (/RETRACTED|【履歴】/.test(line) && /^\s*>/.test(line)) inBox = true;
    if (inBox && !/^\s*>/.test(line) && line.trim() !== '') inBox = false;
    if (inBox || /~~[^~]+~~/.test(line) || /^\|\s*\*\*[A-Z]+\d+/.test(line)) allowed[i] = true;
  });
  const hits = [];
  lines.forEach((line, i) => {
    if (allowed[i]) return;
    for (const t of TOKENS) if (t.re.test(line)) hits.push({ line: i + 1, token: t.id, text: line.slice(0, 110), fp: lineHash(line) });
  });
  if (hits.length) console.log(`## ${f}: ${hits.length} hit(s)`);
  for (const h of hits) {
    const key = `${f}::${h.fp}::${h.token}`;
    activeKeys.add(key);
    const d = triage[key];
    const dispOk = d && d.disposition && DISPOSITION_ENUM.some(e => String(d.disposition).startsWith(e)) && d.reviewer && String(d.reviewer).trim() !== '';
    if (dispOk) { dispositioned++; console.log(`  L${h.line} [${h.token}] (triaged) ${h.text.slice(0, 60)}`); }
    else { open++; console.log(`  L${h.line} [${h.token}] OPEN ${h.text}`); if (writeTriage && !d) newTriage[key] = { file: f, line: h.line, token: h.token, text: h.text, disposition: '', reviewer: '' }; }
  }
}

// ③ orphan 検査
let orphans = Object.keys(triage).filter(k => !activeKeys.has(k));
if (orphans.length && pruneOrphans) {
  for (const k of orphans) delete triage[k];
  fs.writeFileSync(TRIAGE_PATH, JSON.stringify(triage, null, 2));
  console.log(`orphan triage ${orphans.length} 件を prune した`);
  orphans = [];
} else if (orphans.length) {
  failures.push(`ORPHAN-TRIAGE: 現 hit に対応しない record ${orphans.length} 件(--prune-orphans で整理)`);
}
if (writeTriage && Object.keys(newTriage).length) {
  fs.writeFileSync(TRIAGE_PATH, JSON.stringify({ ...triage, ...newTriage }, null, 2));
  console.log(`triage 雛形を追記(disposition は enum 接頭辞 ${DISPOSITION_ENUM.join('|')} で記入)`);
}

// ④ receipt
let sourceCommit = 'unknown'; try { sourceCommit = execSync('git rev-parse HEAD').toString().trim(); } catch {}
const verdict = (open === 0 && failures.length === 0) ? 'CLEAN' : 'BLOCKED';
fs.writeFileSync(RECEIPT_PATH, JSON.stringify({
  schema: 'preflight-receipt/v1', event_id: manifest.event_id, source_commit: sourceCommit,
  lint_version: 'v3', artifacts: artifactReceipts, claims: claimsReceipts,
  certificate_ok: certOk, hits: { open, triaged: dispositioned, orphans: orphans.length },
  failures, verdict, generated_note: 'timestamp は commit が持つ(スクリプトは時刻を打刻しない)',
}, null, 2));

for (const f of failures) console.log('FAIL:', f);
console.log(verdict === 'CLEAN' ? `PREFLIGHT_LINT_CLEAN(open 0 / triaged ${dispositioned} / orphans 0)` : `PREFLIGHT_BLOCKED: open ${open}・manifest/claims/cert failures ${failures.length}・orphans ${orphans.length}`);
process.exit(verdict === 'CLEAN' ? 0 : 1);
