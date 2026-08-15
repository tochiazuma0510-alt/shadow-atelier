# Luna 便 152 — GHA DMTCP provisioning repair receipt

指定された `sol/luna_task_152_gha_repair.md`、`AGENTS.md`、受信便、Sol 返信、d972 v2 の六ファイルを先頭から末尾まで読んだ。run `31902666498` と job `95055698114` を確認した。

## 1. run 31902666498 の事実

- workflow: `.github/workflows/d972-dovetail-v2.yml`
- source commit: `acfb39415a9eca599fcc3659c110a6ba2170276d`
- conclusion: `failure`
- failed step: `Install and inventory GAP plus DMTCP`
- exact log: Ubuntu 24.04 の apt が `Package 'dmtcp' has no installation candidate` を返し、exit code 100。
- producer、checker、DMTCP smoke、GAP smoke、checkpoint、数学 campaign、artifact は未実行・未生成。

したがって、この run には数学的 A/B receipt も resume predecessor も存在しない。失敗原因は GAP や worker ではなく、Ubuntu noble の `dmtcp` binary package 欠品である。

再現確認コマンド:

```text
gh run view 31902666498 --json status,conclusion,headSha,jobs,url
gh run view 31902666498 --log-failed
```

## 2. 実施した修理

変更は d972 v2 の workflow と manifest、およびこの返信だけである。apt の `dmtcp` を別名で緩く置き換えることはせず、DMTCP を release source から再現可能に構築する。

固定値:

```text
DMTCP release tag       = v4.2.0
DMTCP release commit    = f8009ce7b4ad211311ca2f72a929b975e4aa1155
archive URL              = https://api.github.com/repos/dmtcp/dmtcp/tarball/v4.2.0
archive SHA-256          = 0288457860517cf3b221da794bbf0bea8804d846fcb629a50181a7225b93a392
archive root             = dmtcp-dmtcp-f8009ce
provisioning SHA-256     = e91b29b61ebb4eb35ce863c2f66b68bfaeed565dc24c63cd9cfeff2b886cebc0
DMTCP contract SHA-256   = 46a1e95024ebb148c01a982828dc58e163166fbcab65afd3fd1393581e5a403b
```

workflow は `gap build-essential ca-certificates curl` のみ apt から導入し、archive を `curl --fail --location --retry 5 --retry-all-errors` で取得、SHA-256 検査後に展開する。`./configure --prefix=$GITHUB_WORKSPACE/.dmtcp-prefix`、`make -j$(nproc)`、`make install` を実行し、以後の全 step はその prefix の `bin` を `PATH` の先頭にする。

さらに `dmtcp_launch`、`dmtcp_command`、`dmtcp_coordinator`、`dmtcp_restart` の `command -v` が prefix 内の実体と一致することを要求する。runtime version receipt には release commit と archive SHA を付加するため、resume 時にも同じ供給物であることが DMTCP/GAP/Python runtime compatibility に結合される。provisioning の digest は dmtcp contract の `provisioning_sha256` として contract hash に含めた。

既存の coordinator、`--kcheckpoint`、open-file checkpoint、stateful restart smoke、GAP worker-v2 smoke、secret-free `env -i`、fail-closed terminal gate は変更していない。

## 3. 変更ファイルと最終 SHA-256

```text
.github/workflows/d972-dovetail-v2.yml
  636c2e5ffd36ad053446d30d9d2fd7ea773f4f14b375d6745c03c766172ed8d7
search/d972_dovetail_manifest_v2.json
  c30d101d5156e25b4a800d85da3730bd3ce1711f114ab52c531afbcb95caa9ef
search/d972_dovetail_worker_v2.g
  7367780a6c11fa65aeafdf8214065d881141b7461d2d71eadac8db6ea4bd98f0
search/d972_dovetail_producer_v2.py
  8bd965efa7c5564478b277a1649dd2dfaa01f022619c99590de95be92bbed5dc
search/check_d972_dovetail_v2.py
  46445ae5cbea96c87b3548e1df227fc546d895a0d64f3c0a7fd9c74cf8a6e4b2
search/d972_dovetail_state_schema_v2.json
  85acbb14729ddfec366564b8663cdb085ca21bf329a386fca616bef2c23cae78
```

前回から変わらない四つの v2 code/schema hash も再計算して記載した。manifest 変更により producer self-test の新しい binding set SHA-256 は `1124f7c47449402537f1839e222979d0d72bd955553a6815f45916d59f5667b3` である。

## 4. 実行した検査

すべて PASS:

```text
python -B search/d972_dovetail_producer_v2.py --self-test
  status=PASS
  contract_sha256=46a1e95024ebb148c01a982828dc58e163166fbcab65afd3fd1393581e5a403b
  binding_set_sha256=1124f7c47449402537f1839e222979d0d72bd955553a6815f45916d59f5667b3

python -B search/check_d972_dovetail_v2.py --self-test
  status=PASS
  negative_cases=11
  independent_calibration_positive=PASS
  independent_calibration_tamper_negative=2
  partial_checkpoint_terminal_authority=false

embedded Python heredoc compile from parsed workflow YAML
  11 blocks PASS

workflow YAML parse
  PASS

manifest JSON parse, canonical provisioning digest, canonical contract digest
  PASS

git diff --check -- workflow and manifest
  PASS
```

Windows 側では Linux `apt`、DMTCP source build、POSIX coordinator/restart、GAP smoke を実行できないため、これらを local cross-check と称していない。次の GHA run が provisioning、stateful restart、実 GAP smoke を fail-closed に実証する。

## 5. 親 broker への dispatch 指示

commit/push/dispatch は行っていない。親が上記 workflow と manifest を含む commit を作成して push した後、次を初回入力にする。

```text
workflow: .github/workflows/d972-dovetail-v2.yml
resume_run_id: ""
slice_minutes: "240"
```

run `31902666498` は失敗 artifact を持たないため、そこから resume してはならない。新 commit を ref にした fresh dispatch が正しい。source commit、workflow SHA、manifest contract SHA、DMTCP archive SHA が一致しない場合は実行せず fail closed とする。

成功しても `UNKNOWN_RESUME` は数学的結論ではなく、直ちに同一最新 artifact を継続する。`A_WITNESS_CROSSCHECKED` と `final-v2-completion.json` の完全な final seal が揃うまで A/B を宣言しない。timeout、cap、nontermination、checkpoint から B は推論しない。

```text
RUN_31902666498_MATH_STATUS=NO_CAMPAIGN_REACHED;
RUN_31902666498_FAILURE=APT_DMTCP_NO_CANDIDATE;
DMTCP_PROVISIONING=PINNED_SOURCE_V4.2.0;
DMTCP_ARCHIVE_SHA256=0288457860517cf3b221da794bbf0bea8804d846fcb629a50181a7225b93a392;
REPAIR_STATUS=READY_FOR_PARENT_COMMIT_AND_FRESH_GHA;
DISPATCH_REQUIRED=YES;
```

## 6. v2 repair — run 31904750698 (`--version` probe)

親から指定された run `31904750698`（job `95060721958`、source commit `2470d8cb77bf0dc40544274be2ee8259ec6dcd36`）を追加監査した。source download の SHA 検査、展開、configure、make、make install はすべて成功している。失敗はその直後で、数学処理には到達していない。

### 6.1 source-level cause audit

DMTCP v4.2.0 source archive の `src/dmtcp_launch.cpp` では、`processArgs` の

```cpp
} else if ((s == "--version") && argc == 1) {
  printf("%s", DMTCP_VERSION_AND_COPYRIGHT_INFO);
  exit(0);
}
```

が確認できる。一方、同じ archive の `src/dmtcp_command.cpp` は version 表示後に `return 1`、`src/dmtcprestartinternal.cpp` の restart probe は `exit(0)` である。従って `--version` の終了コードを一律に「表示成功なら常に zero」と仮定するのは危険であり、run 31904750698 の実環境で `dmtcp_launch --version` が `set -e` の assignment を停止させたことを、output を隠したまま無視しないよう修理した。

新 probe は `set +e` の狭い範囲で終了コードを取得し、次を全て要求する。

1. 終了コードが manifest の `version_probe.allowed_exit_codes = [0,1]` に含まれる。
2. captured output に `DMTCP` が含まれる。
3. captured output に manifest 固定 release tag `v4.2.0` の version token `4.2.0` が含まれる。
4. `dmtcp_launch`、`dmtcp_command`、`dmtcp_coordinator`、`dmtcp_restart` は従来どおり pinned prefix の実体である。
5. runtime receipt は `version_probe_exit`、source commit、archive SHA を結合する。

従って、任意の非 zero を飲み込む変更ではない。version output の内容、pinned source archive、4つの binary path、後続の help gate、stateful restart smoke が全て残り、異常な status/output は fail-closed のままである。今回の実行では source 内の launch 分岐は zero を明記しているため、実際の status が 1 でも正しい固定 output がなければ停止する。

### 6.2 v2 変更と新 digest

`search/d972_dovetail_manifest_v2.json` の provisioning に version probe policy を追加し、provisioning digest と contract digest を更新した。

```text
provisioning_sha256 = 425dafd0b4a303a8c6b1f59df2a241825382109ca84ddcfe578eb21158ff7570
contract_sha256     = 8fc91988171621c78e5d674f37f14fd546d487d9a77665934a8c0cd6a0c54ffd
producer binding    = 5999ea1750af283186d09e8810afbac78dc8a5c4387514b039a240082596ec29
workflow SHA-256    = 455fb21a440ad93cdea8d9c789651d17fa4b3cdea4ce8674616a2a7d419c8886
manifest SHA-256    = 7baa250272f5aa5f4add3d481db87be85a2f07cd5f976beb6930fbe114283195
```

### 6.3 v2 tests

```text
python -B search/d972_dovetail_producer_v2.py --self-test       PASS
python -B search/check_d972_dovetail_v2.py --self-test          PASS
workflow YAML parse                                             PASS
embedded Python heredocs                                        11/11 PASS
canonical provisioning + contract digest                        PASS
git diff --check (workflow, manifest, reply)                     PASS
```

この session では Linux binary の直接起動はできないため、run 31904750698 の observed status をローカルで捏造していない。次の fresh dispatch は、上記 v2 workflow/manifest を含む親 commit に対して `resume_run_id=""`, `slice_minutes="240"` とする。run 31904750698 は失敗 artifact を持たず、resume 対象ではない。

```text
RUN_31904750698_MATH_STATUS=NO_CAMPAIGN_REACHED;
RUN_31904750698_FAILURE=POST_INSTALL_DMTCP_VERSION_PROBE;
VERSION_PROBE=CAPTURED_OUTPUT_PLUS_PINNED_TOKEN_AND_ALLOWED_RC;
REPAIR_V2_STATUS=READY_FOR_PARENT_COMMIT_AND_FRESH_GHA;
```

## 7. v3 correction — run 31904750698 attribution retracted

Sol の親監査を受理し、§6 の帰属を訂正する。run `31904750698` のログは `make install` の最後で止まっており、silent command substitution のどれが nonzero だったかはログだけから特定できない。従って、§6 が「`dmtcp_launch --version` が停止原因」と断定したのは不正確であり、**その attribution を撤回する**。

凍結した v4.2.0 source の一次確認結果は次のとおりである。

- `src/dmtcp_launch.cpp:234-239`: `--version` は `printf` 後 `exit(0)`。
- `src/dmtcp_command.cpp:86-91`: `--help` と `--version` は表示後 `return 1`。
- `src/dmtcprestartinternal.cpp:696-701`: `dmtcp_restart --help` は表示後 `exit(0)`。

このため、v3 は probe semantics を source と一致する exact policy にした。

```text
dmtcp_launch --version       allowed exit = [0]
dmtcp_command --help         allowed exit = [1]
dmtcp_restart --help         allowed exit = [0]
```

各 command はそれぞれ狭い `set +e` 範囲で output と status を捕捉し、manifest宣言の exact status を要求する。`dmtcp_command --help` は `--kcheckpoint`、`dmtcp_restart --help` は `--ckptdir` を必須 token とする。launch probe は `DMTCP` と `4.2.0` を必須とする。任意の nonzero を許容する処理ではなく、source-pinned executable、output token、exact exit code、後続 stateful restart smoke の全てが残る。

v3 manifest provisioning policy と contract は更新済みである。

```text
provisioning_sha256 = 37d739ea0a6775ff119e98e43e083541e954bd473fc2de89d10049655c39de50
contract_sha256     = 1c97981e298d33f342a6ee9e60b8449889c2450e1d986c69826e743d7b63ccf1
producer binding    = 325c2e2868ba5c7bb9566035dc66bf48dc52fbcfcd6189ab7c9939423fe8f4c6
```

検査結果:

```text
producer v2 self-test                       PASS
checker v2 self-test                        PASS
workflow YAML parse                         PASS
embedded Python heredocs                    11/11 PASS
canonical provisioning/contract digest      PASS
policy semantic assertions                   PASS
git diff --check                             PASS
```

v3 の最終ファイル SHA-256 は次のとおり。

```text
.github/workflows/d972-dovetail-v2.yml      732a899f286403014baf988b777788e13c48eaa29e98e1b50cb70a5362f6ebeb
search/d972_dovetail_manifest_v2.json       4f6b946e93c271c487ef790f6f0363fe9bdbd0afc646504afe174bc96954fbc7
```

上記はv3 policyを含む実ファイルの再計算値である。run `31904750698` は数学未到達・artifactなしであり、再dispatch はこのv3 workflow/manifestを含む fresh commit に対してのみ行う。`resume_run_id=""`, `slice_minutes="240"`。commit/push/dispatch は行っていない。

```text
RUN_31904750698_MATH_STATUS=NO_CAMPAIGN_REACHED;
RUN_31904750698_ATTRIBUTION_V2=RETRACTED;
V3_PROBE_POLICY=SOURCE_EXACT_LAUNCH0_COMMAND_HELP1_RESTART_HELP0;
REPAIR_V3_STATUS=READY_FOR_PARENT_AUDIT;
```

## 8. v4 correction — run 31905492945 Bash parser failure

run `31905492945`（job `95062483505`、source `f396e8cc`）を監査した。DMTCP source download/hash/configure/make/make install の失敗ではない。生成された install step は build後、line 46 の

```text
syntax error in conditional expression: unexpected token `;'
```

で Bash parser により停止した。従って v3 の三つの probe は一つも実行されておらず、status や output の証拠として扱わない。

原因は、manifestのsingleton policy membershipを Bash wildcard `[[ " ... " == *" ... "*" ]]` で判定した式である。この形式を workflow から全て除去した。

v4 は各 policy を Python の一行 loader で読み、`assert len(x)==1` を通った declared singleton code を得て、実測statusを単純な

```bash
test "$actual_rc" = "$declared_rc"
```

で比較する。比較対象は次の固定値である。

```text
dmtcp_launch --version       declared=0
dmtcp_command --help         declared=1
dmtcp_restart --help         declared=0
```

これにより wildcard、glob、semicolonを含むfragile conditionalは残っていない。policyがsingletonでなければ loader 自体が停止し、status mismatch、必須出力token欠落、pinned binary path不一致も従来どおり fail-closed である。

さらに expensive な source build より前、checkout lock の直後に `Bash syntax gate for exact DMTCP inventory step` を追加した。gateは別のfixtureを再入力せず、現在の `.github/workflows/d972-dovetail-v2.yml` から `Install and inventory GAP plus DMTCP` の実際の `run: |` blockを `awk` で `$RUNNER_TEMP` に抽出し、`bash -n` する。したがって同じ構文エラーは build時間を消費する前に検出される。

v4で追加のmanifest内容はなく、contract/provisioning digestは変更しない。

```text
contract_sha256       = 1c97981e298d33f342a6ee9e60b8449889c2450e1d986c69826e743d7b63ccf1
provisioning_sha256   = 37d739ea0a6775ff119e98e43e083541e954bd473fc2de89d10049655c39de50
producer binding       = 3437024fe4ce3823ac3701f744c2edb6ea4b7b71820415b05879aa368921d713
workflow SHA-256       = 80040dc42da759a62b43fc6164d7fe0ea0999f9d88685c5b8e86b6f02bb96848
manifest SHA-256       = 4f6b946e93c271c487ef790f6f0363fe9bdbd0afc646504afe174bc96954fbc7
```

v4 tests:

```text
producer v2 self-test                       PASS
checker v2 self-test                        PASS
workflow YAML parse                         PASS
embedded Python heredocs                    11/11 PASS
canonical provisioning/contract digest      PASS
singleton policy assertions                 PASS
git diff --check                             PASS
```

run `31905492945` は数学未到達・artifactなしであり、resume対象ではない。親brokerがv4を含むfresh commitをpush後、`resume_run_id=""`, `slice_minutes="240"` で再発火する。commit/push/dispatch は行っていない。

```text
RUN_31905492945_MATH_STATUS=NO_CAMPAIGN_REACHED;
RUN_31905492945_FAILURE=BASH_PARSE_IN_WILDCARD_MEMBERSHIP_CONDITIONAL;
V4_STATUS=READY_FOR_PARENT_COMMIT_AND_FRESH_GHA;
```
