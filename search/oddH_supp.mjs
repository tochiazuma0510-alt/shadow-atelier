// oddH_supp.mjs -- 補助検算(合成数 n を含む)。
//  (S1) H_{j,α,β} が部分群・|H|=2n^2・p3 成立・(p2 ⟺ α≠0)  [逆向き=存在の側のみ。悉皆性は証明の担当]
//  (S2) ordered passport の閉形式:  d := gcd(α,n) として
//        j=2:  (X,Y,Z)-型 = ( 2n , 2^{n-1}1^2 , (2n/d)^d )
//        j=3:  (X,Y,Z)-型 = ( 2n , (2n/d)^d , 2^{n-1}1^2 )
//  (S3) 「K3/K5 と同型の passport」を満たす類の数 = φ(n)/2 (各 j)

const gcd = (a,b) => b ? gcd(b, a%b) : a;
const phi = (n) => { let c = 0; for (let k = 1; k <= n; k++) if (gcd(k,n) === 1) c++; return c; };

function run(n) {
  const n2 = n*n, n3 = n*n*n;
  const mod = (a) => ((a % n) + n) % n;
  const encA = (v) => v[0] + n*v[1] + n2*v[2];
  const decA = (a) => [a % n, Math.floor(a/n) % n, Math.floor(a/n2)];
  const klein = [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]];
  const sgn = (q,i) => (q === 0 || q === i) ? 1 : -1;
  const actQ = (q,v) => [mod(sgn(q,1)*v[0]), mod(sgn(q,2)*v[1]), mod(sgn(q,3)*v[2])];
  const gEnc = (v,q) => q*n3 + encA(v);
  const gV = (g) => decA(g % n3), gQ = (g) => Math.floor(g/n3);
  const gmul = (g,h) => { const v=gV(g),q=gQ(g),w=gV(h),p=gQ(h),qw=actQ(q,w);
    return gEnc([mod(v[0]+qw[0]),mod(v[1]+qw[1]),mod(v[2]+qw[2])], klein[q][p]); };
  const ginv = (g) => { const v=gV(g),q=gQ(g),qv=actQ(q,v); return gEnc([mod(-qv[0]),mod(-qv[1]),mod(-qv[2])],q); };
  const ID = gEnc([0,0,0],0), Xg = gEnc([1,0,0],1), Yg = gEnc([1,1,1],2);
  const Zg = ginv(gmul(Xg,Yg));

  const XPow = []; { let g = ID; for (let i = 0; i < 2*n; i++) { XPow.push(g); g = gmul(g,Xg); } }
  const ordX = (() => { let g = ID, k = 0; do { g = gmul(g,Xg); k++; } while (g !== ID && k <= 8*n); return k; })();

  const makeH = (j,al,be) => {
    const arr = []; const q = j;
    const L = (j === 2) ? [[0,1,0],[al,0,1]] : [[0,0,1],[al,1,0]];
    for (let s = 0; s < n; s++) for (let t = 0; t < n; t++) {
      const u = [mod(s*L[0][0]+t*L[1][0]), mod(s*L[0][1]+t*L[1][1]), mod(s*L[0][2]+t*L[1][2])];
      arr.push(gEnc(u,0));
      arr.push(gEnc([mod(u[0]+be), u[1], u[2]], q));
    }
    return arr;
  };

  const cyc = (perm) => { const seen = new Array(perm.length).fill(false), out = [];
    for (let i = 0; i < perm.length; i++) { if (seen[i]) continue; let l = 0, j = i; while (!seen[j]) { seen[j] = true; j = perm[j]; l++; } out.push(l); }
    return out.sort((a,b)=>b-a).join("."); };

  const fails = [];
  let nSub = 0;
  for (const j of [2,3]) for (let al = 0; al < n; al++) for (let be = 0; be < n; be++) {
    const arr = makeH(j,al,be); const S = new Set(arr); nSub++;
    if (S.size !== 2*n2) fails.push(`|H_{${j},${al},${be}}| = ${S.size} ≠ 2n^2`);
    // 部分群性
    for (const g of arr) { for (const h of arr) if (!S.has(gmul(g,h))) { fails.push(`closure fail ${j},${al},${be}`); break; } }
    // p3: <X> ∩ H = 1 かつ |<X>| = 2n = [P:H]  ⇒ 単純推移
    let inter = 0; for (const t of XPow) if (t !== ID && S.has(t)) inter++;
    const p3 = (inter === 0);
    if (!p3) fails.push(`p3 fail ${j},${al},${be}`);
    // p2: <X> は(p3 のとき)H の左剰余類の完全代表系 ⇒ 2n-1 個で判定
    let extra = 0;
    for (const t of XPow) { if (t === ID) continue; const ti = ginv(t);
      let ok = true; for (const h of arr) if (!S.has(gmul(gmul(t,h),ti))) { ok = false; break; }
      if (ok) extra++; }
    const p2 = (extra === 0);
    if (p2 !== (al !== 0)) fails.push(`p2 ⟺ α≠0 fail at ${j},${al},${be}  (p2=${p2})`);
  }

  // (S2) passport (β=0 の代表で)
  const rows = [];
  for (const j of [2,3]) for (let al = 0; al < n; al++) {
    const arr = makeH(j,al,0); const S = new Set(arr);
    // coset table: element -> i with element ∈ X^i H
    const tbl = new Int32Array(4*n3).fill(-1);
    for (let i = 0; i < 2*n; i++) for (const h of arr) tbl[gmul(XPow[i],h)] = i;
    if (tbl.some(v => v < 0)) { fails.push(`transversal fail ${j},${al}`); continue; }
    const permOf = (g) => XPow.map((xi) => tbl[gmul(g, xi)]);
    const t = [cyc(permOf(Xg)), cyc(permOf(Yg)), cyc(permOf(Zg))];
    const d = gcd(al === 0 ? n : al, n);
    const deg = Array(d).fill(2*n/d).join(".");
    const std = Array(n-1).fill(2).concat([1,1]).join(".");
    const want = (j === 2) ? [String(2*n), std, deg] : [String(2*n), deg, std];
    const ok = (al !== 0) && t.join("|") === want.join("|");
    rows.push({ j, al, d, t: t.join(" , "), ok, want: want.join(" , ") });
  }
  const badPassport = rows.filter(r => r.al !== 0 && !r.ok);

  // (S3) K3/K5 型 passport (第 2/第 3 成分の一方が 2n) を持つ類の数
  const stdCount = rows.filter(r => r.al !== 0 && r.j === 2 && r.t.split(" , ")[2] === String(2*n)).length;

  return { n, ordX, nSub, fails, rows, badPassport, stdCountPerJ_elements: stdCount, phiHalf: phi(n)/2 };
}

for (const n of [3,5,9,13,15,21,25,27]) {
  const t0 = Date.now();
  const r = run(n);
  console.log(`\n===== n = ${n}  (${Date.now()-t0} ms) =====`);
  console.log(`  ord(X) = ${r.ordX} (期待 ${2*n})`);
  console.log(`  検査した H_{j,α,β} = ${r.nSub} 個 (= 2n^2 = ${2*n*n})`);
  console.log(`  [${r.fails.length === 0 ? "PASS" : "FAIL"}] 部分群性・|H|=2n^2・p3・(p2 ⟺ α≠0)` + (r.fails.length ? `  ${r.fails.slice(0,5).join(" ; ")}` : ""));
  console.log(`  [${r.badPassport.length === 0 ? "PASS" : "FAIL"}] passport 閉形式 (2n/d)^d, d=gcd(α,n)` + (r.badPassport.length ? `  例: j=${r.badPassport[0].j} α=${r.badPassport[0].al} 実測 ${r.badPassport[0].t} / 予測 ${r.badPassport[0].want}` : ""));
  // 退化する α の一覧
  const degen = r.rows.filter(x => x.al !== 0 && x.j === 2 && x.d > 1).map(x => `α=${x.al}(d=${x.d})`);
  console.log(`  passport が退化する α (j=2): ${degen.length ? degen.join(" ") : "なし"}`);
  console.log(`  K3/K5 型 passport (2n, 2^{n-1}1^2, 2n) をもつ α の個数 (j=2) = ${r.stdCountPerJ_elements}  (= φ(n) = ${2*r.phiHalf})  ⇒ 類数 φ(n)/2 = ${r.phiHalf}`);
}
