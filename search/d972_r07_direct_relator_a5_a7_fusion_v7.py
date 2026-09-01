#!/usr/bin/env python3
"""Exact Task193-v5/zero-base-v5 successor of frozen fusion v6."""
from __future__ import annotations
import hashlib
from pathlib import Path
BASE=Path(__file__).with_name("d972_r07_direct_relator_a5_a7_fusion_v6.py");x=BASE.read_bytes()
if len(x)!=57826 or hashlib.sha256(x).hexdigest()!="da9e8ca8e5ea2c30e92eef2d1dba772a0aa4d3eed9d894c7441c40cb49ac6441":raise SystemExit("fusion v7 base drift")
changes=[(b'd972-r07-direct-relator-a5-a7-fusion/v6',b'd972-r07-direct-relator-a5-a7-fusion/v7'),(b'R07_DIRECT_RELATOR_A5_A7_FUSION_V6',b'R07_DIRECT_RELATOR_A5_A7_FUSION_V7'),
(b'"search/d972_r07_zero_base_a5_a6_compiler_v4.py", 59239,\n    "3949c5b98432cabebef989304cb70201266d48b7bdd71a6301a955000a9755c7"',b'"search/d972_r07_zero_base_a5_a6_compiler_v5.py", 2810,\n    "df659de36c8c27255836c6da06812ab8af61185566e98210f46f32ae75fb4cd2"'),
(b'"crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v4.py", 45942,\n    "cc88aeed18c4f14481971595ab22070720f68ce3fbe48f1057ecd89b610178aa"',b'"crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v5.py", 2698,\n    "4dcd1b0540ffce929702bbd4ca6bebce9a53cd9ffb0c2dd4fa902df046897019"'),
(b'"search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v4.g", 4255,\n    "2349f5a84afadcd90e26aad9bb98689c8df099e733951cc3cd8fd7425a2cbef0"',b'"search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v5.g", 1812,\n    "3ea33ee4ed8fdcf6a6f004ced6431d6c622e6d76cf8334cd8f57e72af4076ec1"'),
(b'"search/d972_r07_second_frattini_affine_prefix_compiler_v4.py", 2851,\n    "a6e1d54c1c656ab496ed54e6bcac5fa8c027edc5686fa913c86cc1c0fe349d1a"',b'"search/d972_r07_second_frattini_affine_prefix_compiler_v5.py", 12207,\n    "fab51e296170ac34ebe48b49d79d3460017a51cd797d524e7b0d89481f23960f"'),
(b'"crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v4.py", 2986,\n    "04f7c7df3395e841a21fe75fec71bd5fef1f35a4fbc4c0e642b5db7fa31e390d"',b'"crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v5.py", 7795,\n    "941eab0d9c60726436c866427de04b7c25b4ae1934fbf0a1d464f2010a7e2b9e"'),
(b'"search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v4.g", 5798,\n    "7447b2da4c83ba0f9818a3ea355636310368b22c8585e6b95632100894dfafb4"',b'"search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v5.g", 2269,\n    "d2cab901ae608d88bcff6dacdee6072c780b9157e1955cbaa740d227a8f2fe7a"'),(b'task193_v4',b'task193_v5'),(b'a5_v4',b'a5_v5'),(b'for_fusion_v6',b'for_fusion_v7')]
counts=[1,1,1,1,1,1,1,1,5,5,2]
if len(changes)!=len(counts):raise SystemExit("fusion v7 count roster")
for (a,b),n in zip(changes,counts):
 if x.count(a)!=n or (b and x.count(b)!=0):raise SystemExit("fusion v7 patch cardinality "+repr(a))
 x=x.replace(a,b)
 if x.count(a)!=0 or (b and x.count(b)!=n):raise SystemExit("fusion v7 post cardinality "+repr(a))
if len(x)!=57825 or hashlib.sha256(x).hexdigest()!="bcc426b361d17d5de56fae9a16acabcb6474102b96cc71c42ab53be537c5f005":raise SystemExit("fusion v7 generated body drift")
exec(compile(x,str(Path(__file__).resolve()),"exec"),globals(),globals())
