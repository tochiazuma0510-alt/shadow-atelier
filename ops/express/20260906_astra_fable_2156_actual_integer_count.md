# Astra → 司令塔: 2156のstart基点推測を実値で棄却、整数1/bool混同を修理

2156/速達を全文読了。原実64 candidate9977040548のoutput/start.json（54707 B/87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b）を直接読んだ値は rank1386/gen8091/completed_steps0、external_e_attachedは**整数1**、external_e_numerically_replayedは**false**です。startは元33親の凍結値で、resume基点に改名されていません。失敗原因はWF985:796/P982:836の `is True`。別startへのpin変更や原cert改変は採用しません。
991で新P/WF v2のstrict int1（bool拒否）とproduction直結型逆対照へ、992でC v2のpath-only、993で独立差分監査。原math/source/旧版を保持。次diagnosticには当該五字段と元start全hashを含めます。
診断9978026066はrootもwhole ZIP244085 B/e6565d625f42e9e3202a1faedc271ff07c5c6cfee9cc38558f879155312522b4を回収、安全64file/1345404 B。alwaysはaccept前のparent-paths/all-source-before未保存が原因のINCOMPLETEで、原型拒否と区別して修理します。F8.62/v220 Delta599。GHA全jobは75秒、4秒は失敗accept stepだけです。canary/P/D未実行、数学判定なし。
