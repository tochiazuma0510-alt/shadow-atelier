# Sol(max) Task636: final re-audit of induced-grade repair v478

Read this mail completely, then read:

- `sol/proof_r07_eleven_endpoint_six_row_restriction_repair_v478.md`,
  5,131 bytes, SHA-256
  `a7e5df7f14d35b7dc971127e187fbc16abe00b3b5190fac341666b94bbf1e72b`;
- `sol/sol_reply_635_reaudit_r07_eleven_endpoint_six_row_v477.md`,
  8,687 bytes, SHA-256
  `0438c0d2e01747dc33863b9748001f1f482a9612d6ad0b9cdcd2047a77658421`;
- the pinned v477 parent, Task633 reply, Task630 reply, and only those
  v437/v445/v446/v451/v470/v471 definitions needed for a counterexample.

Decide whether v478 closes Task635's sole repair without regression:

1. (I_V=\operatorname{Aug}(k[V])) and
   (T_{\le2}=k[V]/I_V^3) are the kernel objects;
2. (G_2=k[Q_1]\otimes_k(I_V^2/I_V^3)), not the bare kernel grade, and its
   Fourier--monomial decomposition and dimension 12,096 are correct;
3. the full/truncated/grade occurrence dimensions
   653,184 / 241,920 / 145,152, source-with-auxiliary width 241,928, and
   physical 32,260 / 48,384 are correctly typed;
4. importing the exact pinned v477 ledger/theorem/executable boundary and
   replacing only its typed display is logically unambiguous; and
5. no control-byte, P-zero, algebraic 11-to-6 adapter, source-word
   commutation, actual-payload, A0, fake or Ihara overclaim appears.

Do not broaden the task, implement, run production/GHA, or perform git.
Write only `sol/sol_reply_636_reaudit_r07_eleven_endpoint_six_row_v478.md`
with exact inputs and `PASS` / `PASS_AFTER_REPAIR` / `FAIL`.  State remaining
actual inputs and `verified=false`.
