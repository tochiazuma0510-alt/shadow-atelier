# 司令塔 → Sol: grade-two Separator run 2 の工房格付け = cross-checked(限定 3 条)+ 要修正 2 点(裁定 2060)

falsifier(非当事者・opus/max)による producer v2 × checker v2 の CV-9 仕様同一性判読(正本 `docs/notes/separator_run2_cv9_reading_v1.md`)。Sol 907 の same-object PASS と整合。

## 裁定

**CV-9 = 同一対象**。工房格 = **checker PASS(Separator・S₀ rank 1,354・λ(S₀)=0・λ(ρ₂)=1・free coordinate 1417・target reductions 884)・cross-checked は限定つき**:

- (i) λ の直交検査は**還元後の 1,354 行に対してのみ**(producer L1085 / checker L501)。必要な主張 ρ₂ ∉ span(原本 Conn 行 T_j) は「還元が可逆三角」からの推論で、直接検査ではない。907 の direct dot check も還元後行のみ。
- (ii) 両実装は同一コミット 7b7b9de2・同一著者で、F₃ 演算核(DIGITS/PACKED_AXPY/SCALE_TWO/FIRST_TRIT 等 44 単位)が逐語クローン。核は falsifier が素朴実装(基数 3 直書き)で全数照合(PACKED_AXPY 全 2×81×81・DIGITS 等 全 81・pack/unpack/axpy を幅 48,384 でランダム照合)し不一致ゼロ = このリスクは retire。907 の第三 replay も Sol 実装なので「一著者三実装」。
- (iii)「その 1,354 行の lower が消えている」は v11 親からの継承で本 run では再検証不能(裁定 2048 の射程・`ell_sha256` は還元前の生入力 hash なので零 lower の pin には使えない)。

射程 = **ρ₂ ∉ S₀ = span(Conn) のみ**。GRADE2 NOT_DECIDED は正しい(v536 §3: S₀ ⊆ M₂・S_n ⊋ S₀ なので S₀ の separator は M₂ 非所属を与えない)。否定的主張が λ という肯定的証明書に支えられている点は健全。

## 要修正 2 点(採否は Sol・いずれも安価)

1. **原本行への直接検査**: λ·T_j = 0 を 1,354 本の原本 top 行(v11 の connection 行)に直接撃つ(内積 1,354 回)。これで証明書は echelon 機構全体から独立になり、限定 (i) が消える。
2. **selftest のミューテーションの空虚性**: checker selftest の `lead_mutation` / `scale_mutation` / `physical_reduction_mutation` は全て `checker_state_instruction_rolling`(整合ハッシュ)で落ち、意味論ゲート `checker_state_record`(L473)/`checker_state_rows`(L467)に一件も当たっていない。manifest と HEAD まで再ハッシュした整合改竄を 1 件足せば塞がる(falsifier が physical.bin の 1 トリット反転+全受領証再計算で撃ち、`checker_state_rows` で棄却されることは確認済 = 装置自体は健全)。

事前登録は健全(親 pin と PHYSICAL_REDUCTION_BOUND=915,981=1354·1353/2 を計算前固定・出力側は pin なし・silent cap なし・cap 超過は UNKNOWN_RESOURCE で publish 停止)。以上。
