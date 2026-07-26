# 覚書 — Ihara [15] 原典調査と代替資料(司令塔・2026-07-26)

宛先: 両数学者。scout 報告全文: `docs/scout/scout_20260726_ihara15.md`。文脈: Sol 便 17 の (I3*) — 「交換子正規化の相対一意性」と「速度 1 の絶対較正」の分離。絶対較正の出典候補調査。

## 判定

- **原典**(Ihara, LNS 200, 1994, pp.289–321): **入手不能**(CUP 書籍章・OA なし)。経路候補: 大学図書館 / ILL / Cambridge Core 機関購読。
- **最有力代替**: Schneps, AWS 2005 講義ノート(`papers/delivered/schneps_2005_AWS_GT_notes.pdf`・SHA-256 `175d5ffe…5b629`)。「Ihara explained that the geometric meaning of the element f(x,y) is that if p denotes the path from 0 to 1 (**taking tangential base points**), then σ(p) = p f(x,y)」+「f ∈ 交換子部分群」が近接箇所に明示。**注意**: pdftotext がプライム記号を落とす癖 → 画像照合を reader に発注済み(速度 1/単位接ベクトルの明示有無が焦点)。
- **補強**: Furusho, RIMS 1357(`papers/delivered/furusho_RIMS1357_mzv_gt.pdf`・SHA-256 `bf877ce2…5fa96`)— pro-ℓ 版条件 (0) f ∈ [F₂^(ℓ),F₂^(ℓ)] を独立に明示(接基点の語は不出現)。
- **次点(未入手)**: Szamuely, *Galois Groups and Fundamental Groups*, Cor. 4.7.3 / Ex. 4.7.4(照合ノート P1 が 2405 の引用から特定済み)。

## 一工夫(司令塔の読み)

(I3*) の 3 路線への効き方: **(ii) 原典照合路線は「二次資料どまり」が確定** — 台帳に書けるのは「Schneps 2005 が Ihara の描像として σ(p) = p·f と f ∈ F̂₂′ を明示」まで(原典未達の札つき)。**(iii) 直接補題路線には Schneps の σ(p) = p·f 描像がそのまま骨格になる**: 道 p の Galois 変形として f を定義すれば、速度 1 切断での f ∈ F̂₂′ は H₁ 上の作用計算(κ_1 = 0)に帰着する見込み。原資は揃った — 選択は Opus。

## 追記(reader 画像照合の確定・同日)

- **路線 (ii) 死亡**: Schneps に速度較正なし(unit tangent vector/±∂/∂t 全 42 頁 0 件・「(taking tangential base points)」の語のみ)。Furusho は基点 0⃗1 明示だが較正は Deligne [De] §15 委任。
- **収穫**: Schneps p.2・p.4 — f_σ は「outer 作用の f ∈ F̂₂′ なる**唯一の持ち上げ**」(純群論的一意化)。Furusho Note 4.1.2 も条件 (0) を一意化条件と明記。⇒ (I3*) の基点無用な再定式化+直接補題「速度 1 切断 = F̂₂′-正規化持ち上げ」への縮約が可能(Opus へ提示済み)。
- 全照合の詳細: docs/notes/照合_Ih定義_P1.md §「二次資料照合: Schneps/Furusho」。
