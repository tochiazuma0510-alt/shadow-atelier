// mb-plan-validate.mjs — search/mb-shard-plan.json の構造検証(JSON schema 検証)。
// GitHub Actions job "plan" の step (a)。探索器の判定ロジックには一切触れない
// (plan ファイル自体の構造チェックのみ)。
//
// usage: node search/mb-plan-validate.mjs <path-to-plan.json>

import { readFileSync } from 'node:fs';

function fail(msg) {
  console.error(`SCHEMA_INVALID: ${msg}`);
  process.exitCode = 1;
}

function isNonEmptyString(v) {
  return typeof v === 'string' && v.length > 0;
}

function validate(plan) {
  const errors = [];
  if (plan.schema !== 'mb/shard-plan/v1') {
    errors.push(`schema must be "mb/shard-plan/v1", got ${JSON.stringify(plan.schema)}`);
  }
  if (!isNonEmptyString(plan.frozen_commit) || plan.frozen_commit.length < 7) {
    errors.push('frozen_commit must be a non-empty string of at least 7 chars');
  }
  for (const [key, label] of [['frozen_docs', 'frozen_docs'], ['searcher_files', 'searcher_files']]) {
    const arr = plan[key];
    if (!Array.isArray(arr) || arr.length === 0) {
      errors.push(`${label} must be a non-empty array`);
      continue;
    }
    arr.forEach((item, i) => {
      if (!item || typeof item !== 'object') { errors.push(`${label}[${i}] must be an object`); return; }
      if (!isNonEmptyString(item.path)) errors.push(`${label}[${i}].path must be a non-empty string`);
      if (!isNonEmptyString(item.sha256) || !/^[0-9a-f]{64}$/i.test(item.sha256)) {
        errors.push(`${label}[${i}].sha256 must be a 64-hex-char string`);
      }
    });
  }
  if (!Array.isArray(plan.shards) || plan.shards.length === 0) {
    errors.push('shards must be a non-empty array');
  } else {
    const seenIds = new Set();
    plan.shards.forEach((s, i) => {
      if (!s || typeof s !== 'object') { errors.push(`shards[${i}] must be an object`); return; }
      if (!isNonEmptyString(s.shard_id) || !/^[A-Za-z0-9_-]+$/.test(s.shard_id)) {
        errors.push(`shards[${i}].shard_id must be a non-empty string of [A-Za-z0-9_-]`);
      } else if (seenIds.has(s.shard_id)) {
        errors.push(`shards[${i}].shard_id "${s.shard_id}" is duplicated`);
      } else {
        seenIds.add(s.shard_id);
      }
      if (!isNonEmptyString(s.script)) errors.push(`shards[${i}].script must be a non-empty string`);
      if (s.env !== undefined && (typeof s.env !== 'object' || Array.isArray(s.env) || s.env === null)) {
        errors.push(`shards[${i}].env must be an object if present`);
      }
      if (s.timeout_minutes !== undefined && !(typeof s.timeout_minutes === 'number' && s.timeout_minutes > 0)) {
        errors.push(`shards[${i}].timeout_minutes must be a positive number if present`);
      }
    });
  }
  return errors;
}

function main() {
  const planPath = process.argv[2];
  if (!planPath) {
    fail('usage: node mb-plan-validate.mjs <path-to-plan.json>');
    return;
  }
  let plan;
  try {
    plan = JSON.parse(readFileSync(planPath, 'utf8'));
  } catch (e) {
    fail(`could not read/parse ${planPath}: ${e.message}`);
    return;
  }
  const errors = validate(plan);
  if (errors.length > 0) {
    for (const e of errors) console.error(`SCHEMA_INVALID: ${e}`);
    process.exitCode = 1;
    return;
  }
  console.log(`SCHEMA_OK: ${planPath} (${plan.shards.length} shard(s))`);
}

main();
