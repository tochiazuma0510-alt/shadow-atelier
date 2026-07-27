// mb-polyops-selftest.mjs — mb-polyops.mjs の自己検算(既知の手計算例と突合)。
// 探索器の内部自己テストであり、crosscheck/ の照合器ではない
// (照合器は別途、証明書だけを入力に独立実装する)。

import { Frac, F0, F1 } from './mb-frac.mjs';
import { polyAdd, polySub, polyMul, polyDerivative, polyDivMod, polyGCD, polyMonic, polyEqual, polyToString } from './mb-polyops.mjs';

function fr(x) { return Frac.from(x); }
function P(...coeffsLowToHigh) { return coeffsLowToHigh.map(fr); }

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; }
  else { fail++; console.error(`FAIL: ${name} ${detail || ''}`); }
}

// 1. (x+1)*(x-1) = x^2-1
{
  const a = P(1, 1);   // 1+x
  const b = P(-1, 1);  // -1+x
  const prod = polyMul(a, b);
  check('mul (x+1)(x-1)=x^2-1', polyEqual(prod, P(-1, 0, 1)), polyToString(prod));
}

// 2. derivative of x^3+2x^2+3x+4 = 3x^2+4x+3
{
  const p = P(4, 3, 2, 1); // 4+3x+2x^2+x^3
  const dp = polyDerivative(p);
  check('deriv x^3+2x^2+3x+4', polyEqual(dp, P(3, 4, 3)), polyToString(dp));
}

// 3. division: (x^3-1) / (x-1) = x^2+x+1, rem 0
{
  const p = P(-1, 0, 0, 1); // x^3-1
  const q = P(-1, 1);       // x-1
  const { quot, rem } = polyDivMod(p, q);
  check('div (x^3-1)/(x-1) quot', polyEqual(quot, P(1, 1, 1)), polyToString(quot));
  check('div (x^3-1)/(x-1) rem=0', rem.length === 0, polyToString(rem));
}

// 4. GCD: gcd(x^2-1, x^2-3x+2) = (x-1) up to scalar
{
  const p = P(-1, 0, 1);     // x^2-1 = (x-1)(x+1)
  const q = P(2, -3, 1);     // x^2-3x+2 = (x-1)(x-2)
  const g = polyMonic(polyGCD(p, q));
  check('gcd(x^2-1,x^2-3x+2)=x-1', polyEqual(g, P(-1, 1)), polyToString(g));
}

// 5. 合成テスト: h = f6*p2^2 の分解を検出できるか
// f6 = x^6+x+1 (squarefree の想定), p2 = x^2+1
{
  const f6 = P(1, 1, 0, 0, 0, 0, 1); // 1+x+x^6
  const p2 = P(1, 0, 1);             // 1+x^2
  const p2sq = polyMul(p2, p2);
  const h = polyMul(f6, p2sq);
  const hp = polyDerivative(h);
  const g = polyMonic(polyGCD(h, hp));
  check('recovered p2 from h via gcd(h,h\')', polyEqual(g, p2), polyToString(g));
  const { quot, rem } = polyDivMod(h, polyMul(g, g));
  check('recovered f6 via h/p2^2', polyEqual(quot, f6), polyToString(quot));
  check('exact division remainder is zero', rem.length === 0, polyToString(rem));
}

// 6. negative control: h = x^6+x^5+1 (no repeated factor expected generically)
// gcd(h,h') should have degree 0 for a generic squarefree sextic-ish poly.
{
  const h = P(1, 0, 0, 0, 0, 1, 1); // 1+x^5+x^6
  const hp = polyDerivative(h);
  const g = polyGCD(h, hp);
  const dg = g.length - 1;
  check('generic poly has gcd(h,h\') degree <=0 (squarefree)', g.length === 0 || dg === 0, `deg=${dg}`);
}

console.log(JSON.stringify({ schema: 'mb/polyops-selftest/v1', pass, fail }, null, 2));
if (fail > 0) process.exit(1);
