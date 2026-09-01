#!/usr/bin/env python3
"""Exact positive MEMBER checker successor of frozen Task456 fusion checker."""
import ast,hashlib
from pathlib import Path
BASE=Path(__file__).with_name("check_d972_r07_direct_relator_a5_a7_fusion_v7.py");B=3409;H="e15cc28ad80407341dbce66d61cb6755bb9270a4db336f7c3dab50c70fee42e8"
b=BASE.read_bytes()
if len(b)!=B or hashlib.sha256(b).hexdigest()!=H:raise SystemExit("fusion checker v8 base drift")
t=ast.parse(b);vals={}
for n in t.body:
 if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=="changes":vals["changes"]=ast.literal_eval(n.value)
for n in ast.walk(t):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="with_name" and isinstance(n.args[0],ast.Constant):vals["inner"]=n.args[0].value;break
x=BASE.with_name(vals["inner"]).read_bytes()
for a,c in vals["changes"]:x=x.replace(a,c)
if len(x)!=29828 or hashlib.sha256(x).hexdigest()!="173e51a1c84b603fc3d7d75b6d3a58250c15e14a10f680cf5e67383ce53ecc88":raise SystemExit("fusion checker inherited body drift")
changes=[(b'd972-r07-direct-relator-a5-a7-fusion/v7',b'd972-r07-direct-relator-a5-a7-fusion/v8'),(b'/checker-verdict/v7',b'/checker-verdict/v8'),(b'R07_DIRECT_RELATOR_A5_A7_FUSION_V7',b'R07_DIRECT_RELATOR_A5_A7_FUSION_V8'),
(b'"search/d972_r07_direct_relator_a5_a7_fusion_v7.py", 3038,\n    "8d3d071d608687fef9249bc2ddeb99789c88dc42e21cd2eb51f9fe5b982142f4"',b'"search/d972_r07_direct_relator_a5_a7_fusion_v8.py", 4302,\n    "f0d108259f13c1c87c4129aa08a5c8f17fd4466604f76fdb5d7fb8172a487fa8"'),
(b'"search/d972_r07_zero_base_a5_a6_compiler_v5.py", 2810,\n    "df659de36c8c27255836c6da06812ab8af61185566e98210f46f32ae75fb4cd2"',b'"search/d972_r07_zero_base_a5_a6_compiler_v6.py", 2342,\n    "32cbc1a8e1faea0d4dc7a88a41a2ad3b535e7b2fd94b73ff286d78001262b96c"'),
(b'"crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v5.py", 2698,\n    "4dcd1b0540ffce929702bbd4ca6bebce9a53cd9ffb0c2dd4fa902df046897019"',b'"crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v6.py", 2334,\n    "a4db1b2b1ad5da1135c8ebcef1898c46fd07df7ebdbfa8778bd36a6098507bc3"')]
counts=[1,1,1,1,1,1]
for (a,c),n in zip(changes,counts):
 if x.count(a)!=n or x.count(c)!=0:raise SystemExit("fusion checker v8 cardinality")
 x=x.replace(a,c)
 if x.count(a)!=0 or x.count(c)!=n:raise SystemExit("fusion checker v8 post cardinality")
GENERATED_BYTES=29828;GENERATED_SHA="c5571981145908d6b892fb776aa84d9e8d07c36fb4d27548af95b17e395821ca"
if len(x)!=GENERATED_BYTES or hashlib.sha256(x).hexdigest()!=GENERATED_SHA:raise SystemExit("fusion checker v8 generated drift")
exec(compile(x,str(Path(__file__).resolve()),"exec"),globals(),globals())
