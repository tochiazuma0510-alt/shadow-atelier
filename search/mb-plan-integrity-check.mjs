// mb-plan-integrity-check.mjs — search/mb-shard-plan.json の integrity gate。
// GitHub Actions job "plan" の step (b)(c)。
//
// (b) frozen_docs: plan 記載の frozen_commit から `git show <commit>:<path>` を
//     取り出し sha256 を計算、plan 記載値と照合する。
// (c) searcher_files: 現在のチェックアウト内容(mb-*.mjs)の sha256 を
//     plan 記載値と照合する(判定ロジックが plan 作成時から変わっていないことの
//     保証。掃引範囲は env で外出しするため .mjs の中身自体は変わらない設計)。
//
// 不一致は INTEGRITY_STOP として即 fail(exit code 1)。
// このスクリプトは探索器の判定ロジックには一切触れない(ファイル内容の
// 再計算・比較のみ)。
//
// usage: node search/mb-plan-integrity-check.mjs <path-to-plan.json>

import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';

function sha256(buf) {
  return createHash('sha256').update(buf).digest('hex');
}

function gitShowSha256(commit, path) {
  const buf = execFileSync('git', ['show', `${commit}:${path}`], { maxBuffer: 1024 * 1024 * 64 });
  return sha256(buf);
}

function fileSha256(path) {
  const buf = readFileSync(path);
  return sha256(buf);
}

function main() {
  const planPath = process.argv[2];
  if (!planPath) {
    console.error('usage: node mb-plan-integrity-check.mjs <path-to-plan.json>');
    process.exitCode = 1;
    return;
  }
  const plan = JSON.parse(readFileSync(planPath, 'utf8'));
  const failures = [];

  // (b) frozen_docs
  for (const { path, sha256: expected } of plan.frozen_docs) {
    let actual;
    try {
      actual = gitShowSha256(plan.frozen_commit, path);
    } catch (e) {
      failures.push(`INTEGRITY_STOP: frozen_docs ${path} at ${plan.frozen_commit}: git show failed (${e.message})`);
      continue;
    }
    if (actual !== expected) {
      failures.push(`INTEGRITY_STOP: frozen_docs ${path} at ${plan.frozen_commit}: sha256 mismatch (expected ${expected}, got ${actual})`);
    } else {
      console.log(`OK (frozen_docs): ${path} @ ${plan.frozen_commit} sha256=${actual}`);
    }
  }

  // (c) searcher_files
  for (const { path, sha256: expected } of plan.searcher_files) {
    let actual;
    try {
      actual = fileSha256(path);
    } catch (e) {
      failures.push(`INTEGRITY_STOP: searcher_files ${path}: could not read (${e.message})`);
      continue;
    }
    if (actual !== expected) {
      failures.push(`INTEGRITY_STOP: searcher_files ${path}: sha256 mismatch (expected ${expected}, got ${actual}) -- 判定ロジックが plan 記載時から変更されている`);
    } else {
      console.log(`OK (searcher_files): ${path} sha256=${actual}`);
    }
  }

  if (failures.length > 0) {
    for (const f of failures) console.error(f);
    process.exitCode = 1;
    return;
  }
  console.log('INTEGRITY_GATE_PASS');
}

main();
