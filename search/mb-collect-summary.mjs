// mb-collect-summary.mjs — GitHub Actions job "collect" 用の summary.json 生成。
// 集めた証明書ディレクトリ(各 shard の <id>.json/.err/.provenance.json)と
// plan ファイルを突合し、per-shard 成否を機械的に要約する。
// 探索器の判定ロジックには一切触れない(ファイルの存在・exit_code・
// 証明書内 integrity_flag の読み出しのみ)。
//
// usage: node search/mb-collect-summary.mjs <certs-dir> <plan.json>

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

function readJsonSafe(path) {
  try {
    return { ok: true, value: JSON.parse(readFileSync(path, 'utf8')) };
  } catch (e) {
    return { ok: false, error: String(e && e.message || e) };
  }
}

function main() {
  const certsDir = process.argv[2];
  const planPath = process.argv[3];
  if (!certsDir || !planPath) {
    console.error('usage: node mb-collect-summary.mjs <certs-dir> <plan.json>');
    process.exitCode = 1;
    return;
  }
  const plan = JSON.parse(readFileSync(planPath, 'utf8'));

  const shardSummaries = plan.shards.map(shard => {
    const id = shard.shard_id;
    const certPath = join(certsDir, `${id}.json`);
    const errPath = join(certsDir, `${id}.err`);
    const provPath = join(certsDir, `${id}.provenance.json`);

    const certExists = existsSync(certPath);
    const errExists = existsSync(errPath);
    const provExists = existsSync(provPath);

    let exitCode = null;
    let elapsedMs = null;
    let runId = null;
    if (provExists) {
      const prov = readJsonSafe(provPath);
      if (prov.ok) {
        exitCode = prov.value.exit_code ?? null;
        elapsedMs = prov.value.elapsed_ms ?? null;
        runId = prov.value.run_id ?? null;
      }
    }

    let certParsed = null;
    let certIntegrityFlag = null;
    if (certExists) {
      const cert = readJsonSafe(certPath);
      if (cert.ok) {
        certParsed = true;
        certIntegrityFlag = cert.value.integrity_flag ?? null;
      } else {
        certParsed = false;
      }
    }

    const errSize = errExists ? readFileSync(errPath, 'utf8').length : 0;

    // success 判定: sidecar provenance の exit_code が '0' 文字列(または数値0)
    // であり、証明書が JSON として parse できること。exit_code!=0 や
    // parse 失敗はここでは「失敗」として記録するのみ(判定ロジックの
    // 変更や再解釈は一切しない)。
    const exitCodeStr = String(exitCode);
    const success = certExists && certParsed === true && (exitCodeStr === '0');

    return {
      shard_id: id,
      script: shard.script,
      cert_exists: certExists,
      cert_parsed: certParsed,
      cert_integrity_flag: certIntegrityFlag,
      err_exists: errExists,
      err_size_bytes: errSize,
      exit_code: exitCode,
      elapsed_ms: elapsedMs,
      run_id: runId,
      success,
    };
  });

  const summary = {
    schema: 'mb/actions-collect-summary/v1',
    plan_frozen_commit: plan.frozen_commit,
    shard_count: plan.shards.length,
    shards: shardSummaries,
    all_success: shardSummaries.every(s => s.success),
    success_count: shardSummaries.filter(s => s.success).length,
    failure_count: shardSummaries.filter(s => !s.success).length,
  };

  console.log(JSON.stringify(summary, null, 2));
}

main();
