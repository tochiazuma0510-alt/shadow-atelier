Task1143 の指定2箇所を修理し、正逆 raw 全EOF一致を確認した。原本60829 B / 21127ce22024310b6272bfd581c7362d959d3303eccab86bdb88168c9cc5c9c2、全1209行を読み、作業branchの原本は変更していない。

成果物はすべて `%TEMP%/shadow-atelier-audit163/task1143/`。

| 成果物 | Bytes | SHA-256 |
| --- | ---: | --- |
| d972-dovetail-context-fix-v1.yml | 60922 | ec713229fb4f854819cb5f79f0fe7ff6a80e5b06959dd1a6e19155e1ace8d735 |
| two-edit-raw-proof-v1.json | 5411 | dadeb9809d1f4f0a0043a216cfa6d71657699f517dd892b75dd6a3642b00e7d9 |
| repair-receipt-v1.json | 1734 | b42de51e8cd71836021f4264050b56112d66c84bc19f67ea9420c0e87783dd59 |

旧L43の job-level `RUN_ROOT: ${{ runner.temp }}/d972-dovetail` をLF込み49 B削除した（旧byte offset1188）。旧L49直前、`steps:` 直後へ142 B / 5 LFを追加した（旧offset1508、新offset1459）。修理後L48-52が最初の `Set run root` step、L53から元のcheckoutである。

```yaml
      - name: Set run root
        shell: bash
        run: |
          printf 'RUN_ROOT=%s/d972-dovetail\n' "$RUNNER_TEMP" >> "$GITHUB_ENV"
```

`jobs.<job_id>.env` で `runner` は使用できないため、runner上のbash実行へ初期化を移した。[GitHub公式 context availability](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#context-availability)。`GITHUB_ENV` への書込みは後続stepへ値を渡すので、同じ `$RUNNER_TEMP/d972-dovetail` を後続処理へ供給する。[GitHub公式 environment variable](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands#setting-an-environment-variable)。metadata検索でも設定前の `RUN_ROOT` 使用は0件、設定は新L51、最初の既存consumerは新L189。残る `runner.temp` 2件はstepのwith.path（新L167/L1201）である。

前後ともASCII、CR0、BOMなし、EOFはLF。LF数1209→1213。2 edit以外の60780 Bを3区間で直接比較して完全一致、保存したold/new base64と各座標からの正方向・逆方向の再構成も全EOFまで一致した。proofには全editのold/new bytes/SHA/offset/行位置と未変更区間表を収めた。したがってon/schedule/dispatch/defaults、330/300分とslice caps、全envの残余、親・manifest・schema・producer/checker/GAP、runtime/resume/保存採択/緊急STATE_STOPの全bytesは保持される。

今回のテストは原文との正逆raw一致で足りる。metadata builder `repair_dovetail_context_v1.py`（7560 B / 0c6c235cc7e1a9005d7d7d88f0119d054388d3919deaeb55e824432255f0296f）を全文別読後 `python -I -B` で1回実行し、native exit0（tool492624）。workflow埋込みPythonを含む数学sourceの実行/import/compile/AST、P/C private sourceの読取、git/gh/credentials操作は行っていない。GHAの実挙動・構文入場・配置/push/dispatchはroot担当。masterへの新規WF・依存物追加も行っていない。

LUNA_1143_VERDICT: PASS_EXACT_TWO_EDIT_RAW_RECONSTRUCTION; READY_FOR_ROOT_REVIEW_AND_NOTIFY_AND_GO; GHA_BEHAVIOR_ROOT_OWNED
