# D972 Phase 2b — 非分裂窓の事前登録 v1.1（G5 実装補遺）

- 日付: 2026-08-13
- 親登録: `docs/notes/d972_phase2b_nonsplit_prereg_v1.md`
- 実験 ID: `PH2B-NS64-v1.1`

## 1. 補遺が必要になった理由

親登録後、公式 producer は G0–G4 を通過し source shadow 432 個を得たが、G5 の「凍結 10 語と SymPy が再生成した strong presentation を語順まで一致させる」raw boolean が `false` となり、`raw_image_size=null` のまま停止した。巡回回転・逆語を同一視した二回目も同じ段階で停止した。どちらの実行でも reduction 像集合は作っていない。

原因は、有限置換群から得られる strong presentation が一意でないのに、親登録 §4 の実装文が特定の 10 語との一致を load-bearing にしたことである。凍結 10 語自体は 72 点群内で全て単位元になり、全 432 shadow の像でも全て単位元になる。しかし「その 10 語だけが群全体を表示する」という上界確認を Todd–Coxeter で直接行う方法は hard-timeout 向きでなかった。

## 2. G5 の固定修理

候補・標識・G0–G4・スペクトル・分岐は一切変更しない。G5 だけを次に置き換える。

1. 実際の有限置換群 $E=\langle X,Y\rangle\le S_{72}$ から SymPy の strong-presentation algorithm で表示 $\langle x_0,x_1\mid R_{\rm run}\rangle$ をその公式実行内に再生成する。
2. 置換群の位数が 32256、生成された表示の生成元が $(X,Y)$ に対応することを記録する。$R_{\rm run}$ の全語を certificate に保存する。
3. 各 source shadow の像 $(X',Y')$ について、$R_{\rm run}$ の全語が単位元になることを検査する。これで $X\mapsto X',Y\mapsto Y'$ は $E$ の自己準同型として well-defined である。
4. $(X',Y')$ の商像が $P$ を生成すること、拡大が非分裂で $V$ が既約であることから、像は $E$ 全体である。有限群上の全射自己準同型なので自己同型である。
5. checker は producer の strong-presentation helper を使わず、保存された全 432 対について Cayley graph を $(X,Y)$ と $(X',Y')$ で同期 BFS し、同じ domain element に二つの像が付かないことと像集合が 32256 個であることを直接照合する。

親登録の固定 10 語は regression として全 source shadow 上で引き続き検査・保存するが、表示上界の唯一の根拠にはしない。

## 3. 不変部分

- preflight と PH2-VOID gate は親登録のまま。
- G4 の非空性を先に記録し、G5 の isolatedness の後だけ像を作る順序は不変。
- 凍結スペクトルは $\{324,972\}$ のまま。
- 324 / 972 / その他 / null の行き先は親登録 §5 のまま。
- engineering probe は先行しており、`preregistration_blind=false` のまま。
- $u,c$、封印 K5、既登録量には接触しない。
