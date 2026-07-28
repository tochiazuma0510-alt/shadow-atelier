# 裁定 187 — (n) lane A 残差 3 点の閉鎖検収(2026-07-29 早朝)

- Sol F81-3.1 の 3 残差を実装確認: 重複 entry = MALFORMED(トップレベルスキャン・pushforward escalation と同配置)・retired key 併存 = 無条件 MALFORMED(status 読取り前)・内側 entry schema gate(null crash 解消・{} は算術 FAIL でなく MALFORMED)。Sol の 4 ケースを isolated+end-to-end の 9 検査で回帰化。
- **lane A 70/70・lane B 173/173・normalizer 51/51・全ゼロ FAIL**。設計判断(objVerify 内部不変・唯一の呼び出し元は新スキャン先行)= 承認・直呼び caveat の申告を記帳。
- これで追補 (n) の Sol 指摘は完全消込 — (o) v3 と併せ便 82 で発効請求 → PASS で EP v7 発射。
