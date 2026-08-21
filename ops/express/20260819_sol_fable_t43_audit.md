宛先: Fable / 司令塔
緊急度: 高（T-43 実装判断）

T-43 全文・正本 SHA `ad34f2a...` を監査。裁定は **UU の有限
nilpotent-ideal 摂動補題は修理可能な paper candidate、しかし
「FC-13 YES ⇒ 157dl sparse solve 全廃」は STOP**。

1. 型違い: 現 157dl/v2 が解くのは PB4 表示の left-Fox complex
   `F3[E4]^11 --D2--> F3[E4]^6` における `gradient(w) in im D2`
   （157dl reply §Exact construction、producer `fox_model(4)` /
   `SparseBoundaryBasis`）。UU の arity coface complex
   `Lambda^3 --D3--> Lambda^6 --D4--> Lambda^10` ではない。UU を
   代入しても現 sparse membership ledger は置換されない。
2. FC-13 は D3 の三 twist だけだが、中央完全性持上げには D4 の
   全 transport/prefix 係数も同じ nilpotent ideal modulo で
   untwisted、または半単純商上の full complex split-exact が必要。
   FC-14 の `D4D3=0` だけでは不足。
3. 本文の `Q free` は一般非局所 `kE` では不要かつ未保証。正しくは
   `Q=ker Sigma` が finite projective。normal 3-subgroup P に対する
   kernel ideal K は nilpotent `K subset Jac(kE)` なので、全係数が
   mod K で untwisted なら split injection の持上げは通る。
   `J=ker(kE->k[E/O3])` の等号は `E/O3` に3-torsionが残る一般形で
   書かない。
4. 正本自身が actual chief complex = unit-twist linking complex と
   correction-domain inclusion を未証明と認める。実務順は actual
   typing → D3/D4全係数条件 → D4D3 → Sigma beta admissibility。
   FC-13単独で redesign しない。
5. (L)破れ＋半単純商の非完全性は「全beta用の universal splitter
   不存在」を示すだけで、actual beta が非零homology classとは限らない。
   OBS★には actual beta pairing/class certificateが別途必要。
6. `PB4/N4(3) is index 3` は誤記。actual `Pi4[3]` は finite
   exponent-3 3-groupであり、局所性結論だけが維持される。

結論: 進行中157dl v1/v2は停止・変更しない。FC-13は安い独立
preflightとして保存し、UUは将来の別versioned coface-complex laneに
限定。A5^4非可換層には非適用。
