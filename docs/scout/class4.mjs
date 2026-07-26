// Free nilpotent group of class D (D=3 or 4), rank 2, via truncated free algebra
// Z<xi,eta>/(deg > D).  Magnus: x = 1+xi, y = 1+eta.  Exact BigInt arithmetic.
//
// Computes, on A = gamma_2/gamma_{D+1} (abelian for D <= 4, 2-generator):
//   theta, tau, sigma_m = Ad(Y^-m) o tau,  N = 1 + sigma + sigma^2,
//   E_m = X^m Z^m Y^m,
// and decides the E2 criterion   -E_m  in  N( ker(1+theta) )
// over Z and over Z/2^j (= relatively free object with exponent-2^j derived group).

const D = Number(process.argv[2] || 4);

const WORDS = [];
(function gen(s) { WORDS.push(s); if (s.length < D) { gen(s + "0"); gen(s + "1"); } })("");
const ONE = () => ({ "": 1n });
const clean = (A) => { const R = {}; for (const k in A) if (A[k] !== 0n) R[k] = A[k]; return R; };
function mul(A, B) { const R = {};
  for (const a in A) for (const b in B) { if (a.length + b.length > D) continue; const k = a + b; R[k] = (R[k] || 0n) + A[a] * B[b]; }
  return clean(R); }
const sub = (A, B) => { const R = { ...A }; for (const b in B) R[b] = (R[b] || 0n) - B[b]; return clean(R); };
function inv(A) { const u = sub(A, ONE()); let R = ONE(), t = ONE();
  for (let i = 1; i <= D; i++) { t = mul(t, u); R = i % 2 ? sub(R, t) : { ...R, ...(() => { const S = { ...R }; for (const k in t) S[k] = (S[k] || 0n) + t[k]; return S; })() }; }
  return clean(R); }
function pow(A, n) { if (n < 0) return pow(inv(A), -n); let R = ONE(); for (let i = 0; i < n; i++) R = mul(R, A); return R; }
const comm = (a, b) => mul(mul(inv(a), inv(b)), mul(a, b));
const ser = (A) => { const C = clean(A); return WORDS.filter(k => C[k]).map(k => k + ":" + C[k]).join(","); };
const eq = (A, B) => ser(A) === ser(B);

const x = { "": 1n, "0": 1n }, y = { "": 1n, "1": 1n };
const z = inv(mul(x, y));
const w = comm(x, y), p = comm(w, x), q = comm(w, y);
const r1 = comm(p, x), r2 = comm(p, y), r3 = comm(q, y);

// ---- basis of A = gamma_2/gamma_{D+1}, graded by weight -------------------
const GENS = D === 3 ? [["w", w, 2], ["p", p, 3], ["q", q, 3]]
                     : [["w", w, 2], ["p", p, 3], ["q", q, 3], ["r1", r1, 4], ["r2", r2, 4], ["r3", r3, 4]];
const NAMES = GENS.map(g => g[0]), ELS = GENS.map(g => g[1]), WT = GENS.map(g => g[2]);
const dk = (A, k) => WORDS.filter(s => s.length === k).map(s => A[s] || 0n);

function solveInt(cols, target) {   // cols: array of integer vectors; solve sum c_i cols_i = target over Z
  const n = cols.length, L = target.length;
  const M = []; for (let i = 0; i < L; i++) M.push([...cols.map(c => c[i]), target[i]]);
  const sol = new Array(n).fill(0n); const piv = [];
  let r = 0;
  for (let c = 0; c < n && r < L; c++) {
    let pr = -1; for (let i = r; i < L; i++) if (M[i][c] !== 0n) { pr = i; break; }
    if (pr < 0) continue;
    [M[r], M[pr]] = [M[pr], M[r]];
    for (let i = 0; i < L; i++) if (i !== r && M[i][c] !== 0n) {
      const a = M[r][c], b = M[i][c]; const g = ((u, v) => { u = u < 0n ? -u : u; v = v < 0n ? -v : v; while (v) { [u, v] = [v, u % v]; } return u; })(a, b);
      const fa = a / g, fb = b / g;
      for (let j = 0; j <= n; j++) M[i][j] = M[i][j] * fa - M[r][j] * fb;
    }
    piv.push([r, c]); r++;
  }
  for (let i = r; i < L; i++) if (M[i][n] !== 0n) return null;
  for (const [rr, cc] of piv) { if (M[rr][n] % M[rr][cc]) return null; sol[cc] = M[rr][n] / M[rr][cc]; }
  return sol;
}

function normalForm(g) {              // g in gamma_2 -> integer vector in basis GENS
  const out = new Array(GENS.length).fill(0n);
  let h = { ...g };
  for (let k = 2; k <= D; k++) {
    const idx = GENS.map((_, i) => i).filter(i => WT[i] === k);
    if (!idx.length) continue;
    const target = dk(h, k), cols = idx.map(i => dk(ELS[i], k));
    const s = solveInt(cols, target);
    if (s === null) throw new Error("normalForm: weight " + k + " unsolvable");
    idx.forEach((i, j) => out[i] = s[j]);
    for (const i of idx) h = mul(h, pow(ELS[i], Number(-out[i])));
  }
  if (Object.keys(clean(h)).length !== 1) throw new Error("normalForm: residue");
  return out;
}
const vecToEl = (v) => v.reduce((acc, e, i) => mul(acc, pow(ELS[i], Number(e))), ONE());

// ---- sanity: A abelian, basis consistent ---------------------------------
let fails = 0; const T = (n, c, x2 = "") => { console.log(`${c ? "PASS" : "FAIL"}  ${n}${x2 ? "   " + x2 : ""}`); if (!c) fails++; };
console.log(`### free nilpotent class ${D}, rank 2 ; A = gamma_2/gamma_${D + 1}, rank ${GENS.length}`);
let ab = true;
for (const a of ELS) for (const b of ELS) if (!eq(comm(a, b), ONE())) ab = false;
T("A is abelian", ab);
T("round-trip normalForm", ELS.every((e, i) => { const v = normalForm(e); return v.every((c, j) => c === (i === j ? 1n : 0n)); }));

// ---- endomorphism matrices (columns = images of basis) --------------------
const applyAut = (imgs) => {          // imgs: {x:..., y:...} -> matrix of induced map on A
  const IX = imgs.x, IY = imgs.y;
  const W = comm(IX, IY), P = comm(W, IX), Q = comm(W, IY);
  const map = { w: W, p: P, q: Q, r1: comm(P, IX), r2: comm(P, IY), r3: comm(Q, IY) };
  return NAMES.map(n => normalForm(map[n]));   // rows[i] = coords of image of GENS[i]
};
const theta = applyAut({ x: y, y: x });
const tau = applyAut({ x: y, y: z });
const sigmaOf = (m) => {              // sigma(a) = Y^-m tau(a) Y^m
  const cj = (g) => mul(mul(pow(y, -m), g), pow(y, m));
  const IX = cj(y), IY = cj(z);
  return applyAut({ x: IX, y: IY });
};
const J = (M)=>M.map(r=>r.map(String)).join("|");
const matmul = (A, B) => A.map(row => { // row = coords of image; compose: (A then B)
  const out = new Array(GENS.length).fill(0n);
  row.forEach((c, i) => B[i].forEach((v, j) => out[j] += c * v));
  return out; });
const matadd = (...Ms) => Ms[0].map((_, i) => Ms[0][i].map((_, j) => Ms.reduce((s, M) => s + M[i][j], 0n)));
const ID = NAMES.map((_, i) => NAMES.map((_, j) => (i === j ? 1n : 0n)));
const applyVec = (M, v) => { const o = new Array(GENS.length).fill(0n); v.forEach((c, i) => M[i].forEach((x2, j) => o[j] += c * x2)); return o; };

T("theta^2 = id", J(matmul(theta, theta)) === J(ID));
T("tau^3 = id", J(matmul(matmul(tau, tau), tau)) === J(ID));
T("theta(w) = w^-1 exactly", normalForm(comm(y, x)).every((c, i) => c === (i === 0 ? -1n : 0n)));

// ---- the criterion over Z/2^j -------------------------------------------
function analyse(mod, mMax) {   // mod = 0 means over Z/2^j ; we always work mod 2^j here
    const n = GENS.length;
    const MD = BigInt(mod); const red = (v) => v.map(c => ((c % MD) + MD) % MD);
    const results = [];
    for (let m = 0; m <= mMax; m++) {
      const S = sigmaOf(m);
      const N = matadd(ID, S, matmul(S, S));
      const Em = normalForm(mul(mul(pow(x, m), pow(z, m)), pow(y, m)));
      const target = red(Em.map(c => -c));
      // enumerate ker(1+theta) subgroup of (Z/mod)^n, then image under N ; brute force
      const OneTh = matadd(ID, theta);
      const total = Math.pow(mod, n);
      const hits = [];
      for (let code = 0; code < total; code++) {
        let c = code; const v = [];
        for (let i = 0; i < n; i++) { v.push(BigInt(c % mod)); c = Math.floor(c / mod); }
        if (!red(applyVec(OneTh, v)).every(z2 => z2 === 0n)) continue;      // f in ker(1+theta)
        if (red(applyVec(N, v)).every((z2, i) => z2 === target[i])) hits.push(v);
      }
      results.push({ m, solvable: hits.length > 0, count: hits.length, Em: Em.map(Number), witness: hits[0] ? hits[0].map(Number) : null });
    }
    return results;
}

for (const j of [1, 2, 3]) {
  const mod = 2 ** j;
  if (GENS.length * j > 12) { console.log(`\n--- A = (Z/${mod})^${GENS.length} : skipped (too large) ---`); continue; }
  console.log(`\n--- relatively free object: A = (Z/${mod})^${GENS.length}  (exponent ${mod} derived group) ---`);
  const R = analyse(mod, 2 * mod - 1);
  const bad = R.filter(r => !r.solvable);
  for (const r of R) console.log(`  m=${r.m}: ${r.solvable ? "SOLVABLE  n_tor=" + r.count + "  f=" + (r.witness?"["+r.witness+"]":"-") : "*** MISSING ***"}   E_m=${("["+r.Em+"]")}`);
  console.log(`  => ${bad.length === 0 ? "m-full (torsion part) for all m tested" : "MISSING at m = " + bad.map(r => r.m).join(",")}`);
}

// ---- the closed identity 3*(-E_m) = T_m * kappa_m  (class 3 only) --------
if (D === 3) {
  console.log("\n--- identity check: E_m^-3 = kappa_m^{T_m},  T_m = m(m+1)/2 ---");
  for (let m = 0; m <= 8; m++) {
    const S = sigmaOf(m), N = matadd(ID, S, matmul(S, S));
    const kap = applyVec(N, [1n, 0n, 0n]);
    const Em = normalForm(mul(mul(pow(x, m), pow(z, m)), pow(y, m)));
    const T_m = BigInt(m * (m + 1) / 2);
    const lhs = Em.map(c => -3n * c), rhs = kap.map(c => T_m * c);
    T(`m=${m}: -3E_m = T_m*kappa_m`, lhs.every((c, i) => c === rhs[i]), `-3E=${lhs} T*k=${rhs}`);
  }
}
console.log(`\n${fails === 0 ? "ALL STRUCTURAL CHECKS PASSED" : fails + " FAILURES"}`);
