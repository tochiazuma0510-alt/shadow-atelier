# Luna reply 369 — A4 driver newline repair v21

## 結果

`search/d972_r07_word_independent_successor_kernel_gha_driver_v21.g` を追加した。v20 の `D366NewTail` で literal `\\n` を生成していた3か所を、v16 と同じ GAP source escape `\n` に直した。生成 inner では `end;;`、`Exec(...)`、`if ... fi;`、最終 `Print(...)` がそれぞれ実改行で分離される。

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v21.g` | 5543 | `9a4c26f95b75370ffa88644a393ad973e8a84c514c0e74c747f66a80c401e343` |

producer/checker は変更していない。v21 が保持する pin は次のとおり。

- producer v12: 7209 bytes, `816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5`
- checker v14: 8074 bytes, `7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47`
- frozen v6 driver: 13775 bytes, `a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0`

mode/hot-path/cap/owner 算術は v20 から不変で、versioned output だけ `v21diag` に隔離した。outer gate と inner mode はともに `D366Mode` / `D345Mode = "PRODUCTION"` のままである。

## 静的確認

production 本番は実行していない。一時ディレクトリで outer の `Read(D366Inner)` だけを抑止して inner（14223 bytes）を生成し、以下を確認した。

1. literal `\\nExec` および `fi;\\nPrint` は0件。
2. tail は実改行上の `end;;` → `Exec(...)` → `if ... fi;` → `Print(...)` になった。
3. GAP 4.16.0 の `ReadAsFunction` が生成 inner 全体を構文解析し、`A4_V21_INNER_SYNTAX_PASS` を返した（未束縛 global の静的 warning のみ）。

SELFTEST、producer、checker、重い本番計算は起動していない。
