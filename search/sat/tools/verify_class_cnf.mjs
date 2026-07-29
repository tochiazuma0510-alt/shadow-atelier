// scratchpad/verify_class_cnf.mjs -- ad hoc cross-check, NOT a deliverable.
// Reads the actual DIMACS file written by encode_tail8_n21.py and checks
// every clause is satisfied by the assignment built from the GAP witness
// fixture, using the independent variable-id functions already defined in
// search/sat/check_model_n21.mjs (imported here only for its exported
// helper id functions -- not for any encoding logic).
import { readFileSync } from "node:fs";

const N = 21;
function buildU() {
  const u = new Map();
  for (let i = 1; i <= 12; i++) u.set(i, i + 1);
  u.set(13, 1);
  for (const [a, b] of [[14, 15], [16, 17], [18, 19], [20, 21]]) { u.set(a,b); u.set(b,a); }
  return u;
}
const U = buildU();
const PAIRS = [];
for (let i = 1; i <= N; i++) for (let j = i+1; j <= N; j++) PAIRS.push([i,j]);
const PAIR_IDX = new Map();
PAIRS.forEach(([i,j],k)=>PAIR_IDX.set(`${i},${j}`,k+1));
const X_BASE=0, X_COUNT=PAIRS.length;
function Xvar(i,j){ if(i>j)[i,j]=[j,i]; return X_BASE+PAIR_IDX.get(`${i},${j}`); }
const D_BASE=X_BASE+X_COUNT, D_COUNT=N;
function Dvar(i){ return D_BASE+i; }
const B_BASE=D_BASE+D_COUNT, B_COUNT=N*N;
function Bvar(i,k){ return B_BASE+(i-1)*N+k; }
const CLASS_VAR_COUNT = B_BASE+B_COUNT;

const fixture = JSON.parse(readFileSync("search/sat/fixtures/witness_n21_nontransitive.json","utf8"));
const aImg = fixture.a_images_1indexed;
const bImg = fixture.b_images_1indexed;

const assign = new Array(CLASS_VAR_COUNT+1).fill(false);
for (let i=1;i<=N;i++){
  const ai=aImg[i-1];
  if (ai===i) assign[Dvar(i)] = true; else assign[Xvar(i,ai)] = true;
}
for (let i=1;i<=N;i++){
  assign[Bvar(i,bImg[i-1])] = true;
}

const text = readFileSync("search/sat/out/tail8_n21_class.cnf","utf8");
let nvars=0, nclauses=0;
let violated = 0;
let checked = 0;
for (const line of text.split(/\r?\n/)) {
  const t = line.trim();
  if (t.length===0) continue;
  if (t.startsWith("c")) continue;
  if (t.startsWith("p")) {
    const parts = t.split(/\s+/);
    nvars = Number(parts[2]); nclauses = Number(parts[3]);
    continue;
  }
  const lits = t.split(/\s+/).map(Number);
  if (lits[lits.length-1] !== 0) throw new Error("clause not zero-terminated: "+t);
  lits.pop();
  let sat = false;
  for (const lit of lits) {
    const v = Math.abs(lit);
    const val = assign[v];
    if ((lit>0 && val) || (lit<0 && !val)) { sat = true; break; }
  }
  checked++;
  if (!sat) violated++;
}
console.log(JSON.stringify({nvars, nclauses, clauses_checked: checked, violated}, null, 2));
process.exit(violated===0 ? 0 : 1);
