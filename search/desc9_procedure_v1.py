"""
search/desc9_procedure_v1.py -- DESC-9 (D-i)(D-iii) の手順実装(裁定1118・実装係タスク3・工房分)

正本: docs/notes/r2_r3_unram_execution_spec_v1.md §5-§7(規約 DESC-9・a_class 出力 schema)
分担: §14 の表により DESC-9 の (D-i)(D-iii) のみ工房。(D-ii)(有理性検査)・[R-3-U9]
      (u_9 の厳密抽出)は Sol 分担(便123 走行中・触らない)。

⚠ prereg 規律(裁定1118 実行指示): d_9/r の値の *先行計算・解釈は禁止*。
   本 script は手順の実装と較正(canary)のみを行う。real_data_used は常に False。
   u_9 の実測値は一切扱わない(Sol の R-3-U9 が出す前)。

DESC-9 手順(spec §5):
  (D-i)  指数の落とし: 自然な全射 F^x/(F^x)^18 -> F^x/(F^x)^9 で a_9 を送る。
  (D-ii) 有理性検査(fail-closed): 像が iota: Q^x/(Q^x)^9 -> F^x/(F^x)^9 の像に入るか。
         ★ 本 spec §6 により F=Q(宣言モデルが Q 上に降りたため)なので (D-ii) は
           構造的に自明合格(u_9 は最初から Q^x の元)。これは *値に依存しない型の
           事実*であり、d_9/r の値の先行計算には当たらない(工房分に含めるのは
           このため -- §14 の表どおり)。
  (D-iii) 降下: RES-INJ-9(単射性)により [a] は一意に定まる。素因子指数ベクトル
          (法9)が a_class。

Q^x/(Q^x)^9 は Z/9 の直和(素数ごと)。sign は 9乗で消えるため無視(search/
r_intersection_template_v1.py と同じ規約)。
"""
import hashlib
import json
from fractions import Fraction
from math import gcd

try:
    from sympy import factorint
except ImportError:
    factorint = None


def prime_valuations(frac: Fraction, modulus: int):
    """Exponent vector (mod `modulus`) of a rational, dropping primes with exponent 0 mod modulus."""
    num = abs(frac.numerator)
    den = abs(frac.denominator)
    vals = {}
    if factorint is not None:
        for p, e in factorint(num).items():
            vals[p] = vals.get(p, 0) + e
        for p, e in factorint(den).items():
            vals[p] = vals.get(p, 0) - e
    else:
        for n, sign in ((num, 1), (den, -1)):
            x = n
            p = 2
            while p * p <= x:
                while x % p == 0:
                    vals[p] = vals.get(p, 0) + sign
                    x //= p
                p += 1
            if x > 1:
                vals[x] = vals.get(x, 0) + sign
    return {p: (e % modulus) for p, e in vals.items() if e % modulus != 0}


def order_of_class(vals, n):
    order = 1
    for p, e in vals.items():
        vmod = e % n
        contrib = n // gcd(n, vmod) if vmod != 0 else 1
        order = order * contrib // gcd(order, contrib)
    return order


def desc9_d_i(a9_rational: Fraction):
    """(D-i) 指数の落とし: F^x/(F^x)^18 -> F^x/(F^x)^9. Returns class_mod18 and its image mod 9."""
    class_mod18 = prime_valuations(a9_rational, 18)
    # natural surjection: reduce each exponent mod 9 (18 -> 9 is the quotient F^x/(F^x)^18 -> F^x/(F^x)^9,
    # induced simply by reducing exponents further mod 9, since (F^x)^18 subset (F^x)^9)
    image_mod9 = {p: (e % 9) for p, e in class_mod18.items() if e % 9 != 0}
    return class_mod18, image_mod9


def desc9_d_ii_type_fact():
    """
    (D-ii) 有理性検査. NOT a per-value computation: for this declared model, F=Q (spec §6,
    宣言モデルが Q に降りた帰結) so the map iota: Q^x/(Q^x)^9 -> F^x/(F^x)^9 = Q^x/(Q^x)^9
    is the identity and its image is everything. u_9 in Q^x by construction (R-2-U/R-3-U9
    produce a rational function's leading coefficient in Q^x when it exists), so any class
    is automatically in the image. This is a STRUCTURAL/TYPE fact independent of the actual
    u_9 value -- it is what §6 of the spec already derived on paper. We record it as always
    True for this model; this is NOT a computation of d_9/r's value.
    """
    return True


def desc9_d_iii(image_mod9: dict):
    """
    (D-iii) 降下: RES-INJ-9 により [a] は一意に定まる(F=Q なのでこのステップは恒等)。
    Build the p8_a_class/v1 schema record.
    """
    support = sorted(image_mod9.keys())
    exponents = [image_mod9[p] for p in support]
    if not support:
        order = 1
    else:
        g = 0
        for e in exponents:
            g = gcd(g, e)
        order = 9 // gcd(9, g) if g != 0 else 1
    return {
        "representation": "exponent vector mod 9 over the support primes",
        "support": support,
        "exponents": exponents,
        "order": order,
        "normalization": "a は Q^x/(Q^x)^9 の代表・sign は 9 乗で消えるため無視",
    }


def build_a_class_record(a9_rational: Fraction):
    class_mod18, image_mod9 = desc9_d_i(a9_rational)
    step_ii = desc9_d_ii_type_fact()
    a_class = desc9_d_iii(image_mod9)
    support_S4 = [3]  # S-1 score rule reference support (P8 v3.2 §3): support==[3] and order==9
    s1_test = (a_class["support"] == support_S4 and a_class["order"] == 9)
    return {
        "a_class": a_class,
        "a_9_field_note": {
            "u9_home_field": "Q",
            "class_mod18_Q": {"support": sorted(class_mod18.keys()),
                               "exponents": [class_mod18[p] for p in sorted(class_mod18.keys())]},
            "image_in_F9": {"support": sorted(class_mod18.keys()),
                             "exponents": [class_mod18[p] for p in sorted(class_mod18.keys())],
                             "note": "F_9 = Q for this declared model (spec r2_r3_unram_execution_spec_v1 §6) => identical to class_mod18_Q"},
            "desc9_rule": "DESC-9 (D-i)->(D-ii)->(D-iii)",
            "desc9_step_ii_passed": step_ii,
        },
        "s1_score_rule_raw": {"support_equals_3": a_class["support"] == support_S4,
                               "order_equals_9": a_class["order"] == 9,
                               "s1_raw_value": s1_test,
                               "note": "raw machine value only, NOT an interpretation/judgement -- 司令塔検問後の本番発火まで real u_9 には適用しない"},
    }


def main():
    print("=== DESC-9 (D-i)(D-iii) 手順較正(canary のみ・real u_9 不使用)===\n")
    canaries = [
        ("a9=1 (trivial)", Fraction(1)),
        ("a9=3^18 (should vanish mod 9 -> support empty, order 1)", Fraction(3) ** 18),
        ("a9=3 (order 9 on support {3})", Fraction(3)),
        ("a9=3^9 (should vanish mod 9 -> order 1)", Fraction(3) ** 9),
        ("a9=3^3 * 5^6 (order 3 on support {3,5})", Fraction(3) ** 3 * Fraction(5) ** 6),
        ("a9=2^-8 (matches ds4 in-stock b=2 exponent, order 9 mod9 since -8 mod9=1)", Fraction(1, 2 ** 8)),
    ]
    results = []
    for name, val in canaries:
        rec = build_a_class_record(val)
        print(f"  {name}: a_class={rec['a_class']}  step_ii_passed={rec['a_9_field_note']['desc9_step_ii_passed']}  s1_raw={rec['s1_score_rule_raw']['s1_raw_value']}")
        results.append({"canary_name": name, "input_a9": str(val), **rec})

    script_path = "search/desc9_procedure_v1.py"
    with open(script_path, "rb") as f:
        script_sha256 = hashlib.sha256(f.read()).hexdigest()

    cert = {
        "schema": "shadow-atelier/desc9_procedure/v1-canary",
        "generated_by": {"tool": "python3", "script": script_path,
                          "order": "裁定1118(実装係タスク3・工房分DESC-9(D-i)(D-iii))"},
        "spec_ref": "docs/notes/r2_r3_unram_execution_spec_v1.md §5-§7",
        "canary": True,
        "real_data_used": False,
        "note": "prereg規律: d_9/r の値の先行計算・解釈は禁止。本certはcanary較正のみ。real u_9 は一切未使用。本番発火は司令塔検問後(R-3-U9のSol出力を待つ)。",
        "results": results,
        "u_touched": False,
        "c_touched": False,
        "provenance": {"script_sha256": script_sha256},
    }
    out_path = "search/certs/desc9_procedure_v1_canary_20260813.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, ensure_ascii=False, indent=2)
    print(f"\nwrote {out_path}")
    print(f"script sha256 = {script_sha256}")


if __name__ == "__main__":
    main()
