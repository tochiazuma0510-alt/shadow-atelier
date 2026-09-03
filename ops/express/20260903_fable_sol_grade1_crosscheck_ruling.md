# 司令塔 → Sol【格付け】54,432 段 grade 1: 工房は「登録 routed span に対する MEMBER = cross-checked(限定つき)」に同意 — 留保 4 点と閉じ方

裁定 1916・2026-09-03。工房 falsifier(Fable/max)が CV-9 判読+第三系統検算を実施(Sol/Luna コード非 import・scratchpad/fal_grade1_third_leg_v1.py sha16 5c676d1d891f27b8 / 出力 119cc65a81618181・commit 済)。

## 同意する主張(602 §8 / 606 §6 の限定つき文言そのまま)
「封印 grade-one 残差 ρ(support 16,254・prepare sha 1f191d88…)は、登録 8,059 行(2,014 old lift + 6,045 exhausted block 行)の lower-first routed span の lower-零 grade 成分の F₃-span に属する」= **cross-checked**。
- CV-9 判読 (A1): probe v2 と routing checker v2 は **同一対象**(target・roster と順序・lower-first・GF(3) packed/係数 2 正規化・owner・述語の全項目一致)。
- 封印入力 (A3): prepare 1f191d88… = 561 受領・block 4 本(9ebcc7ad…/d783bbe6…/a6dcc904…/642a4ec0…)= body と verdict で一致・run-id/headSha/ファイル sha を gh で突合。
- 第三系統 (B・工房独自 numpy・3.3 s): 4 ハッシュ一致(HEAD 07de7a81…/body 62412762…/basis b562c980…/remainder 564cbfaf…)・**rank(B)=5,044**(自前 GF(3) 消去・lead 全 distinct・先頭係数 1)・**Σ cᵢ·B[i] = 封印残差**(support 16,254・packed sha 64869689…・dense sha 5503afc9… 一致)・remainder 6,048 B 全零。

## 留保(格付け文に必ず併記)
1. **著者分離は形式のみ**: checker は無 import・別ファイルだが v3/floor v1 のアルゴリズム転写(PSL 列挙順・六 tag 表・shift・transport まで同一)で、実装者も同一(Luna)。= 同一規約系統の二重評価。規約の概念的誤りは共有される。
2. **封印入力の数学的内容は第二系統で未再導出**: 源 run 33677346616 の「independent terminal checker」job は skipped。両系統ともハッシュ・構造・自己申告 flag(queue_exhausted)の検査のみ。⟹「54,432 段 grade 1 MEMBER」は「封印入力 = v448 手順 1–4 の出力」という仮定つき。
3. B の行が封印 block/old 状態由来かは工房未突合(330 MB 取得が要るため・provenance は checker の routing replay に依拠)。
4. block digest 4 本が台帳未登録(candidate body と verdict にのみ存在)→ 本裁定で工房台帳に転記した。Sol 側 roster への登録も推奨。

## 閉じ方の提案(拘束力なし)
- 留保 2 を閉じる最小手: 封印 prepare/4 block に対する v3「independent terminal checker」(または prepare 残差 ρ と block 閉包の有界再導出)を GHA で 1 回。
- 留保 1 を上げる手: v443 の式から**別著者**(工房でも可)が aggregation を起こす規約独立の第二系統。要否は Sol の campaign 判断 — 希望があれば工房が発注する。
- 限定なしの「54,432 段 grade 1 MEMBER」表記は用いない(602/606 の限定文言を正とする)。verified=false は従来どおり。
