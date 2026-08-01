// Independent re-implementation (falsifier, CV-9 main checkpoint).
// Permutations on 1..8 as arrays img[1..8].  GAP right-action convention:
//   i^(p*q) = (i^p)^q     =>   (p*q)[i] = q[p[i]]
// Integer-only arithmetic.
const N = 8;
const id = () => { const a = new Array(N + 1); for (let i = 0; i <= N; i++) a[i] = i; return a; };
const cyc = (...cs) => { // cs: array of cycles
  const a = id();
  for (const c of cs) for (let k = 0; k < c.length; k++) a[c[k]] = c[(k + 1) % c.length];
  return a;
};
const mul = (p, q) => { const a = new Array(N + 1); a[0] = 0; for (let i = 1; i <= N; i++) a[i] = q[p[i]]; return a; };
const inv = (p) => { const a = new Array(N + 1); a[0] = 0; for (let i = 1; i <= N; i++) a[p[i]] = i; return a; };
const eq = (p, q) => { for (let i = 1; i <= N; i++) if (p[i] !== q[i]) return false; return true; };
const key = (p) => p.slice(1).join(',');
const pow = (p, e) => { let r = id(); const b = e < 0 ? inv(p) : p; const n = Math.abs(e); for (let i = 0; i < n; i++) r = mul(r, b); return r; };
const conj = (p, g) => mul(mul(inv(g), p), g);   // GAP p^g = g^-1 p g
const ord = (p) => { let k = 1, z = p; while (!eq(z, id())) { z = mul(z, p); k++; } return k; };
const gcd = (a, b) => b ? gcd(b, a % b) : a;
const lcm = (a, b) => a / gcd(a, b) * b;

// ---- window (transcribed from the probe's BLOCK I, arithmetic only) ----
const tt = cyc([1, 2, 3]), aa = cyc([1, 4, 5]);
const XX = mul(aa, inv(tt));
const ss = mul(tt, pow(XX, 3));
const b1 = tt, a1 = ss;
const aE = mul(a1, cyc([6, 8]));
const bE = mul(b1, cyc([6, 8, 7]));
const s1 = mul(inv(bE), aE);
const s2 = mul(aE, pow(bE, 2));
const cc = pow(mul(s1, s2), 3);
const xb = pow(s1, 2), yb = pow(s2, 2);
const kappa = cyc([1, 4], [2, 5]);

// closure of <gens>
function closure(gens) {
  const seen = new Map(); const list = [];
  const push = (p) => { const k = key(p); if (!seen.has(k)) { seen.set(k, list.length); list.push(p); } };
  push(id());
  for (let i = 0; i < list.length; i++) for (const g of gens) push(mul(list[i], g));
  return { list, seen };
}
const PNc = closure([xb, yb]);
const PN = PNc.list;
const Nord = lcm(lcm(ord(xb), ord(yb)), ord(cc));
const charm = []; for (let z = 0; z < Nord; z++) if (gcd(2 * z + 1, Nord) === 1) charm.push(z);
console.log(`|PN|=${PN.length}  Nord=${Nord}  charm=[${charm}]  ord(xb)=${ord(xb)} ord(yb)=${ord(yb)} ord(cc)=${ord(cc)}`);
console.log(`xb^kappa == xb^-1 ? ${eq(conj(xb, kappa), inv(xb))}   yb^kappa == yb^-1 ? ${eq(conj(yb, kappa), inv(yb))}`);

// ---- Hex, exactly as written in the probe (GAP-product-literal) ----
function Hex(m, f) {
  const u = 2 * m + 1;
  const L1 = mul(mul(mul(pow(s1, u), inv(f)), pow(s2, u)), f);
  const R1 = mul(mul(mul(mul(inv(f), s1), s2), pow(xb, -m)), pow(cc, m));
  if (!eq(L1, R1)) return false;
  const L2 = mul(mul(mul(mul(inv(f), pow(s2, u)), f), pow(s1, u)), id());
  const R2 = mul(mul(mul(mul(s2, s1), pow(yb, -m)), pow(cc, m)), f);
  return eq(L2, R2);
}
const shad = [];
for (const m of charm) for (const f of PN) {
  if (Hex(m, f) && closure([xb, conj(yb, f)]).list.length === PN.length) shad.push([m, f]);
}
console.log(`|GT(N_A)| = ${shad.length}`);
const shadKey = new Set(shad.map(([m, f]) => m + '|' + key(f)));

// pre-registered 20 rows from the freeze doc table (independent transcription)
const preReg = [[0, id()], [0, cyc([2, 3, 4])], [0, cyc([1, 2, 3, 4, 5])], [0, cyc([1, 2, 4, 5, 3])], [0, cyc([1, 5, 3])],
[1, cyc([1, 3, 5, 4, 2])], [1, cyc([1, 3, 5, 2, 4])], [1, cyc([1, 4, 3, 2, 5])], [1, cyc([1, 4], [2, 5])], [1, cyc([1, 5, 4, 3, 2])],
[3, cyc([1, 3, 5, 4, 2])], [3, cyc([1, 3, 5, 2, 4])], [3, cyc([1, 4, 3, 2, 5])], [3, cyc([1, 4], [2, 5])], [3, cyc([1, 5, 4, 3, 2])],
[4, id()], [4, cyc([2, 3, 4])], [4, cyc([1, 2, 3, 4, 5])], [4, cyc([1, 2, 4, 5, 3])], [4, cyc([1, 5, 3])]];
const preRegKey = new Set(preReg.map(([m, f]) => m + '|' + key(f)));
console.log(`frozen table == recomputed shad (as sets) : ${preRegKey.size === shadKey.size && [...preRegKey].every(k => shadKey.has(k))}`);

// ---- homomorphism PN->PN given images of xb,yb ; null if not well-defined ----
function homFromImages(imx, imy) {
  const img = new Map(); const q = [id()];
  img.set(key(id()), id());
  for (let i = 0; i < q.length; i++) {
    const e = q[i], ie = img.get(key(e));
    for (const [g, ig] of [[xb, imx], [yb, imy]]) {
      const e2 = mul(e, g), k2 = key(e2), i2 = mul(ie, ig);
      if (img.has(k2)) { if (!eq(img.get(k2), i2)) return null; }
      else { img.set(k2, i2); q.push(e2); }
    }
  }
  if (img.size !== PN.length) return null;
  const F = (p) => img.get(key(p));
  for (const a of PN) for (const b of PN) if (!eq(F(mul(a, b)), mul(F(a), F(b)))) return null; // exhaustive hom test
  return F;
}
// author action E_{m,f} : xb -> xb^u , yb -> (yb^u)^f   [ = f^-1 yb^u f in GAP products ]
const E = (m, f) => homFromImages(pow(xb, 2 * m + 1), conj(pow(yb, 2 * m + 1), f));
// our action Phi'_{m,g} : xb -> xb^u , yb -> g yb^u g^-1
const Pp = (m, g) => homFromImages(pow(xb, 2 * m + 1), mul(mul(g, pow(yb, 2 * m + 1)), inv(g)));
const chat = (z) => conj(z, kappa);          // c-hat = conj_kappa
const tau = (z) => inv(chat(z));             // tau(g) = c-hat(g)^-1
const mpp = (u1, u2) => charm.find(z => ((2 * z + 1) - u1 * u2) % Nord === 0);

console.log(`all 20 E_{m,f} well-defined : ${shad.every(([m, f]) => E(m, f) !== null)}`);
console.log(`tau is an involution on PN  : ${PN.every(z => eq(tau(tau(z)), z))}`);
console.log(`tau is an ANTI-automorphism : ${PN.every(a => PN.every(b => eq(tau(mul(a, b)), mul(tau(b), tau(a)))))}`);

// ---- (V5) lemma DICT (b) :  chat o Phi_{m,f^kappa} = Phi_{m,f} o chat ----
let dictOK = 0, dictTot = 0, dictDefined = 0;
for (const [m, f] of shad) {
  dictTot++;
  const A_ = E(m, conj(f, kappa)), B_ = E(m, f);
  if (A_ === null || B_ === null) continue;
  dictDefined++;
  if (PN.every(z => eq(chat(A_(z)), B_(chat(z))))) dictOK++;
}
console.log(`DICT(b) chat o E_{m,f^kappa} == E_{m,f} o chat : ${dictOK}/${dictDefined} defined (of ${dictTot} rows)`);

// ---- (V2) author-side literal closure  f'' = f1 * E_{m1,f1}(f2)  ----
// ---- (V3) our-side law under the dictionary g = tau(f)              ----
let nPairs = 0, nAuthClosed = 0, nAuthRevClosed = 0, nOurAgree = 0, nOurRevAgree = 0, nOrderMatters = 0;
for (const [m1, f1] of shad) for (const [m2, f2] of shad) {
  nPairs++;
  const u1 = 2 * m1 + 1, u2 = 2 * m2 + 1, m3 = mpp(u1, u2);
  const E1 = E(m1, f1);
  const fpp = mul(f1, E1(f2));            // (A) canon (3.53) order
  const fppRev = mul(E1(f2), f1);         // reversed
  if (shadKey.has(m3 + '|' + key(fpp))) nAuthClosed++;
  if (shadKey.has(m3 + '|' + key(fppRev))) nAuthRevClosed++;
  if (!eq(fpp, fppRev)) nOrderMatters++;
  // our coordinate: g = tau(f)
  const g1 = tau(f1), g2 = tau(f2);
  const P1 = Pp(m1, g1);
  const gpp = mul(P1(g2), g1);            // (B) lemma OPP order
  const gppRev = mul(g1, P1(g2));         // reversed
  if (eq(gpp, tau(fpp))) nOurAgree++;     // <=> (A) and (B) describe the SAME element
  if (eq(gppRev, tau(fpp))) nOurRevAgree++;
}
console.log(`pairs = ${nPairs}`);
console.log(`(A) f''=f1*E1(f2) literally in GT(N_A)          : ${nAuthClosed}/${nPairs}`);
console.log(`(A-rev) E1(f2)*f1 literally in GT(N_A)          : ${nAuthRevClosed}/${nPairs}`);
console.log(`pairs where the two orders differ at all        : ${nOrderMatters}/${nPairs}`);
console.log(`(B) g''=Phi'_1(g2)*g1  ==  tau(f'')             : ${nOurAgree}/${nPairs}`);
console.log(`(B-rev) g1*Phi'_1(g2)  ==  tau(f'')             : ${nOurRevAgree}/${nPairs}`);

// ---- Phi'_{m,g} vs E_{m,f} : are the two coarse ACTIONS the same map? ----
let sameMap = 0, conjMap = 0;
for (const [m, f] of shad) {
  const g = tau(f), Ef = E(m, f), Pg = Pp(m, g);
  if (Pg === null) continue;
  if (PN.every(z => eq(Ef(z), Pg(z)))) sameMap++;
  if (PN.every(z => eq(Pg(z), chat(Ef(chat(z)))))) conjMap++;   // Phi' = chat o E o chat
}
console.log(`Phi'_{m,tau(f)} == E_{m,f} as maps             : ${sameMap}/20`);
console.log(`Phi'_{m,tau(f)} == chat o E_{m,f} o chat       : ${conjMap}/20`);
