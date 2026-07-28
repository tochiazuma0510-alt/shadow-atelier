// oddH_verify.mjs -- 命題 ODD-H の独立検算(node 単系統・GAP 非依存)
// 目的:
//  (V1) G_n = <(r,s,s),(rs,r,rs)> <= D_n^3 を D_n^3 内で直接構成し、
//       A ⋊ Q 分解・符号表・X = a1 q1・Y = a1a2a3 q2 を検証。
//  (V2) 抽象模型 M_n = (Z/n)^3 ⋊ C_2^2 と G_n の同型を関係式で検証。
//  (V3) 位数 2n^2 の部分群を「完全に」列挙(H∩A の位数 n^2 が強制されることを利用)し、
//       述語 p1(指数)・p2(自己正規化)・p3(<X> 推移性)を独立実装で検査。
//  (V4) 個数・共役類・(j,alpha,beta) 表示との一致を照合。
//  (V5) ordered passport (X,Y,Z の P/H 上の型) を補助的に計算。
// 規律: u・c 平方類・ĉ_μ には触れない。整数演算のみ。

function run(n) {
  const n2 = n * n, n3 = n * n * n;
  const mod = (a) => ((a % n) + n) % n;

  // ---------- A = (Z/n)^3 ----------
  const encA = (v) => v[0] + n * v[1] + n2 * v[2];
  const decA = (a) => [a % n, Math.floor(a / n) % n, Math.floor(a / n2)];

  // ---------- Q = C_2^2 = {0,q1,q2,q3} ----------
  const klein = [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]];
  const sgn = (q, i) => (q === 0 || q === i) ? 1 : -1;   // i in {1,2,3}
  const actQ = (q, v) => [mod(sgn(q,1)*v[0]), mod(sgn(q,2)*v[1]), mod(sgn(q,3)*v[2])];

  // ---------- G = A ⋊ Q, encoding g = q*n3 + encA(v) ----------
  const gEnc = (v, q) => q * n3 + encA(v);
  const gV = (g) => decA(g % n3);
  const gQ = (g) => Math.floor(g / n3);
  const gmul = (g, h) => {
    const v = gV(g), q = gQ(g), w = gV(h), p = gQ(h);
    const qw = actQ(q, w);
    return gEnc([mod(v[0]+qw[0]), mod(v[1]+qw[1]), mod(v[2]+qw[2])], klein[q][p]);
  };
  const ginv = (g) => {
    const v = gV(g), q = gQ(g), qv = actQ(q, v);
    return gEnc([mod(-qv[0]), mod(-qv[1]), mod(-qv[2])], q);
  };
  const ID = gEnc([0,0,0], 0);
  const Xg = gEnc([1,0,0], 1);          // X = a1 q1
  const Yg = gEnc([1,1,1], 2);          // Y = a1a2a3 q2
  const Zg = ginv(gmul(Xg, Yg));        // Z = (XY)^{-1}

  const report = { n, checks: [] };
  const ck = (name, ok, extra) => { report.checks.push({ name, ok, extra }); return ok; };

  // ================= V1: D_n^3 realization =================
  // D_n element [a,e] = r^a s^e ; (a,e)(b,f) = (a + (-1)^e b, e+f)
  const dmul = (x, y) => [ mod(x[0] + (x[1] ? -y[0] : y[0])), (x[1]+y[1]) % 2 ];
  const tmul = (X, Y) => [dmul(X[0],Y[0]), dmul(X[1],Y[1]), dmul(X[2],Y[2])];
  const tEnc = (T) => ((T[0][0]*2+T[0][1]) * (2*n) + (T[1][0]*2+T[1][1])) * (2*n) + (T[2][0]*2+T[2][1]);
  const Xd = [[1,0],[0,1],[0,1]];                        // (r, s, s)
  const Yd = [[1,1],[1,0],[1,1]];                        // (rs, r, rs)
  // closure
  {
    const seen = new Map(); const stack = [];
    const push = (T) => { const k = tEnc(T); if (!seen.has(k)) { seen.set(k, T); stack.push(T); } };
    push([[0,0],[0,0],[0,0]]);
    while (stack.length) {
      const T = stack.pop();
      push(tmul(T, Xd)); push(tmul(T, Yd));
    }
    ck("|G_n| = 4n^3 (D_n^3 内で直接生成)", seen.size === 4*n3, { got: seen.size, want: 4*n3 });
    // a_i, q_j の membership と関係式
    const a = [ [[1,0],[0,0],[0,0]], [[0,0],[1,0],[0,0]], [[0,0],[0,0],[1,0]] ];
    const q = [ null, [[0,0],[0,1],[0,1]], [[0,1],[0,0],[0,1]], [[0,1],[0,1],[0,0]] ];
    let memb = true;
    for (const g of [a[0],a[1],a[2],q[1],q[2],q[3]]) memb = memb && seen.has(tEnc(g));
    ck("a1,a2,a3,q1,q2,q3 ∈ G_n", memb);
    ck("X = a1·q1", tEnc(tmul(a[0], q[1])) === tEnc(Xd));
    ck("Y = a1a2a3·q2", tEnc(tmul(tmul(tmul(a[0],a[1]),a[2]), q[2])) === tEnc(Yd));
    // 符号表: q_j a_i q_j^{-1} = a_i^{sgn(j,i)}
    let tbl = true; const tblRows = [];
    for (let j = 1; j <= 3; j++) {
      const row = [];
      for (let i = 1; i <= 3; i++) {
        const conj = tmul(tmul(q[j], a[i-1]), q[j]);   // q_j^{-1} = q_j
        const plus  = tEnc(conj) === tEnc(a[i-1]);
        const minus = tEnc(conj) === tEnc([[mod(-(i===1?1:0)),0],[mod(-(i===2?1:0)),0],[mod(-(i===3?1:0)),0]]);
        const want = sgn(j, i);
        const ok = (want === 1) ? plus : minus;
        tbl = tbl && ok; row.push(want === 1 ? "+" : "-");
      }
      tblRows.push(row.join(""));
    }
    ck("符号表 q_j a_i q_j = a_i^{±}", tbl, { rows: tblRows });
    // q_i^2 = 1, q1q2 = q3, a_i 可換・位数 n
    let rel = true;
    for (let j = 1; j <= 3; j++) rel = rel && tEnc(tmul(q[j],q[j])) === tEnc([[0,0],[0,0],[0,0]]);
    rel = rel && tEnc(tmul(q[1],q[2])) === tEnc(q[3]);
    rel = rel && tEnc(tmul(q[2],q[1])) === tEnc(q[3]);
    for (let i = 0; i < 3; i++) for (let k = 0; k < 3; k++)
      rel = rel && tEnc(tmul(a[i],a[k])) === tEnc(tmul(a[k],a[i]));
    ck("Q ≅ C_2^2 ・ A 可換(関係式 ⇒ φ: M_n → G_n は準同型)", rel);
    // 全単射: 模型の 4n^3 元の像が相異なる
    const img = new Set();
    for (let qq = 0; qq < 4; qq++) for (let e = 0; e < n3; e++) {
      const v = decA(e);
      let T = [[0,0],[0,0],[0,0]];
      T = tmul(T, [[v[0],0],[0,0],[0,0]]);
      T = tmul(T, [[0,0],[v[1],0],[0,0]]);
      T = tmul(T, [[0,0],[0,0],[v[2],0]]);
      if (qq) T = tmul(T, q[qq]);
      img.add(tEnc(T));
    }
    ck("φ 全単射 (|im| = 4n^3 かつ im ⊆ G_n)", img.size === 4*n3 && [...img].every(k => seen.has(k)));
  }

  // ord(X) = 2n
  {
    let g = ID, k = 0;
    do { g = gmul(g, Xg); k++; } while (g !== ID && k <= 8*n);
    ck("ord(X) = 2n", k === 2*n, { got: k });
  }

  // ================= V3: 位数 2n^2 の部分群の完全列挙 =================
  // 補題: |H| = 2n^2, n 奇 ⇒ |H∩A| = n^2, |π(H)| = 2.
  //  ⇒ H ↔ (U, q, w+U) with U ≤ A, |U| = n^2, U が q-安定, (1+q)w ∈ U.

  // (a) A の位数 n^2 の部分群を双対で列挙: V ≤ Â, |V| = n, U = V^⊥
  const subsOrderN = new Set();  // key -> sorted element list string
  const subKey = (arr) => arr.slice().sort((x,y)=>x-y).join(",");
  const genAdd = (gens) => {
    // 生成部分群(<= n 元で打ち切り)
    const set = new Set([0]);
    let frontier = [0];
    while (frontier.length) {
      const nf = [];
      for (const e of frontier) for (const g of gens) {
        const v = decA(e), w = decA(g);
        const s = encA([mod(v[0]+w[0]), mod(v[1]+w[1]), mod(v[2]+w[2])]);
        if (!set.has(s)) { set.add(s); nf.push(s); if (set.size > n) return null; }
      }
      frontier = nf;
    }
    return set.size === n ? [...set] : null;
  };
  for (let f = 0; f < n3; f++) {
    const S = genAdd([f]); if (S) subsOrderN.add(subKey(S));
  }
  // 非巡回の場合(n が素数冪合成数など): 素数 p | n について exponent p の部分を走査
  const primes = []; { let m = n; for (let p = 3; p * p <= m; p += 2) { if (m % p === 0) { primes.push(p); while (m % p === 0) m /= p; } } if (m > 1) primes.push(m); }
  for (const p of primes) {
    const tors = []; for (let e = 0; e < n3; e++) { const v = decA(e); if (v.every(c => mod(c*p) === 0)) tors.push(e); }
    for (const f of tors) for (const g of tors) { const S = genAdd([f,g]); if (S) subsOrderN.add(subKey(S)); }
  }
  const Vlist = [...subsOrderN].map(s => s.split(",").map(Number));
  // 双対 pairing <f,v> = f·v mod n ; U = V^perp
  const Ulist = [];
  const Useen = new Set();
  for (const V of Vlist) {
    const U = [];
    for (let e = 0; e < n3; e++) {
      const v = decA(e);
      let ok = true;
      for (const f of V) { const fv = decA(f); if (mod(fv[0]*v[0] + fv[1]*v[1] + fv[2]*v[2]) !== 0) { ok = false; break; } }
      if (ok) U.push(e);
    }
    const k = subKey(U);
    if (U.length === n2 && !Useen.has(k)) { Useen.add(k); Ulist.push(U); }
  }
  ck("A の位数 n^2 部分群の列挙(双対経由)", Ulist.length > 0, { count: Ulist.length });

  // (b) H の列挙
  const cosetRepsOfU = (U) => {
    const inU = new Set(U); const reps = []; const covered = new Set();
    for (let e = 0; e < n3; e++) {
      if (covered.has(e)) continue;
      reps.push(e);
      const v = decA(e);
      for (const u of U) { const w = decA(u); covered.add(encA([mod(v[0]+w[0]), mod(v[1]+w[1]), mod(v[2]+w[2])])); }
    }
    return reps;
  };
  const Hlist = [];
  for (const U of Ulist) {
    const inU = new Set(U);
    for (let q = 1; q <= 3; q++) {
      // U が q-安定か
      let stable = true;
      for (const u of U) { if (!inU.has(encA(actQ(q, decA(u))))) { stable = false; break; } }
      if (!stable) continue;
      for (const w of cosetRepsOfU(U)) {
        const wv = decA(w), qw = actQ(q, wv);
        const sq = encA([mod(wv[0]+qw[0]), mod(wv[1]+qw[1]), mod(wv[2]+qw[2])]);  // (1+q)w
        if (!inU.has(sq)) continue;
        const H = [];
        for (const u of U) {
          H.push(gEnc(decA(u), 0));
          const uv = decA(u);
          H.push(gEnc([mod(wv[0]+uv[0]), mod(wv[1]+uv[1]), mod(wv[2]+uv[2])], q));
        }
        Hlist.push({ U, q, w, elts: H, set: new Set(H) });
      }
    }
  }
  // 部分群性の独立検証(閉性)
  {
    let ok = true;
    for (const H of Hlist) {
      for (const g of H.elts) { for (const h of H.elts) { if (!H.set.has(gmul(g,h))) { ok = false; break; } } if (!ok) break; }
      if (!ok) break;
    }
    ck("列挙された各 H が実際に部分群(積閉包)", ok, { count: Hlist.length });
  }

  // (c) 述語
  const XPow = []; { let g = ID; for (let i = 0; i < 2*n; i++) { XPow.push(g); g = gmul(g, Xg); } }
  const results = [];
  for (const H of Hlist) {
    // p3: <X> の P/H 上の推移性(軌道で判定)
    // coset gH の正準代表 = min_{h∈H} enc(g h)
    const canon = (g) => { let m = Infinity; for (const h of H.elts) { const t = gmul(g,h); if (t < m) m = t; } return m; };
    const orb = new Set(); let cur = canon(ID);
    for (let i = 0; i < 2*n + 2; i++) { orb.add(cur); cur = canon(gmul(Xg, cur)); }
    const p3 = (orb.size === 2*n);
    // p2: 自己正規化。N(H) は H の左剰余類の合併 ⇒ 剰余類代表で判定
    const cosets = []; { const seen = new Set(); for (let g = 0; g < 4*n3; g++) { const c = canon(g); if (!seen.has(c)) { seen.add(c); cosets.push(c); } } }
    let normExtra = 0;
    for (const g of cosets) {
      if (H.set.has(g)) continue;
      const gi = ginv(g);
      let ok = true;
      for (const h of H.elts) { if (!H.set.has(gmul(gmul(g,h), gi))) { ok = false; break; } }
      if (ok) normExtra++;
    }
    const p2 = (normExtra === 0);
    results.push({ H, p2, p3, cosets, canon });
  }

  const qualifying = results.filter(r => r.p3);      // p1 & p3 (p1 は構成で自動)
  const good = results.filter(r => r.p2 && r.p3);    // p1 & p2 & p3
  const selfNorm = results.filter(r => r.p2);        // p1 & p2 (p3 なし) = GAP の self_normalizing_conjugate_total 相当

  ck("|{p1&p3}| = 2n^2", qualifying.length === 2*n2, { got: qualifying.length, want: 2*n2 });
  ck("|{p1&p2&p3}| = 2n(n-1)", good.length === 2*n*(n-1), { got: good.length, want: 2*n*(n-1) });
  ck("|{p1&p3} \\ {p2}| = 2n (α=0 の層)", qualifying.length - good.length === 2*n, { got: qualifying.length - good.length });
  report.selfNormalizingTotal_noP3 = selfNorm.length;

  // (d) (j,alpha,beta) 表示との一致
  //  H_{2,α,β} = <a2, a1^α a3, a1^β q2> ; H_{3,α,β} = <a3, a1^α a2, a1^β q3>
  const makeH = (j, al, be) => {
    const set = new Set();
    const q = j;                                   // j=2 -> q2, j=3 -> q3
    const lines = (j === 2) ? [[0,1,0],[al,0,1]] : [[0,0,1],[al,1,0]];
    for (let s = 0; s < n; s++) for (let t = 0; t < n; t++) {
      const u = [mod(s*lines[0][0] + t*lines[1][0]), mod(s*lines[0][1] + t*lines[1][1]), mod(s*lines[0][2] + t*lines[1][2])];
      set.add(gEnc(u, 0));
      set.add(gEnc([mod(u[0]+be), u[1], u[2]], q));
    }
    return set;
  };
  {
    const keyOf = (s) => [...s].sort((x,y)=>x-y).join(",");
    const paramSets = new Map();
    for (const j of [2,3]) for (let al = 0; al < n; al++) for (let be = 0; be < n; be++)
      paramSets.set(keyOf(makeH(j,al,be)), [j,al,be]);
    ck("(1.2) の族 2n^2 個が相異なる", paramSets.size === 2*n2, { got: paramSets.size });
    const qualKeys = new Set(qualifying.map(r => keyOf(r.H.set)));
    const paramKeys = new Set(paramSets.keys());
    const same = qualKeys.size === paramKeys.size && [...qualKeys].every(k => paramKeys.has(k));
    ck("{p1&p3} = (1.2) の族(集合として一致)", same, { qual: qualKeys.size, param: paramKeys.size });
    // good ⟺ α ≠ 0
    let ok = true;
    for (const r of qualifying) {
      const [j, al, be] = paramSets.get(keyOf(r.H.set));
      if ((al !== 0) !== r.p2) { ok = false; break; }
    }
    ck("自己正規化 ⟺ α ≠ 0 (1.3)", ok);
    report.paramSets = paramSets;
    report.keyOf = keyOf;
  }

  // (e) 共役類
  {
    const keyOf = report.keyOf;
    const gens = [gEnc([1,0,0],0), gEnc([0,1,0],0), gEnc([0,0,1],0), gEnc([0,0,0],1), gEnc([0,0,0],2)];
    const conj = (set, g) => { const gi = ginv(g); const out = new Set(); for (const h of set) out.add(gmul(gmul(g,h), gi)); return out; };
    const seen = new Set(); const classes = [];
    for (const r of good) {
      const k0 = keyOf(r.H.set); if (seen.has(k0)) continue;
      const cls = new Map([[k0, r.H.set]]); const stack = [r.H.set];
      while (stack.length) {
        const S = stack.pop();
        for (const g of gens) { const T = conj(S, g); const k = keyOf(T); if (!cls.has(k)) { cls.set(k, T); stack.push(T); } }
      }
      for (const k of cls.keys()) seen.add(k);
      classes.push([...cls.keys()]);
    }
    ck("good の P_n-共役類数 = n-1", classes.length === n-1, { got: classes.length });
    ck("各類のサイズ = 2n", classes.every(c => c.length === 2*n), { sizes: [...new Set(classes.map(c=>c.length))] });
    // 類の不変量 (j,[α])
    const inv = classes.map(c => {
      const params = c.map(k => report.paramSets.get(k));
      const js = [...new Set(params.map(p => p[0]))];
      const als = [...new Set(params.map(p => p[1]))].sort((a,b)=>a-b);
      return { j: js, alphas: als };
    });
    ck("各類で j 一定・α は {±α}", inv.every(v => v.j.length === 1 && v.alphas.length === 2 && mod(v.alphas[0]+v.alphas[1]) === 0), { inv: inv.map(v=>`j=${v.j[0]} α=${v.alphas.join("/")}`) });
    report.classInvariants = inv.map(v => `j=${v.j[0]} [α]={${v.alphas.join(",")}}`);
  }

  // (f) 自己正規化(p3 なし)の共役類数と総数 -- GAP JSON との照合用
  {
    const keyOf = report.keyOf;
    const gens = [gEnc([1,0,0],0), gEnc([0,1,0],0), gEnc([0,0,1],0), gEnc([0,0,0],1), gEnc([0,0,0],2)];
    const conj = (set, g) => { const gi = ginv(g); const out = new Set(); for (const h of set) out.add(gmul(gmul(g,h), gi)); return out; };
    const seen = new Set(); const classes = [];
    for (const r of selfNorm) {
      const k0 = keyOf(r.H.set); if (seen.has(k0)) continue;
      const cls = new Map([[k0, r.H.set]]); const stack = [r.H.set];
      while (stack.length) {
        const S = stack.pop();
        for (const g of gens) { const T = conj(S, g); const k = keyOf(T); if (!cls.has(k)) { cls.set(k, T); stack.push(T); } }
      }
      for (const k of cls.keys()) seen.add(k);
      classes.push([...cls.keys()]);
    }
    report.selfNormClasses = classes.length;
    report.selfNormClassSizes = [...new Set(classes.map(c=>c.length))].sort((a,b)=>a-b);
  }

  // (g) ordered passport (X,Y,Z) の P/H 上の型 -- 補助観測
  {
    const cycType = (H, g) => {
      const canon = (x) => { let m = Infinity; for (const h of H.elts) { const t = gmul(x,h); if (t < m) m = t; } return m; };
      const reps = []; { const seen = new Set(); for (let x = 0; x < 4*n3; x++) { const c = canon(x); if (!seen.has(c)) { seen.add(c); reps.push(c); } } }
      const idx = new Map(reps.map((c,i)=>[c,i]));
      const perm = reps.map(c => idx.get(canon(gmul(g, c))));
      const seen = new Array(reps.length).fill(false); const cyc = [];
      for (let i = 0; i < reps.length; i++) { if (seen[i]) continue; let l = 0, j = i; while (!seen[j]) { seen[j] = true; j = perm[j]; l++; } cyc.push(l); }
      return cyc.sort((a,b)=>b-a).join(".");
    };
    const rows = [];
    const done = new Set();
    for (const r of good) {
      const p = report.paramSets.get(report.keyOf(r.H.set));
      const key = `${p[0]}|${Math.min(p[1], n - p[1])}`;
      if (done.has(key)) continue; done.add(key);
      rows.push({ j: p[0], alpha: p[1], passport: [cycType(r.H, Xg), cycType(r.H, Yg), cycType(r.H, Zg)].join(" , ") });
    }
    report.passports = rows;
  }

  return report;
}

const out = [];
for (const n of [3,5,7,9,11]) {
  const t0 = Date.now();
  const r = run(n);
  out.push(r);
  console.log(`\n=========== n = ${n}  (${Date.now()-t0} ms) ===========`);
  for (const c of r.checks) console.log(`  [${c.ok ? "PASS" : "FAIL"}] ${c.name}` + (c.extra ? `   ${JSON.stringify(c.extra)}` : ""));
  console.log(`  自己正規化(p3 なし)総数 = ${r.selfNormalizingTotal_noP3} / 類数 = ${r.selfNormClasses} / 類サイズ = ${JSON.stringify(r.selfNormClassSizes)}`);
  console.log(`  good 類の不変量: ${r.classInvariants.join("  |  ")}`);
  console.log(`  ordered passport (X,Y,Z):`);
  for (const p of r.passports) console.log(`     j=${p.j} α=${p.alpha}:  ${p.passport}`);
}

console.log("\n=========== 総括 ===========");
console.log("n | 2n^2 | p1&p3 | 2n(n-1) | p1&p2&p3 | 類数 | 自己正規化(p3 なし)総数 | その類数");
for (const r of out) {
  const n = r.n;
  const q = r.checks.find(c => c.name.startsWith("|{p1&p3}|")).extra;
  const g = r.checks.find(c => c.name.startsWith("|{p1&p2&p3}|")).extra;
  console.log(`${n} | ${2*n*n} | ${q.got} | ${2*n*(n-1)} | ${g.got} | ${r.classInvariants.length} | ${r.selfNormalizingTotal_noP3} | ${r.selfNormClasses}`);
}
const allOk = out.every(r => r.checks.every(c => c.ok));
console.log(`\nALL CHECKS: ${allOk ? "PASS" : "FAIL"}`);
