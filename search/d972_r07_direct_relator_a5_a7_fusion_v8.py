#!/usr/bin/env python3
"""Positive-only quarantine successor of frozen Task456 fusion owner."""
import ast,hashlib
from pathlib import Path
BASE=Path(__file__).with_name("d972_r07_direct_relator_a5_a7_fusion_v7.py");B=3038;H="8d3d071d608687fef9249bc2ddeb99789c88dc42e21cd2eb51f9fe5b982142f4"
b=BASE.read_bytes()
if len(b)!=B or hashlib.sha256(b).hexdigest()!=H:raise SystemExit("fusion v8 base drift")
t=ast.parse(b);vals={}
for n in t.body:
 if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=="changes":vals["changes"]=ast.literal_eval(n.value)
for n in ast.walk(t):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="with_name" and isinstance(n.args[0],ast.Constant):vals["inner"]=n.args[0].value;break
x=BASE.with_name(vals["inner"]).read_bytes()
for a,c in vals["changes"]:x=x.replace(a,c)
if len(x)!=57825 or hashlib.sha256(x).hexdigest()!="bcc426b361d17d5de56fae9a16acabcb6474102b96cc71c42ab53be537c5f005":raise SystemExit("fusion inherited body drift")
old=b'''        if a5.get("terminal_kind") == "NONMEMBER":
            checkpoint = checkpoint_value("A5_NONMEMBER_COMPLETE", owners, a5,
                                          None, None, None, None)
            receipt = seal({
                "schema": SCHEMA, "status": "COMPLETE", "terminal": NONMEMBER,
                "mode": "PRODUCTION", "source": source_identity(),
                "static_bindings": static_bindings(), "owners": owners,
                "result": {"a5": a5, "canonical_M_only": True,
                           "v351_lift_null": "NOT_REACHED"},
                "claims": {"A5": "NONMEMBER", "A6_M": False, "A7": "NONE",
                           "compatible_lift": "NONE", "fake": "NONE",
                           "Ihara": "NONE"},
            })
            return receipt, checkpoint, None
'''
new=b'''        if a5.get("terminal_kind") == "NONMEMBER":
            checkpoint = checkpoint_value("A5_INCOMPLETE_SPAN", owners, a5,
                                          None, None, None, None)
            receipt = seal({
                "schema": SCHEMA, "status": "UNKNOWN_INCOMPLETE",
                "terminal": "UNKNOWN_INCOMPLETE:K_conjugation_closure_not_implemented",
                "mode": "PRODUCTION", "source": source_identity(),
                "static_bindings": static_bindings(), "owners": owners,
                "result": {"a5": a5, "canonical_M_only": True,
                           "v351_lift_null": "NOT_REACHED"},
                "claims": {"A5": "NONE", "A6_M": False, "A7": "NONE",
                           "compatible_lift": "NONE", "fake": "NONE",
                           "Ihara": "NONE"},
            })
            return receipt, checkpoint, None
'''
changes=[(b'd972-r07-direct-relator-a5-a7-fusion/v7',b'd972-r07-direct-relator-a5-a7-fusion/v8'),(b'R07_DIRECT_RELATOR_A5_A7_FUSION_V7',b'R07_DIRECT_RELATOR_A5_A7_FUSION_V8'),(b'"search/d972_r07_zero_base_a5_a6_compiler_v5.py", 2810,\n    "df659de36c8c27255836c6da06812ab8af61185566e98210f46f32ae75fb4cd2"',b'"search/d972_r07_zero_base_a5_a6_compiler_v6.py", 2342,\n    "32cbc1a8e1faea0d4dc7a88a41a2ad3b535e7b2fd94b73ff286d78001262b96c"'),(b'"crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v5.py", 2698,\n    "4dcd1b0540ffce929702bbd4ca6bebce9a53cd9ffb0c2dd4fa902df046897019"',b'"crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v6.py", 2334,\n    "a4db1b2b1ad5da1135c8ebcef1898c46fd07df7ebdbfa8778bd36a6098507bc3"'),(b'"search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v5.g", 1812,\n    "3ea33ee4ed8fdcf6a6f004ced6431d6c622e6d76cf8334cd8f57e72af4076ec1"',b'"search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v6.g", 2106,\n    "212c76f2ca2e06df1aae2b2d783a15fcf1d4e5041d70cba26198d64d9bd4d4d6"'),(old,new)]
counts=[1,1,1,1,1,1]
for (a,c),n in zip(changes,counts):
 if x.count(a)!=n or x.count(c)!=0:raise SystemExit("fusion v8 cardinality")
 x=x.replace(a,c)
 if x.count(a)!=0 or x.count(c)!=n:raise SystemExit("fusion v8 post cardinality")
GENERATED_BYTES=57892;GENERATED_SHA="a21a7061bf1c4b59b29a1ab1bb11bf18d9fab7b3b1f788dbec22b2213d7ab692"
if len(x)!=GENERATED_BYTES or hashlib.sha256(x).hexdigest()!=GENERATED_SHA:raise SystemExit("fusion v8 generated drift")
exec(compile(x,str(Path(__file__).resolve()),"exec"),globals(),globals())
