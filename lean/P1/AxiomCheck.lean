/-
P1/AxiomCheck.lean -- generated, fail-closed theorem/axiom inventory for the P1 library.

Building this module enumerates every theorem declaration whose owning module has prefix `P1.`,
sorts the exact axiom set of each theorem, hashes its metadata-free kernel declaration type, and
writes `P1/AXIOMS.manifest.json`.  Any dependency outside the explicit Lean-core allowlist, any
`sorryAx`, any quarantined bare-T2 declaration, or an empty inventory aborts elaboration.
-/

import P1.BlockA
import P1.BlockE
import P1.BlockH
import P1.ShadowAxioms
import Lean

open Lean Lean.Elab Lean.Elab.Command

structure P1AxiomRow where
  moduleName : Name
  theoremName : Name
  typeDigest : UInt64
  axioms : Array Name

def p1AllowedAxioms : Array Name := #[``propext, ``Quot.sound, ``Classical.choice]

def p1ForbiddenT2 : Array Name := #[
  `ShadowAxioms.T2_thm43_explicit_isolated,
  `ShadowAxioms.T2_thm43_isolated,
  `ShadowAxioms.T2_15_Ih_decomp,
  `ShadowAxioms.T2_composition_hom
]

def p1IsAllowedAxiom (n : Name) : Bool := p1AllowedAxioms.any (· == n)

def p1ContainsSorry (n : Name) : Bool :=
  n.toString.contains ("sorryAx" : String)

def p1OwningModule? (env : Environment) (n : Name) : Option Name := do
  let idx ← env.getModuleIdxFor? n
  env.header.moduleNames[idx.toNat]?

def p1AuditRows (env : Environment) : CommandElabM (Array P1AxiomRow) := do
  let decls := env.constants.toList.mergeSort (fun a b => Name.lt a.1 b.1)
  let mut rows : Array P1AxiomRow := #[]
  for (n, ci) in decls do
    if ci.isTheorem then
      match p1OwningModule? env n with
      | none => pure ()
      | some modName =>
        if modName.toString.startsWith ("P1." : String) then
          let axs ← Lean.collectAxioms n
          rows := rows.push {
            moduleName := modName
            theoremName := n
            typeDigest := ci.type.consumeMData.hash
            axioms := axs.qsort Name.lt
          }
  return rows

def p1RowJson (r : P1AxiomRow) : Json :=
  Json.mkObj [
    ("module", Json.str r.moduleName.toString),
    ("theorem", Json.str r.theoremName.toString),
    ("normalizedTypeDigest", Json.str (toString r.typeDigest)),
    ("axioms", Json.arr (r.axioms.map fun n => Json.str n.toString))
  ]

def p1ManifestJson (sourceModules : Array Name) (rows : Array P1AxiomRow) : Json :=
  Json.mkObj [
    ("schema", Json.str "p1-axiom-manifest/v2"),
    ("leanVersion", Json.str Lean.versionString),
    ("normalization", Json.str "Expr.consumeMData; Expr.hash; bound variables are de Bruijn"),
    ("allowedAxioms", Json.arr (p1AllowedAxioms.qsort Name.lt |>.map fun n => Json.str n.toString)),
    ("projectAxiomDeclarations", Json.arr #[]),
    ("auditedSourceModules", Json.arr (sourceModules.map fun n => Json.str n.toString)),
    ("theoremCount", Json.str (toString rows.size)),
    ("theorems", Json.arr (rows.map p1RowJson))
  ]

/-- Match the current flat `P1/*.lean` source set against the actual import environment.  The
    checker module itself is excluded because it is still being elaborated. -/
def p1CheckSourceSet (env : Environment) : CommandElabM (Array Name) := do
  let entries ← liftIO <| System.FilePath.readDir "P1"
  let mut modules : Array Name := #[]
  for entry in entries do
    let file := entry.fileName
    if file.endsWith (".lean" : String) && file != "AxiomCheck.lean" then
      let stem := (file.dropEnd 5).toString
      let modName := Name.str (Name.str .anonymous "P1") stem
      if (env.getModuleIdx? modName).isNone then
        throwError m!"P1 AXIOM AUDIT FAIL: source module is not imported: {modName}"
      modules := modules.push modName
  if modules.isEmpty then
    throwError "P1 AXIOM AUDIT FAIL: P1 source-module set is empty"
  return modules.qsort Name.lt

def p1RunAxiomAudit : CommandElabM Unit := do
  let env ← Lean.MonadEnv.getEnv
  let sourceModules ← p1CheckSourceSet env
  for n in p1ForbiddenT2 do
    if env.contains n then
      throwError m!"P1 AXIOM AUDIT FAIL: quarantined bare-T2 declaration is present: {n}"
  -- Audit every P1-owned declaration, not only theorem roots.  This catches an unused project
  -- axiom and a `sorryAx` hidden in a definition before either can reach a main theorem.
  for (n, ci) in env.constants.toList do
    match p1OwningModule? env n with
    | none => pure ()
    | some modName =>
      if modName.toString.startsWith ("P1." : String) then
        if ci.isAxiom then
          throwError m!"P1 AXIOM AUDIT FAIL: project axiom declaration {n} in {modName}"
        let axs ← Lean.collectAxioms n
        for ax in axs do
          if p1ContainsSorry ax then
            throwError m!"P1 AXIOM AUDIT FAIL: declaration {n} depends on {ax}"
          if !p1IsAllowedAxiom ax then
            throwError m!"P1 AXIOM AUDIT FAIL: declaration {n} has unexpected axiom {ax}"
  let rows ← p1AuditRows env
  if rows.isEmpty then
    throwError "P1 AXIOM AUDIT FAIL: theorem inventory is empty"
  for r in rows do
    for ax in r.axioms do
      if p1ContainsSorry ax then
        throwError m!"P1 AXIOM AUDIT FAIL: {r.theoremName} depends on {ax}"
      if !p1IsAllowedAxiom ax then
        throwError m!"P1 AXIOM AUDIT FAIL: {r.theoremName} has unexpected axiom {ax}"
    logInfo m!"P1_AXIOM_ROW|{r.moduleName}|{r.theoremName}|{r.typeDigest}|{r.axioms.toList}"
  let manifest := (p1ManifestJson sourceModules rows).pretty
  liftIO <| IO.FS.writeFile "P1/AXIOMS.manifest.json" (manifest ++ "\n")
  logInfo m!"P1_AXIOM_AUDIT_PASS|modules={sourceModules.size}|theorems={rows.size}|manifest=P1/AXIOMS.manifest.json"

run_cmd p1RunAxiomAudit
