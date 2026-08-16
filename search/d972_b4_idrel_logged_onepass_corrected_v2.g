#############################################################################
## d972_b4_idrel_logged_onepass_corrected_v2.g
##
## Repo-local copy of IdRel 2.49 LoggedOnePassKB (GAP 4.16.0).
##
## Provenance:
##   installed source:
##   C:/Program Files/GAP-4.16.0/runtime/opt/gap-4.16.0/pkg/idrel/lib/logrws.gi
##   Package IdRel 2.49, Date 02/10/2025
##   source SHA256 =
##   2836dd6aca49ed7fe0e51d07abb5efb1b7f3ff6b70f17fd1070c6dd44d35ed5e
##   upstream method lines 771--984.
##
## The algorithm and all type-2 formulas are unchanged.  The only algorithmic
## change is the type-1 pair log assignment at the marked lines below.  With
## l1=u*l2*v, c2u = c2 shifted by u^-1, crit1=u*r2*v, crit2=r1, the F6
## invariant gives
##
##   red1 -> red2 : inv(log1)+inv(c2u)+c1+log2
##   red2 -> red1 : inv(log2)+inv(c1)+c2u+log1.
##
## A higher-rank method is installed only in this GAP process.  No installed
## package file is modified.  The direct v2 producer still applies its
## independent all-rule and final norm F6 checks.
#############################################################################

if LoadPackage("idrel") <> true then
  Error("d972 corrected IdRel: idrel package unavailable");
fi;

D972B4CheckedSubword := function(word,first,last)
  local ans;
  ans:=Subword(word,first,last);
  if ans=fail then
    Error("d972 corrected IdRel: Subword returned fail");
  fi;
  return ans;
end;;
D972B4CheckedReduceWordKB := function(word,rules)
  local ans;
  ans:=ReduceWordKB(word,rules);
  if ans=fail then
    Error("d972 corrected IdRel: ReduceWordKB returned fail");
  fi;
  return ans;
end;;
D972B4CheckedLoggedReduceWordKB := function(word,rules)
  local ans;
  ans:=LoggedReduceWordKB(word,rules);
  if not IsList(ans) or Length(ans)<>2 or ans[1]=fail or ans[2]=fail then
    Error("d972 corrected IdRel: LoggedReduceWordKB returned fail");
  fi;
  return ans;
end;;

D972B4LoggedOnePassKB_Corrected := function( mG, r0 )

    local fmG, gfmG, id, rules, invrules, newrules, newrule, critnum, critn,
           rule1, l1, c1, r1, len1, rule2, l2, c2, r2, len2,
           pos1, pos2, u, v, iu, ur2v, red1, log1, ilog1, red2, log2, ilog2,
           crit1, crit2, redrule, n, lenu, lenv, i, c2u, ic2u, ic1, c, j,
           lenc, L, iL, numrules, use;

    fmG := FreeGroupOfPresentation( mG );
    gfmG := GeneratorsOfGroup( fmG );
    id := One( fmG );
    rules := ShallowCopy( r0 );
    invrules := InverseRulesOfPresentation( mG );
    Info( InfoIdRel, 2, "in corrected D972B4LoggedOnePassKB with ",
          Length(rules), " rules" );
    Info( InfoIdRel, 3, "rules = ", rules );
    newrules := [ ];
    critnum := 0;
    critn := 0;
    # Find all the critical pairs:
    for rule1 in rules do
        l1 := rule1[1];
        c1 := rule1[2];
        r1 := rule1[3];
        if l1=fail or c1=fail or r1=fail then
            Error("d972 corrected IdRel: type1 rule1 contains fail");
        fi;
        len1 := Length( l1 );
        for rule2 in rules do
            l2 := rule2[1];
            c2 := rule2[2];
            r2 := rule2[3];
            if l2=fail or c2=fail or r2=fail then
                Error("d972 corrected IdRel: type1 rule2 contains fail");
            fi;
            len2 := Length( l2 );
            # Search for type 1 pairs (when l2 is contained in l1):
            pos1 := PositionWord( l1, l2, 1 );
            if IsInt( pos1 ) then
                pos2 := pos1 + len2;
                if ( pos1 = 1 ) then
                    u := id;
                else
                    u := D972B4CheckedSubword( l1, 1, pos1-1 );
                fi;
                if ( pos2-1 = len1 ) then
                    v := id;
                else
                    v := D972B4CheckedSubword( l1, pos2, len1 );
                fi;
                iu := InverseWordInFreeGroupOfPresentation( fmG, u );
                if iu=fail then
                    Error("d972 corrected IdRel: type1 inverse word fail");
                fi;
                ur2v := u * r2 * v;
                if not ( ur2v = r1 ) then
                    critnum := critnum + 1;
                    Info( InfoIdRel, 2, "corrected type 1 pair: ",
                          [ u*r2*v, r1 ] );
                    critn := critn + 1;
                    Unbind(newrule);
                    if u=fail or r2=fail or v=fail then
                        Error("d972 corrected IdRel: type1 critical word fail");
                    fi;
                    crit1 := ur2v;
                    c2u := List( c2,
                         c -> [ c[1], D972B4CheckedReduceWordKB(
                                      c[2]*iu, invrules ) ] );
                    red1 := D972B4CheckedLoggedReduceWordKB( crit1, rules );
                    log1 := List( red1[1],
                         c -> [ c[1], D972B4CheckedReduceWordKB(
                                      c[2], invrules ) ] );
                    red1 := red1[2];
                    crit2 := r1;
                    red2 := D972B4CheckedLoggedReduceWordKB( crit2, rules );
                    log2 := List( red2[1],
                         c -> [ c[1], D972B4CheckedReduceWordKB(
                                      c[2], invrules ) ] );
                    red2 := red2[2];
                    # Orientate them.  The two assignments below are the
                    # sole correction relative to IdRel 2.49 source.
                    ilog2 := Reversed( List( log2,
                                      c -> [ -c[1], c[2] ] ) );
                    ilog1 := Reversed( List( log1,
                                      c -> [ -c[1], c[2] ] ) );
                    ic2u := Reversed( List( c2u,
                                      c -> [ -c[1], c[2] ] ) );
                    ic1 := Reversed( List( c1,
                                      c -> [ -c[1], c[2] ] ) );
                    L := Concatenation( ilog2, ic1, c2u, log1 );
                    iL := Concatenation( ilog1, ic2u, c1, log2 );
                    if red1=fail or red2=fail then
                        Error("d972 corrected IdRel: type1 reduced word fail");
                    fi;
                    if ( ( red1 in gfmG ) and ( red2 in gfmG ) ) then
                        if ( Position( gfmG, red1 )
                             > Position( gfmG, red2 ) ) then
                            newrule := [ red1, iL, red2 ];
                        else
                            newrule := [ red2, L, red1 ];
                        fi;
                    elif ( red1 < red2 ) then
                        newrule := [ red2, L, red1 ];
                    elif ( red2 < red1 ) then
                        newrule := [ red1, iL, red2 ];
                    fi;
                    # Add them in as new rules:
                    if red1<>red2 and not IsBound(newrule) then
                        Error("d972 corrected IdRel: type1 orientation fail");
                    fi;
                    if ( red1 = red2 ) then
                        redrule := LogSequenceReduce( mG, L );
                        if ( redrule <> [ ] ) then
                            Info( InfoIdRel, 2, " !! red1 = red2 at:\n", L );
                        fi;
                    else
                        c := newrule[2];
                        lenc := Length( c );
                        j := 1;
                        while( j < lenc ) do
                            if ( ( c[j][1] = - c[j+1][1] ) and
                                 ( c[j][2] =   c[j+1][2] ) ) then
                                c := Concatenation( c{[1..j-1]},
                                                    c{[j+2..lenc]} );
                                j := j - 2;
                                Info( InfoIdRel, 2, "reduced to: ", c );
                                lenc := lenc - 2;
                            fi;
                            j := j + 1;
                        od;
                        newrule[2] := c;
                        Add( newrules, newrule );
                        Info( InfoIdRel, 2, "(corrected 1) newrule = ",
                              newrule );
                    fi;
                fi;
            fi;
            # Now search for type 2 pairs.  This branch is unchanged from
            # IdRel 2.49 logrws.gi:883--970.
            i := 1;
            while not( ( i > len2 ) or ( i > len1 ) ) do
                if ( D972B4CheckedSubword( l1, len1-i+1, len1 )
                     = D972B4CheckedSubword( l2, 1, i ) ) then
                    if ( len1 = i ) then
                        u := id;
                    else
                        u := D972B4CheckedSubword( l1, 1, len1-i );
                    fi;
                    if ( len2 = i ) then
                        v := id;
                    else
                        v := D972B4CheckedSubword( l2, i+1, len2 );
                    fi;
                    Info( InfoIdRel, 2, "type 2 overlap word: ",
                          rule1[1]*v );
                    c1 := rule1[2];
                    iu := InverseWordInFreeGroupOfPresentation( fmG, u );
                    if iu=fail then
                        Error("d972 corrected IdRel: type2 inverse word fail");
                    fi;
                    c2u := List( rule2[2],
                           c -> [ c[1], D972B4CheckedReduceWordKB(
                                        c[2]*iu, invrules ) ] );
                    if u=fail or v=fail or r1=fail or r2=fail then
                        Error("d972 corrected IdRel: type2 critical word fail");
                    fi;
                    if not ( r1*v = u*r2 ) then
                        critnum := critnum + 1;
                        critn := critn + 1;
                        Unbind(newrule);
                        crit1 := r1*v;
                        red1 := D972B4CheckedLoggedReduceWordKB( crit1, rules );
                        log1 := List( red1[1],
                          c -> [ c[1], D972B4CheckedReduceWordKB(
                                       c[2], invrules ) ] );
                        red1 := red1[2];
                        crit2 := u*r2;
                        red2 := D972B4CheckedLoggedReduceWordKB( crit2, rules );
                        log2 := List( red2[1],
                          c -> [ c[1], D972B4CheckedReduceWordKB(
                                       c[2], invrules ) ] );
                        red2 := red2[2];
                        # Orientate them:
                        ilog2 := Reversed( List( log2,
                                          c -> [ -c[1], c[2] ] ) );
                        ilog1 := Reversed( List( log1,
                                          c -> [ -c[1], c[2] ] ) );
                        ic2u := Reversed( List( c2u,
                                          c -> [ -c[1], c[2] ] ) );
                        ic1 := Reversed( List( c1,
                                          c -> [ -c[1], c[2] ] ) );
                        L := Concatenation( ilog2, ic2u, c1, log1 );
                        iL := Concatenation( ilog1, ic1, c2u, log2 );
                        if red1=fail or red2=fail then
                            Error("d972 corrected IdRel: type2 reduced word fail");
                        fi;
                        if ( ( red1 in gfmG ) and ( red2 in gfmG ) ) then
                            if ( Position( gfmG, red1 )
                                 > Position( gfmG, red2 ) ) then
                                newrule := [ red1, iL, red2 ];
                            else
                                newrule := [ red2, L, red1 ];
                            fi;
                        elif ( red1 < red2 ) then
                            newrule := [ red2, L, red1 ];
                        elif ( red2 < red1 ) then
                            newrule := [ red1, iL, red2 ];
                        fi;
                        # Add them in as new rules:
                        if red1<>red2 and not IsBound(newrule) then
                            Error("d972 corrected IdRel: type2 orientation fail");
                        fi;
                        if ( red1 = red2 ) then
                            Info( InfoIdRel, 2, "LHS = RHS" );
                            redrule := LogSequenceReduce( mG, L );
                            if ( redrule <> [ ] ) then
                                Info( InfoIdRel, 2,
                                  " !! type2, red1=red2= ", red1,
                                  " at:", L );
                            fi;
                        else
                            c := newrule[2];
                            lenc := Length( c );
                            j := 1;
                            while ( j < lenc ) do
                                if ( ( c[j][1] = - c[j+1][1] ) and
                                     ( c[j][2] =   c[j+1][2] ) ) then
                                    c := Concatenation( c{[1..j-1]},
                                                        c{[j+2..lenc]});
                                    j := j - 2;
                                    Info( InfoIdRel, 2, "reduced to : ", c);
                                    lenc := lenc - 2;
                                    if ( ( j = -1 ) and ( lenc > 0 ) ) then
                                        j := 0;
                                    fi;
                                fi;
                                j := j + 1;
                            od;
                            newrule[2] := c;
                            Add( newrules, newrule );
                            Info( InfoIdRel, 2, "(2) newrule = ", newrule );
                        fi;
                    fi;
                fi;
                i := i + 1;
            od;
        od;
    od;
    Append( rules, newrules );
    Sort( rules, BetterLoggedRuleByReductionOrLength );
    ## remove duplicates
    numrules := Length( rules );
    use := [1..numrules];
    for i in [2..numrules] do
        if ( rules[i] = rules[i-1] ) then
            use := Difference( use, [i] );
        fi;
    od;
    return rules{use};
end;

if not IsBound(D972B4CorrectedOnePassInstalled) then
  InstallMethod( LoggedOnePassKB,
    "d972 B4 repo-local corrected IdRel 2.49 type-1",
    true, [ IsMonoidPresentationFpGroup, IsHomogeneousList ], 10,
    D972B4LoggedOnePassKB_Corrected );
  D972B4CorrectedOnePassInstalled := true;
fi;
