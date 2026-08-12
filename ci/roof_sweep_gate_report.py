#!/usr/bin/env python3
"""Informational report for roof-sweep-v1.yml's Gate step (extracted from an inline
heredoc that had an indentation bug -- heredoc terminators must not be indented with
spaces unless using <<- with tabs; a standalone script avoids that class of bug)."""
import json
import sys

path = sys.argv[1]
p = json.load(open(path, encoding="utf-8"))
print("progress:", p.get("progress"))
for r in p.get("rows", []):
    print(r.get("left"), "x", r.get("right"), "->", r.get("status"),
          "shadow_total=", r.get("shadow_total"))
