// crosscheck/agree6-tables.mjs
// E2 sakuyou-hyou class-6 (A = gamma2(F2)/gamma7(F2), rank 21) two-system agreement check.
// Input: ONLY crosscheck/agree6_claude.json and crosscheck/agree6_sol2.json
// (transcriptions of docs/week4-E2作用表6_claude_v1.md and sol/sol2_reply_03_actions6.md).
// This script does NOT import any GAP output, any search/ helper, docs/scout/hall6.mjs,
// or code from the two derivation documents themselves. It only reads the two JSON
// certificates and recomputes independently in BigInt.
//
// NOTE: "cross-checked", NOT "verified" (verified is reserved for Lean).

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const A = JSON.parse(fs.readFileSync(path.join(__dirname, 'agree6_claude.json'), 'utf8'));
const B = JSON.parse(fs.readFileSync(path.join(__dirname, 'agree6_sol2.json'), 'utf8'));

const BASIS = ["w","p","q","r1","r2","r3","t1","t2","t3","t4","t5","t6","s1","s2","s3","s4","s5","u1","u2","u3","u4"];
const IDX = Object.fromEntries(BASIS.map((b,i)=>[b,i]));
const N = BASIS.length; // 21
const CCOORDS = ["t5","t6","u1","u2","u3","u4"];

let PASS = 0, FAIL = 0, CELLS = 0;
const fails = [];

function vecEq(u, v) {
  if (u.length !== v.length) return false;
  for (let i=0;i<u.length;i++) if (BigInt(u[i]) !== BigInt(v[i])) return false;
  return true;
}
function check(label, u, v, extra) {
  CELLS += u.length;
  if (vecEq(u,v)) { PASS++; }
  else { FAIL++; fails.push({label, A:u, B:v, extra}); }
}

// exact binomial C(n,k) for integer n (any sign), integer k>=0, via BigInt.
function binom(n, k) {
  n = BigInt(n); k = BigInt(k);
  if (k < 0n) return 0n;
  if (k === 0n) return 1n;
  let num = 1n;
  for (let i=0n;i<k;i++) num *= (n - i);
  let den = 1n;
  for (let i=1n;i<=k;i++) den *= i;
  if (num % den !== 0n) throw new Error(`binom(${n},${k}) not integral: ${num}/${den}`);
  return num / den;
}

function zeroVec() { return new Array(N).fill(0n); }
function rowVec(obj) {
  // fill a 21-vector from a sparse {coord: value} object (missing = 0)
  const v = zeroVec();
  for (const [k, val] of Object.entries(obj)) {
    if (k.startsWith('_')) continue;
    v[IDX[k]] = BigInt(val);
  }
  return v;
}

// ---- 1. collection table [g,x],[g,y] (21 basis) ----
for (const g of BASIS) {
  for (const gen of ["x","y"]) {
    check(`collection[${g}][${gen}]`, A.collection_table[g][gen], B.collection_table[g][gen]);
  }
}

// ---- 2. theta table (21 basis) ----
for (const g of BASIS) {
  check(`theta(${g})`, A.theta_table[g], B.theta_table[g]);
}

// ---- 3. sigma_m table (21 basis), evaluated at m in {-3..10} ----
function polyEval(coefs, m) {
  const c = coefs.map(BigInt);
  let s = 0n;
  for (let i=0;i<c.length;i++) s += c[i]*binom(m,i);
  return s;
}
function sigmaVecAt(sys, g, m) {
  const row = sys.sigma_table_poly[g] || {};
  return BASIS.map(b => polyEval(row[b] || [0,0,0,0,0], m));
}
const M_RANGE = [];
for (let m=-3;m<=10;m++) M_RANGE.push(m);

for (const g of BASIS) {
  for (const m of M_RANGE) {
    const va = sigmaVecAt(A, g, m);
    const vb = sigmaVecAt(B, g, m);
    check(`sigma_${m}(${g})`, va, vb, {m});
  }
}

// ---- 4. E_m closed form (21 coords), evaluated at m in {-3..10} plus extras ----
function EmVecAt(sys, m) {
  return BASIS.map(b => {
    const terms = sys.Em_components[b] || [];
    let s = 0n;
    for (const t of terms) s += BigInt(t.coef) * binom(m + t.shift, t.k);
    return s;
  });
}
const M_RANGE_EM = [...M_RANGE, 17, 31, 63, -12];
for (const m of M_RANGE_EM) {
  check(`Em(m=${m})`, EmVecAt(A,m).map(String), EmVecAt(B,m).map(String), {m});
}

// ---- 5. kappa / product / power / inverse / cs (21-dim, 6-term kappa incl. new u4 term a_q*b_p) ----
function kappaAt(sys, a, b) {
  const out = zeroVec();
  for (const t of sys.kappa_terms.terms) {
    out[IDX[t.out]] += BigInt(t.coef) * BigInt(a[IDX[t.in1]]) * BigInt(b[IDX[t.in2]]);
  }
  return out;
}
function productAt(sys, a, b) {
  const k = kappaAt(sys, a, b);
  return a.map((x,i)=>BigInt(x)+BigInt(b[i])-k[i]);
}
function powerAt(sys, a, n) {
  const k = kappaAt(sys, a, a); // delta(a) = kappa(a,a)
  const c2 = binom(n,2);
  return a.map((x,i)=>BigInt(n)*BigInt(x) - c2*k[i]);
}
function inverseAt(sys, a) {
  const k = kappaAt(sys, a, a);
  return a.map((x,i)=>-BigInt(x) - k[i]);
}
function csAt(sys, u, v) {
  const k = kappaAt(sys, u, v);
  return k.map(x=>-x);
}

// deterministic test vector list (21-dim, fixed - not random)
function ev(name) { const v = zeroVec(); v[IDX[name]] = 1n; return v; }
const TESTVECS = [
  ev('w'), ev('p'), ev('q'), ev('r1'), ev('r2'), ev('r3'),
  [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0].map(BigInt),
  [2,-1,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0].map(BigInt),
  [-1,2,0,1,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0].map(BigInt),
  [3,3,-2,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0].map(BigInt),
  [0,0,1,-1,2,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0].map(BigInt),
  [1,2,-1,0,1,-1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0].map(BigInt),
];

for (let i=0;i<TESTVECS.length;i++) {
  for (let j=0;j<TESTVECS.length;j++) {
    const a = TESTVECS[i], b = TESTVECS[j];
    check(`product(v${i},v${j})`, productAt(A,a,b).map(String), productAt(B,a,b).map(String));
    check(`cs(v${i},v${j})`, csAt(A,a,b).map(String), csAt(B,a,b).map(String));
  }
  for (const n of [-3,-2,-1,0,1,2,3,5,63]) {
    check(`power(v${i},n=${n})`, powerAt(A,TESTVECS[i],n).map(String), powerAt(B,TESTVECS[i],n).map(String));
  }
  check(`inverse(v${i})`, inverseAt(A,TESTVECS[i]).map(String), inverseAt(B,TESTVECS[i]).map(String));
}

// explicit named self-checks quoted by both docs (section 2.4' / 1.2)
{
  const w = ev('w'), p = ev('p'), q = ev('q');
  const zero21 = new Array(21).fill('0');
  check("c_s(w,p)==0", csAt(A,w,p).map(String), zero21);
  const t5only = zeroVec(); t5only[IDX.t5]=-1n;
  check("c_s(p,w)==-t5", csAt(A,p,w).map(String), t5only.map(String));
  const u4only = zeroVec(); u4only[IDX.u4]=-1n;
  check("c_s(q,p)==-u4", csAt(A,q,p).map(String), u4only.map(String));
  const u2only = zeroVec(); u2only[IDX.u2]=-1n;
  check("c_s(r2,w)==-u2", csAt(A,ev('r2'),w).map(String), u2only.map(String));
}

// ---- 6. d_theta, d_sigma closed forms (linear + quadratic terms incl. -a_p*a_q), eval on e_k and test vecs, over m range ----
function termValue(term, a, m) {
  const poly = polyEval(term.mcoef, m);
  let factor = 1n;
  for (const v of term.vars) {
    const mC = v.match(/^C\((.+)\)$/);
    if (mC) {
      const av = BigInt(a[IDX[mC[1]]]);
      factor *= binom(av, 2);
    } else {
      factor *= BigInt(a[IDX[v]]);
    }
  }
  return poly * factor;
}
function dPhiAt(sys, formula, a, m) {
  return CCOORDS.map(c => {
    const terms = formula[c] || [];
    let s = 0n;
    for (const t of terms) s += termValue(t, a, m);
    return s;
  });
}

// basis unit vectors e_k for the 15 bar-A basis, plus composite test vecs (some with nonzero w,p,q
// simultaneously, to exercise the new -a_p*a_q / m*a_w*a_q / C(a_q,2) quadratic terms)
const ABAR = ["w","p","q","r1","r2","r3","t1","t2","t3","t4","s1","s2","s3","s4","s5"];
const EKS = ABAR.map(name => ev(name).map(String).map(Number));
const DPHI_TESTVECS = [
  ...EKS,
  [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [3,-1,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [-2,1,0,1,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [5,3,-2,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [4,0,1,-1,2,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [1,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   // a_p,a_q both nonzero -> exercises -a_p a_q
  [2,-3,5,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0],  // a_w,a_p,a_q all nonzero -> exercises m*a_w*a_q, C(a_q,2)
  [-1,2,-4,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0],
];

for (const a of EKS) {
  check(`d_theta(${ABAR[EKS.indexOf(a)]})`, dPhiAt(A,A.d_theta_formula,a,0).map(String), dPhiAt(B,B.d_theta_formula,a,0).map(String));
}
for (const a of DPHI_TESTVECS) {
  // d_theta is m-independent; still check once per vector
  check(`d_theta(${a.join(',')})`, dPhiAt(A,A.d_theta_formula,a,0).map(String), dPhiAt(B,B.d_theta_formula,a,0).map(String));
  for (const m of M_RANGE) {
    check(`d_sigma(${a.join(',')},m=${m})`, dPhiAt(A,A.d_sigma_formula,a,m).map(String), dPhiAt(B,B.d_sigma_formula,a,m).map(String), {m});
  }
}

// ---- report ----
console.log(`PASS=${PASS} FAIL=${FAIL} (raw scalar cells compared: ${CELLS})`);
if (fails.length) {
  console.log('---- FAILS ----');
  for (const f of fails) console.log(JSON.stringify(f));
}
process.exit(FAIL === 0 ? 0 : 1);
