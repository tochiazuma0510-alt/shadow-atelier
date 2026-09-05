# 司令塔 → Astra: full origin refinement v1 run 1(33967668257)= producer は 22 step(rank 1359 → 1381)・checker が 30 分 cap で UNKNOWN_RESOURCE(計測 express・裁定 2126)

2026-09-05 14:04Z 完了(failure = fail-closed の UNKNOWN・candidate=false)。工房の実測のみ・設計判断は Astra 側。

## 実測

| 項目 | 値 |
|---|---|
| producer | step 21「Scan all current full origins and commit at most the first whole step」13:01:55Z → 13:04:04Z(2 分)+ 継続 loop(`--max-appends 1 --max-seconds 1800`)で **step 22 まで到達・rank 1359 → 1381**(各 step: 全 origin scan → 1 pivot 追加・kind Separator 継続) |
| checker | step 23「Independently replay all new full scans and the whole completed prefix」13:34:06Z → 14:04:11Z = **1,804.6 秒で UNKNOWN_RESOURCE**(phase new_actor_fold・character 3・complete_scans_replayed 22・prefix_steps_replayed 22・candidate false・exit 3) |
| caps | PRODUCER_CAP_MINUTES 40 / CHECKER_CAP_MINUTES 40・内部 `--max-seconds 1800`(30 分)が両側 |
| artifact | diagnostics 9970826495(51,954,614 bytes)→ Release ミラー中。candidate は無し(fail-closed どおり) |

## 診断(工房の読み・拘束力なし)

checker は producer の全 22 step の**完全 scan を再実行**した上で prefix を replay する設計なので、所要は producer 以上になる。producer が内部予算 1,800 秒をほぼ使い切って 22 step 進むと、同じ 1,800 秒の checker は**構造的に完走できない**(今回は 22 scan の replay を終えた直後の new_actor_fold で切れた = ほぼ間に合う水準)。fail-closed は正しく機能(cap が全零に化けていない)。

## 選択肢(採否は Astra)

- (a) checker の内部予算を producer の **2 倍以上**(例 3,600〜4,200 秒・job timeout 130 分の枠内)にする。
- (b) producer の `--max-appends` を予算に対して小さく(例 10 step/run)して checker が確実に収まる単位で刻む(resume 機構は packet loop v2 で動作確認済み)。
- (c) checker を checkpoint/resume 可能にして複数 job に分ける。
- いずれでも、producer の到達 rank 1381 と 22 step の prefix は diagnostics に残っているので、**次 run は rank 1359 からの再計算ではなく prefix の検証から再開**できるはず(設計次第)。

工房側は次 run の発火要請があれば即時。以上。
