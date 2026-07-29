// scratchpad/verify_transitive_cnf.mjs -- ad hoc cross-check, NOT a
// deliverable. Builds an HONEST full assignment for tail8_n21_transitive.cnf
// from the GAP witness fixture: a,b as before, E/STEP/R computed by a
// straightforward independent BFS (not "lying" to force the goal true).
// Since the fixture is known non-transitive (orbits [6,15]), the honest
// assignment is expected to satisfy every clause EXCEPT the goal unit
// clauses for the 15 unreached points -- i.e. exactly the transitivity
// goal fails and nothing else, which is exactly what should happen if the
// class+BFS wiring is sound. This is a strong non-solver sanity check on
// the n=21 transitive CNF before it ever goes near kissat.
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
const UINV = new Map(); for (const [k,v] of U) UINV.set(v,k);

const PAIRS = [];
for (let i = 1; i <= N; i++) for (let j = i+1; j <= N; j++) PAIRS.push([i,j]);
const PAIR_IDX = new Map();
PAIRS.forEach(([i,j],k)=>PAIR_IDX.set(`${i},${j}`,k+1));
const NUM_PAIRS = PAIRS.length;
const X_BASE=0, X_COUNT=NUM_PAIRS;
function Xvar(i,j){ if(i>j)[i,j]=[j,i]; return X_BASE+PAIR_IDX.get(`${i},${j}`); }
const D_BASE=X_BASE+X_COUNT, D_COUNT=N;
function Dvar(i){ return D_BASE+i; }
const B_BASE=D_BASE+D_COUNT, B_COUNT=N*N;
function Bvar(i,k){ return B_BASE+(i-1)*N+k; }
const CLASS_VAR_COUNT = B_BASE+B_COUNT;
const E_BASE = CLASS_VAR_COUNT, E_COUNT = NUM_PAIRS;
function Evar(i,j){ if(i>j)[i,j]=[j,i]; return E_BASE+PAIR_IDX.get(`${i},${j}`); }
const STEP_ORDERED = [];
for (let w=1;w<=N;w++) for (let v=1;v<=N;v++) if (w!==v) STEP_ORDERED.push([w,v]);
const STEP_IDX = new Map(); STEP_ORDERED.forEach(([w,v],k)=>STEP_IDX.set(`${w},${v}`,k+1));
const STEP_PER_T = STEP_ORDERED.length; // 420
const NUM_T = N-1; // 1..20
const STEP_BASE = E_BASE+E_COUNT, STEP_COUNT = NUM_T*STEP_PER_T;
function STEPvar(t,w,v){ return STEP_BASE + (t-1)*STEP_PER_T + STEP_IDX.get(`${w},${v}`); }
const R_BASE = STEP_BASE+STEP_COUNT, R_COUNT = N*N;
function Rvar(t,v){ return R_BASE + t*N + v; } // t=0..20
const TRANS_VAR_COUNT = R_BASE+R_COUNT;

const fixture = JSON.parse(readFileSync("search/sat/fixtures/witness_n21_nontransitive.json","utf8"));
const aImg = fixture.a_images_1indexed;
const bImg = fixture.b_images_1indexed;

const a = new Array(N+1).fill(null);
const b = new Array(N+1).fill(null);
for (let i=1;i<=N;i++){ a[i]=aImg[i-1]; b[i]=bImg[i-1]; }

const assign = new Array(TRANS_VAR_COUNT+1).fill(false);
for (let i=1;i<=N;i++){
  const ai=a[i];
  if (ai===i) assign[Dvar(i)] = true; else assign[Xvar(i,ai)] = true;
}
for (let i=1;i<=N;i++){
  assign[Bvar(i,b[i])] = true;
}
// E: honest adjacency from a and b (a-edge, b-edge, b^-1-edge)
const bInv = new Array(N+1).fill(null);
for (let i=1;i<=N;i++) bInv[b[i]] = i;
for (const [i,j] of PAIRS) {
  const adj = (a[i]===j) || (b[i]===j) || (b[j]===i);
  if (adj) assign[Evar(i,j)] = true;
}
// R: honest BFS distances (cap at 20) from point 1 using generators {a,b,bInv}
const dist = new Array(N+1).fill(Infinity);
dist[1]=0;
const queue=[1];
while(queue.length){
  const v=queue.shift();
  for (const g of [a,b,bInv]) {
    const w=g[v];
    if (dist[w]===Infinity){ dist[w]=dist[v]+1; queue.push(w); }
  }
}
for (let t=0;t<=N-1;t++){
  for (let v=1;v<=N;v++){
    if (dist[v] <= t) assign[Rvar(t,v)] = true;
  }
}
// STEP: honest definition STEP[t][w][v] = E[w,v] & R[t-1][w]
for (let t=1;t<=NUM_T;t++){
  for (const [w,v] of STEP_ORDERED){
    const val = assign[Evar(w,v)] && assign[Rvar(t-1,w)];
    if (val) assign[STEPvar(t,w,v)] = true;
  }
}

const text = readFileSync("search/sat/out/tail8_n21_transitive.cnf","utf8");
let checked=0, violatedLines=[];
let lineNo = 0;
for (const line of text.split(/\r?\n/)) {
  const t = line.trim();
  if (t.length===0) continue;
  if (t.startsWith("c")) continue;
  if (t.startsWith("p")) continue;
  lineNo++;
  const lits = t.split(/\s+/).map(Number);
  lits.pop(); // trailing 0
  let sat = false;
  for (const lit of lits) {
    const v = Math.abs(lit);
    const val = assign[v];
    if ((lit>0 && val) || (lit<0 && !val)) { sat = true; break; }
  }
  checked++;
  if (!sat) violatedLines.push(lineNo);
}
const unreached = [];
for (let v=1; v<=N; v++) if (dist[v] > N-1) unreached.push(v);

console.log(JSON.stringify({
  clauses_checked: checked,
  num_violated: violatedLines.length,
  violated_clause_line_numbers: violatedLines,
  transitivity_goal_clause_range: [50108, 50128], // 1-indexed clause count, matches manifest
  unreached_points_by_bfs_distance: unreached,
  note: "expected: violated clauses are exactly (a subset of) the goal " +
        "unit clauses for genuinely-unreached points, and nothing else -- " +
        "confirms the class+BFS wiring is sound without running a solver."
}, null, 2));
