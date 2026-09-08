# Task1110 追補 — Task1107 診断schemaの公開誤記訂正 v1

宛先: 独立C作者（packet_checker / Task1110）。Task1107の公開wire作者として、1110全consumer監査と共に次の版管理訂正を行う。実行・Git・credential操作は依然0。rootの正式監査返信はreply163 F8.171以降へ記帳する。

F1. 訂正理由と最大範囲

1107 public-interface-proposed-v2.md の F5「Diagnostic proposed schema is d972.r07.fixed-lambda-cycle-batch.v6.diagnostic」と keysets v2 の対応scalarは誤記。採用済み保存枝の公開契約は次の二型であり、generic .diagnostic は保存schemaではない。

| file | schema | status | terminal |
|---|---|---|---|
| resource-stop.json | d972.r07.fixed-lambda-cycle-batch.v6.resource-stop | UNKNOWN_RESOURCE | UNKNOWN_RESOURCE |
| rejected.json | d972.r07.fixed-lambda-cycle-batch.v6.rejected | FAIL | REJECTED |

rootは保存側の全文とC側公開DIAGNOSTIC_TYPESの対応を静読し、この公開誤記の訂正を裁定した。私的P helper/source/body/fixtureは渡さない。Cは自身のcompare_diagnosticと通常callerの既存意味を独立に再読して上表に結ぶ。

F2. 新版の必須成果

TEMP/task1107 に既版を保持して public-interface-proposed-v3.md / public-keysets-and-delta-proposed-v3.json / diagnostic-schema-erratum-v1.json / final-material-manifest-v4.json を作る。公開29 key、二filename、各null型、他19族、18親/9-key/start44/intake49/layout11、C8/P8の公開目的/label/prefixは不変。

診断族は単一schemaを偽装しない。proposed_schema=null とし、proposed_variantsを上表の順で二件の実配列として追加する。各項はexact {file,schema,status,terminal} とし、全値は非空文字列。actual_file/actual_schemaは今回のsuccess親に当該枝が未観測なのでnullを維持する。generic .v6.diagnosticをaccepted alternativeへ残さない。

erratumには旧v2のfull pin、変更した全JSON pathのbefore/after、他19族およびdiagnostic key列挙/順序/added/removedの全raw/構造不変を記す。新manifestはmaterial bytesの整数合計を実配列から計算して記帳し、旧版も消さない。既rootのF8.170/Delta707にあったgeneric schema採択のみを撤回する訂正で、実GHA停止枝を観測したとはしない。最終reply1110にもこの経緯と最終公開pinを書く（reply1107の凍結版は上書きしない）。

F3. 各consumerへの結合

rootがv3全差分を別読して採択後、P作者とGHA外側作者へ共通wire v3を渡す。C自身の全consumer票はv3へ結ぶ。既sourceの保存枝を .diagnostic へ改変せず、過去v5 payloadを改名/resealせず、29-keyや停止時nullを変えない。実selftest/実停止枝試行は新たに行わず、既許可GHAに向けた静的公開契約修理とする。
