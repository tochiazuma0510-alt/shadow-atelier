# 宛: Sol(112e セッション) — 実行環境スペック補足(司令塔)

便 112e の性能目標の較正用: 本番実行環境 = GitHub-hosted `ubuntu-latest`(public repo 標準 runner)= **4 vCPU / RAM 16GB / SSD 14GB**。python 3.13+numpy 2.5.1(edim.yml で pin 済・依存追加不可は便どおり)。ローカル実測(k=10 = 56 分/素数)はこの runner でおよそ 1.5〜2 倍に伸びた実績(90 分 timeout 抵触)。k=11/12 のメモリ見積りも 16GB を天井に。あなたのサンドボックスでのベンチはこの倍率で換算されたい。
