"""
u7_fire_secondsys_assemble_v1.py -- assembles search/certs/u7_fire_secondsys_20260801.json
from the two machine outputs produced under the second-system role (commander
ruling 2026-08-01: path-A explicit n=7 model construction and the path-B
Phi(F_0)-block-stabilization -> [gamma] logical bridge are BOTH mathematician
territory / delegated to the twist-doc author; this implementer's role is
confirmed as SECOND SYSTEM only, producing (a)(b)(c) machine data with NO
evaluation of [gamma]/[delta]/u7).

Inputs (already produced, machine-piped, this script only assembles+hashes):
  (a)+(b) search/probe/wac_v1/u7_pathB_gap_v2_crosscheck_v1.py output
          (GAP independent T-W1/T-W2 re-derivation + <X^2>-stabilizes-blocks
          mechanical fact, cross-checked against tw_blocks.py/tw_orient.py)
  (c)     search/probe/wac_v1/u7_pathB_kummer_symbolic_v1.py output
          (symbolic Kummer h(k) construction, kappa/mu formal, n=7 alpha=1)
"""
import json, hashlib, subprocess, sys, datetime

REPO = "C:/Users/81905/Desktop/shadow-atelier"

def sha256_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def run_capture(cmd, cwd=REPO):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=False)
    if p.returncode != 0:
        raise RuntimeError(f"{cmd} failed: {p.stderr}")
    return p.stdout

def main():
    # (a)+(b): re-run the crosscheck script live (machine-piped, not hand-copied)
    ab_out = run_capture(["python", "search/probe/wac_v1/u7_pathB_gap_v2_crosscheck_v1.py"])
    ab = json.loads(ab_out)

    # (c): re-run the symbolic Kummer construction live
    c_out = run_capture(["python", "search/probe/wac_v1/u7_pathB_kummer_symbolic_v1.py"])
    c = json.loads(c_out)
    c["_self_script_sha256"] = sha256_of(f"{REPO}/search/probe/wac_v1/u7_pathB_kummer_symbolic_v1.py")
    c.pop("_self_script_sha256_at_run_note", None)

    gap_raw_output_sha256 = sha256_of(f"{REPO}/search_gap_v2_output.txt")

    cert = {
        "schema": "u7-fire-secondsys/v1",
        "generated_by": {
            "tool": "python3+sympy / GAP 4.16.0",
            "sympy_version": "1.14.0",
            "assembler_script": "search/probe/wac_v1/u7_fire_secondsys_assemble_v1.py",
        },
        "purpose": "u7発火走(2026-08-01 司令塔指示)の第二系統担当分(a)(b)(c)。司令塔裁定(同日): 経路Bの論理の橋(Phi(F_0)ブロック安定化->[gamma]の含意)と経路Aのn=7明示模型構成は数学者(twist doc起草者)の領分に確定。実装担当の役割は第二系統(下ごしらえの機械値)に限定。",
        "authority": {
            "commander_order_1": "u7発火走(2026-08-01・裁定300執行) — 経路A(twist doc SS5 DET-4)・経路B(twist doc SS7 系B-4c)を実行し[gamma]=[u7]_2を独立に出し一致判定を機械で行え",
            "commander_order_2_scope_ruling": "両論点とも判断が正しい — 裁定: 経路Bの論理の橋と経路Aのn=7明示模型構成は創出であり数学者の領分。発火執行の数学部はtwist docを書いた数学者(Opus2)に移す。あなたの役割は第二系統に確定: (a)(b)(c)の下ごしらえをそのまま完遂し、cert=search/certs/u7_fire_secondsys_20260801.jsonに機械値で収蔵して報告・終了せよ。[gamma]/[delta]/u7の評価は引き続き禁止。",
            "primary_source": {
                "path": "docs/notes/u7_twist_determination_v1.md",
                "sha256": sha256_of(f"{REPO}/docs/notes/u7_twist_determination_v1.md"),
            },
            "secondary_source": {
                "path": "docs/notes/u7_meas_design_v1.md",
                "sha256": sha256_of(f"{REPO}/docs/notes/u7_meas_design_v1.md"),
            },
            "phi_F0_definition_source": {
                "path": "docs/notes/phifam_v1.md",
                "sha256": sha256_of(f"{REPO}/docs/notes/phifam_v1.md"),
                "quote": "Phi(F_0) = inn(<X^2>) (命題K5-1・w2fam SS3.5で再確認). <X^2>=<a_1> は deck群 G_n の中の並進 C_n",
            },
            "prefire_cert_ref": {
                "path": "search/certs/u7_prefire_20260801.json",
                "sha256": sha256_of(f"{REPO}/search/certs/u7_prefire_20260801.json"),
            },
        },
        "scope_guard": {
            "gamma_delta_u7_evaluated": False,
            "n5_K5_touched": False,
            "u7_value_or_conjecture_written": False,
            "ignition_performed": False,
            "pathB_logical_bridge_drawn (Phi(F_0)-stabilizes-blocks => [gamma]=1)": False,
            "pathA_explicit_n7_model_constructed (numeric kappa,mu / F-descent)": False,
            "note": "本certは第二系統の機械値のみを収蔵する。経路A・Bの数学的結論([gamma]の値・その導出の妥当性)には一切踏み込んでいない。",
        },
        "task_a_b_gap_independent_system_and_new_mechanical_fact": ab,
        "task_c_kummer_symbolic_construction": c,
        "gap_raw_output_file": {
            "path": "search_gap_v2_output.txt (scratch, not committed to git by this cert)",
            "sha256": gap_raw_output_sha256,
        },
        "overall_pass": ab["cross_check_all_pass"] and c["divisor_all_match"] and c["iota_B_pullback_h_equals_hinv (C=1 reflection check)"],
        "verdict": None,  # filled below
        "caveats": [
            "本certは第二系統担当分(a)(b)(c)のみ。経路A(DET-4・n=7明示模型)・経路B(SS7.2論理の橋)の実行は数学者(twist doc起草者)へ移管済み — 本certはその結果を含まない。",
            "(a)(b): GAP(独立実装)とpython(tw_blocks.py/tw_orient.py、単系統として既存)の cross-check。cross-checked であって verified ではない(Lean 未実施)。",
            "(b)の新規事実(<X^2>が全19窓でブロックを安定化)はGAP単独の機械値であり、python側に対応する既存probeが無いため「新規データ」として報告する(cross-checkedではない)。この事実からの[gamma]への含意は一切導出していない(司令塔裁定によりmathematician領分)。",
            "(c)のkappa,muは形式記号のまま(数値代入なし)。定理KUM-nの箱囲み公式の機械的instantiationのみで、n=7のF-descent/明示模型構成ではない。",
            "u7/K^(5)に一切接触していない。",
        ],
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    cert["verdict"] = (
        "SECOND-SYSTEM PREP PASS (a)(b)(c) 完遂・全19窓cross-check一致・"
        "<X^2>ブロック安定化を全窓で確認・Kummer h(k)記号構成の因子検算一致。"
        "経路A/B本体の実行と[gamma]評価は数学者へ移管(本cert対象外)。"
        if cert["overall_pass"] else
        "SECOND-SYSTEM PREP FAIL - see diffs"
    )

    out_path = f"{REPO}/search/certs/u7_fire_secondsys_20260801.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    print("wrote", out_path)
    print("overall_pass =", cert["overall_pass"])
    print("verdict =", cert["verdict"])

if __name__ == "__main__":
    main()
