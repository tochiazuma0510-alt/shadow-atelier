#!/usr/bin/env node
// search/patch-target-hash.mjs -- pure infra utility (NOT part of crosscheck/): computes
// target_hash = SHA-256(canonical JSON of target_definition) per manifest_spec_v1.md sec.0
// canonicalization rule (gtsh-canon/v1: UTF-8, sorted keys, no whitespace, decimal ints).
// This performs no group-theoretic checking and is not the independent照合器 -- it is a
// deterministic hashing step applied to whatever target_definition object the GAP explorer
// wrote into the certificate file. Usage:
//   node search/patch-target-hash.mjs <certificate-path.json>
'use strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value !== null && typeof value === 'object') {
    const out = {};
    for (const k of Object.keys(value).sort()) out[k] = canonicalize(value[k]);
    return out;
  }
  return value;
}

function canonicalJson(value) {
  return JSON.stringify(canonicalize(value));
}

const path = process.argv[2];
if (!path) { console.error('usage: node search/patch-target-hash.mjs <cert-path>'); process.exit(1); }

const raw = readFileSync(path, 'utf8');
const cert = JSON.parse(raw);
if (!cert.target_definition) { console.error('cert has no target_definition field:', path); process.exit(1); }

const canon = canonicalJson(cert.target_definition);
const hash = createHash('sha256').update(canon, 'utf8').digest('hex');
cert.target_hash = hash;

writeFileSync(path, JSON.stringify(cert));
console.log('canonical target_definition:', canon);
console.log('target_hash (sha256):', hash);
console.log('patched:', path);
