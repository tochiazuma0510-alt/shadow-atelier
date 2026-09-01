#!/usr/bin/env python3
"""MEMBER-only checker successor of frozen Task456 zero checker."""
import ast,hashlib
from pathlib import Path
BASE=Path(__file__).with_name("check_d972_r07_zero_base_a5_a6_compiler_v5.py");B=2698;H="4dcd1b0540ffce929702bbd4ca6bebce9a53cd9ffb0c2dd4fa902df046897019"
b=BASE.read_bytes()
if len(b)!=B or hashlib.sha256(b).hexdigest()!=H:raise SystemExit("zero checker v6 base drift")
t=ast.parse(b); vals={}
for n in t.body:
 if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=="changes":vals["changes"]=ast.literal_eval(n.value)
for n in ast.walk(t):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="with_name" and isinstance(n.args[0],ast.Constant):vals["inner"]=n.args[0].value;break
x=BASE.with_name(vals["inner"]).read_bytes()
for a,c in vals["changes"]:x=x.replace(a,c)
if len(x)!=45942 or hashlib.sha256(x).hexdigest()!="82641acb296573cb90fcf8a05048ce089e6b3e0355894f5c9e42fc3fd84d0e00":raise SystemExit("zero checker inherited body drift")
changes=[(b'd972-r07-zero-base-a5-a6-compiler/v5',b'd972-r07-zero-base-a5-a6-compiler/v6'),(b'/checker-verdict/v5',b'/checker-verdict/v6'),(b'R07_ZERO_BASE_A5_A6_COMPILER_V5',b'R07_ZERO_BASE_A5_A6_COMPILER_V6'),(b'"search/d972_r07_zero_base_a5_a6_compiler_v5.py", 2810,\n    "df659de36c8c27255836c6da06812ab8af61185566e98210f46f32ae75fb4cd2"',b'"search/d972_r07_zero_base_a5_a6_compiler_v6.py", 2342,\n    "32cbc1a8e1faea0d4dc7a88a41a2ad3b535e7b2fd94b73ff286d78001262b96c"'),(b'receipt.get("terminal") in (MEMBER, NONMEMBER)',b'receipt.get("terminal") == MEMBER'),(b'checked = check_member(model, result) if receipt["terminal"] == MEMBER else check_nonmember(model, result)',b'checked = check_member(model, result)  # positive-only quarantine')]
counts=[1,2,1,1,1,1]
for (a,c),n in zip(changes,counts):
 if x.count(a)!=n or x.count(c)!=0:raise SystemExit("zero checker v6 cardinality")
 x=x.replace(a,c)
 if x.count(a)!=0 or x.count(c)!=n:raise SystemExit("zero checker v6 post cardinality")
GENERATED_BYTES=45888;GENERATED_SHA="cf44a9a8397eebf99271a4444bb41bd300fe5cfa60cc00696e9811a1469b52c7"
if len(x)!=GENERATED_BYTES or hashlib.sha256(x).hexdigest()!=GENERATED_SHA:raise SystemExit("zero checker v6 generated drift")
exec(compile(x,str(Path(__file__).resolve()),"exec"),globals(),globals())
