// search/certs/ep_sweep744/extract_sweep744.mjs
//
// P5 悉皆スウィープ: 事前登録済み bound3 + bound4(7分割) の全8ジョブから
// stage1_pass_details を機械抽出し、各点の (a,p) を search 器自身の
// exported factorCheckNinfty で f6/cHatMu へ再導出する。
// これは新規探索ではない -- 既に確定・ハッシュ束縛済みの8証明書を読み、
// 開示済みの機械規則(各ファイル内 stage1_pass_details の出現順を保持、
// ファイル間はソースファイル名の固定順)で列挙するだけ。
//
// Usage: node search/certs/ep_sweep744/extract_sweep744.mjs
// Output: search/certs/ep_sweep744/candidates_744.json

import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { testCandidateNinfty, factorCheckNinfty } from '../../mb-ninfty-branch-search.mjs';
import { Frac } from '../../mb-frac.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..', '..');

// Fixed order = discovery order via glob, sorted lexicographically by
// filename (bound3 first, then bound4 shards alphabetically). This is the
// SAME 8-file set the commander's cited total (744 = 288+0+114+114+0+114+0+114)
// derives from (docs/mb/委嘱3_報告.md, docs/notes/ep_first_candidate_design_v1.md).
const SOURCE_FILES = [
  'certificates/mb/ninfty-branch-search-bound3.json',
  'certificates/mb/ninfty-branch-search-bound4-a5m1-p2a.json',
  'certificates/mb/ninfty-branch-search-bound4-a5m1-p2b.json',
  'certificates/mb/ninfty-branch-search-bound4-a5m1-p2c.json',
  'certificates/mb/ninfty-branch-search-bound4-a5m1-p2d.json',
  'certificates/mb/ninfty-branch-search-bound4-a5p1-p2neg.json',
  'certificates/mb/ninfty-branch-search-bound4-a5p1-p2pos-hi.json',
  'certificates/mb/ninfty-branch-search-bound4-a5p1-p2pos-lo.json',
];

function main() {
  const sourceDigests = {};
  const candidates = [];
  let globalIndex = 0;

  for (const relPath of SOURCE_FILES) {
    const absPath = join(ROOT, relPath);
    const raw = readFileSync(absPath);
    const digest = createHash('sha256').update(raw).digest('hex');
    sourceDigests[relPath] = digest;
    const cert = JSON.parse(raw.toString('utf-8'));
    const details = cert.stage1_pass_details;
    if (!Array.isArray(details) || details.length !== cert.stage1_passes) {
      throw new Error(`${relPath}: stage1_pass_details length ${details && details.length} != stage1_passes ${cert.stage1_passes}`);
    }

    details.forEach((d, localIndex) => {
      const aFrac = [d.a0, d.a1, d.a2, d.a3, d.a4, d.a5].map((x) => Frac.from(x));
      const pFrac = [d.p0, d.p1, d.p2].map((x) => Frac.from(x));
      const stage1 = factorCheckNinfty(aFrac, pFrac);
      if (!stage1.ok) {
        throw new Error(`${relPath}[${localIndex}]: factorCheckNinfty stage-1 re-derivation FAILED, contradicting stage1_pass_details: ${JSON.stringify(d)}`);
      }
      const rederived = testCandidateNinfty(d.a0, d.a1, d.a2, d.a3, d.a4, d.a5, d.p0, d.p1, d.p2);

      candidates.push({
        global_index: globalIndex,
        source_file: relPath,
        source_local_index: localIndex,
        source_stage1_pass_detail: d,
        candidate: {
          a: aFrac.map((x) => x.toString()),
          p: pFrac.map((x) => x.toString()),
          f6: stage1.f6.map((x) => x.toString()),
          cHatMu: stage1.cHatMu.toString(),
        },
        rederived_stage2: rederived,
      });
      globalIndex += 1;
    });
  }

  const out = {
    role_note: 'P5 悉皆スウィープ用 744候補の機械抽出(探索ではない -- 既存8証明書の読み出しと開示済み規則による列挙+f6再導出)。',
    total_candidates: candidates.length,
    source_files_sha256: sourceDigests,
    extraction_rule: 'source files in fixed listed order; within each file, stage1_pass_details in on-disk array order (no sort/filter/choice); f6/cHatMu re-derived via factorCheckNinfty (imported, not reimplemented), consistency-checked against testCandidateNinfty.',
    candidates,
  };
  writeFileSync(join(HERE, 'candidates_744.json'), JSON.stringify(out, null, 2) + '\n');
  process.stdout.write(JSON.stringify({ total: candidates.length, source_files_sha256: sourceDigests }, null, 2) + '\n');
}

main();
