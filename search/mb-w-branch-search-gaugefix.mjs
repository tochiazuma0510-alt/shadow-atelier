// mb-w-branch-search-gaugefix.mjs — 枝(W)探索・gauge 固定版(a2 in {1,-1} に
// 固定し a0,a1 をより広く走査する補完探索)。正規形・判定基準は
// mb-w-branch-search.mjs と同一(Rule 1 M2 の残余トーラス tau: a_i -> a_i/tau^{2i-5}
// の作用で a2(重み tau^{-1} 相当)を 1 に正規化できる場合をカバーする)。
import { testCandidate } from './mb-w-branch-search.mjs';

function main() {
  const BOUND = Number(process.env.MB_W_BOUND2 || 60);
  const hits = [];
  const errors = [];
  let tested = 0;
  const t0 = Date.now();
  for (const a2 of [1, -1]) {
    for (let a1 = -BOUND; a1 <= BOUND; a1++) {
      for (let a0 = -BOUND; a0 <= BOUND; a0++) {
        tested++;
        try {
          const r = testCandidate(a0, a1, a2);
          if (r.ok) hits.push(r);
        } catch (e) {
          errors.push({ a0, a1, a2, error: String(e && e.message || e) });
        }
      }
    }
  }
  const elapsedMs = Date.now() - t0;
  console.log(JSON.stringify({
    schema: 'mb/w-branch-search-gaugefix/v1',
    branch: 'W',
    note: 'a2 を {1,-1} に固定し a0,a1 を広く走査する補完探索(残余トーラスで a2 を正規化できる場合をカバー)',
    search_bound_a0_a1: BOUND,
    tested, hits, error_count: errors.length, errors: errors.slice(0, 20),
    elapsed_ms: elapsedMs,
    contact_discipline: '本探索器は c の値・平方類・平方因子・符号を一切計算していない。',
  }, null, 2));
}
main();
