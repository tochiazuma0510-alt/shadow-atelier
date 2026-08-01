# Independent symbolic re-confirmation (sympy) of the "paper calculation" formulas in
# docs/notes/u7_fire_log_v1_addendum_grade.md Sec 4.2.3.2(ii):
#   h(k) = (k-i)/(k+i) * ((k+1)/(k-1))^alpha ,  g(k) = (k+1)/(k-1)
#   sigma: k -> -k ,  theta: k -> 1/k
# Claims to check as EXACT rational-function identities in k (for each integer alpha):
#   h^sigma := h(-k)      == h(k)^{-1}
#   g^sigma := g(-k)      == g(k)^{-1}
#   g^theta := g(1/k)     == -g(k)
#   h^theta := h(1/k)     == (-1)^{alpha+1} * h(k)^{-1} * g(k)^{2*alpha}
# This script is independent of cbeta_model.py / cbeta_nielsen.py (does not import them);
# it only checks the raw rational-function claim via sympy.simplify(lhs-rhs)==0.
import sympy as sp

k = sp.symbols('k')
i = sp.I

def h_of(k_expr, alpha):
    return (k_expr - i)/(k_expr + i) * ((k_expr+1)/(k_expr-1))**alpha

def g_of(k_expr):
    return (k_expr+1)/(k_expr-1)

results = []
for alpha in [1,2,3,4,5]:
    h = h_of(k, alpha)
    g = g_of(k)

    h_sigma = sp.simplify(h_of(-k, alpha) - h**-1)
    g_sigma = sp.simplify(g_of(-k) - g**-1)
    g_theta = sp.simplify(g_of(1/k) - (-g))
    lhs = sp.simplify(h_of(1/k, alpha))
    rhs = sp.simplify((-1)**(alpha+1) * h**-1 * g**(2*alpha))
    h_theta = sp.simplify(lhs - rhs)

    row = dict(alpha=alpha,
               h_sigma_eq_hinv=(h_sigma == 0),
               g_sigma_eq_ginv=(g_sigma == 0),
               g_theta_eq_negg=(g_theta == 0),
               h_theta_eq_claim=(h_theta == 0),
               h_theta_residual=str(h_theta))
    results.append(row)
    print(row)

all_ok = all(r['h_sigma_eq_hinv'] and r['g_sigma_eq_ginv'] and r['g_theta_eq_negg'] and r['h_theta_eq_claim'] for r in results)
print("ALL_IDENTITIES_HOLD =", all_ok)
