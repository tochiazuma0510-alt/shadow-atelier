// crosscheck/check-kummer.mjs
// Rule 1 SS8 exact Kummer 判定器の独立照合器。
// search/kummer-decide.g の GAP 実装(Factors ベース)とは**別のアルゴリズム**
// で同じ命題「w は K=Q(zeta_n) の M 乗か」を判定する(GAP のコード・
// 中間結果は import しない。読むのは kummer-decide.g が書き出した
// 証明書 JSON の中の w / ord / witness 数値だけ)。
//
// 便 34 P6-K1 (Sol 便 34 blocker 3 後半 / F4.4): 従来は最終 ord の数値
// 比較だけで、(a) witness が満たすべき正しい等式 witness^M = w^ord の検算、
// (b) ord の最小性(証明書の minimality_obstructions が主張する「約数 d' は
// M 乗でない」)の独立検算、をしていなかった。本版は
// crosscheck/cyclo-ring-lib.mjs(円分多項式の環演算・GAP を import しない
// 独立実装)を使って witness^M = w^ord を厳密に再検算し、かつ
// minimality_obstructions の各エントリを独立アルゴリズム(下記
// isMthPowerInK)で再判定する。
//
// 独立アルゴリズムの根拠(exact・非発見的):
//  (a) K=Q(zeta_n) は Q 上アーベル拡大 -- アーベル群の部分群はすべて正規
//      なので K の任意の部分体は Q 上アーベル(ガロア)。
//  (b) 奇素数 p と有理数 w について、X^p-w は「w が Q で p 乗」でない限り
//      Q 上既約(古典的事実)。既約かつ次数 p (>1) の拡大 Q(w^{1/p}) が
//      アーベルになるのは Q(zeta_p) 込みで次数 p(p-1) の分解体がアーベルに
//      潰れる場合のみだが [Q(zeta_p):Q]=p-1 と p は互いに素(p 素数)なので
//      次数 p の巡回群が (p-1 の巡回) と両立するのは自明拡大のときだけ。
//      ゆえに: **奇素数 p では w が K で p 乗 <=> w が Q で p 乗**。
//  (c) p=2 は例外(K は虚二次部分体を複数持ちうる)。K=Q(zeta_n) の二次
//      部分体の判別式 d は「導手 cond(d) が n を割る」squarefree 整数
//      (古典的な円分体の理論)。w (rational, 非零) が K で平方 <=>
//      ある登録済み d についてw*d が Q で平方。
//      本ファイルは n in {12, 20} の**事前登録された**二次部分体の
//      判別式表のみを使う(それ以外の n は UNKNOWN)。
//        n=12: Q(zeta_12) = Q(i, sqrt(3))  -> d in {1, -1, -3, 3}
//        n=20: Q(zeta_20) つまり Q(i, sqrt(5)) (Rule1 SS8.5 に同じ記載:
//              「K の二次部分体は Q(i), Q(sqrt5), Q(sqrt(-5))」)
//                                            -> d in {1, -1, 5, -5}
//
// 入力: kummer-decide.g が書いた証明書 JSON(w, M, ord, witness)。
// 出力: 独立算出した ord と一致するかどうかの照合レポート。

import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { Q as RingQ, polyPowMod, polyEqConst, cyclotomicPolynomialAscending } from './cyclo-ring-lib.mjs';

function gcdBig(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }
// --- 司令塔追加委嘱(裁定41 対応中・便40 F1.2 の水準を横展開): u-compare 系
// と同じ strict rational literal grammar(全文一致・符号付き整数 or 分子/
// 分母一組だけ・分母 0 拒否・d>0 invariant)。malformed rational は
// RationalFormatError を throw し、末尾の実行ブロックの catch が structured
// INTEGRITY_STOP に変換する。
// **司令塔独自攻撃(裁定41続報)修理**: trim を廃止し、入力文字列そのままが
// 正規表現に一致することを要求する(先頭/末尾空白混入は拒否)。 ---
class RationalFormatError extends Error {}
const RATIONAL_LITERAL_RE = /^([+-]?\d+)(?:\/([+-]?\d+))?$/;
function parseRatMaybeNumber(x) {
  if (typeof x === 'number') { return ratFromNumber(x); }
  const s = String(x);
  const m = RATIONAL_LITERAL_RE.exec(s);
  if (!m) {
    throw new RationalFormatError(
      `malformed rational literal ${JSON.stringify(x)}: must match ^[+-]?\\d+(/[+-]?\\d+)?$ ` +
      `(signed integer, or exactly one numerator/denominator pair)`
    );
  }
  const nRaw = BigInt(m[1]);
  const dRaw = m[2] !== undefined ? BigInt(m[2]) : 1n;
  if (dRaw === 0n) {
    throw new RationalFormatError(`malformed rational literal ${JSON.stringify(x)}: denominator is zero`);
  }
  const r = norm(nRaw, dRaw);
  if (r.d <= 0n) {
    throw new RationalFormatError(`internal invariant violated: reduced denominator is not positive for ${JSON.stringify(x)} (n=${r.n}, d=${r.d})`);
  }
  return r;
}
function ratFromNumber(x) {
  if (!Number.isInteger(x)) throw new Error('non-integer JSON number encountered for w (unexpected for this fixture)');
  return norm(BigInt(x), 1n);
}
function norm(n, d) { if (d < 0n) { n = -n; d = -d; } const g = gcdBig(n, d) || 1n; return { n: n / g, d: d / g }; }
function ratMul(a, b) { return norm(a.n * b.n, a.d * b.d); }
function ratPow(a, k) {
  if (k === 0) return norm(1n, 1n);
  if (k > 0) { let r = norm(1n, 1n); for (let i = 0; i < k; i++) r = ratMul(r, a); return r; }
  const p = ratPow(a, -k); return norm(p.d, p.n);
}
function ratEq(a, b) { return a.n === b.n && a.d === b.d; }

// 整数 n の素因数分解(絶対値・符号は別途扱う)
function factorizeAbs(n) {
  n = n < 0n ? -n : n;
  const f = new Map();
  let d = 2n;
  while (d * d <= n) {
    while (n % d === 0n) { f.set(d, (f.get(d) ?? 0) + 1); n /= d; }
    d += 1n;
  }
  if (n > 1n) f.set(n, (f.get(n) ?? 0) + 1);
  return f;
}

// 有理数が(符号込みで)整数 p 乗かどうか(p は素数、正または負の w を許す;
// p が奇数なら符号も p 乗根に吸収できるので自由、p が偶数(=2)ならここでは
// 呼ばない -- 二次の場合は下の quadratic subfield ルートを使う)
function isPerfectPthPowerInQ_odd(w, pBig) {
  // w = sign * n/d (既約・d>0)。奇素数 p: sign 自体 (+-1) は (+-1)^p = 同じ符号 なので
  // 常に p 乗根で吸収可能。n,d の素因数がすべて p の倍数指数であればよい。
  const p = Number(pBig);
  const nAbs = w.n < 0n ? -w.n : w.n;
  const fn = factorizeAbs(nAbs);
  const fd = factorizeAbs(w.d);
  for (const [, e] of fn) if (e % p !== 0) return false;
  for (const [, e] of fd) if (e % p !== 0) return false;
  return true; // sign は奇数乗根で吸収可能なので判定に影響しない
}

// 有理数が(非負であれば)Q で平方かどうか(整数指数がすべて偶数)
function isPerfectSquareInQ(w) {
  if (w.n < 0n) return false; // 実平方は負にならない(実根の意味での「Q の平方」)
  const fn = factorizeAbs(w.n);
  const fd = factorizeAbs(w.d);
  for (const [, e] of fn) if (e % 2 !== 0) return false;
  for (const [, e] of fd) if (e % 2 !== 0) return false;
  return true;
}

const QUADRATIC_SUBFIELD_DISCRIMINANTS = {
  12: [1n, -1n, -3n, 3n],   // Q(zeta_12) = Q(i, sqrt(3)) = Q(i, sqrt(-3))
  20: [1n, -1n, 5n, -5n],   // Rule1 SS8.5: K の二次部分体は Q(i), Q(sqrt5), Q(sqrt(-5))
};

// w (rational, != 0) が K=Q(zeta_n) で平方か(独立・非 Factors 判定)
function isSquareInK(w, n) {
  const table = QUADRATIC_SUBFIELD_DISCRIMINANTS[n];
  if (!table) return { decided: false, reason: `n=${n} の二次部分体判別式表が未登録 -- UNKNOWN` };
  for (const dRaw of table) {
    const d = norm(dRaw, 1n);
    const wd = ratMul(w, d);
    if (isPerfectSquareInQ(wd)) return { decided: true, isPower: true, viaDiscriminant: dRaw.toString() };
  }
  return { decided: true, isPower: false };
}

// w (rational) が K=Q(zeta_n) で p 乗か (p は M の素因数, p=2 or 奇素数)
function isPthPowerInK(w, p, n) {
  if (p === 2n) return isSquareInK(w, n);
  return { decided: true, isPower: isPerfectPthPowerInQ_odd(w, p) };
}

function primeFactorsDistinct(M) {
  let m = M; const ps = [];
  let d = 2n;
  while (d * d <= m) { if (m % d === 0n) { ps.push(d); while (m % d === 0n) m /= d; } d += 1n; }
  if (m > 1n) ps.push(m);
  return ps;
}

function divisorsOf(M) {
  const ds = [];
  for (let d = 1n; d <= M; d++) if (M % d === 0n) ds.push(d);
  return ds;
}

// w^d が K^{*M} かどうか (SS8.2 (8.1): すべての素因数 p|M で p 乗であること)
function isMthPowerInK(wd, M, n) {
  const primes = primeFactorsDistinct(M);
  if (primes.reduce((a, b) => a * b, 1n) !== M) {
    return { decided: false, reason: `M=${M} is not squarefree product of distinct primes -- out of SS8.2 scope` };
  }
  for (const p of primes) {
    const res = isPthPowerInK(wd, p, n);
    if (!res.decided) return { decided: false, reason: res.reason };
    if (!res.isPower) return { decided: true, isPower: false, obstructionPrime: p.toString() };
  }
  return { decided: true, isPower: true };
}

// 独立版 ord: w^d in K^{*M} となる最小の d | M
function ordModMIndependent(w, M, n) {
  const divs = divisorsOf(M);
  for (const d of divs) {
    const wd = ratPow(w, Number(d));
    const res = isMthPowerInK(wd, M, n);
    if (!res.decided) return { decided: false, reason: res.reason, triedDivisor: d.toString() };
    if (res.isPower) return { decided: true, ord: d.toString() };
  }
  return { decided: false, reason: 'no divisor produced isPower=true (unexpected)' };
}

// 便 34 P6-K1: minimality_obstructions の各エントリ(「divisor は M 乗でない、
// 障害素数は obstruction_prime」)を、GAP から独立に isMthPowerInK で再判定する。
function checkMinimalityObstructions(cert, w, M, n) {
  const obstructions = cert.minimality_obstructions ?? [];
  const results = [];
  for (const o of obstructions) {
    const wd = ratPow(w, o.divisor);
    const res = isMthPowerInK(wd, M, n);
    let ok;
    if (!res.decided) {
      ok = false;
    } else {
      // res.isPower が false であるべき(minimality obstruction の主張)、かつ
      // 障害素数が cert の obstruction_prime と一致すること。
      ok = (res.isPower === false) && (res.obstructionPrime !== undefined
        ? Number(res.obstructionPrime) === o.obstruction_prime : true);
    }
    results.push({ divisor: o.divisor, claimedObstructionPrime: o.obstruction_prime,
                   independentDecided: res.decided, independentIsPower: res.decided ? res.isPower : null,
                   independentObstructionPrime: res.decided && !res.isPower ? Number(res.obstructionPrime) : null,
                   ok });
  }
  return results;
}

// 便 34 P6-K1: witness^M = w^ord を独立の円分多項式環演算で厳密に再検算する
// (crosscheck/cyclo-ring-lib.mjs、GAP の AlgebraicExtension/Factors は不使用)。
// 司令塔追加委嘱での execution-block リファクタ(グローバル const M を
// runCheckKummer() のローカルへ移したことに伴う修理): 旧版はここで `M` を
// 呼び出し元スコープのグローバル変数として暗黙参照していた(定義時は
// たまたま動いていたが、関数の外から見える保証のない結合だった)。M を
// 明示引数化する。
function checkWitnessEquation(cert, w, ord, n, M) {
  const coeffsRaw = cert.witness_coeffs_basis_powers_of_root;
  if (!coeffsRaw) return { checked: false, reason: 'witness_coeffs_basis_powers_of_root missing from certificate' };
  const coeffs = coeffsRaw.map((s) => { const r = parseRatMaybeNumber(s); return new RingQ(r.n, r.d); });
  const modPoly = cyclotomicPolynomialAscending(Number(n));
  const lhs = polyPowMod(coeffs, Number(M), modPoly);
  // w^ord は有理数(BigInt 分数)。RingQ の BigInt 有理数として渡す。
  const wPowOrd = ratPow(w, Number(ord));
  const rhsMatches = polyEqConst(lhs, new RingQ(wPowOrd.n, wPowOrd.d));
  return { checked: true, lhs: lhs.map(String), rhs: `${wPowOrd.n}/${wPowOrd.d}`, match: rhsMatches };
}

//////////////////// 実行 ////////////////////
// 裁定42/便41 F4.2-F4.3 対応: u-compare 系と同水準の副作用なし Core 関数を
// export する(保存 harness の in-process fallback 用)。旧版は判定ロジック
// (runCheckKummer)の中で console.log/process.exit を直接呼んでおり、かつ
// この 実行 セクションに direct-run guard が無かった(import しただけで
// process.argv[2] を読んで走ってしまう)。本版は
//   - runCheckKummerCore(cert, certPath): 副作用なし、{report, exitCode} を返す
//   - runCliCore(argv): ファイル読み込み + RationalFormatError 変換込みの
//     副作用なし版(harness は certPath だけ渡せばよい)
// を export し、実際の CLI 実行は import.meta.url による direct-run guard の
// 中でのみ発火する。
export function runCheckKummerCore(cert, certPath) {
  return runCheckKummer(cert, certPath);
}
export function runCliCore(argv) {
  const certPath = argv[0];
  if (!certPath) {
    return { exitCode: 2, stdout: '', stderr: 'usage: node check-kummer.mjs <kummer-decide cert JSON>\n' };
  }
  let cert;
  try {
    cert = JSON.parse(readFileSync(certPath, 'utf8'));
  } catch (e) {
    return { exitCode: 1, stdout: '', stderr: `INTEGRITY_STOP: unhandled exception in check-kummer.mjs CLI wrapper -- ${e && e.stack ? e.stack : e}\n` };
  }
  try {
    const { report, exitCode } = runCheckKummerCore(cert, certPath);
    return { exitCode, stdout: JSON.stringify(report, null, 2), stderr: '', report };
  } catch (e) {
    if (e instanceof RationalFormatError) {
      const report = {
        schema: 'check-kummer/v2', certPath, result: 'INTEGRITY_STOP',
        reason: `(strict rational parser) ${e.message}`,
      };
      return { exitCode: 1, stdout: JSON.stringify(report, null, 2), stderr: '', report };
    }
    throw e;
  }
}
function runCli() {
  const r = runCliCore(process.argv.slice(2));
  if (r.stdout) console.log(r.stdout);
  if (r.stderr) process.stderr.write(r.stderr.endsWith('\n') ? r.stderr.slice(0, -1) + '\n' : r.stderr);
  if (r.exitCode !== 0) process.exit(r.exitCode);
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  runCli();
}

// 裁定42/便41 F4.2-F4.3 対応: 旧版は各分岐で console.log + process.exit を
// 直接呼んでいた(副作用あり・in-process fallback から結果だけを取り出せ
// なかった)。本版は副作用なしで {report, exitCode} を返すのみとし、
// 実際の print/exit は runCliCore/runCli 側でまとめて行う(exit code の
// 対応関係は旧版のまま保存: UNKNOWN->0, MISMATCH/INTEGRITY_STOP->1, MATCH->0)。
function runCheckKummer(cert, certPath) {
const w = parseRatMaybeNumber(cert.w);
const M = BigInt(cert.M);
const n = cert.field_n;

const indep = ordModMIndependent(w, M, n);

const report = {
  schema: 'check-kummer/v2',
  certPath,
  label: cert.label,
  field_n: n,
  M: cert.M,
  w: cert.w,
  gap_ord: cert.ord,
  independent_ord: indep.decided ? Number(indep.ord) : null,
  independent_decided: indep.decided,
};

if (!indep.decided) {
  report.result = 'UNKNOWN';
  report.reason = indep.reason;
  return { report, exitCode: 0 };
}

if (Number(indep.ord) !== cert.ord) {
  report.result = 'MISMATCH';
  report.reason = `independent ord (${indep.ord}) != GAP ord (${cert.ord})`;
  return { report, exitCode: 1 };
}

// 最小性 obstruction の独立検算
const obstructionChecks = checkMinimalityObstructions(cert, w, M, n);
report.minimality_obstruction_checks = obstructionChecks;
const obstructionsOk = obstructionChecks.every((r) => r.ok);
if (!obstructionsOk) {
  report.result = 'MISMATCH';
  report.reason = 'independent recomputation could not confirm one or more minimality_obstructions entries';
  return { report, exitCode: 1 };
}
// 証明書が主張する ord 未満の全ての約数(M の約数のうち ord より小さいもの)
// について obstruction が記録されていること自体も検査する(取りこぼし禁止)。
{
  const M_num = Number(M);
  const divisorsOfM = [];
  for (let d = 1; d <= M_num; d++) if (M_num % d === 0) divisorsOfM.push(d);
  const smallerDivisors = divisorsOfM.filter((d) => d < cert.ord);
  const coveredDivisors = new Set(obstructionChecks.map((r) => r.divisor));
  const missing = smallerDivisors.filter((d) => !coveredDivisors.has(d));
  if (missing.length > 0) {
    report.result = 'MISMATCH';
    report.reason = `minimality_obstructions does not cover all divisors of M smaller than ord: missing ${JSON.stringify(missing)}`;
    return { report, exitCode: 1 };
  }
}

// witness^M = w^ord の独立再検算(円分体の環演算)
const witnessCheck = checkWitnessEquation(cert, w, BigInt(cert.ord), n, M);
report.witness_equation_check = witnessCheck;
if (witnessCheck.checked && !witnessCheck.match) {
  report.result = 'MISMATCH';
  report.reason = `witness^M = w^ord failed independent recheck: ${JSON.stringify(witnessCheck)}`;
  return { report, exitCode: 1 };
}
if (!witnessCheck.checked) {
  report.result = 'MISMATCH';
  report.reason = `witness equation could not be independently checked: ${witnessCheck.reason}`;
  return { report, exitCode: 1 };
}

report.result = 'MATCH';
return { report, exitCode: 0 };
} // end runCheckKummer
