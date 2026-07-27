// version-event preflight lint v4(便 53 F5/F6/F9 反映・裁定 64)
// v4 の変更(v3 比):
//  ① version は regex 含有でなく typed parser: header 1 行目から /v\d+(\.\d+)*/ を 1 個 parse し
//     manifest.input_version と文字列 equality(F9.1)。二版を許す regex は廃止。
//  ② manifest 拡張: checker(path+sha256+期待件数を実走で assert)・certificate
//     (pass/fail/fail_closed+script/node digest)・CLAIMS 必須 token。
//  ③ worktree-clean 検査: 対象 path 群が未 commit 変更を持てば BLOCKED(receipt path は除外)。
//  ④ 二段 receipt(F9.2): commit C(clean payload)上で走らせ、source_commit=C・source_tree・
//     全 digest・checker 観測値を receipt に記録。receipt は後続 commit R に入れる。
//  ⑤ --selftest: 三 mutant(版不一致・stale 手続き token・certificate 改変)が全て BLOCKED に
//     なることを自己回帰として検査(F9.3)。
//  ⑥ scope token 追加(F9.4):「窓にも…依らない」を独立 token 化。
// 使い方: node search/version-event-preflight-lint.mjs [--triage] [--prune-orphans] [--selftest]
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
  { id: 're-fusion-modM',    re: /単位[^\n]{0,12}\\?varepsilon[^\n]{0,12}の\s*mod\s*\d+\s*還元|\\varepsilon[^\n]{0,8}の\s*\\?bmod\s*M\s*還元が/ },
  { id: 'window-independent', re: /窓にも[^\n]{0,14}依らな/ },
  { id: 'unconditional',     re: /無条件(?![^\n]{0,60}(root-link-free|ではなく|ではない|と書いた|と呼んだ|と呼んでよいのは))/ },
];

const lineHash = s => crypto.createHash('sha1').update(s.replace(/\s+/g, ' ').trim()).digest('hex').slice(0, 16);
const sha256buf = b => crypto.createHash('sha256').update(b).digest('hex');
const sha256file = f => sha256buf(fs.readFileSync(f));
const parseVersion = header => { const m = header.match(/v\d+(?:\.\d+)*/); return m ? m[0] : null; };

// ---- 検査本体(content map に対して走る — selftest の mutant 適用を可能にする) ----
function runChecks(manifest, readFileText, readCertJson) {
  const failures = [];
  const artifacts = [];
  for (const a of manifest.artifacts) {
    const text = readFileText(a.path);
    const parsed = parseVersion(text.split('\n')[0]);
    const ok = parsed === a.input_version;
    if (!ok) failures.push(`VERSION-IDENTITY: ${a.path} parsed=${parsed} != manifest.input_version=${a.input_version}`);
    artifacts.push({ path: a.path, parsed_version: parsed, input_version: a.input_version, header_ok: ok });
    for (const tok of a.stale_tokens || []) {
      if (text.includes(tok)) failures.push(`STALE-TOKEN: ${a.path} に「${tok}」が live 残存`);
    }
  }
  const claimsText = readFileText('provenance/CLAIMS.md');
  const claims = [];
  for (const c of manifest.claims) {
    const row = claimsText.split('\n').find(l => l.startsWith(`| ${c.row_id} |`)) || '';
    const missing = c.must_contain.filter(t => !row.includes(t));
    if (missing.length) failures.push(`CLAIMS-SYNC: ${c.row_id} 欠落: ${missing.join(' / ')}`);
    claims.push({ row_id: c.row_id, ok: missing.length === 0, row_hash: lineHash(row) });
  }
  const cert = readCertJson(manifest.certificate.path);
  const cp = manifest.certificate;
  const certChecks = [
    [cert.provenance?.input_doc_path === cp.input_doc_path, 'input_doc_path'],
    [cert.pass_count === cp.expected_pass, `pass_count=${cert.pass_count}(期待 ${cp.expected_pass})`],
    [cert.fail_count === 0, `fail_count=${cert.fail_count}`],
    [cert.fail_closed === true, 'fail_closed'],
    [!cp.script_sha256 || cert.provenance?.script_sha256 === cp.script_sha256, 'script_sha256'],
    [!cp.node_counterpart_sha256 || cert.provenance?.node_counterpart_sha256 === cp.node_counterpart_sha256, 'node_counterpart_sha256'],
  ];
  for (const [ok, label] of certChecks) if (!ok) failures.push(`CERT: ${label} 不一致`);
  // input_doc_sha256 は現物 BFC と一致するか
  const bfc = manifest.artifacts.find(a => a.path === cp.input_doc_path);
  if (bfc && cert.provenance?.input_doc_sha256 !== sha256buf(Buffer.from(readFileText(cp.input_doc_path)))) {
    failures.push('CERT-BINDING: input_doc_sha256 が現物と不一致(再束縛が必要)');
  }
  return { failures, artifacts, claims, cert };
}

// ---- selftest(F9.3 の三 mutant) ----
function selftest(manifest) {
  const base = p => fs.readFileSync(p, 'utf8');
  const certBase = p => JSON.parse(fs.readFileSync(p, 'utf8'));
  const mutants = [
    { name: 'M1 版不一致(header を別版へ)', text: (p, s) => p === manifest.artifacts[0].path ? s.replace(manifest.artifacts[0].input_version, 'v9.9') : s, cert: c => c },
    { name: 'M2 stale 手続き token 注入', text: (p, s) => p === manifest.artifacts[1].path ? s + '\n本草案 v6 を差分ゲートに回す。' : s, cert: c => c },
    { name: 'M3 certificate pass_count 改変', text: (p, s) => s, cert: c => ({ ...c, pass_count: c.pass_count - 1 }) },
  ];
  let ok = true;
  for (const m of mutants) {
    const r = runChecks(manifest, p => m.text(p, base(p)), p => m.cert(certBase(p)));
    const blocked = r.failures.length > 0;
    console.log(`  selftest ${m.name}: ${blocked ? 'BLOCKED(期待どおり)' : '素通り(FAIL)'}`);
    if (!blocked) ok = false;
  }
  return ok;
}

// ---- main ----
const argv = process.argv.slice(2);
const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));

if (argv.includes('--selftest')) {
  const ok = selftest(manifest);
  console.log(ok ? 'SELFTEST_PASS(3 mutant 全 BLOCKED)' : 'SELFTEST_FAIL');
  process.exit(ok ? 0 : 1);
}

let failures = [];
// ③ worktree-clean(対象 path 群のみ・receipt は除外)
const guarded = [...manifest.artifacts.map(a => a.path), 'provenance/CLAIMS.md', manifest.certificate.path, ...(manifest.checkers || []).map(c => c.path), MANIFEST_PATH, TRIAGE_PATH, 'search/version-event-preflight-lint.mjs'];
try {
  const dirty = execSync('git status --porcelain').toString().split('\n').filter(Boolean)
    .map(l => l.slice(3).replace(/"/g, '')).filter(p => guarded.includes(p));
  if (dirty.length) failures.push(`WORKTREE-DIRTY: 対象 path に未 commit 変更: ${dirty.join(', ')}`);
} catch {}

// ①② manifest 照合
const core = runChecks(manifest, p => fs.readFileSync(p, 'utf8'), p => JSON.parse(fs.readFileSync(p, 'utf8')));
failures.push(...core.failures);

// checker 実走 assert
const checkerReceipts = [];
for (const c of manifest.checkers || []) {
  let out = ''; try { out = execSync(`node ${c.path}`, { encoding: 'utf8' }); } catch (e) { out = String(e.stdout || '') + String(e.stderr || ''); }
  const m = out.match(/=== (\d+)\/(\d+) PASS ===/);
  const observed = m ? `${m[1]}/${m[2]}` : 'no-match';
  const ok = observed === c.expected && (!c.sha256 || sha256file(c.path) === c.sha256);
  if (!ok) failures.push(`CHECKER: ${c.path} observed=${observed}(期待 ${c.expected})/digest ${c.sha256 ? '照合' : '未 pin'}`);
  checkerReceipts.push({ path: c.path, sha256: sha256file(c.path), observed, expected: c.expected, ok });
}

// token 走査+triage(v3 と同じ block 型 allowlist)
let triage = {}; try { triage = JSON.parse(fs.readFileSync(TRIAGE_PATH, 'utf8')); } catch {}
const writeTriage = argv.includes('--triage');
const pruneOrphans = argv.includes('--prune-orphans');
const files = [...manifest.artifacts.map(a => a.path), 'provenance/CLAIMS.md'];
let open = 0, dispositioned = 0;
const activeKeys = new Set(); const newTriage = {};
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
    if (dispOk) { dispositioned++; }
    else { open++; console.log(`  L${h.line} [${h.token}] OPEN ${h.text}`); if (writeTriage && !d) newTriage[key] = { file: f, line: h.line, token: h.token, text: h.text, disposition: '', reviewer: '' }; }
  }
}
let orphans = Object.keys(triage).filter(k => !activeKeys.has(k));
if (orphans.length && pruneOrphans) {
  for (const k of orphans) delete triage[k];
  fs.writeFileSync(TRIAGE_PATH, JSON.stringify(triage, null, 2));
  console.log(`orphan triage ${orphans.length} 件を prune した`); orphans = [];
} else if (orphans.length) failures.push(`ORPHAN-TRIAGE: ${orphans.length} 件`);
if (writeTriage && Object.keys(newTriage).length) {
  fs.writeFileSync(TRIAGE_PATH, JSON.stringify({ ...triage, ...newTriage }, null, 2));
  console.log('triage 雛形を追記');
}

// ④ 二段 receipt(source_commit = 現 HEAD = clean payload commit C)
let sourceCommit = 'unknown', sourceTree = 'unknown';
try { sourceCommit = execSync('git rev-parse HEAD').toString().trim(); sourceTree = execSync('git rev-parse HEAD^{tree}').toString().trim(); } catch {}
const verdict = (open === 0 && failures.length === 0) ? 'CLEAN' : 'BLOCKED';
fs.writeFileSync(RECEIPT_PATH, JSON.stringify({
  schema: 'preflight-receipt/v2', event_id: manifest.event_id,
  source_commit: sourceCommit, source_tree: sourceTree,
  manifest_sha256: sha256file(MANIFEST_PATH), lint_sha256: sha256file('search/version-event-preflight-lint.mjs'),
  triage_sha256: sha256file(TRIAGE_PATH), certificate_sha256: sha256file(manifest.certificate.path),
  artifacts: core.artifacts.map(a => ({ ...a, sha256: sha256file(a.path) })),
  claims: core.claims, checkers: checkerReceipts,
  hits: { open, triaged: dispositioned, orphans: orphans.length },
  ordered_steps: ['worktree-clean', 'version-equality', 'stale-tokens', 'claims-sync', 'certificate-asserts', 'checker-runs', 'token-scan+triage', 'receipt'],
  failures, verdict,
}, null, 2));
for (const f of failures) console.log('FAIL:', f);
console.log(verdict === 'CLEAN' ? `PREFLIGHT_LINT_CLEAN(open 0 / triaged ${dispositioned} / orphans 0)` : `PREFLIGHT_BLOCKED: open ${open}・failures ${failures.length}・orphans ${orphans.length}`);
process.exit(verdict === 'CLEAN' ? 0 : 1);
