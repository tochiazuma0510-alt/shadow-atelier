#############################################################################
## Tiny IdRel API self-test for d972_b4_u_idrel_direct_logged_v1.g.
##
## This is not the B4 presentation and never contributes a B4 result.  It
## exercises the exact APIs used by the producer on <a | a^2>, where the
## norm a^2 is logged as relator 1 and the conjugator is the identity.
## The independent Python toy test additionally checks a nontrivial
## conjugator and a deliberate mutation.
#############################################################################
if LoadPackage("idrel") <> true then Error("IdRel toy: package unavailable"); fi;
D972IDLTOYF:=FreeGroup(1,"a");;
D972IDLTOYG:=GeneratorsOfGroup(D972IDLTOYF);;
D972IDLTOYU:=D972IDLTOYF/[D972IDLTOYG[1]^2];;
D972IDLTOYM:=MonoidPresentationFpGroup(D972IDLTOYU);;
D972IDLTOYR0:=InitialLoggedRulesOfPresentation(D972IDLTOYM);;
if Length(D972IDLTOYR0)=0 then Error("IdRel toy: initial rules missing"); fi;
D972IDLTOYMF:=FreeGroupOfPresentation(D972IDLTOYM);;
D972IDLTOYMG:=GeneratorsOfGroup(D972IDLTOYMF);;
D972IDLTOYWord:=D972IDLTOYMG[1]^2;;
D972IDLTOYAns:=LoggedReduceWordKB(D972IDLTOYWord,D972IDLTOYR0);;
if not IsList(D972IDLTOYAns) or Length(D972IDLTOYAns)<>2 or
   Length(D972IDLTOYAns[1])=0 or not IsOne(D972IDLTOYAns[2]) then
  Error("IdRel toy: logged reduction shape/equality failed");
fi;
Print("B4_IDREL_DIRECT_LOGGED_TOY_PASS rules=",Length(D972IDLTOYR0),
  " log_length=",Length(D972IDLTOYAns[1])," reduced=id\n");
