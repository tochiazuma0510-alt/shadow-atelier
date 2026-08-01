// Mirror test: read EVERY product string in the paper formulas under the
// opposite product (a .op b = b .gap a) and redo the whole coarse layer.
// Question: does the machine distinguish the two readings, or are both
// self-consistent?  (relevant to question (1): is the order pinned by data?)
const N = 8;
const id = () => { const a = new Array(N + 1); for (let i = 0; i <= N; i++) a[i] = i; return a; };
const cyc = (...cs) => { const a = id(); for (const c of cs) for (let k = 0; k < c.length; k++) a[c[k]] = c[(k + 1) % c.length]; return a; };
const gmul = (p, q) => { const a = new Array(N + 1); a[0] = 0; for (let i = 1; i <= N; i++) a[i] = q[p[i]]; return a; };
const inv = (p) => { const a = new Array(N + 1); a[0] = 0; for (let i = 1; i <= N; i++) a[p[i]] = i; return a; };
const eq = (p, q) => { for (let i = 1; i <= N; i++) if (p[i] !== q[i]) return false; return true; };
const key = (p) => p.slice(1).join(',');
const gpow = (p, e) => { let r = id(); const b = e < 0 ? inv(p) : p; for (let i = 0; i < Math.abs(e); i++) r = gmul(r, b); return r; };
const tt = cyc([1, 2, 3]), aa = cyc([1, 4, 5]);
const XX = gmul(aa, inv(tt)), ss = gmul(tt, gpow(XX, 3));
const aE = gmul(ss, cyc([6, 8])), bE = gmul(tt, cyc([6, 8, 7]));
const s1 = gmul(inv(bE), aE), s2 = gmul(aE, gpow(bE, 2));
const cc = gpow(gmul(s1, s2), 3), xb = gpow(s1, 2), yb = gpow(s2, 2);

// two readings of the SAME formula strings
function makeReading(op) {   // op = 'gap' (literal) or 'opp' (reversed)
  const M = (...xs) => xs.reduce((a, b) => op === 'gap' ? gmul(a, b) : gmul(b, a));
  const P = (p, e) => gpow(p, e);   // powers are reading-independent
  const conj = (z, f) => M(inv(f), z, f);            // "f^-1 z f" as written
  return { M, P, conj };
}
function run(op) {
  const { M, P } = makeReading(op);
  const PN = (() => { const seen = new Set(), L = [id()]; seen.add(key(id()));
    for (let i = 0; i < L.length; i++) for (const g of [xb, yb]) { const e = M(L[i], g); if (!seen.has(key(e))) { seen.add(key(e)); L.push(e); } }
    return L; })();
  const Hex = (m, f) => {
    const u = 2 * m + 1;
    const A1 = M(P(s1, u), inv(f), P(s2, u), f), B1 = M(inv(f), s1, s2, P(xb, -m), P(cc, m));
    if (!eq(A1, B1)) return false;
    const A2 = M(inv(f), P(s2, u), f, P(s1, u)), B2 = M(s2, s1, P(yb, -m), P(cc, m), f);
    return eq(A2, B2);
  };
  const gen = (gens) => { const seen = new Set(), L = [id()]; seen.add(key(id()));
    for (let i = 0; i < L.length; i++) for (const g of gens) { const e = M(L[i], g); if (!seen.has(key(e))) { seen.add(key(e)); L.push(e); } }
    return L.length; };
  const shad = [];
  for (const m of [0, 1, 3, 4]) for (const f of PN) if (Hex(m, f) && gen([xb, M(inv(f), yb, f)]) === PN.length) shad.push([m, f]);
  const SK = new Set(shad.map(([m, f]) => m + '|' + key(f)));
  // E_{m,f} in this reading
  const hom = (imx, imy) => { const img = new Map([[key(id()), id()]]); const q = [id()];
    for (let i = 0; i < q.length; i++) { const e = q[i], ie = img.get(key(e));
      for (const [g, ig] of [[xb, imx], [yb, imy]]) { const e2 = M(e, g), k2 = key(e2), i2 = M(ie, ig);
        if (img.has(k2)) { if (!eq(img.get(k2), i2)) return null; } else { img.set(k2, i2); q.push(e2); } } }
    if (img.size !== PN.length) return null;
    const F = p => img.get(key(p));
    for (const a of PN) for (const b of PN) if (!eq(F(M(a, b)), M(F(a), F(b)))) return null;
    return F; };
  const E = (m, f) => hom(P(xb, 2 * m + 1), M(inv(f), P(yb, 2 * m + 1), f));
  const mpp = (u1, u2) => [0, 1, 3, 4].find(z => ((2 * z + 1) - u1 * u2) % 5 === 0);
  let closed = 0, rev = 0, tot = 0, allDef = true;
  for (const [m1, f1] of shad) for (const [m2, f2] of shad) {
    tot++; const E1 = E(m1, f1); if (E1 === null) { allDef = false; continue; }
    const m3 = mpp(2 * m1 + 1, 2 * m2 + 1);
    if (SK.has(m3 + '|' + key(M(f1, E1(f2))))) closed++;      // (3.53) as written
    if (SK.has(m3 + '|' + key(M(E1(f2), f1)))) rev++;          // reversed
  }
  return { n: shad.length, allDef, closed, rev, tot, keys: SK };
}
const g = run('gap'), o = run('opp');
console.log(`literal reading : |shad|=${g.n}  all E defined=${g.allDef}  (3.53) closes ${g.closed}/${g.tot}  reversed ${g.rev}/${g.tot}`);
console.log(`opposite reading: |shad|=${o.n}  all E defined=${o.allDef}  (3.53) closes ${o.closed}/${o.tot}  reversed ${o.rev}/${o.tot}`);
const same = g.keys.size === o.keys.size && [...g.keys].every(k => o.keys.has(k));
console.log(`the two readings give the SAME 20-row set : ${same}`);
// how do the two 20-row sets relate?  test f -> f^-1
const invKey = k => { const [m, s] = k.split('|'); const p = [0, ...s.split(',').map(Number)]; return m + '|' + key(inv(p)); };
console.log(`opposite set == { (m, f^-1) : literal set }  : ${[...g.keys].every(k => o.keys.has(invKey(k)))}`);
console.log(`overlap of the two 20-row sets              : ${[...g.keys].filter(k => o.keys.has(k)).length}/20`);
