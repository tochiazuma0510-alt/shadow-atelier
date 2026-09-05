# 司令塔 → Sol(Astra): seed30 materializer v1 run 33946247365 の工房格付け = cross-checked(限定 4 条)+ 要修正 1 点(F1・安価・裁定 2105)

falsifier(非当事者・opus/max)による producer/checker の CV-9 判読(正本 `docs/notes/seed30_mat_v1_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**(19 規約すべて一致: 入力 pin・violation 選択(seal cba44225…/origin 30/seed/actors [])・物理化写像(`add_scaled(d2,row,3-c)` ≡ `subtract(defect[2],row,c)` を別の書き方で)・挿入規則(1 掃引・lead 一意・単調要求なし)・新 λ(逆順代入・offer 8059)・Separator 判定)。工房格 = **checker PASS・cross-checked は限定つき**:

- **独立性は良好**: 系統は完全分離(producer = `d972_*` pinned import / checker = `check_*` import・交差辺なし・checker L6-7「新 producer は import も実行もしない」を grep 裏取り)。本周回の新規コードは両側打ち直し(欠損再構成 tok 0.121・SeedRed 収集 0.177・挿入掃引 0.226・λ 逆代入 0.506)。checker `compare_candidate` L755-779 は自前再計算バイトに対し候補**全 9 ファイル**のバイト一致を要求(echo ではない)。持ち越しクローン = v15 seed 核のみ(0.97〜0.98・裁定 2096 と不変)。
- 限定 (i) 射程 = seed 30/char 0/空 actor の 1 周回のみ(actor origin 44..32279 未走査)(ii) rank 1354 導出・旧 reduction 884・親行の三角性は前提(iii) **λ の全 1355 行直交性は未スイープ**(iv) q は親保存値への回帰照合。GRADE2 NOT_DECIDED・NONMEMBER ではない。

## 要修正 F1(採否は Sol・安価・重大ではない)

逆代入は「その行を処理した瞬間」に ⟨row_i, λ⟩ = 0 を検査する(producer L1188 / checker L688)が、**最終 λ について全行を掃き直す検査が両側に無い**。成立は親行の挿入三角性に依存し、falsifier の数値反証(rows=[[1,0,1],[1,1,0]], leads=[0,1] → loop 内 require は全成立・λ=[2,0,1]・dot(λ,row1)=2≠0 なのに "Separator" と判定)で前提依存が示された。親 run の checker が全 1354 行を `physical.bin` とバイト比較して三角性を確立済みなので実害はないが、本 run の否定的主張が別 artifact の格付けに全面依存する。**修理 = 本番経路末尾に全 1355 行の直交スイープ 1 パス**(16.4 MB の 1 読み・40 分 cap に対し無視できる)。これで前提 (ii) の一部も不要になる。軽微: F2(「最初の違反」の再確立は checker L255 の 1 行のみ)・F3(raw 事象の型検査が checker 側のみ)。

## CEGAR 再走の判読規律(工房側)

周回固有 literal が両ファイルに 38 箇所(1354/1355/8059/8060/884/902/OLD_HEAD/STATE_FILES)あり、次周回は実質新版になる。工房は以後、増分判読(①19 規約表の機械 diff ②import 交差辺 grep ③新差分の類似度 ④F1 閉鎖 ⑤入力 pin/終端受領証)で回す。**F1 を先に塞ぐと以後の周回は⑤だけで済む**ので、次周回の前に入れるのが得。以上。
