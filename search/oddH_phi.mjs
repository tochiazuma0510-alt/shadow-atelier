// oddH_phi.mjs -- 裁定 105 追加設問: Phi_{m,f} の (j,[alpha]) 類への作用(n=9)
//  (A) GT(K^(9)) を簡約 hexagon (3.10)(3.11) から独立に再列挙(paper 積・両向き比較)
//  (B) Phi_{m,f}: X -> X^u, Y -> f^{-1} Y^u f  の A への誘導作用(固有値)を実測
//  (C) Phi(H_{2,1,0}) の (j,alpha,beta) を実測し、類 (2,[1]) に留まるか
//  (D) 共役方向を反転した Phi': Y -> f Y^u f^{-1} で同じことを実施(実装罠の再現テスト)

const n = 9, n2 = n*n, n3 = n*n*n;
const mod = (a) => ((a % n) + n) % n;
const encA = (v) => v[0] + n*v[1] + n2*v[2];
const decA = (a) => [a % n, Math.floor(a/n) % n, Math.floor(a/n2)];
const klein = [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]];
const sgn = (q,i) => (q === 0 || q === i) ? 1 : -1;
const actQ = (q,v) => [mod(sgn(q,1)*v[0]), mod(sgn(q,2)*v[1]), mod(sgn(q,3)*v[2])];
const gEnc = (v,q) => q*n3 + encA(v);
const gV = (g) => decA(g % n3), gQ = (g) => Math.floor(g/n3);
const mul = (g,h) => { const v=gV(g),q=gQ(g),w=gV(h),p=gQ(h),qw=actQ(q,w);
  return gEnc([mod(v[0]+qw[0]),mod(v[1]+qw[1]),mod(v[2]+qw[2])], klein[q][p]); };
const inv = (g) => { const v=gV(g),q=gQ(g),qv=actQ(q,v); return gEnc([mod(-qv[0]),mod(-qv[1]),mod(-qv[2])],q); };
const pow = (g,e) => { let r = ID, b = g, k = e; if (k < 0) { b = inv(g); k = -k; } for (let i=0;i<k;i++) r = mul(r,b); return r; };
const ID = gEnc([0,0,0],0);
const X = gEnc([1,0,0],1), Y = gEnc([1,1,1],2);
const Z = inv(mul(X,Y));
const e1 = gEnc([1,0,0],0), e2 = gEnc([0,1,0],0), e3 = gEnc([0,0,1],0);
const q1 = gEnc([0,0,0],1), q2 = gEnc([0,0,0],2);

// ---- BFS 語表現(右から生成元を掛ける)----
const G = [], idx = new Map();
{ const stack = [ID]; idx.set(ID, 0); G.push(ID);
  while (stack.length) { const g = stack.shift();
    for (const s of [X, Y, inv(X), inv(Y)]) { const h = mul(g, s); if (!idx.has(h)) { idx.set(h, G.length); G.push(h); stack.push(h); } } } }
if (G.length !== 4*n3) throw new Error("G_9 size " + G.length);

// 生成元像 (imX, imY) から自己準同型を BFS で構成。準同型でなければ null。
function homFromImages(imX, imY) {
  const map = new Map([[ID, ID]]); const stack = [ID];
  const gens = [X, Y, inv(X), inv(Y)];
  const imgs = [imX, imY, inv(imX), inv(imY)];
  while (stack.length) { const g = stack.shift();
    for (let i = 0; i < 4; i++) { const h = mul(g, gens[i]); const val = mul(map.get(g), imgs[i]);
      if (!map.has(h)) { map.set(h, val); stack.push(h); } else if (map.get(h) !== val) return null; } }
  if (map.size !== G.length) return null;
  return map;
}
const theta = homFromImages(Y, X);            // theta: x<->y
const tau   = homFromImages(Y, Z);            // tau: x->y->z->x
if (!theta || !tau) throw new Error("theta/tau が G_9 の自己準同型でない");
const isAut = (m) => new Set(m.values()).size === G.length;
console.log(`theta, tau は G_9 の自己同型: ${isAut(theta)} / ${isAut(tau)}`);

// ---- (A) 簡約 hexagon による GT(K^(9)) の独立列挙 ----
// charming: u = 2m+1 が (Z/N_ord)^x、f ∈ [G,G] = A。 N_ord = lcm(9,2) = 18
const Nord = 18;
const gcd = (a,b) => b ? gcd(b, a%b) : a;
const charming = []; for (let m = 0; m < Nord; m++) if (gcd(2*m+1, Nord) === 1) charming.push(m);
console.log(`charming set X_9 = [${charming}]  (|.| = ${charming.length})`);

function enumerate(orderMode) {
  // orderMode: "paper" = (3.10) f*theta(f), (3.11) tau^2(W)*tau(W)*W  (paper 積そのまま)
  //            "rev"   = すべて逆順
  const shadows = []; let h10fail = 0, h11fail = 0, genfail = 0;
  for (const m of charming) {
    const u = 2*m+1;
    for (let a = 0; a < n3; a++) {
      const f = gEnc(decA(a), 0);                       // f ∈ A = [G,G]
      const tf = theta.get(f);
      const c310 = (orderMode === "paper") ? mul(f, tf) : mul(tf, f);
      if (c310 !== ID) { h10fail++; continue; }
      const W = mul(pow(Y, m), f);                      // paper 語 y^m f
      const W2 = (orderMode === "paper") ? mul(pow(Y,m), f) : mul(f, pow(Y,m));
      const t1 = tau.get(W2), t2 = tau.get(t1);
      const c311 = (orderMode === "paper") ? mul(mul(t2, t1), W2) : mul(mul(W2, t1), t2);
      if (c311 !== ID) { h11fail++; continue; }
      // 全射性
      const im = new Set([ID]); const st = [ID]; const gg = [pow(X,u), mul(mul(inv(f), pow(Y,u)), f)];
      while (st.length) { const g = st.shift(); for (const s of gg) { const h = mul(g,s); if (!im.has(h)) { im.add(h); st.push(h); } } }
      if (im.size !== G.length) { genfail++; continue; }
      shadows.push({ m, f, fv: decA(a) });
    }
  }
  return { shadows, h10fail, h11fail, genfail };
}
for (const mode of ["paper", "rev"]) {
  const r = enumerate(mode);
  console.log(`\n[hexagon 列挙 / ${mode}] shadow 総数 = ${r.shadows.length}  (3.10)fail=${r.h10fail}  (3.11)fail=${r.h11fail}  生成不十分=${r.genfail}`);
  const per = {}; for (const s of r.shadows) per[s.m] = (per[s.m]||0)+1;
  console.log(`  m ごと: ${Object.entries(per).map(([k,v])=>`${k}:${v}`).join(" ")}`);
  if (r.shadows.length && r.shadows.length <= 200) {
    // Thm 4.3 の形 (2k, -2k, kappa(m)) と一致するか
    const kap = (m) => (m % 2 === 1) ? mod(m+1) : mod(-m);
    let ok = 0, bad = [];
    for (const s of r.shadows) { const [f1,f2,f3] = s.fv;
      if (mod(f1+f2) === 0 && f3 === kap(s.m)) ok++; else bad.push(`m=${s.m} f=(${s.fv})`); }
    console.log(`  Thm 4.3 形 (t,-t,kappa(m)) との一致: ${ok}/${r.shadows.length}` + (bad.length ? `  例外例: ${bad.slice(0,4).join(" ; ")}` : ""));
  }
}

// ---- (B)(C)(D) ----
const gt = enumerate("paper").shadows;
const Hfun = (() => { const s = new Set();
  for (let a=0;a<n;a++) for (let b=0;b<n;b++) { const u = [mod(b*1), mod(a), mod(b)];  // a*e2 + b*(1*e1+e3)
    s.add(gEnc(u,0)); s.add(gEnc([u[0], u[1], u[2]], 2)); } return s; })();
// 正確に作り直す: H_{2,alpha,beta} = <e2, alpha e1 + e3, (beta e1) q2>
const makeH = (j, al, be) => { const s = new Set(); const L = (j===2)?[[0,1,0],[al,0,1]]:[[0,0,1],[al,1,0]];
  for (let a=0;a<n;a++) for (let b=0;b<n;b++) { const u = [mod(a*L[0][0]+b*L[1][0]), mod(a*L[0][1]+b*L[1][1]), mod(a*L[0][2]+b*L[1][2])];
    s.add(gEnc(u,0)); s.add(gEnc([mod(u[0]+be), u[1], u[2]], j)); } return s; };
const keyOf = (s) => [...s].sort((a,b)=>a-b).join(",");
const paramOf = new Map();
for (const j of [2,3]) for (let al=0; al<n; al++) for (let be=0; be<n; be++) paramOf.set(keyOf(makeH(j,al,be)), [j,al,be]);
const H = makeH(2,1,0);
console.log(`\nH^fun = H_{2,1,0}: |H| = ${H.size} (期待 162)  パラメータ照合 = ${JSON.stringify(paramOf.get(keyOf(H)))}`);

function analyse(convention) {
  const rows = []; let stay = 0, notHom = 0, notAut = 0, notInFamily = 0;
  for (const sh of gt) {
    const u = 2*sh.m + 1, f = sh.f;
    const imY = (convention === "A") ? mul(mul(inv(f), pow(Y,u)), f)     // paper: f^{-1} y^u f
                                     : mul(mul(f, pow(Y,u)), inv(f));   // 反転: f y^u f^{-1}
    const Phi = homFromImages(pow(X,u), imY);
    if (!Phi) { notHom++; rows.push({ m: sh.m, f: sh.fv, status: "not-hom" }); continue; }
    const aut = isAut(Phi);
    if (!aut) notAut++;
    // A への誘導作用(固有値)
    const ev = [e1,e2,e3].map((e,i) => { const im = Phi.get(e); const v = gV(im);
      return (gQ(im) === 0 && v.filter((c,jj)=>jj!==i && c!==0).length === 0) ? v[i] : null; });
    const imH = new Set([...H].map(g => Phi.get(g)));
    const p = paramOf.get(keyOf(imH));
    if (!p) notInFamily++;
    const inClass = !!p && p[0] === 2 && (p[1] === 1 || p[1] === n-1);
    if (inClass) stay++;
    rows.push({ m: sh.m, f: sh.fv, u, aut, ev, imParam: p || null, inClass });
  }
  return { rows, stay, notHom, notAut, notInFamily };
}

for (const conv of ["A", "B"]) {
  const r = analyse(conv);
  const label = conv === "A" ? "A(paper: f^{-1} Y^u f)" : "B(反転: f Y^u f^{-1} = GAP の生の f^-1*Y^u*f)";
  console.log(`\n===== 規約 ${label} =====`);
  console.log(`  108 shadow 中: 準同型でない ${r.notHom} / 自己同型でない ${r.notAut} / (1.2) の族に落ちない ${r.notInFamily}`);
  console.log(`  Phi(H^fun) が類 (2,[1]) に留まる件数 = ${r.stay} / ${r.rows.length}`);
  const byM = {};
  for (const x of r.rows) { const k = x.m; if (!byM[k]) byM[k] = { stay:0, tot:0, ev:x.ev, aut:x.aut }; byM[k].tot++; if (x.inClass) byM[k].stay++; }
  console.log(`  m ごと(留まる件数/9・A 上の固有値 (e1,e2,e3)・自己同型か):`);
  for (const m of charming) { const b = byM[m];
    console.log(`    m=${String(m).padStart(2)}  u=${String(2*m+1).padStart(2)}  留=${b.stay}/9  ev=${JSON.stringify(b.ev)}  aut=${b.aut}`); }
  // 落ちる先の alpha
  const dests = new Map();
  for (const x of r.rows) if (x.imParam) { const k = `j=${x.imParam[0]},α=${x.imParam[1]}`; dests.set(k, (dests.get(k)||0)+1); }
  console.log(`  Phi(H^fun) の行き先 (j,α) 分布: ${[...dests.entries()].map(([k,v])=>`${k}:${v}`).join("  ")}`);
}
