// a5_dessin_unique.mjs -- (5,5,5)/次数5/monodromy A5 の dessin の一意性と、
// 5 個の A4 部分群 = D(v) の対応(比較補題 FC-6 の橋)を悉皆で確認。
const N = 5;
const idp = [1, 2, 3, 4, 5];
const key = (p) => p.join('');
const comp = (f, g) => g.map(i => f[i - 1]);        // (f∘g)(i) = f(g(i))
const inv = (f) => { const r = [0, 0, 0, 0, 0]; f.forEach((v, i) => r[v - 1] = i + 1); return r; };
const cycType = (f) => { const seen = new Array(6).fill(false); const t = []; for (let i = 1; i <= 5; i++) { if (seen[i]) continue; let l = 0, j = i; while (!seen[j]) { seen[j] = true; j = f[j - 1]; l++; } t.push(l); } return t.sort((a, b) => b - a).join(''); };
const sign = (f) => { let s = 1; for (let i = 0; i < 5; i++) for (let j = i + 1; j < 5; j++) if (f[i] > f[j]) s = -s; return s; };

// S5 全体
const S5 = [];
(function gen(cur, rest) { if (!rest.length) { S5.push(cur); return; } rest.forEach((v, i) => gen([...cur, v], rest.filter((_, j) => j !== i))); })([], idp);
const A5 = S5.filter(p => sign(p) === 1);
console.log('|S5| =', S5.length, ', |A5| =', A5.length);

const five = A5.filter(p => cycType(p) === '5');
console.log('5-サイクルの個数 =', five.length);

// (a,b,c) 全て 5-サイクル, abc = 1
const triples = [];
for (const a of five) for (const b of five) { const c = inv(comp(a, b)); if (cycType(c) === '5') triples.push([a, b, c]); }
console.log('(5,5,5) 三つ組 (abc=1) の総数 =', triples.length, '  [期待 192]');

const generates = (a, b) => { const seen = new Set([key(idp)]); const st = [idp]; while (st.length) { const x = st.pop(); for (const g of [a, b]) { const y = comp(x, g); if (!seen.has(key(y))) { seen.add(key(y)); st.push(y); } } } return seen.size; };
const gen60 = triples.filter(([a, b]) => generates(a, b) === 60);
console.log('A5 を生成する三つ組 =', gen60.length, '  [期待 120]');
console.log('残り(= C5 内)=', triples.length - gen60.length, '  [期待 72]');

// A5-軌道 / S5-軌道(同時共役)
function orbits(list, group) {
  const kk = (T) => T.map(key).join('|');
  const set = new Map(list.map(T => [kk(T), T]));
  const reps = []; const done = new Set();
  for (const [k, T] of set) { if (done.has(k)) continue; reps.push(T); for (const g of group) { const gi = inv(g); const U = T.map(p => comp(comp(g, p), gi)); done.add(kk(U)); } }
  return reps;
}
const oA = orbits(gen60, A5), oS = orbits(gen60, S5);
console.log('A5-軌道数 =', oA.length, '  [期待 2]');
console.log('S5-軌道数 =', oS.length, '  [期待 1 = dessin が一意]');

// Aut(被覆) = C_{S5}(A5)
const cent = S5.filter(g => A5.every(p => key(comp(g, p)) === key(comp(p, g))));
console.log('C_{S5}(A5) の位数 =', cent.length, '  [期待 1 ⇒ Aut(被覆)=1 ⇒ Q-モデルは一意・捻れなし]');

// ---- FC-6 の橋: D(v) --(q ↦ Fix q)--> {5 点}  が全単射 ----
const v = [2, 3, 4, 5, 1]; // (1 2 3 4 5)
const T2 = A5.filter(p => cycType(p) === '221');
const T3 = A5.filter(p => cycType(p) === '311');
const Dv = [];
for (const qq of T2) for (const rr of T3) if (key(comp(comp(qq, rr), v)) === key(idp)) Dv.push([qq, rr]);
console.log('D(v) = {(q,r): q∈2A, r∈3A, q r v = 1} の個数 =', Dv.length, '  [期待 5]');
const fix = (p) => { const f = []; for (let i = 1; i <= 5; i++) if (p[i - 1] === i) f.push(i); return f; };
const images = Dv.map(([qq]) => fix(qq));
console.log('各 q の不動点集合 =', JSON.stringify(images), ' [各 1 点・全 5 点を尽くす?]');
const ok = images.every(f => f.length === 1) && new Set(images.map(f => f[0])).size === 5;
console.log(ok ? 'PASS  (q,r) ↦ Fix(q) は D(v) → {1..5} の全単射(⟨v⟩-同変・Aut(A5)-自然)' : '*** FAIL');
// ⟨v⟩ 同変性
const vconj = ([qq, rr]) => [comp(comp(v, qq), inv(v)), comp(comp(v, rr), inv(v))];
let equiv = true;
for (const d of Dv) { const d2 = vconj(d); const inD = Dv.some(e => key(e[0]) === key(d2[0]) && key(e[1]) === key(d2[1])); const f1 = fix(d[0])[0], f2 = fix(d2[0])[0]; if (!inD || v[f1 - 1] !== f2) equiv = false; }
console.log(equiv ? 'PASS  ⟨v⟩-同変性: Fix(v q v^{-1}) = v·Fix(q)' : '*** FAIL 同変性');
if (!ok || !equiv) process.exitCode = 1;
