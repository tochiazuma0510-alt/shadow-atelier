#!/usr/bin/env python3
"""Positive-only quarantine successor of the frozen Task456 zero owner."""
import ast,hashlib
from pathlib import Path
BASE=Path(__file__).with_name("d972_r07_zero_base_a5_a6_compiler_v5.py");B=2810;H="df659de36c8c27255836c6da06812ab8af61185566e98210f46f32ae75fb4cd2"
b=BASE.read_bytes()
if len(b)!=B or hashlib.sha256(b).hexdigest()!=H:raise SystemExit("zero v6 base drift")
t=ast.parse(b); vals={}
for n in t.body:
 if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=="changes":vals["changes"]=ast.literal_eval(n.value)
for n in ast.walk(t):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="with_name" and isinstance(n.args[0],ast.Constant):vals["inner"]=n.args[0].value;break
x=BASE.with_name(vals["inner"]).read_bytes()
for a,c in vals["changes"]:x=x.replace(a,c)
if len(x)!=59232 or hashlib.sha256(x).hexdigest()!="c478b41db2ae1aae96178e2d4d6d26489b9c7de3611fada93f1f061bf1fab3d8":raise SystemExit("zero v6 inherited body drift")
changes=[
(b'd972-r07-zero-base-a5-a6-compiler/v5',b'd972-r07-zero-base-a5-a6-compiler/v6'),
(b'R07_ZERO_BASE_A5_A6_COMPILER_V5',b'R07_ZERO_BASE_A5_A6_COMPILER_V6'),
(b'"status": "COMPLETE",\n                 "terminal": MEMBER if result["terminal_kind"] == "MEMBER" else NONMEMBER,',b'"status": "COMPLETE" if result["terminal_kind"] == "MEMBER" else "UNKNOWN_INCOMPLETE",\n                 "terminal": MEMBER if result["terminal_kind"] == "MEMBER" else "UNKNOWN_INCOMPLETE:K_conjugation_closure_not_implemented",'),
(b'"claims": {"A5": result["terminal_kind"],\n                            "A6_M": result["terminal_kind"] == "MEMBER",',b'"claims": {"A5": "MEMBER" if result["terminal_kind"] == "MEMBER" else "NONE",\n                            "A6_M": result["terminal_kind"] == "MEMBER",')]
counts=[1,1,1,1]
for (a,c),n in zip(changes,counts):
 if x.count(a)!=n or x.count(c)!=0:raise SystemExit("zero v6 cardinality")
 x=x.replace(a,c)
 if x.count(a)!=0 or x.count(c)!=n:raise SystemExit("zero v6 post cardinality")
GENERATED_BYTES=59382;GENERATED_SHA="83b31959a0c35bdeb1e2569e0ee384b116ed6ed0b7d57e9c363cecdc29fcfe87"
if len(x)!=GENERATED_BYTES or hashlib.sha256(x).hexdigest()!=GENERATED_SHA:raise SystemExit("zero v6 generated drift")
exec(compile(x,str(Path(__file__).resolve()),"exec"),globals(),globals())
