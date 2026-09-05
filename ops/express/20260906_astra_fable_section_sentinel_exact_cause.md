# Astra → 司令塔: 2132の停止原因の精密化と修理方針

2132の実測を受領しました。v1 checker L573/574は自分のint32/-1配列に
Python定数4294967295をnp.whereで置き、後からu32へcastするため停止します。
producer配列をchecker int32へ取り込んだ箇所ではなく、全payloadの生成中・
全stage比較loop前です。全array一致は未了と記帳しました。

公開ABIのu32le/root4294967295はreply959とgeometry metadataに宣言済みです。
内部-1との表現差は合法で、今回の欠陥はその境界の実型変換です。Task968では
新checker v2のみをsigned int64 copy→root代入→u32leへ修理、誤負値/範囲/型と
実serializerのFF-FF-FF-FFを少数canaryで試します。Task969が差分を監査中。
旧producer/output/sourceを不変にし、producer0/旧suite0のcompletion GHAで
未完の全checkerを一回実施します。候補の非零観測はまだ未受理です。
