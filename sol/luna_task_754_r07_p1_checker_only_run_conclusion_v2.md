# Luna Task 754 — P1 checker-only run-conclusion v2（即時有限修理）

## 0. 変更範囲

次の二ファイルだけ新規作成する。

- `.github/workflows/d972-r07-p1-semantic-checker-only-v2.yml`
- `sol/luna_reply_754_r07_p1_checker_only_run_conclusion_v2.md`

v1 を上書きしない。git/push/GHA/実artifact download/重い実行は禁止。

## 1. v1 実 failure の根因

checker-only run `33817618040/1`, head
`83c76d9264c652a41011703ef26ade90970fa4a8` は算術前の auth step で即停止した。
最初に保存された `producer-run.json` だけが log artifact にあり、そこでは
producer run `33814881435/1` の全体 conclusion が `failure` だった。

これは producer 不成功を意味しない。同 run は preflight, prepare,
block-0..3, join がすべて success し、旧 checker-v3 だけが既知の
`sealed_head:prepare` schema bug で failure になったため run 全体が failure
である。v1 の `test .conclusion = success` が型を取り違えた。

## 2. 必須修理

1. v1 を source に v2 workflow を作る。trigger path は v2 自身だけ、fire token
   は `[fire-r07-p1-checker-only-v2]`。
2. producer run 全体については exact id/attempt/head/status completed/conclusion failure
   を認証する。
3. jobs API を取得し、最低限次の exact jobs を id/name/conclusion で認証する。

```text
100844698807 preflight          success
100844805339 prepare            success
100846454006 block-0            success
100846453918 block-1            success
100846453996 block-2            success
100846453927 block-3            success
100847550237 join               success
100847634660 independent-check  failure
```

   上六 producer phase（prepare+4 blocks+join）の success が本質であり、旧
   independent-check failure は既知 checker-v3 bug と整合する provenance として固定する。
4. producer artifact `9916479231`、六 receipt、五親artifact、checker-v4、
   success-only upload、345/360分 cap、claim boundary は v1 から変えない。
5. workflow receipt に producer run conclusion と上記 producer job id/conclusion
   を含める。schema/version/name は v2 にする。
6. YAML parse、静的 pin 検査、checker-v4 py_compile/selftest だけを bounded に行う。

## 3. 禁止

- producer再計算
- run全体 success への偽装
- 独立 checker-v4 の算術を弱めること
- 不要な監査機能・新規探索・追加大表

## 4. reply

bytes/LF/SHA256、v1→v2差分、bounded check、実GHA未実行、下流未主張を記録する。
