// crosscheck/agree-tables.mjs
// E2 sakuyou-hyou (action table) two-system agreement check.
// Input: ONLY crosscheck/agree_claude.json and crosscheck/agree_sol2.json
// (transcriptions of docs/week4-E2作用表_v1.md and sol/sol2_reply_02_actions.md).
// This script does NOT import any GAP output, any search/ helper, or any
// code from the two derivation documents themselves. It only reads the
// two JSON certificates and recomputes independently in BigInt.
//
// NOTE: "cross-checked", NOT "verified" (verified is reserved for Lean).

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const A = JSON.parse(fs.readFileSync(path.join(__dirname, 'agree_claude.json'), 'utf8'));
const B = JSON.parse(fs.readFileSync(path.join(__dirname, 'agree_sol2.json'), 'utf8'));

const BASIS = ["w","p","q","r1","r2","r3","t1","t2","t3","t4","t5","t6"];
const IDX = Object.fromEntries(BASIS.map((b,i)=>[b,i]));
const W=IDX.w, P=IDX.p, Q=IDX.q, T5=IDX.t5, T6=IDX.t6;

let PASS = 0, FAIL = 0;
const fails = [];

function vecEq(u, v) {
  if (u.length !== v.length) return false;
  for (let i=0;i<u.length;i++) if (BigInt(u[i]) !== BigInt(v[i])) return false;
  return true;
}
function check(label, u, v, extra) {
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

// ---- 1. collection table [g,x],[g,y] (12 basis) ----
for (const g of BASIS) {
  for (const gen of ["x","y"]) {
    check(`collection[${g}][${gen}]`, A.collection_table[g][gen], B.collection_table[g][gen]);
  }
}

// ---- 2. theta table (12 basis) ----
for (const g of BASIS) {
  check(`theta(${g})`, A.theta_table[g], B.theta_table[g]);
}

// ---- 3. sigma_m table (12 basis), evaluated at m in {-3..10} ----
function polyEval(coefs, m) {
  const [c0,c1,c2,c3] = coefs.map(BigInt);
  return c0 + c1*BigInt(m) + c2*binom(m,2) + c3*binom(m,3);
}
function sigmaVecAt(sys, g, m) {
  const row = sys.sigma_table_poly[g];
  return BASIS.map(b => polyEval(row[b], m));
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

// ---- 4. E_m closed form (12 coords), evaluated at m in {-3..10} ----
function EmVecAt(sys, m) {
  return BASIS.map(b => {
    const terms = sys.Em_components[b];
    let s = 0n;
    for (const t of terms) s += BigInt(t.coef) * binom(m + t.shift, t.k);
    return s;
  });
}
for (const m of M_RANGE) {
  check(`Em(m=${m})`, EmVecAt(A,m), EmVecAt(B,m), {m});
}

// ---- 5. product / power / inverse / cs formulas: read STRUCTURED coefficients
// independently from each system's own JSON (agree_claude.json / agree_sol2.json),
// not a shared hardcoded rule. If either document's transcribed coefficient differs,
// the two systems' computed vectors will differ and the diff will surface below.
function productAt(sys, a, b) {
  const f = sys.product_formula;
  const out = a.map((x,i)=>BigInt(x)+BigInt(b[i]));
  out[T5] += BigInt(f.t5_coef_ap_bw) * BigInt(a[P]) * BigInt(b[W]);
  out[T6] += BigInt(f.t6_coef_aq_bw) * BigInt(a[Q]) * BigInt(b[W]);
  return out;
}
function powerAt(sys, a, n) {
  const f = sys.power_formula;
  const out = a.map(x=>BigInt(n)*BigInt(x));
  const c = binom(n,2);
  out[T5] += BigInt(f.t5_coef_C2_ap_aw) * c * BigInt(a[P]) * BigInt(a[W]);
  out[T6] += BigInt(f.t6_coef_C2_aq_aw) * c * BigInt(a[Q]) * BigInt(a[W]);
  return out;
}
function inverseAt(sys, a) {
  const f = sys.inverse_formula;
  const out = a.map(x=>-BigInt(x));
  out[T5] += BigInt(f.t5_coef_ap_aw) * BigInt(a[P]) * BigInt(a[W]);
  out[T6] += BigInt(f.t6_coef_aq_aw) * BigInt(a[Q]) * BigInt(a[W]);
  return out;
}
function csAt(sys, u, v) {
  const f = sys.cs_formula;
  const out = new Array(12).fill(0n);
  out[T5] = BigInt(f.t5_coef_up_vw) * BigInt(u[P]) * BigInt(v[W]);
  out[T6] = BigInt(f.t6_coef_uq_vw) * BigInt(u[Q]) * BigInt(v[W]);
  return out;
}

// deterministic test vector list (7 fixed vectors, as instructed)
const TESTVECS = [
  [1,0,0,0,0,0,0,0,0,0,0,0],   // w
  [0,1,0,0,0,0,0,0,0,0,0,0],   // p
  [1,1,0,0,0,0,0,0,0,0,0,0],   // w+p
  [2,-1,3,0,1,0,0,0,0,0,0,0],
  [-1,2,0,1,-1,1,0,0,0,0,0,0],
  [3,3,-2,0,0,1,1,0,0,0,0,0],
  [0,0,1,-1,2,0,0,1,0,0,0,0],
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

// explicit named self-checks quoted by both docs
{
  const w = TESTVECS[0], p = TESTVECS[1];
  check("c_s(w,p)==0", csAt(A,w,p).map(String), ["0","0","0","0","0","0","0","0","0","0","0","0"]);
  check("c_s(p,w)==-t5", csAt(A,p,w).map(String), ["0","0","0","0","0","0","0","0","0","0","-1","0"]);
}

// ---- 6. d_theta, d_sigma closed forms (linear + quadratic in a_w), eval on e_k and test vecs, over m range ----
function dThetaAt(sys, a) {
  const f = sys.d_theta_formula;
  const val = (coefs) => {
    let s = 0n;
    for (const [key, c] of Object.entries(coefs)) {
      const varName = key.replace('a_','');
      s += BigInt(c) * BigInt(a[IDX[varName]]);
    }
    return s;
  };
  return [ val(f.t5_coefs), val(f.t6_coefs) ];
}
function dSigmaAt(sys, a, m) {
  const f = sys.d_sigma_formula;
  const aw = BigInt(a[IDX.w]);
  const c2 = binom(aw,2);
  const val = (coefs) => {
    let s = 0n;
    for (const [key, c] of Object.entries(coefs)) {
      if (key === 'C(a_w,2)') s += BigInt(c) * c2;
      else if (key === 'm*C(a_w,2)') s += BigInt(c) * BigInt(m) * c2;
      else s += BigInt(c) * BigInt(a[IDX[key.replace('a_','')]]);
    }
    return s;
  };
  return [ val(f.t5_coefs), val(f.t6_coefs) ];
}

// basis unit vectors e_k for the first 10 coords (A-bar), plus a spread of composite test vecs
const ABAR = ["w","p","q","r1","r2","r3","t1","t2","t3","t4"];
const EKS = ABAR.map(name => {
  const v = new Array(12).fill(0);
  v[IDX[name]] = 1;
  return v;
});
const DSIGMA_TESTVECS = [
  ...EKS,
  [2,0,0,0,0,0,0,0,0,0,0,0],
  [3,-1,2,0,1,0,0,0,0,0,0,0],
  [-2,1,0,1,-1,1,0,0,0,0,0,0],
  [5,3,-2,0,0,1,1,0,0,0,0,0],
  [4,0,1,-1,2,0,0,1,0,0,0,0],
];

for (const a of EKS) {
  check(`d_theta(e_${ABAR[EKS.indexOf(a)]})`, dThetaAt(A,a).map(String), dThetaAt(B,a).map(String));
}
for (const a of DSIGMA_TESTVECS) {
  for (const m of M_RANGE) {
    check(`d_sigma(${a.join(',')},m=${m})`, dSigmaAt(A,a,m).map(String), dSigmaAt(B,a,m).map(String));
  }
}

// ---- report ----
console.log(`PASS=${PASS} FAIL=${FAIL}`);
if (fails.length) {
  console.log('---- FAILS ----');
  for (const f of fails) console.log(JSON.stringify(f));
}
process.exit(FAIL === 0 ? 0 : 1);
