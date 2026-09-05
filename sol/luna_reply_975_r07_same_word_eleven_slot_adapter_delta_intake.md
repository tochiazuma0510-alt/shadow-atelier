# Task975 — 同一ordered SLPの独立11slot adapter差分intake

F1. reply958全文、v518/v511/v516全文を前提に、自系v9 endpoint checker・owner join v9・四B checker v4の実経路、v478/v484/v512を静的に辿った。変更は本返信のみ。新producer算術の読取/import/コピー、ローカル数値/Python/import/AST/GAP、network/git/credential/追加agentはない。継続run33984832010/1（launch `b8c9e95ddd0183d9e43b7fcc961cb251fdaea13e`）についてrootはcap1/resume32と全出力/親不変保存success、独立checker工程が19:09:25Z failure（step wall754秒）と通知した。原因・新rank/terminalは未観測で、算術不一致とは推測しない。公刊v1は不変。本intakeは診断修理の待ち条件ではない。

結論は、**独立Fox/printed演算の原始とflat直接照合は既存であり、欠品はone-root DAG adapterと現physical codomainへのtyped row adapter**である。producer-only `ProducerAllSeven` を呼ぶ案は不要。以下のA/Bは将来のversioned実装単位の提案で、今回新たに実装・実行したものではない。

F2. 実在する独立checker入口は `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v9.py`（113012 bytes / `7b2beb39dbdc65494f85fa4451ed69d99a22685d11f1d4fef6e671322d24098d`）である。

| 実関数と行 | 既にある演算/契約 | 新adapterとの差分 |
|---|---|---|
| `LocalPc:152`, `LocalQ:184`, `local_quotients:192` | pinned Q3 JSONからPB3/PB4 marked quotientを独立構成。`mul/inverse/eval`、局所PB presentation gate | 型・markingを現root ownerへ束ねる。旧Task601固定CLIを現ownerへ流用しない |
| `cfox:194`, `LocalWords.translate_vector:206` | flat PB wordの左Fox、`(component, group_element)→F3`、左乗算 `t*h` | DAGの一般product/inverse/Actへ接続し、whole wordのflat展開を除く |
| `build_checker_light:1679`, `IndependentAllSeven:1750` | producer/旧checkerのimportなし。actual十coordinate/十一specをlocal算術で構成 | 新input manifest・context hash・one-root DAGを受けるversioned入口 |
| `coordinates:1798`, `occurrence_prefix_gate:435`, `occurrence_prefix_contract:481` | 10 unique blobs、重複coordinate一致、実g760依存の十一prefix/sign/label | 各node endpoint/Foxを同時memoize。11 occurrenceをcoordinate dedupで失わない |
| `occurrence_column:1778`, `direct_column:1871` | 一つのflat `(delta,relator)`、literal conjugate、`g760+conjugate` のH1/H2/P Fox差分、十一occurrence和との全sparse一致 | 任意のcurrent ordered SLPの同じrootへ拡張。既往23 reached seedsのcanaryを新root全体の代用にしない |
| `row_key:1577`, `decode_row_key:1587`, `_serial_group:1655` | typed block/component/elementのcanonical sparse行 | node/slot/owner/root hashを外側receiptへ付け、block別component範囲を厳密にする |
| `Context:1215`, `qnorm:1424`, `aggregate:1494` | six source tagsのPB3 normal、precision2、現在の二hexagon aggregation | これらは11typed PB rowsを直接受けない。後述Bのtyped row→normal→grade bridgeが必要 |

`build_checker_light` は `runtime={old:LocalWords,e3,e4,g760,pcontexts,model}` を作る。generic boundary/campaignを起動せず、`boundary_row:1714` が期待する `runtime['boundary_group']` も作らない。後者をこのlight runtimeで呼ぶことは解決策ではない。v9 `main:1955` / `validate_payload:833` はTask601の固定parent/rootを要求するため、新版は実算術原始を使う薄い別entryに切る。

F3. Aの公開型を以下に固定できる。値は `E3=(perm36,pc4)` または `E4=(perm144,pc10)`。既存blobは各々40/154 bytes（permutation bytesの後にPC trits）、演算は `pmul(a,b)[i]=b[a[i]]` とLocalPcの積、inverseは双方の実逆元。decodeには長さ/全置換/PC各0..2/対応したmarked group ownerを要求する。E3のPB generator componentは1..3、E4は1..6。raw rowは `dict[(component,typed_element),1|2]`。公開keyは `b'R'+bytes(block,component)+len(blob).to_bytes(2,'big')+blob`。block1/2はE3、block3はE4で、E4→E3変換や `%6` はない。

| ordinal / label | block / sign | coordinate / type |
|---|---|---|
| 1 H1_fxy | 1 / + | 0 / E3 |
| 2 H1_fxz | 1 / − | 1 / E3 |
| 3 H1_fyz | 1 / + | 2 / E3 |
| 4 H2_fux | 2 / − | 3 / E3 |
| 5 H2_fxy | 2 / − | 0 / E3 |
| 6 H2_fuy | 2 / + | 4 / E3 |
| 7 P_b1 | 3 / + | 5 / E4 |
| 8 P_b2 | 3 / + | 6 / E4 |
| 9 P_b3 | 3 / + | 7 / E4 |
| 10 P_b5_inverse | 3 / − | 8 / E4 |
| 11 P_b4_inverse | 3 / − | 9 / E4 |

各node/unsigned coordinateで `(a,J)=(ev(W),D(W))` を保持する。積は `(a,J)*(b,K)=(ab,J+L_a K)`、inverseは `(a^-1,-L_(a^-1)J)`、identityは `(1,0)`。`Rel(s)` は同じ固定辞書のliteral relatorを各specのleft/rightへ代入し、最初の六specだけF2→PB3のx↦A12/y↦A23埋込を行う。`Prod` は記録されたnative順にleft foldし、`Ref` は同owner/contextのprior nodeだけを読む。文字列/ID/lead順へのsortは語の変換として許さず、sparse行の表示sortと分ける。

`Act(P,W)=PWP^-1` は一般に `(pup^-1, D(P)+L_pD(W)−L_(pup^-1)D(P))`。子のendpoint-oneを当該slotで実際に確認した場合だけ `L_pD(W)` へ短縮できる。P自身がkernelとは仮定しない。actor tuple `(t1,...,tm)` はv518(3.2)どおりt1が最外、右extensionは最内。Relすべての11endpoint-oneを旧23-seed canaryから推論せず、一般再帰を残して新rootの十一endpoint gateを直接出す。符号2はInv、Inv(Prod)は順反転込みである。

A出力は一つのSLP manifest/root hash、reachable node receipt、11件のordinal/coordinate/type/endpoint/unsigned Fox row hash＋EOF。memo keyはowner/context/node hash/coordinateを含む。coordinate0のunsigned計算を共有してもordinal1と5のblock/sign/prefix receiptを分ける。normalized pairは974のCと同じrootへ束ねる。v9 `exponent_pair` / `b'E'+index` は通常指数mod3で、18で割ったnormalized pairの代用品ではない。

F4. Bのprinted aggregationもflat不要で具体化できる。unsigned slot pairを `F_o(W)` とし、固定g760の各slot pairと掛けて `F_o(gW)` を得る。既存 `paper_product:1573` は**表示因子を逆順に連結**するので、DAGのnative ordered Prodへこのreverseを二重に適用しない。現actual native列は、H1=`(3,+)(2,−)(1,+)`、H2=`(6,+)(5,−)(4,−)`、P/A18=`(11,−)(10,−)(9,+)(8,+)(7,+)`。これはv9 `_pentagon:1863` / `pentagon_factor_word:428` のnatural contextsと同じ式である。

一般のpair積/inverseで三printed blockの `D(B(gW))−D(B(g))` を直接計算し、endpointと全sparse rowを保存する。rootの全slot endpointが1なら、これと `sum_o sign_o L_(U_o)D_o(W)` を別経路で照合できる。v512§1の実prefixは、`G_ab=slot_ab(g)`、P自然contextsをG0..G4として、順に `1, G_yz, G_yz, G_uy G_xy^-1, G_uy, G_uy, 1, G4^-1 G2^-1 G0 G3, G4^-1 G2^-1 G0, G4^-1, 1`。prefix自体はendpointに由来し、gのFox差分で相殺したからといってidentityへ置き換えない。Dをunsignedで保存する方式ではsignを一回だけ掛ける。endpoint非1ならこの短縮式を使わず、相違/未適用を記録する。

**現gradeでのP側の必須条件は全五E4 endpointとtyped receipt、同じrootのprinted P/A18とoccurrence/direct整合である。P側Fox行が零という条件は現rho2 equalityのgateではない。** v478§2(2.7)/§3末尾は全十一slotとdirect H1/H2/pentagon canaryを保ち、現145152→48384 graded mapへordinal1–6だけを入れると明記する。残る五P endpoint/rowをsealed receiptとして保持した後、現在のcodomainはPB4 blockを明示的に落とす。したがって48384一致から未収載P成分の零を推論せず、逆に未登録のfull P零を当該grade MEMBERへ追加しない。v518条件5はこのtyped current codomainへのprinted aggregationとして接続する。full P/A0側の未射影PB4残差・より細かい方程式は別のowner/targetを要する。

F5. Bで新たに必要なのは、直接得たfirst-sixのtyped PB3 Fox rowsを現Q2/PB3 normalへ写す操作である。v9 `qnorm` はflat F2入力で、このrow APIは持たない。実現式はv437(2.3)を現Q2で用い、`h e_a → e_z,aug − h a e_b − h a b e_c`、`h e_b→h e_b`、`h e_c→h e_c`、a=X/b=(YX)^-1/c=Y。先に各occurrenceのrowを保ち、translation/signを適用してからnormal/集約する。PB3の三generatorのまま既存二component配列へ詰めない。

E3→Q2は任意のblob型変換でなく、実marked coarse Q0への射影とN→N/N³の商を必要とする。具体候補はE3の36点置換を、先頭9点のPSL pと三9点blockの `u↦s_i u+t_i (mod9)` に分解し、全36点一致・s_i∈{±1}・s2=s0*s1を確認、`e0=[s1=-1], e1=[s0=-1], v=(t0,t1,t2) mod3` とすること。これはv443§2のsection-left/kernel-right型で、X=(1,0,0)、Y=(1,1,1)のactual liftとmarking/product/inverseを結ぶ新mapである。PC因子を落とす根拠はE3のcoarse射影であり、E4を同じ型へ投げない。このdecoder/commuting-squareは**未実装のB作業**として区別する。

normal後は `E(v)=prod(1+u_i)^v_i mod I³`、character/Fourier・transport・monomial/PSL順を現mapと一致させる。sourceはd0=24192/d1=72576/d2=145152/aux8でsource lower=96776。physicalはd0=8064/d1=24192/aux4でlower=32260、top=48384。raw source lower零とphysical lower零、associated top四B和と完全filtered aggregationは別gateである。source lower零の後にだけ四Bのassociated mapと直接topの一致を読む。

owner joinの実入口は `check_d972_r07_grade2_forward_adjoint_maps_v4.py:IndependentContext:317/prefix_record:371/aggregation_records:443`。六triples `((0,0,1),(1,0,2),(2,0,1),(3,1,2),(4,1,2),(5,1,1))`、四character順、六monomial順、PSL index、実marking/word hash、六affine prefixを全て結ぶ。Task712のB manifest/source pinsとcurrent source/ownerの同じ値を要求し、一般の物理行作用へ置き換えない。新Bはこのownerで `Pi_H(direct eleven rows)` のlower全32260=0/top全48384=rho2と、同rootのsource lift→四B和を比較する。

F6. exact fresh-rho2 parentはrun33839962829/1、head `17a8439c766d92719d7ae7d35846ea444da598fa`、artifact9925190479、name `task640-fresh-rho2-v17-33839962829-1`、ZIP6049643 bytes / `01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4`。`check_d972_r07_targeted_grade2_owner_generated_join_v9.py:rho2_parent:384` がacquisition/variant/七payload/roots/成功verdict/packingを結ぶ既存入場型で、sourceは114748 bytes / `6e53d2947231f26183c4a97906fccee067d3d034d06d97a0b968ec5db2b209cd`。

今回 `%TEMP%/shadow-atelier-rho2-run33839962829` の下記七fileをbytes/SHAで直接読み、固定値と一致した。数値unpack/新零照合は行わず、lower/top既往一致は成功verdictのmetadataとして読んだ。

| file | bytes | SHA256 |
|---|---:|---|
| task640-payload/manifest.json | 26047 | `55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488` |
| task640-verdict.json | 418 | `cdf0654738a10acf59844df3b9dda5ab8efdf2e387bba7d69b691a4ad46b2848` |
| task640-payload/rho2.bin | 12096 | `b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e` |
| task640-payload/rho2-dense.bin | 48384 | `abfafbc7521af43c75f1b5a73a6da5d37b90ec1648b649401d684a58cf16752e` |
| task640-payload/lower-dense.bin | 32260 | `c5657f998c12426cb1f2c1b4ae1e3a99ce4df9d61101eb33fba7921303bb4830` |
| task640-payload/target-dense.bin | 80644 | `122dca3cf3dc3299214f1ba4c2bc5b82dbe64e510f8aef482329316c2a935ea2` |
| task640-payload/authenticated-roots.json | 255846 | `af1b035e0eb0af6e593770affb52a52905609fd9c19e988b0b7e8cf69e7592c5` |

元rootは `Compose(C_<1,C_T)`、source ancestry `315f9d9be5c7301b7b54ca5f545a17ca1d491f2d1d24e40f426ce831388f2908`、words `90ba6033…`、g760 `518f0982…`。新DAG rootはこのfresh targetを減らすDelta C2であり、元C1 rootを新rootへ改称しない。現在の `e902cf3b…` 等のtarget剰余やDERIVED lambda receiptをoriginal rho2 bytesの代わりに比較しない。線形readoutの元rho2 hash、旧差分親列、全new step/state head、SLP rootを同時に結ぶ。

F7. 最小追加closureは、(i)974が出すone-root DAG/target readout/normalized pairとcurrent accepted HEAD/owner/source、(ii)上記fresh-rho2 artifactのmanifest/verdict/七payload＋acquisition証拠、(iii)44 relators/PURE_Q1_WORDS/g760/必要なE normalizer literalのraw辞書、(iv)Q3 PB3/PB4 marked JSONとfull36 marking、(v)四BのTask712 manifest/完全payload、(vi)新A/Bのsource/runtime receiptである。P1/Task554/Conn/physical ancestryは974のcompiler provenanceを認証し、旧scanや全old instruction算術の再走をこのDへ追加しない。v9親入場をそのまま使う場合、path-signatures/signature-bucketsの保存bytesも固定七payloadの一部として認証するが、旧bucket数値再計算は不要。

実metadata確認済みの基礎入力は、Q3 JSON `ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json`=231570 bytes / `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`、full36 marking=4709 / `625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba`、paper words=115928 / `90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893`、四B checker v4=49643 / `7ba94ee884db49bbe42d11a84228a6bdf7c88a3918407928af90c71b65fe4a29`。frozen v9の `SevenSources.authenticate` を利用する版なら同SEVEN_PINS全六件もhash依存として残す。producerの旧31contexts/59049 fine-deletion runtimeはこの独立direct-substitution法の算術入力ではなく、旧受理parentの由来である。十一slotだけを独立31-context証明と呼ばない（v512§3）。

F8. 実装の切り方はA=`typed_same_root_DAG`（入力DAG認証、全node general endpoint/Fox、11slot sealまで）、B=`direct_printed_current_grade`（A＋固定g760三printed式、direct/occurrence一致、E3→Q2/normal/完全physical、fresh rho2比較まで）。Aだけならendpoint/Foxの有限receiptであり、grade MEMBERではない。Bにも未登録full P零・IM所属・無限cofinal条件を追加しない。現sourceを修理せず新版へ切る。

必要canaryは実関数を通す少数のものにする。①非可換x,yでProd順のswapとAct_x(Act_y(R))逆転を拒否し、Inv(UV)のendpoint/FoxをInv(V)Inv(U)と一致させる。②nonunit childのActでD(P)項を勝手に消す実装を検出、root-unitの場合だけ短縮式と一致。③ordinal1/5の同coordinate・異block/sign/prefixを両方保持し、一件削除/二重適用を拒否。④slot10 sign/prefixとP native因子順の変更を実direct/occurrence比較で拒否し、E4 154-byteをE3 40-byteへ渡すmutationも拒否。⑤同じendpointでも異なるFoxを持つwordを使い、endpoint-onlyの代用を拒否。⑥owner/marking/g760/root hash/Ref prior性を一つずつ変えたtyped refusal、および全sparse/packed末尾1byteを拒否する。fixtureの期待値は新producerからコピーせず、自己系の短いflat cfoxまたは明示式をanchorにする。新runtime上限や成功値はここで予測しない。

AUDIT_975_VERDICT: INDEPENDENT_LOCAL_FOX_AND_PRINTED_PRIMITIVES_IDENTIFIED; ONE_ROOT_DAG_AND_TYPED_CURRENT_PHYSICAL_ADAPTERS_SPECIFIED_NOT_IMPLEMENTED; PB4_DROPPED_GRADE_BOUNDARY_EXPLICIT; FRESH_RHO2_METADATA_PINS_MATCH; NO_NEW_NUMERICAL_RESULT; CONTINUATION_FAILURE_DIAGNOSIS_PENDING; verified=false
