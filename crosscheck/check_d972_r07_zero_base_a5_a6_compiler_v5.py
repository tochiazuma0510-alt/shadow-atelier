#!/usr/bin/env python3
"""Exact Task193-v5 ABI successor of frozen A5/A6 checker v4."""
from __future__ import annotations
import hashlib
from pathlib import Path
BASE=Path(__file__).with_name("check_d972_r07_zero_base_a5_a6_compiler_v4.py");x=BASE.read_bytes()
if len(x)!=45942 or hashlib.sha256(x).hexdigest()!="cc88aeed18c4f14481971595ab22070720f68ce3fbe48f1057ecd89b610178aa":raise SystemExit("A5 checker v5 base drift")
changes=[(b'd972-r07-zero-base-a5-a6-compiler/v4',b'd972-r07-zero-base-a5-a6-compiler/v5'),(b'/checker-verdict/v4',b'/checker-verdict/v5'),(b'R07_ZERO_BASE_A5_A6_COMPILER_V4',b'R07_ZERO_BASE_A5_A6_COMPILER_V5'),(b'd972-r07-second-frattini-affine-prefix-compiler/v4',b'd972-r07-second-frattini-affine-prefix-compiler/v5'),(b'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V4',b'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V5'),
(b'"search/d972_r07_second_frattini_affine_prefix_compiler_v4.py", 2851,\n    "a6e1d54c1c656ab496ed54e6bcac5fa8c027edc5686fa913c86cc1c0fe349d1a"',b'"search/d972_r07_second_frattini_affine_prefix_compiler_v5.py", 12207,\n    "fab51e296170ac34ebe48b49d79d3460017a51cd797d524e7b0d89481f23960f"'),
(b'"crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v4.py", 2986,\n    "04f7c7df3395e841a21fe75fec71bd5fef1f35a4fbc4c0e642b5db7fa31e390d"',b'"crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v5.py", 7795,\n    "941eab0d9c60726436c866427de04b7c25b4ae1934fbf0a1d464f2010a7e2b9e"'),
(b'"search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v4.g", 5798,\n    "7447b2da4c83ba0f9818a3ea355636310368b22c8585e6b95632100894dfafb4"',b'"search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v5.g", 2269,\n    "d2cab901ae608d88bcff6dacdee6072c780b9157e1955cbaa740d227a8f2fe7a"'),
(b'"search/d972_r07_zero_base_a5_a6_compiler_v4.py", 59239,\n    "3949c5b98432cabebef989304cb70201266d48b7bdd71a6301a955000a9755c7"',b'"search/d972_r07_zero_base_a5_a6_compiler_v5.py", 2810,\n    "df659de36c8c27255836c6da06812ab8af61185566e98210f46f32ae75fb4cd2"'),(b'task193_v4',b'task193_v5'),(b'a5_v4',b'a5_v5')]
counts=[1,2,1,1,1,1,1,1,1,2,1]
if len(changes)!=len(counts):raise SystemExit("A5 checker v5 count roster")
for (a,b),n in zip(changes,counts):
 if x.count(a)!=n or (b and x.count(b)!=0):raise SystemExit("A5 checker v5 patch cardinality "+repr(a))
 x=x.replace(a,b)
 if x.count(a)!=0 or (b and x.count(b)!=n):raise SystemExit("A5 checker v5 post cardinality "+repr(a))
if len(x)!=45942 or hashlib.sha256(x).hexdigest()!="82641acb296573cb90fcf8a05048ce089e6b3e0355894f5c9e42fc3fd84d0e00":raise SystemExit("A5 checker v5 generated body drift")
exec(compile(x,str(Path(__file__).resolve()),"exec"),globals(),globals())
