// B_FC 攻略(正本 = docs/week4-BFC攻略_opus_v2.md)— 精密化した前件 (W1)..(W5) の K^(3) 窓での整合検査。
// search/r6act-check.mjs の G3 <= D3^3 再構成を流用し、追加で次を確認する:
//   V1  [P:H] = 6 = M = ord(X)  かつ <X> は P/H 上推移的(全分岐)
//   V2  N_P(H) = H(⇒ Fib -> Lambda が全単射・descent の cocycle 条件が自動)
//   V3  補題 B-2 の逆向き: 「<X> が P/H 上推移的 かつ |Lambda| = ord(X)」を満たす
//       すべての H で N_P(H) = H が自動(P = G3 の全部分群を悉皆)
//   V4  P/H -> Lambda, gH |-> gHg^{-1} は <X>-同変な全単射(tau と左移動が対応)
//   V5  Lambda は Phi(F_0)-安定(K-model の存在に効く)
//   V6  Lambda は Phi(GT(K^(3))) 全 12 元でも安定(Q-model に効く・本稿の新規検査)
//   V7  Lambda は Aut(G3) 全体では安定でない(6+6 融合)— V6 が自明でないことの対照
//   V8  b-不変性の finite 版(正本 §10・系 B-8): 任意の b in (Z/6)^x に対し tau(z^b) の生成する群は tau(mu_6)
//       で、ord(kappa) と ker(kappa) は b で不変(R^cyc_formal の結論が b に依存しない)
let pass = 0, fail = 0;
const ck = (n, ok, x = '') => { (ok ? pass++ : fail++); console.log(`[${ok ? 'PASS' : 'FAIL'}] ${n}${x ? '  ' + x : ''}`); };

const dec = (c) => [Math.floor(c / 2) % 3, c % 2];
const enc1 = (a, e) => 2 * (((a % 3) + 3) % 3) + e;
const mul1 = (c1, c2) => { const [a1, e1] = dec(c1), [a2, e2] = dec(c2); return enc1(a1 + (e1 ? -a2 : a2), e1 ^ e2); };
const E = (x) => [x % 6, Math.floor(x / 6) % 6, Math.floor(x / 36) % 6];
const N = (v) => v[0] + 6 * v[1] + 36 * v[2];
const mul = (x, y) => { const a = E(x), b = E(y); return N([mul1(a[0], b[0]), mul1(a[1], b[1]), mul1(a[2], b[2])]); };
const ID = N([enc1(0, 0), enc1(0, 0), enc1(0, 0)]);
const inv = (x) => { for (let y = 0; y < 216; y++) if (mul(x, y) === ID) return y; throw new Error('no inv'); };
const pow = (x, n) => { let r = ID; const k = ((n % 6) + 6) % 6; for (let i = 0; i < k; i++) r = mul(r, x); return r; };
const R = (a) => enc1(a, 0), S = (a) => enc1(a, 1);
const XB = N([R(1), S(0), S(0)]), YB = N([S(1), R(1), S(1)]), ZB = N([S(2), S(2), R(1)]);
const gen = (gs) => { const s = new Set([ID]), st = [ID]; while (st.length) { const g = st.pop(); for (const h of gs) { const p = mul(g, h); if (!s.has(p)) { s.add(p); st.push(p); } } } return s; };
const G = [...gen([XB, YB, inv(XB), inv(YB)])].sort((a, b) => a - b);
const key = (s) => [...s].sort((a, b) => a - b).join(',');
const closure = (e) => gen([...e, ...e.map(inv)]);
let subs = new Map([[key(new Set([ID])), new Set([ID])]]);
for (let ch = true; ch;) { ch = false; for (const [, Ss] of [...subs]) { if (Ss.size === 108) continue; for (const g of G) { if (Ss.has(g)) continue; const T = closure([...Ss, g]), k = key(T); if (!subs.has(k)) { subs.set(k, T); ch = true; } } } }
const ALL = [...subs.values()];
const normalizer = (H) => G.filter(g => { const gi = inv(g); for (const h of H) if (!H.has(mul(mul(g, h), gi))) return false; return true; });
const conjSub = (H, g) => { const gi = inv(g); return new Set([...H].map(h => mul(mul(g, h), gi))); };
const conjClass = (H) => { const m = new Map(); for (const g of G) m.set(key(conjSub(H, g)), conjSub(H, g)); return [...m.values()]; };
const cosets = (H) => { const seen = new Map(), out = []; for (const g of G) { const c = new Set([...H].map(h => mul(g, h))), k = key(c); if (!seen.has(k)) { seen.set(k, out.length); out.push(c); } } return { list: out, index: seen }; };
const permOf = (H, cs, g) => cs.list.map(c => cs.index.get(key(new Set([...c].map(x => mul(g, x))))));
const cyc = (p) => { const n = p.length, sn = new Array(n).fill(false), t = []; for (let i = 0; i < n; i++) { if (sn[i]) continue; let j = i, l = 0; while (!sn[j]) { sn[j] = true; j = p[j]; l++; } t.push(l); } return t.sort((a, b) => b - a).join('.'); };
const M = 6; // ord(XB)
ck('0  ord(X) = 6 = M', pow(XB, 6) === ID && pow(XB, 3) !== ID && pow(XB, 2) !== ID);

// 標的クラス(定理 K3 §2.2 と同じ選択)
let target = null;
for (const H of ALL) { if (H.size !== 18) continue; const cs = cosets(H); if (cyc(permOf(H, cs, XB)) === '6' && cyc(permOf(H, cs, YB)) === '2.2.1.1' && cyc(permOf(H, cs, ZB)) === '6' && normalizer(H).length === 18) { target = H; break; } }
ck('1  標的 H を再取得', target !== null);
const csT = cosets(target);
ck('V1 [P:H] = 6 = M かつ <X> は P/H 上推移的(全分岐)', csT.list.length === 6 && cyc(permOf(target, csT, XB)) === '6');
ck('V2 N_P(H) = H', normalizer(target).length === target.size);
const lam = conjClass(target); const lamK = lam.map(key);
ck('1b |Lambda| = 6 = M', lam.length === 6);

// V3: 「<X> が P/H 上推移的 かつ |Lambda| = ord(X) = 6」なら N_P(H) = H(悉皆)
let v3n = 0, v3bad = 0;
for (const H of ALL) { if (H.size === 108 || H.size === 1) continue; const cs = cosets(H); if (cyc(permOf(H, cs, XB)) !== String(cs.list.length)) continue; if (conjClass(H).length !== 6) continue; v3n++; if (normalizer(H).length !== H.size) v3bad++; }
ck('V3 <X> 推移的 かつ |Lambda| = ord(X) を満たす全 H で N_P(H) = H', v3bad === 0 && v3n > 0, `該当 H = ${v3n} 個, 反例 = ${v3bad}`);

// V4: P/H -> Lambda, gH |-> gHg^{-1} が <X>-同変な全単射
const cosToLam = csT.list.map(c => { const g = [...c][0]; return lamK.indexOf(key(conjSub(target, g))); });
const permX = permOf(target, csT, XB);
const tau = lam.map(C => lamK.indexOf(key(conjSub(C, XB))));
ck('V4 P/H -> Lambda は全単射かつ <X>-同変(左移動 <-> tau)',
  new Set(cosToLam).size === 6 && !cosToLam.includes(-1) && csT.list.every((_, i) => cosToLam[permX[i]] === tau[cosToLam[i]]));
ck('V4b tau は Lambda 上の 6-サイクル(単純推移)', cyc(tau) === '6');

// Phi_{m,k}(全 12 元)
const idx = new Map(G.map((g, i) => [g, i]));
const par = new Array(108).fill(-1), via = new Array(108).fill(-1), ord2 = [];
{ const q = [ID], sn = new Set([ID]); while (q.length) { const g = q.shift(); ord2.push(g); for (const [gi, gg] of [[0, XB], [1, YB]]) { const p = mul(g, gg); if (!sn.has(p)) { sn.add(p); par[idx.get(p)] = idx.get(g); via[idx.get(p)] = gi; q.push(p); } } } }
const autOf = (X2, Y2) => { const img = new Array(108).fill(-1); img[idx.get(ID)] = ID; for (const g of ord2) { const i = idx.get(g); if (g === ID) continue; img[i] = mul(img[par[i]], via[i] === 0 ? X2 : Y2); } if (new Set(img).size !== 108) return null; for (const g of G) { const i = idx.get(g); if (img[idx.get(mul(g, XB))] !== mul(img[i], X2) || img[idx.get(mul(g, YB))] !== mul(img[i], Y2)) return null; } return img; };
const kappa = (m) => (m % 2 === 1) ? m + 1 : -m;
const GTel = [];
for (const m of [0, 2, 3, 5]) for (let k = 0; k < 3; k++) { const u = 2 * m + 1, f = N([R(2 * k), R(-2 * k), R(kappa(m))]), fi = inv(f); GTel.push({ m, k, aut: autOf(pow(XB, u), mul(mul(fi, pow(YB, u)), f)) }); }
ck('2  GT(K^(3)) の 12 元がすべて Aut(G3) の元', GTel.length === 12 && GTel.every(s => s.aut !== null));
const applySub = (aut, H) => new Set([...H].map(h => aut[idx.get(h)]));
const stab = (aut) => lam.every(C => lamK.includes(key(applySub(aut, C))));
const F0el = GTel.filter(s => s.m === 0);
ck('V5 Lambda は Phi(F_0)(3 元)で安定', F0el.length === 3 && F0el.every(s => stab(s.aut)));
ck('V6 ★Lambda は Phi(GT(K^(3))) 全 12 元で安定(Q-model 側の前件・本稿の新規検査)', GTel.every(s => stab(s.aut)));

// V7: Aut(G3) 全体では安定でない(6+6 融合)。Aut は生成元像の全探索で構成。
let autAll = 0, autStab = 0;
const ordOf = (g) => { let n = 1, p = g; while (p !== ID) { p = mul(p, g); n++; } return n; };
for (const X2 of G) { if (ordOf(X2) !== ordOf(XB)) continue; for (const Y2 of G) { if (ordOf(Y2) !== ordOf(YB)) continue; const a = autOf(X2, Y2); if (!a) continue; autAll++; if (stab(a)) autStab++; } }
ck('V7 ★Aut(G3) 全体では Lambda は安定でない(V6 は自明でない)', autAll > autStab && autStab > 0, `|Aut(G3)| = ${autAll}, Lambda を保つ元 = ${autStab}`);

// V8: b-不変性(finite 版)
const comp = (p, q) => p.map((_, i) => q[p[i]]);
const T6 = []; { let p = lam.map((_, i) => i); for (let i = 0; i < 6; i++) { T6.push(p); p = comp(p, tau); } }
let v8ok = true;
for (const b of [1, 5]) { // (Z/6)^x
  // kappa: G_K -> mu_6 の像として可能な部分群 <z^t> について ord と ker が b で不変
  for (let t = 0; t < 6; t++) { const ordT = 6 / gcd(6, t), ordBT = 6 / gcd(6, (b * t) % 6); if (ordT !== ordBT) v8ok = false; if ((t === 0) !== (((b * t) % 6) === 0)) v8ok = false; }
  const gp = new Set(); for (let t = 0; t < 6; t++) gp.add(T6[(b * t) % 6].join(','));
  if (gp.size !== 6) v8ok = false;
}
function gcd(a, b) { return b ? gcd(b, a % b) : a; }
ck('V8 ★b in (Z/6)^x のひねりで ord(kappa) も ker(kappa) も tau(mu_6) も不変', v8ok);

console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
