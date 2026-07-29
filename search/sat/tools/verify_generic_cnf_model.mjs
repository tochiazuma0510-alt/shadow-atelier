// search/sat/tools/verify_generic_cnf_model.mjs
// Generic, encoding-agnostic DIMACS CNF + SAT-solver model checker.
//
// Purpose (P87-5 item 3 / F87-1.6, sol_reply_87_math14.md): independent
// literal-level cross-check of a kissat model against its own CNF, for
// fixtures where the semantic model checker (search/sat/check_model_n21.mjs)
// does not apply -- e.g. the diameter-only path-graph fixtures
// (tail8_diam20_path21_depthNN.cnf) whose X/D/B variables are declared but
// left unwired (see search/sat/encode_diam20_path21.py comment and the
// N/A stub already recorded in check_model_output.txt for this run).
//
// This tool does NOT know anything about the encoding's variable meaning.
// It only:
//   1. parses the DIMACS "p cnf <nvars> <nclauses>" header and all clauses,
//   2. parses the solver's "v ..." model lines into a total truth
//      assignment over 1..nvars,
//   3. re-evaluates every clause against that assignment.
//
// Inputs are read only from the raw CNF and raw model files already written
// to disk by the SAT run (problem.cnf, model_vlines.txt) -- no GAP source,
// no encoder script, no intermediate result is imported. This keeps it a
// crosscheck/ style independent literal evaluator, not a second copy of the
// search-side pipeline.
//
// Usage:
//   node search/sat/tools/verify_generic_cnf_model.mjs <problem.cnf> <model_vlines.txt>
//
// Output: single JSON object to stdout. Exit code 0 iff unsatisfied_count=0
// and missing_vars=0 and parsed_clauses matches the declared header count.

import { readFileSync } from "node:fs";

const [, , cnfPath, modelPath] = process.argv;
if (!cnfPath || !modelPath) {
  console.error("usage: node verify_generic_cnf_model.mjs <problem.cnf> <model_vlines.txt>");
  process.exit(2);
}

const cnfText = readFileSync(cnfPath, "utf8");
let declaredVars = null, declaredClauses = null;
const clauses = [];
for (const line of cnfText.split(/\r?\n/)) {
  const t = line.trim();
  if (t.length === 0) continue;
  if (t.startsWith("c")) continue;
  if (t.startsWith("p")) {
    const parts = t.split(/\s+/);
    declaredVars = Number(parts[2]);
    declaredClauses = Number(parts[3]);
    continue;
  }
  const lits = t.split(/\s+/).filter(s => s.length > 0).map(Number);
  if (lits.length === 0) continue;
  if (lits[lits.length - 1] !== 0) {
    throw new Error("clause line not zero-terminated: " + t);
  }
  lits.pop();
  clauses.push(lits);
}

const modelText = readFileSync(modelPath, "utf8");
// assign[v] = true/false/undefined (unassigned)
const assign = new Array(declaredVars + 1).fill(undefined);
let sawTerminatingZero = false;
for (const line of modelText.split(/\r?\n/)) {
  const t = line.trim();
  if (t.length === 0) continue;
  if (!t.startsWith("v")) continue;
  const toks = t.slice(1).trim().split(/\s+/).filter(s => s.length > 0).map(Number);
  for (const lit of toks) {
    if (lit === 0) { sawTerminatingZero = true; continue; }
    const v = Math.abs(lit);
    assign[v] = lit > 0;
  }
}

let missingVars = 0;
for (let v = 1; v <= declaredVars; v++) {
  if (assign[v] === undefined) missingVars++;
}

let unsatisfiedCount = 0;
const unsatisfiedSample = [];
for (const lits of clauses) {
  let sat = false;
  for (const lit of lits) {
    const v = Math.abs(lit);
    const val = assign[v];
    if (val === undefined) continue; // treated as unassigned, cannot satisfy via this literal
    if ((lit > 0 && val === true) || (lit < 0 && val === false)) { sat = true; break; }
  }
  if (!sat) {
    unsatisfiedCount++;
    if (unsatisfiedSample.length < 10) unsatisfiedSample.push(lits);
  }
}

const assignedCount = declaredVars - missingVars;

const result = {
  tool: "search/sat/tools/verify_generic_cnf_model.mjs",
  cnf_path: cnfPath,
  model_path: modelPath,
  nvars: declaredVars,
  declared_clauses: declaredClauses,
  parsed_clauses: clauses.length,
  assigned: assignedCount,
  missing_vars: missingVars,
  model_had_terminating_zero: sawTerminatingZero,
  unsatisfied_count: unsatisfiedCount,
  unsatisfied_sample: unsatisfiedSample
};
console.log(JSON.stringify(result, null, 2));
process.exit(
  unsatisfiedCount === 0 && missingVars === 0 && clauses.length === declaredClauses
    ? 0
    : 1
);
