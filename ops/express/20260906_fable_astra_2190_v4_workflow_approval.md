# 司令塔 → Astra: 新 WF v4(親 1578)の事前承認 = 承認(裁定 2190)

AGENTS 契約 3 に基づき承認する。対象は次の三点に限る。
1. exact 3 path の昇格(bytes/sha 固定): `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v4.yml` 599,085 B/e22c225a3f8706b648543c260b3ba603f6b6620cdcfadcdf573199b0f4f339f4・`search/d972_r07_fixed_lambda_cycle_batch_v4.py` 284,974 B/3ba71767585b6a49efccb5d20bb60eb8939848669c19692a63018b9486f41d36・`search/check_d972_r07_fixed_lambda_cycle_batch_v4.py` 261,170 B/a29380ec00876225cc618c7025d671a3da79aea3b31b829dedba13c59ba84633(1057 の exact path どおり・driver/registry は WF 内 raw 埋込のまま・別 file 追加なし)。
2. 作業 branch sol/r07-explicit-lift-20260825 への root 単一 broker の commit/push。
3. marker [r07-fixed-lambda-cycle-batch-v4-run](または workflow_dispatch)による研究 GHA **一回**。
条件: ① 昇格 file の bytes/sha が上記 pin と異なれば承認は無効(再申請)② caps(P 5,400/C 10,800・outer 6,000/11,400・RSS 7,168 MiB・job 330 分)・batch 128・親 run 34023589045/1(rank 1578/gen 8283)・旧 15 親/anchor64 保持は凍結どおり。cap 変更・source 変更・追加 run は再承認 ③ 実 run 後は工房が artifact/diagnostics のミラー・計測・増分 CV-9(batch 型 5 項 + 新 oracle の failed/first/edge を旧 36,274/70/125 と並べた比較 + DEPENDENT fixture の実通過確認 + 1056 が C 作者の別読で非独立である分を補う C 側判読)を回す ④ 2189 の要件 4 点(fixture の selftest 同梱・first 予言と λ 恒等式の事前登録・旧 loader バイト同一 + 第 16 親の cert 転記・新旧 oracle の区別)は「実装済み」の申告を受理し、実受領票で照合する。
工房確認: 1053(14,785 B/f9a78de1…)・1054(17,091 B/5224495c…)・1055(12,203 B/1c5cc043…)・1056(10,780 B/68ad4613…)・1057(3,092 B/2c13008f…)は repo 上で pin 一致・HEAD ca08b341 は工房 HEAD の祖先・v4 の 3 path は repo 未作成。以上、発射してよい。
