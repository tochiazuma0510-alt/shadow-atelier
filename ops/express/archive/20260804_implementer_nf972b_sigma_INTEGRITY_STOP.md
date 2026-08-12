宛先: 司令塔
緊急度: 今すぐ(INTEGRITY_STOP・σ辞書が構築できない・作業停止中)

本文:
指示通り σ ∈ S₉ の機械決定に着手しましたが、**σ が存在しないことを示す機械的証拠**が出ました。指示のfail-closed規定(「候補が0なら本物の不一致…INTEGRITY_STOP」)に従い、ここで停止・保存・速達します。

**手順と結果**:
1. S4.v2.json の `settled_detail`(54行)を自前パーサで独立に読み、各行の `automorphism_witness` を P_cert として抽出。
2. 同じ行の `f_word` を自分の生成元(Xperm,Yperm)で評価した置換を P_B として算出。
3. σ*P_B*σ⁻¹=P_cert を全54行で同時満足するσをRepresentativeAction+Centralizerのcoset探索で求めたところ、**候補0件**(基点行=3・centralizer位数9・9候補全て他の行で不一致)。

**原因の特定**: conjugation は cycle type を保存するため、σが存在するための必要条件は「全行でP_BとP_certのcycle typeが一致すること」。これを直接検査したところ、**一致するのは54行中わずか7行**でした(scratchpad/diag_sigma_check.log)。例:
```
row 2 m=8 PB=[] Pcert=[4] sameCycleType=false   (PB=identity・cycle type[]なのにPcertは4-cycle成分を含む)
row 7 m=2 PB=[,,,,,1] Pcert=[1,,,,1] sameCycleType=false
```
cycle type が違う以上、**いかなるσでもP_BをP_certへ共役で移せません**(数学的に σ 探索は必ず失敗する)。

**推測(検証はしていません・司令塔/数学者の判断を仰ぐ点)**: `automorphism_witness` は S4.v2.json 生成スクリプト(week3-psl-common.g の RunPSLWindow)を読んだ限り、shadow元 f そのものではなく、「isolated/settled 判定」用の**別の等式** h⁻¹Xh=Xᵘ ∧ h⁻¹Yh=f⁻¹Yᵘf **を満たす conjugator h** です(f の点ラベル違い表現ではなく、f から構成される別の方程式の解)。これが「格納witness」の指す対象として正しいかどうか自体、私の側では判断できません。指示の「P_certの格納witness」がこの `automorphism_witness` で正しいか、あるいはS4.v2.json中の別フィールド(またはA側から独立に届く別データ)を指すのか、確認をお願いします。

**現状**: v1・v2 cert は既存のまま(前回報告済み)。v3 は書き出していません(σが求まらない限り書けないため)。診断ログ: `scratchpad/diag_sigma_check.log`(cycle type比較)。スクリプトの σ 探索部分(search/probe/wac_v1/nf972_sourcemap_b_run.g・「S4側 sigma 辞書の機械決定」節)は実装済みで、正しい P_cert の定義さえ確定すれば即座に再実行できます。指示をお待ちします。
