// mb-w-branch-search-rational.mjs — 委嘱2(Model-Builder)探索器・枝 (W) の
// 非整数有理数拡張(委嘱1 §5 の残された工程 1「非整数有理数」の実行)。
//
// 委嘱1 の 3 走査(bound12/bound20/gaugefix-60)はいずれも a0,a1,a2 を
// **整数**に限っていた。しかし正規形 (3.2')
//   y^2 = a(x)^2+x^5,  a=a0+a1x+a2x^2 (deg a<=2)
// 自体は a_i in Q を許す(整数制約は M3/M4 の denominator-clearing の
// 便宜であって、正規形の要求ではない)。残余ゲージ tau(3.2'')は
// a_i -> tau^(2i-5) a_i という連続 Q^x 作用であり、その軌道上の点は
// 一般に非整数の代表元を持つ。本探索器は a_i = n_i/D(共通分母 D)の形で
// 小さい分母をスキャンし、整数格子だけでは踏めない有理点を試す。
//
// 判定は mb-w-branch-search.mjs の testCandidateFrac をそのまま再利用する
// (同一の exact 判定アルゴリズム・禁止事項の遵守は元ファイルの説明を継承)。

import { Frac } from './mb-frac.mjs';
import { testCandidateFrac } from './mb-w-branch-search.mjs';

function fr(x) { return Frac.from(x); }

function main() {
  const NUM_BOUND = Number(process.env.MB_WRAT_NUM_BOUND || 12); // |n_i| <= NUM_BOUND
  const DENOMS = (process.env.MB_WRAT_DENOMS || '2,3').split(',').map(s => Number(s.trim())).filter(d => d >= 2);
  const hits = [];
  const errors = [];
  const skips = [];
  let tested = 0;
  const t0 = Date.now();

  for (const D of DENOMS) {
    for (let n2 = -NUM_BOUND; n2 <= NUM_BOUND; n2++) {
      for (let n1 = -NUM_BOUND; n1 <= NUM_BOUND; n1++) {
        for (let n0 = -NUM_BOUND; n0 <= NUM_BOUND; n0++) {
          // 分母 D で「本質的に非整数」(少なくとも 1 個が D で割り切れない)
          // ものだけに絞る — 整数格子の再走(委嘱1 と重複)を避ける。
          if (n0 % D === 0 && n1 % D === 0 && n2 % D === 0) continue;
          tested++;
          const aFrac = [new Frac(BigInt(n0), BigInt(D)), new Frac(BigInt(n1), BigInt(D)), new Frac(BigInt(n2), BigInt(D))];
          try {
            const r = testCandidateFrac(aFrac, `n=(${n0},${n1},${n2})/${D}`);
            if (r.ok) hits.push(r);
            else if (r.skip) skips.push({ n0, n1, n2, D, reason: r.reason });
          } catch (e) {
            errors.push({ n0, n1, n2, D, error: String(e && e.message || e) });
          }
        }
      }
    }
  }
  const elapsedMs = Date.now() - t0;
  const integrityFlag = skips.length > 0 || errors.length > 0;
  const result = {
    schema: 'mb/w-branch-search-rational/v2',
    branch: 'W',
    normal_form: 'y^2=a(x)^2+x^5, a=(a0,a1,a2) in Q^3 with common denominator D, a2 x^2+a1 x+a0',
    num_bound: NUM_BOUND,
    denominators_tried: DENOMS,
    tested,
    hits,
    skip_count: skips.length,
    skips,
    error_count: errors.length,
    errors: errors.slice(0, 20),
    integrity_flag: integrityFlag,
    elapsed_ms: elapsedMs,
    contact_discipline: '本探索器は c(lambda=c*mu^2 の定数)の値・平方類・平方因子・符号を一切計算していない。出力は a(x) の有理係数(文字列)と D(v) の構造検査結果(k, h)のみ。',
    note: '整数格子(委嘱1: bound12/bound20/gaugefix-60)と重複しないよう、少なくとも1成分が D で割り切れない有理点だけを試した(positive-only・非網羅)。',
  };
  console.log(JSON.stringify(result, null, 2));
  if (integrityFlag) process.exitCode = 2;
}

if (import.meta.url === `file://${process.argv[1]}` || import.meta.url.endsWith(process.argv[1]?.replace(/\\/g,'/'))) {
  main();
}
