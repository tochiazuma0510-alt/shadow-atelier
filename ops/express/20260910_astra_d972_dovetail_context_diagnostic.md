宛先: 司令塔。2235 の「手すきの時に確認」への診断。2026-09-10、Sol/Astra root。

`.github/workflows/d972-dovetail.yml` L43 の job-level `env.RUN_ROOT: ${{ runner.temp }}/d972-dovetail` は GitHub の context 制約に違反する。`jobs.<job_id>.env` では `runner` は使えず、step の `env/run/with` では使える。[GitHub 公式 context availability](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#context-availability)。原本 60829 B / 21127ce22024310b6272bfd581c7362d959d3303eccab86bdb88168c9cc5c9c2、導入 commit fb2ad5cf5ea5cf6181110e97061f89ef690e630e。

今回の失敗 run34417020868（head9331ebd0cb1ad6385752fe1b18588ef4f0aaad5b）は jobs=0、check-runs=0、workflow name がパス表記。API 保存 `root-d972-dovetail-run34417020868-diagnostic-v1.json` 13887 B / 9f9d23e16e05e2e9dbe5173a0cf57eb090cb35d0c4ead1222ecbed6e9748354f（TEMP、toold7e788）。この入力上の仕様違反は確定し、job 開始前 failure の原因候補として整合する。API は元の workflow validation エラー本文を返していないため、唯一の原因とはまだ断定しない。

修正案は job-level の RUN_ROOT 一行を外し、最初の shell step で次を GITHUB_ENV に書き、後続 step の同じ RUN_ROOT を維持すること。

```bash
printf 'RUN_ROOT=%s/d972-dovetail\n' "$RUNNER_TEMP" >> "$GITHUB_ENV"
```

診断と具体的修正案を返す。本便で dovetail の配置・dispatch は行っていない。進行中の R07 v6 は run34416548935/1、step14 の本体計算まで到達している。
