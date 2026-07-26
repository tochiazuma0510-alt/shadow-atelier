// week4-19a19e.mjs — 委嘱 20: 【GAP-19a】exact conjugator と【GAP-19e】Aut(G₃)-軌道
// 正本 = D1 抽出 (3.1)(3.6)。置換はすべて 1-indexed(p[i-1] = i の像)で統一。
const OK = []; const chk = (n, ok, d = '') => { OK.push(ok); console.log(`${ok ? 'PASS' : '*** FAIL'}  ${n}${d ? '  :: ' + d : ''}`); };

//////////////////// G₃ ≤ D₃³ ////////////////////
const n = 3;
const dm = (a, b) => [((a[0] + (a[1] ? -b[0] : b[0])) % n + n) % n, a[1] ^ b[1]];
const di = (a) => a[1] ? a : [(n - a[0]) % n, 0];
const T = (a, b) => [dm(a[0], b[0]), dm(a[1], b[1]), dm(a[2], b[2])];
const Ti = (a) => a.map(di);
const gk = (t) => t.map(c => c.join('')).join('|');
const r = [1, 0], s = [0, 1], rs = dm(r, s), e1 = [0, 0], E = [e1, e1, e1];
const X = [r, s, s], Y = [rs, r, rs], Z = [dm(dm(r, r), s), dm(di(r), s), r];   // (3.1)(3.6)
const seen = new Map([[gk(E), E]]); { const st = [E];
  while (st.length) { const a = st.pop(); for (const g of [X, Y]) { const b = T(a, g); if (!seen.has(gk(b))) { seen.set(gk(b), b); st.push(b); } } } }
const els = [...seen.values()];
const gord = (g) => { let k = 1, p = g; while (gk(p) !== gk(E)) { p = T(p, g); k++; } return k; };
const closure = (gs) => { const S = new Set([gk(E)]); const q = [E];
  while (q.length) { const p = q.pop(); for (const g of gs) { const t = T(p, g); if (!S.has(gk(t))) { S.add(gk(t)); q.push(t); } } } return S; };
chk('(0) |G₃| = 108、passport = (6,6,6)', els.length === 108 && [X, Y, Z].every(g => gord(g) === 6));

//////////////////// S₆(1-indexed) ////////////////////
const id6 = [1, 2, 3, 4, 5, 6];
const cmp = (f, g) => id6.map(i => f[g[i - 1] - 1]);              // (f∘g)(i) = f(g(i))
const pinv = (f) => { const o = [0, 0, 0, 0, 0, 0]; f.forEach((v, i) => o[v - 1] = i + 1); return o; };
const pk = (f) => f.join('');
const ptype = (f) => { const sn = Array(7).fill(false), t = [];
  for (let i = 1; i <= 6; i++) { if (sn[i]) continue; let l = 0, j = i; while (!sn[j]) { sn[j] = true; j = f[j - 1]; l++; } t.push(l); }
  return t.sort((a, b) => b - a).join(''); };
const S6 = []; (function g(c, rest) { if (!rest.length) { S6.push(c); return; } rest.forEach((v, i) => g([...c, v], rest.filter((_, j) => j !== i))); })([], id6);
const pgen = (gs) => { const S = new Set([pk(id6)]); const q = [id6];
  while (q.length) { const p = q.pop(); for (const g of gs) { const t = cmp(p, g); if (!S.has(pk(t))) { S.add(pk(t)); q.push(t); } } } return S; };

//////////////////// 次数 6 表現(H: |H| = 18, H∩⟨x̄⟩ = 1) ////////////////////
const xpow = []; { let p = E; for (let i = 0; i < 6; i++) { xpow.push(p); p = T(p, X); } }
const subs = new Map();
for (const a of els) for (const b of els) { const c = closure([a, b]); if (c.size !== 18) continue;
  const k = [...c].sort().join(','); if (!subs.has(k)) subs.set(k, c); }
const cand = [...subs.values()].filter(H => xpow.every((p, i) => i === 0 || !H.has(gk(p))));
const rep6 = (H) => {                                            // 左剰余類上の置換表現(1-indexed)
  const cos = []; const asg = new Set();
  for (const g of els) { if (asg.has(gk(g))) continue; const cs = new Set();
    for (const hk2 of H) { const h = els.find(t => gk(t) === hk2); cs.add(gk(T(g, h))); }
    for (const t of cs) asg.add(t); cos.push(cs); }
  const io = (g) => cos.findIndex(cs => cs.has(gk(g))) + 1;
  const pm = (g) => cos.map(cs => io(T(g, els.find(t => cs.has(gk(t))))));
  return { px: pm(X), py: pm(Y), pz: pm(Z), img: [...new Set(els.map(g => pk(pm(g))))].map(t => t.split('').map(Number)) };
};
const info = cand.map(H => { const R = rep6(H);
  const cent = S6.filter(p => R.img.every(g => pk(cmp(p, g)) === pk(cmp(g, p)))).length;
  return { H, ...R, cent, ord: R.img.length }; });
const good = info.filter(t => t.cent === 1);
chk('(1) H の候補 18 個・うち中心化群 1 のものが 12 個・像の位数 36', cand.length === 18 && good.length === 12 && good.every(t => t.ord === 36),
    `候補 ${cand.length}、cent=1 が ${good.length}、像の位数 ${[...new Set(good.map(t => t.ord))]}`);

//////////////////// 【GAP-19e】Aut(G₃)-軌道 ////////////////////
const auts = [];
for (const a of els) { if (gord(a) !== 6) continue; for (const b of els) { if (gord(b) !== 6) continue;
  if (gord(Ti(T(a, b))) !== 6) continue; if (closure([a, b]).size !== 108) continue;
  const map = new Map([[gk(E), E]]); const st = [[E, E]]; let ok = true;
  while (st.length && ok) { const [p, ip] = st.pop();
    for (const [g, ig] of [[X, a], [Y, b]]) { const q = T(p, g), iq = T(ip, ig);
      if (map.has(gk(q))) { if (gk(map.get(gk(q))) !== gk(iq)) ok = false; } else { map.set(gk(q), iq); st.push([q, iq]); } } }
  if (ok && new Set([...map.values()].map(gk)).size === 108) auts.push(map); } }
const hkey = (H) => [...H].sort().join(',');
const goodSet = new Set(good.map(t => hkey(t.H)));
const orbits = []; const done = new Set();
for (const t of good) { if (done.has(hkey(t.H))) continue;
  const orb = new Set();
  for (const al of auts) orb.add([...t.H].map(x => gk(al.get(x))).sort().join(','));
  for (const o of orb) done.add(o);
  orbits.push({ size: orb.size, inGood: [...orb].filter(o => goodSet.has(o)).length }); }
chk('(2)【GAP-19e】中心化群 1 の H = 12 個 が Aut(G₃)-軌道**ちょうど 1 つ**をなす',
    orbits.length === 1 && orbits[0].inGood === 12,
    `|Aut(G₃)| = ${auts.length}、軌道 = ${JSON.stringify(orbits)}`);

//////////////////// 【GAP-19a】exact conjugator ////////////////////
// 6T9 標準代表 = 位数 36 層の辞書式最小三つ組。
// ★ λ 割当を我々の対象に合わせる: (x̄,ȳ,z̄) = (0,1,∞) 上で型 (6, 2²1², 6)。
const A6 = S6.filter(f => ptype(f) === '6');
let rep = null;
for (const a of A6) { for (const b of S6) { if (ptype(b) !== '2211') continue;
  const c = pinv(cmp(a, b)); if (ptype(c) !== '6') continue; if (pgen([a, b]).size !== 36) continue; rep = [a, b, c]; break; } if (rep) break; }
console.log(`\n6T9 標準代表(辞書式最小・型 (6,2²1²,6)): σ₀ = [${rep[0]}]  σ₁ = [${rep[1]}]  σ∞ = [${rep[2]}]`);
const t0 = good[0];
console.log(`G₃ 側(good[0] の次数 6 表現): x̄ = [${t0.px}]  ȳ = [${t0.py}]  z̄ = [${t0.pz}]`);
const hs = S6.filter(h => { const hi = pinv(h);
  return pk(cmp(cmp(h, t0.px), hi)) === pk(rep[0]) && pk(cmp(cmp(h, t0.py), hi)) === pk(rep[1]); });
chk('(3)【GAP-19a】exact conjugator h が存在し**一意**(⇔ 三つ組の同時中心化群が自明)', hs.length === 1,
    hs.length ? `h = [${hs[0]}](${hs.length} 個)` : 'なし');
if (hs.length) { const h = hs[0], hi = pinv(h);
  chk('(3b) 検算: h x̄ h⁻¹ = σ₀、h ȳ h⁻¹ = σ₁、**h z̄ h⁻¹ = σ∞**(三本目は独立検査)',
      pk(cmp(cmp(h, t0.px), hi)) === pk(rep[0]) && pk(cmp(cmp(h, t0.py), hi)) === pk(rep[1]) && pk(cmp(cmp(h, t0.pz), hi)) === pk(rep[2]));
  chk('(3c) 積の規約: x̄·ȳ·z̄ = id(左作用合成)', pk(cmp(cmp(t0.px, t0.py), t0.pz)) === pk(id6));
}
// ブロック構造(6T6-a との識別子)
{ const G = t0.img; const blocks = [];
  for (let msk = 1; msk < 64; msk++) { const B = []; for (let i = 0; i < 6; i++) if (msk >> i & 1) B.push(i + 1);
    if (!B.includes(1) || B.length === 1 || B.length === 6 || 6 % B.length) continue;
    const ok = G.every(g => { const im = B.map(i => g[i - 1]).sort().join(','); const b0 = B.slice().sort().join(',');
      return im === b0 || B.every(i => !im.split(',').map(Number).includes(i)); });
    if (ok) blocks.push(B.join('')); }
  chk('(4) ブロック構造 = サイズ 3 × 2 個(⇒ primitivization は次数 2。LMFDB 6T6-a は次数 3 で別物)',
      blocks.length > 0 && blocks.every(b => b.length === 3), `1 を含む非自明ブロック: ${blocks.join(' ')}`);
}

console.log(`\n==== ${OK.filter(Boolean).length}/${OK.length} PASS ====`);
if (OK.some(v => !v)) process.exitCode = 1;
