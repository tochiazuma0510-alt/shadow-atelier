import json, sympy as sp
x=sp.symbols('x'); c3,c5,c7,c9,h4,h2,h0=sp.symbols('c3 c5 c7 c9 h4 h2 h0')
q=x**3+x; f6=sp.expand(q**2-27)
U=sp.expand((c3+c5*x**2)*q+c7*x*(2*q**2-27)+c9*(4*q**3-81*q))
B=sp.expand(c3+c5*x**2+2*c7*x*q+c9*(4*q**2-27))
P=sp.expand(U**2-B**2*f6-sp.Rational(27,4))
h=x**6+h4*x**4+h2*x**2+h0
pe=sp.Poly(sp.expand(sp.expand(P**2+27*U**2)-432*c9**2*h**3),x)
DEG=pe.degree(); cf={DEG-i:sp.expand(co) for i,co in enumerate(pe.all_coeffs())}
subs={}; tops=sorted([d for d in cf if d%2==0],reverse=True)[:3]
for deg,var in zip(tops,(h4,h2,h0)):
    subs[var]=sp.together(sp.solve(sp.Eq(sp.expand(cf[deg].subs(subs)),0),var,dict=True)[0][var])
rest=[]
for deg in sorted([d for d in cf if d not in tops and d%2==0],reverse=True):
    e=sp.expand(sp.numer(sp.cancel(sp.together(cf[deg].subs(subs)))))
    if e!=0: rest.append((deg,e))
rep={"schema":"u-meas-caseb-groebner/v1","status":"PARTIAL - exact solve not completed",
 "sympy_version":sp.__version__,"gap_version":"4.16.0 (monodromy sieve only)",
 "curve":"y^2 = f6(x), f6 = (x^3+x)^2 - 27   [a=2, b=1, c=-27; e=0; theta*thetabar = -27]",
 "curve_source":"CRT over p=7,13,19 of I1=b/a^2=1/4 and I2=c/a^3=-27/8 (addendum 2); NOT yet proved exact",
 "disc_f6_note":"coordinator: disc(f6) = 2^6 * 3^9 * 733^2 ; 31,37 do not divide -> curve has good reduction there",
 "basis_L9Pbar_minus":["theta = y + q","x^2*theta","x*theta^2","theta^3"],
 "t":"t = 3/2 + c3*theta + c5*x^2*theta + c7*x*theta^2 + c9*theta^3, c9 != 0",
 "rationalisation":{"U":"A - 3/2 (odd)","B":"even","P":"U^2 - B^2 f6 - 27/4 (even, deg 8)",
   "identity":"N_tau1 * N_tau2 = P^2 + 27 U^2","branch_condition":"P^2 + 27 U^2 = 432 c9^2 h(x)^3, h monic even deg 6"},
 "verified_degrees":{"deg_U":int(sp.degree(U,x)),"deg_B":int(sp.degree(B,x)),"deg_P":int(sp.degree(P,x)),
   "deg_LHS":int(sp.degree(sp.expand(P**2+27*U**2),x)),"deg_E_after_leading_cancel":int(DEG),
   "odd_coefficients_all_zero":True},
 "h_elimination_closed_form":{str(k):str(sp.simplify(v)) for k,v in subs.items()},
 "residual_system":[{"from_coeff_of":"x^%d"%d,"total_degree":int(sp.total_degree(e)),
                     "n_monomials":len(sp.Poly(e,c3,c5,c7,c9).monoms())} for d,e in rest],
 "attempts":[{"method":"sympy.solve on 9 eqs / 7 unknowns","wall_limit_s":1500,"result":"did not finish"},
             {"method":"staged h-elimination + sympy.solve on 6 eqs / 4 unknowns","wall_limit_s":570,"result":"did not finish"},
             {"method":"staged h-elimination + groebner(grevlex) on 6 eqs / 4 unknowns","wall_limit_s":560,"result":"did not finish"}],
 "u_touched":False,
 "note":"Raw machine output only. Single implementation (sympy). NOT cross-checked, NOT Lean-verified. u has NOT been read (U-LOC not fired)."}
json.dump(rep,open("search/certs/u_meas_caseb_groebner_20260731.json","w"),indent=1,sort_keys=True)
print("cert written; residual degrees:",[r["total_degree"] for r in rep["residual_system"]])
