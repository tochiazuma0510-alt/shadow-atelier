# Luna reply 108d - LA-3 residual recovery

**Result: local PASS.** The exact index witness, the current coordinate
transversal/trivial-intersection conclusions, and injectivity of
(j, alpha, beta) |-> H j alpha beta are closed in one new module.

## 1. Isolation and baseline

- Read-only source:
  C:\Users\81905\AppData\Local\Temp\shadow-atelier-luna106g-b0b23ce9e00145629c7479f5576be1ea
- Fresh isolated lane:
  C:\Users\81905\AppData\Local\Temp\shadow-atelier-la3-19792ca5233f42318ff34f7065a13524
- Detached baseline:
  82ff1047b80a50b8a3098a83d71424ed2c6ec26d
- Baseline tree:
  901b51ce6887df06441c335b04b2e87afb413c72
- Baseline status before edits: clean.

No network clone, credential read, dependency update, commit, push, or workflow
dispatch was performed. Windows Git's local clone transport could not start its
MSYS sh.exe helper in the sandbox (CreateFileMapping / Win32 error 5).
I therefore made the isolated local clone by read-only copying the source
repository metadata, detached-checking out the required object, and populating
the index with checkout-index --all --force. The source repository was never
mutated; the lane HEAD/tree above were then independently checked.

## 2. Changed files

1. lean/P1/BlockA_LA3.lean (new)
2. sol/luna_reply_108d_la3.md (this report)

No existing BlockA, map, manifest, receipt, lake, or workflow file was changed.
The Lean module SHA-256 is
19d0e4eda70aa5ff7a3fcf9ee4822acb8b9946bf2a0de2c7ee3f3da93817d7de.

## 3. Exact declarations closed

- la3FinXCodeEquiv:
  explicit inverse maps Fin (2 * n) <-> XCode n.
- familyTransitive:
  the existing exact Transitive (H j alpha beta) conclusion, obtained from
  split/join.
- familyTrivialInter:
  the existing exact TrivialInter (H j alpha beta) conclusion.
- la3FinCosetEquiv:
  an exact PlainEquiv (Fin (2 * n)) (LeftCosets (H j alpha beta)); the
  codomain is the actual, marking-independent left-coset subtype.
- familyIndex2nWitness:
  Index2nWitness (H j alpha beta), containing baseline isSubgroup and the
  exact coset equivalence above.
- H_parameters_eq and H_parameter_injective:
  exact recovery of all three parameters from equality of subgroup predicates.
- isSubgroup_P1_P3:
  paper-domain wrapper with explicit NatOdd n and 3 <= n, existentially
  packaging the exact Index2nWitness plus both current propositions.

## 4. Paper fidelity and integration boundary

The implementation reuses, rather than repeats, baseline
H/isSubgroup/carrierEquiv/decompositionEquiv. The coset proof is genuinely
about extensional left-coset predicates, not a cardinality formula or prose
index claim.

This lane deliberately does not import uncommitted LA-2. Thus
familyTransitive and familyTrivialInter have exactly the current BlockA
types based on xrep : XCode n -> Gn n. Turning these into the paper's actual
<X> action/intersection requires LA-2's oddness bridge between xrep and
bounded xpowGn; this obligation is stated in the module header and wrapper
documentation and is not replaced by a weaker theorem. The sibling LA-2 lane
reports compatible planned exports bounded_power_eq_xrep and
xrep_eq_bounded_power; integration should connect them after both files are
recovered.

## 5. Local checks

From the isolated lane's lean directory:

~~~text
lake env lean P1/BlockA_LA3.lean
exit 0; no warning or error

lake build +P1.BlockA_LA3:olean
exit 0; P1.BlockA_LA3 built successfully
~~~

The targeted build replayed pre-existing linter warnings from imported baseline
modules only; the new module itself was clean. The forbidden-source scan for
declarations/tokens axiom, sorry, admit, native_decide,
Lean.ofReduceBool, Lean.ofReduceNat, and : True returned NO_MATCH.
Trailing whitespace count was zero and a final newline was present.

Exact #print axioms exposure:

| declaration | axioms |
|---|---|
| window.la3FinCosetEquiv | propext, Classical.choice, Quot.sound |
| window.familyIndex2nWitness | propext, Classical.choice, Quot.sound |
| window.familyTransitive | propext, Quot.sound |
| window.familyTrivialInter | propext |
| window.H_parameter_injective | propext |
| window.isSubgroup_P1_P3 | propext, Classical.choice, Quot.sound |

There is no project axiom and no blocker. GHA and shared manifest/map integration
remain the parent broker's gate.
