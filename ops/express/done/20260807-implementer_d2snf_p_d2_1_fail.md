宛先: 司令塔
緊急度: 驚き値(STOP・express・生値のみ・素性への言及なし — 単任務2連の任務2/2完了報告に同梱)

本文:
D2-SNF-1(docs/notes/tor_sweep_design_v1_addendum_b.md §1.4 発注仕様)を逐語実施しました。cert・独立checkerとも commit --only 済み(search/d2_snf_sweep_v1.py・crosscheck/check_d2_snf_sweep.py・search/certs/d2_snf_sweep_v1_20260807.json)。

**カナリアは全11重み(k=12..32)でPASS**(D-b: rank_Qがprereg表と完全一致・D-c: k=12,16,18,20で核ベクトルが裁定727の値(1,-3)/(2,-7,11)/(8,-25,26)/(3,-10,14,-13)と符号違いまで完全一致)⟹ 実装バグによるSTOPなし・完走。

**生値**: P_D2_1(捩れゼロ予言)は **k=12のみPASS**(gcd_abs=1・torsion_primes=[]、既知の定理C-Aと整合)。**k=14〜32は全てFAIL**(torsion_primes非空):
- k=14: [2,3](gcd_abs=6)
- k=16: [2](gcd_abs=2)
- k=18: [2](gcd_abs=2)
- k=20: [2,3](gcd_abs=12)
- k=22: [2,3](gcd_abs=6)
- k=24: [2](gcd_abs=2)
- k=26: [2,3](gcd_abs=6)
- k=28: [2,3](gcd_abs=12)
- k=30: [2,3](gcd_abs=6)
- **k=32: [2,3,5](gcd_abs=60=2^2*3*5)** ← p≥5の素数が唯一ここに出現

独立checker(search/を一切importしない別実装)が全11重みの rank_Q・kernel・elementary_divisors・torsion_primes を完全一致で再現(cross-checked、両実装が同じバグを共有していない限り実装ミスの可能性は低い)。

**私(実装係)の判断が要る2点**(素性への言及は避け、設計判断としてのみ記載):
1. **測定対象の座標化**: 追補§1.4 D-aは「深さ2括弧を整ベクトルとして書く」とのみ指示し、target空間の具体的な整数格子の取り方(内在的Lyndon基底 vs ambient tensor座標)を明記していません。私は「自由Lie環はtensor環に飽和部分加群として埋め込まれる(Reutenauer, Free Lie Algebras)」という標準事実に基づき、ambient tensor(word)座標での SNF が内在Lie基底での SNF と一致するという判断で実装しました。この判断は追補本文に記載がなく、**本追補にも私の実装にも独立の検分がありません**(【B-GAP-2】は Ihara括弧の閉形式自体の未検分を述べていますが、この座標化判断は追補未記載の追加判断です)。数学者/Solでの検分を要請します。
2. **p≥5限定の有無**: P-T-1本体は「全ての素数はp≥5に限る」と明記(TOR-S3・Maschke由来)ですが、P-D2-1の凍結文言(§1.2)には同じ限定が明記されていません。p=2,3の捩れは(S3構造由来として)プロジェクト全体で想定内かもしれませんが、**k=32のp=5は明記されたp≥5限定の枠内で唯一の非自明事例**です。P-D2-1の量化子(p≥5限定を含むか)の確定判断を仰ぎます。

以上、判定語・素性への言及を避け生値のみで報告します。作業は本件でSTOP、次の指示をお待ちします。
