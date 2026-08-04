## search/probe/hsp7_cond4_laneP/driver_step0_a5conv.g
## Lane P (pentagon), HS 発火条件4較正走 -- 0手目(全レーン共通、SS0.2逐語).
## A5-CONV fixture: docs/notes/hsp7_cond4_lanespec_v1.md SS0.2 (== 定義ノート SS1.5.4).
## fail-closed: a5_conv_result <> "correct" ならこのレーンは以降の較正走を一切実行しない.
##
## WARNING (SS0.2 逐語の帰結・W-1): paper 語の掛け算 "AB" は GAP では B*A になる
## (i^(A*B) = (i^A)^B の右作用規約のもとで、paper の "AB" という語順を GAP へそのまま
## 打つと違う置換が出る). 定義式 X=a t^-1, Y=t X t^-1, s=t X^3 も paper 積であり、
## GAP へ literal に打つと違う値が出る(実測は lanespec SS0.2 の貼付テキストに記載).
## 一般則(本ドライバが採用): paper の語 g1 g2 ... gk (左から右へ書かれた積) を GAP で
## 同じ元にするには、逆順の積 gk * ... * g2 * g1 を GAP で計算する(べき g^n は単一の
## "文字"として扱い、内部では反転しない).

Read("search/probe/wac_v1/gap_output_prelude.g");

Print("=== Lane P driver_step0: A5-CONV ===\n");

t := (1,2,3);;
a := (1,4,5);;

## aX := a t^-1 (paper, 2-letter word) -> GAP: t^-1 * a  (W-1 反転)
aX := t^-1 * a;;
Print("X (=a t^-1, paper; GAP: t^-1*a) = ", aX, "\n");

## aY := t X t^-1 (paper, 3-letter word) -> GAP: t^-1 * X * t (W-1 反転, 全体を逆順)
aY := t^-1 * aX * t;;
Print("Y (=t X t^-1, paper; GAP: t^-1*X*t) = ", aY, "\n");

## as := t X^3 (paper, 2-letter word, X^3 は単一の文字として扱う) -> GAP: X^3 * t
as := aX^3 * t;;
Print("s (=t X^3, paper; GAP: X^3*t) = ", as, "\n");

## 主判定: paper 語 y x^-1 (2文字) -> GAP: X^-1 * Y (W-1 反転)
ev_yxinv := aX^-1 * aY;;
Print("ev(y x^-1) (paper; GAP: X^-1*Y) = ", ev_yxinv, "\n");

expected_correct := (1,2,4);;
expected_reversed := (2,5,3);;

a5_result := "other";;
if ev_yxinv = expected_correct then
  a5_result := "correct";;
elif ev_yxinv = expected_reversed then
  a5_result := "reversed";;
fi;

Print("expected X (spec) = (1,3,2,4,5) ; got X = ", aX, " ; match = ", aX = (1,3,2,4,5), "\n");
Print("expected Y (spec) = (1,3,4,5,2) ; got Y = ", aY, " ; match = ", aY = (1,3,4,5,2), "\n");
Print("expected s (spec) = (1,4)(3,5) ; got s = ", as, " ; match = ", as = (1,4)(3,5), "\n");
Print("a5_conv_result = \"", a5_result, "\"\n");

if a5_result <> "correct" then
  Print("A5-CONV FAIL-CLOSED: a5_conv_result <> \"correct\". Lane P STOPS. No further calibration output.\n");
  Print("STAGE0_FAIL_CLOSED\n");
else
  Print("A5-CONV PASS. Proceeding to stage1.\n");
  Print("STAGE0_PASS\n");
fi;

QUIT;
