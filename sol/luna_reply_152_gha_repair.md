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
