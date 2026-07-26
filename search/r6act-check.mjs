// R6-act の縮約(rho_0(F_0) = tau(mu_M[e]))の検算 — scratchpad 単発。
// D1 (3.6)(4.9)(4.12) から G3 <= D3^3 を再構成し、標的クラス Lambda(6 元)上で
//   (i) Phi_{0,k}(xbar) = xbar,
//   (ii) rho_Lambda(F_0) が <xbar>-平行移動群 tau(mu_6) の中に入る,
//   (iii) rho_Lambda(F_0) = tau(mu_6[3]) = <tau^2>,
//   (iv) 【W2 対照】型 3.3 だけでは部分群を同定しない(S_6 内の型 3.3 の C_3 は 20 個)
// を確認する。
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
const H18 = [...subs.values()].filter(s => s.size === 18);
const normalizer = (H) => G.filter(g => { const gi = inv(g); for (const h of H) if (!H.has(mul(mul(g, h), gi))) return false; return true; });
const conjSub = (H, g) => { const gi = inv(g); return new Set([...H].map(h => mul(mul(g, h), gi))); };
const conjClass = (H) => { const m = new Map(); for (const g of G) m.set(key(conjSub(H, g)), conjSub(H, g)); return [...m.values()]; };
const cosets = (H) => { const seen = new Map(), out = []; for (const g of G) { const c = new Set([...H].map(h => mul(g, h))), k = key(c); if (!seen.has(k)) { seen.set(k, out.length); out.push(c); } } return { list: out, index: seen }; };
const permOf = (H, cs, g) => cs.list.map(c => cs.index.get(key(new Set([...c].map(x => mul(g, x))))));
const cyc = (p) => { const n = p.length, sn = new Array(n).fill(false), t = []; for (let i = 0; i < n; i++) { if (sn[i]) continue; let j = i, l = 0; while (!sn[j]) { sn[j] = true; j = p[j]; l++; } t.push(l); } return t.sort((a, b) => b - a).join('.'); };

// 標的クラス: ordered passport (6, 2^2 1^2, 6)・N_G(H)=H
let target = null;
for (const H of H18) { const cs = cosets(H); const tX = cyc(permOf(H, cs, XB)), tY = cyc(permOf(H, cs, YB)), tZ = cyc(permOf(H, cs, ZB)); if (tX === '6' && tY === '2.2.1.1' && tZ === '6' && normalizer(H).length === 18) { target = H; break; } }
ck('A  標的クラスの H が存在(ordered passport (6,2^2 1^2,6)・N_G(H)=H)', target !== null);
const lam = conjClass(target); const lamK = lam.map(key);
ck('B  |Lambda| = 6', lam.length === 6);

// tau: <xbar> の Lambda 上の平行移動
const tau = lam.map(C => lamK.indexOf(key(conjSub(C, XB))));
ck('C  tau(xbar) は Lambda 上の 6-サイクル(単純推移)', cyc(tau) === '6');
const comp = (p, q) => p.map((_, i) => q[p[i]]);
const T6 = []; { let p = lam.map((_, i) => i); for (let i = 0; i < 6; i++) { T6.push(p); p = comp(p, tau); } }
const T6K = new Set(T6.map(p => p.join(',')));

// Aut と F_0
const idx = new Map(G.map((g, i) => [g, i]));
const par = new Array(108).fill(-1), via = new Array(108).fill(-1), ord2 = [];
{ const q = [ID], sn = new Set([ID]); while (q.length) { const g = q.shift(); ord2.push(g); for (const [gi, gg] of [[0, XB], [1, YB]]) { const p = mul(g, gg); if (!sn.has(p)) { sn.add(p); par[idx.get(p)] = idx.get(g); via[idx.get(p)] = gi; q.push(p); } } } }
const autOf = (X2, Y2) => { const img = new Array(108).fill(-1); img[idx.get(ID)] = ID; for (const g of ord2) { const i = idx.get(g); if (g === ID) continue; img[i] = mul(img[par[i]], via[i] === 0 ? X2 : Y2); } if (new Set(img).size !== 108) return null; for (const g of G) { const i = idx.get(g); if (img[idx.get(mul(g, XB))] !== mul(img[i], X2) || img[idx.get(mul(g, YB))] !== mul(img[i], Y2)) return null; } return img; };
const kappa = (m) => (m % 2 === 1) ? m + 1 : -m;
const F0 = [];
for (let k = 0; k < 3; k++) { const m = 0, u = 2 * m + 1, f = N([R(2 * k), R(-2 * k), R(kappa(m))]), fi = inv(f); F0.push({ k, X2: pow(XB, u), Y2: mul(mul(fi, pow(YB, u)), f), aut: autOf(pow(XB, u), mul(mul(fi, pow(YB, u)), f)) }); }
ck('D  F_0 の 3 元はすべて Aut(G3) の元', F0.every(s => s.aut !== null));
ck('E  ★Phi_{0,k}(xbar) = xbar  (chi~ = u_0 = 1 ゆえ) — 縮約の要', F0.every(s => s.X2 === XB));

const applySub = (aut, H) => new Set([...H].map(h => aut[idx.get(h)]));
const rho = F0.map(s => lam.map(C => lamK.indexOf(key(applySub(s.aut, C)))));
ck('F  rho_Lambda(F_0) は Lambda を保つ・忠実(3 個相異)', rho.every(p => p.every(v => v >= 0)) && new Set(rho.map(p => p.join(','))).size === 3);
ck('G  ★rho_Lambda(F_0) ⊆ tau(mu_6)  (平行移動群の中に入る)', rho.every(p => T6K.has(p.join(','))));
const T3K = new Set([T6[0], T6[2], T6[4]].map(p => p.join(',')));
ck('H  ★rho_Lambda(F_0) = tau(mu_6[3]) = <tau^2>', new Set(rho.map(p => p.join(','))).size === 3 && rho.every(p => T3K.has(p.join(','))));
// 直接検算: rho は tau と可換
ck('I  rho_Lambda(F_0) の各元は tau と可換', rho.every(p => comp(p, tau).join(',') === comp(tau, p).join(',')));

// 【W2 対照】型 3.3 だけでは部分群を同定しない
const perms = []; const permute = (a, l) => { if (!l.length) { perms.push(a); return; } for (let i = 0; i < l.length; i++) permute([...a, l[i]], l.filter((_, j) => j !== i)); };
permute([], [0, 1, 2, 3, 4, 5]);
const t33 = perms.filter(p => cyc(p) === '3.3');
const c3subs = new Set(t33.map(p => { const q = comp(p, p); return [p.join(','), q.join(',')].sort().join('|'); }));
ck('J  【W2 対照】S_6 の型 3.3 の元は 40 個・それが生成する C_3 は 20 個 — 型だけでは 1 個に定まらない',
  t33.length === 40 && c3subs.size === 20, `elts=${t33.length}, C_3 subgroups=${c3subs.size}`);
console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
