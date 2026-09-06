# Task1002 — batch P/Cの保持closure・root実pin公開表

宛先: Task994/995/996。以下は公開metadataだけで、新算術本文/私的APIは含まない。
実64候補run33990567016/1のresume-source-receipt.json（4657 B/76c5cbd01fafb30e8ba503e27ae949f5a3e2dbb46e9108ca3d691d6d996369b0）をrootが読み、
全19保持Pythonと3rawの現実file bytes/SHAを各保存pinへ再照合して一致した。
旧C continuation v1は元失敗のprovenanceであり今回の実import closureから除外、Cはv2を用いる。
新P/C各一本の最終pinは完成後に別途実測する。現時点で未知の最終bytes/SHAを埋めない。
新P/C2本＋P保持9＋C保持10で21 executable、raw3。追加importが必要と分かったらrootへ公開metadataとして先に返す。
同じscopeの既受理TCBを保持し、これを新しい第三の独立算術とは呼ばない。相手の新source/返信を読まず、以下のpin表だけを使う。
JSON配列は各受付code.producer_dependencies / checker_dependencies / dataのexact値で、file完全文字列順。

## producer_dependencies

```json
[
    {
        "file":  "search/d972_r07_actual_grade2_root_scalar_batch_v2.py",
        "bytes":  118315,
        "sha256":  "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856"
    },
    {
        "file":  "search/d972_r07_actual_root_seed_materializer_v3.py",
        "bytes":  86643,
        "sha256":  "36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332"
    },
    {
        "file":  "search/d972_r07_complete_oracle_cegar_continuation_v1.py",
        "bytes":  126940,
        "sha256":  "67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c"
    },
    {
        "file":  "search/d972_r07_fixed_root_packet_loop_v2.py",
        "bytes":  84173,
        "sha256":  "e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6"
    },
    {
        "file":  "search/d972_r07_full_origin_refinement_v1.py",
        "bytes":  97806,
        "sha256":  "d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa"
    },
    {
        "file":  "search/d972_r07_rank1355_root_seed_scalars_v1.py",
        "bytes":  31578,
        "sha256":  "973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb"
    },
    {
        "file":  "search/d972_r07_section_cochain_oracle_v1.py",
        "bytes":  73290,
        "sha256":  "4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb"
    },
    {
        "file":  "search/d972_r07_selected_cycle_materializer_v1.py",
        "bytes":  88929,
        "sha256":  "4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3"
    },
    {
        "file":  "search/d972_r07_targeted_grade2_owner_generated_join_v15.py",
        "bytes":  126565,
        "sha256":  "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632"
    }
]
```

## checker_dependencies

```json
[
    {
        "file":  "search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py",
        "bytes":  119619,
        "sha256":  "e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6"
    },
    {
        "file":  "search/check_d972_r07_actual_root_seed_materializer_v3.py",
        "bytes":  64626,
        "sha256":  "eca60918eb943edddc321054f04b8547b3e88e5f7421f4de1e09ea04d7ca2701"
    },
    {
        "file":  "search/check_d972_r07_complete_oracle_cegar_continuation_v2.py",
        "bytes":  129557,
        "sha256":  "e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3"
    },
    {
        "file":  "search/check_d972_r07_fixed_root_packet_loop_v2.py",
        "bytes":  66251,
        "sha256":  "5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5"
    },
    {
        "file":  "search/check_d972_r07_full_origin_refinement_v1.py",
        "bytes":  75083,
        "sha256":  "1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2"
    },
    {
        "file":  "search/check_d972_r07_rank1355_root_seed_scalars_v1.py",
        "bytes":  36236,
        "sha256":  "f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62"
    },
    {
        "file":  "search/check_d972_r07_section_cochain_oracle_v1.py",
        "bytes":  80740,
        "sha256":  "2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967"
    },
    {
        "file":  "search/check_d972_r07_section_cochain_oracle_v2.py",
        "bytes":  84402,
        "sha256":  "a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d"
    },
    {
        "file":  "search/check_d972_r07_selected_cycle_materializer_v1.py",
        "bytes":  103757,
        "sha256":  "a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4"
    },
    {
        "file":  "search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py",
        "bytes":  141770,
        "sha256":  "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662"
    }
]
```

## data

```json
[
    {
        "file":  "scratchpad/a0_paper_words_v1.json",
        "bytes":  115928,
        "sha256":  "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"
    },
    {
        "file":  "scratchpad/a0_v2_words.json",
        "bytes":  106133,
        "sha256":  "fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612"
    },
    {
        "file":  "scratchpad/fuda1_a0_rmax_data.g",
        "bytes":  4709,
        "sha256":  "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba"
    }
]
```
