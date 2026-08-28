#!/usr/bin/env python3
"""Typed coefficient/joint-slice kernel.  SELFTEST has exactly one input: fixture."""
from __future__ import annotations
import argparse, hashlib, itertools, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA="d972-r07-joint-slice-kernel-general/v9"
SELF=SCHEMA+"/selftest"
PASS="R07_JOINT_SLICE_KERNEL_GENERAL_V9_PRODUCER_SELFTEST_PASS"
STATIC="STATIC_BLOCKED:actual typed matrices are not staged"
FIXTURE="search/certs/d972_r07_joint_slice_kernel_general_selftest_v9_20260828.json"
FIXTURE_SEAL="literal-static-fixture-v9"
OWNERS=("field_modulus","theta_seed","theta_action","z_action","eta_action","D_entry","O_entry","C_entry","action_order","premature_C","target","seed_index","parent","row_theta","left_kernel","Hd1","member_ancestry","dual","terminal")

def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
def digest(x): return hashlib.sha256(canon(x)).hexdigest()
def mutation_seal(x):
    body=dict(x);body.pop("mutation_fixture_seal",None);return digest(body)
def vnorm(v): return [int(x)%3 for x in v]
def mvec(m,v): return vnorm([sum(m[i][j]*v[j] for j in range(len(v))) for i in range(len(m))])
def mmul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b)))%3 for j in range(len(b[0]))] for i in range(len(a))]
def rowsum(rows,coeff):
    out=[0]*len(rows[0]) if rows else []
    for i,c in enumerate(coeff):
        for j,x in enumerate(rows[i]):out[j]=(out[j]+c*x)%3
    return vnorm(out)
def rref(matrix):
    a=[vnorm(row) for row in matrix]; r=0; piv=[]
    for c in range(len(a[0]) if a else 0):
        q=next((i for i in range(r,len(a)) if a[i][c]),None)
        if q is None:continue
        a[r],a[q]=a[q],a[r]; s=1 if a[r][c]==1 else 2; a[r]=vnorm([s*x for x in a[r]])
        for i in range(len(a)):
            if i!=r and a[i][c]:a[i]=vnorm([a[i][j]-a[i][c]*a[r][j] for j in range(len(a[i]))])
        piv.append(c);r+=1
        if r==len(a):break
    return a,piv
def nullspace(matrix,n):
    rr,piv=rref(matrix); free=[c for c in range(n) if c not in piv];out=[]
    for f in free:
        x=[0]*n;x[f]=1
        for i,c in reversed(list(enumerate(piv))):x[c]=(-sum(rr[i][j]*x[j] for j in free))%3
        out.append(x)
    return out
def rank(rows): return len(rref(rows)[1])
def member(rows,target):
    if not rows:return not any(target)
    return rank(rows)==rank(rows+[target])
def span_solve(rows,target):
    for coeff in itertools.product(range(3),repeat=len(rows)):
        if rowsum(rows,coeff)==vnorm(target):return list(coeff)
    raise ValueError("target outside span")
def require(ok,msg):
    if ok is not True:raise RuntimeError(msg)
def check_matrix(m,n):require(isinstance(m,list) and len(m)==n and all(isinstance(r,list) and len(r)==n and all(type(x) is int and x%3==x for x in r) for r in m),"matrix")
def check_map(m,r,c):require(isinstance(m,list) and len(m)==r and all(isinstance(x,list) and len(x)==c and all(type(y) is int and y%3==y for y in x) for x in m),"map")
def validate_fixture(value):
    require(value.get("schema")==SELF and type(value.get("fixture_seal")) is str and value.get("fixture_seal")==FIXTURE_SEAL,"fixture seal/schema");require(value.get("modulus")==3 and len(value.get("cases",[]))==5,"fixture cases")
    basis=value.get("typed_basis",{});require(basis=={"Theta":["theta0","theta1"],"Z":["z0","z1"],"E_hat":["occurrence%02d"%i for i in range(11)],"E":["printed0"]},"typed basis")
    require(set(value.get("expected_cases",{}))=={c["name"] for c in value["cases"]},"fixture expectations")
    require(value.get("mutation_roster")==list(OWNERS),"mutation roster");return value
def fixture_preflight(value):
    """Fail closed on every literal owner binding before any case compilation."""
    shapes = {
        "A_theta": (2, 2), "A_Z": (2, 2), "A_E": (11, 11),
        "D": (2, 2), "O": (11, 2), "C": (1, 11),
    }
    require(isinstance(value.get("cases"), list) and len(value["cases"]) == 5,
            "fixture preflight case count")
    for case in value["cases"]:
        require(isinstance(case, dict), "fixture preflight case object")
        for base, binding in (
            ("A_theta", "A_theta_binding"), ("A_Z", "A_Z_binding"),
            ("A_E", "A_E_binding"), ("D", "D_binding"),
            ("O", "O_binding"), ("C", "C_binding"),
        ):
            rows, cols = shapes[base]
            left, right = case.get(base), case.get(binding)
            require(left == right, "fixture preflight binding equality " + base)
            for label, matrix in ((base, left), (binding, right)):
                require(isinstance(matrix, list) and len(matrix) == rows and
                        all(isinstance(row, list) and len(row) == cols and
                            all(type(x) is int and 0 <= x < 3 for x in row)
                            for row in matrix),
                        "fixture preflight dimensions " + label)
    return value

def parse_fixture(path):
    value = validate_fixture(json.loads(path.read_text(encoding="utf-8")))
    return fixture_preflight(value)
def compile_case(case):
    require(case.get("modulus")==3,"modulus");require(case["theta_seeds"]==case["seed_bindings"],"theta seeds");require(case["A_theta"]==case["A_theta_binding"] and case["A_Z"]==case["A_Z_binding"] and case["A_E"]==case["A_E_binding"],"action owner")
    require(case["D"]==case["D_binding"] and case["O"]==case["O_binding"] and case["C"]==case["C_binding"],"map owner")
    require(case["action_names"]==case["action_order_binding"] and len(case["theta_seeds"])==len(case["seed_bindings"]) and case["parent_hint"]==0 and case["C_phase"]=="after-closure" and case["left_kernel_method"]=="rref","control owner")
    require(case.get("occurrence_count")==11 and case.get("occurrence_tags")==["occurrence%02d"%i for i in range(11)],"eleven occurrence")
    tdim=len(case["theta_seeds"][0]);zdim=len(case["D"]);edim=len(case["O"]);qdim=len(case["C"])
    check_matrix(case["A_theta"],tdim);check_matrix(case["A_Z"],zdim);check_matrix(case["A_E"],edim)
    require(rank(case["A_theta"])==tdim and rank(case["A_Z"])==zdim and rank(case["A_E"])==edim,"invertible action")
    check_map(case["D"],zdim,tdim);check_map(case["O"],edim,tdim);check_map(case["C"],qdim,edim)
    require(mmul(case["D"],case["A_theta"])==mmul(case["A_Z"],case["D"]),"D equivariance");require(mmul(case["O"],case["A_theta"])==mmul(case["A_E"],case["O"]),"O equivariance")
    require(len(case["actions"])==len(case["action_names"]) and len(case["theta_seeds"])>=1,"action/seed count")
    for name,action in zip(case["action_names"],case["actions"]):
        require(action["name"]==name,"action name")
        check_matrix(action["theta_matrix"],tdim);check_matrix(action["z_matrix"],zdim);check_matrix(action["eta_matrix"],edim)
        require(mmul(case["D"],action["theta_matrix"])==mmul(action["z_matrix"],case["D"]) and mmul(case["O"],action["theta_matrix"])==mmul(action["eta_matrix"],case["O"]),"action equivariance")
    require(case["theta_seeds"]==case["seed_bindings"],"seed binding")
    queue=[{"theta":vnorm(seed),"seed_index":i,"parent":None,"action":"seed","kind":"seed"} for i,seed in enumerate(case["theta_seeds"])] ; seen=[]
    while queue:
        item=queue.pop(0);z=mvec(case["D"],item["theta"]);eta=mvec(case["O"],item["theta"]);flat=z+eta
        if seen and rank([x["flat"] for x in seen]+[flat])==rank([x["flat"] for x in seen]):continue
        item=dict(item,z=z,eta=eta,flat=flat);seen.append(item)
        current=[x["flat"] for x in seen]
        for name,a in zip(case["action_names"],case["actions"]):
            candidate=mvec(a["theta_matrix"],item["theta"]);candidate_flat=mvec(case["D"],candidate)+mvec(case["O"],candidate)
            if rank(current+[candidate_flat])>rank(current):queue.append({"theta":candidate,"seed_index":item["seed_index"],"parent":len(seen)-1,"action":name,"kind":"action"})
    e=[mvec(case["C"],x["eta"]) for x in seen]; nvec=nullspace([[e[j][i] for j in range(len(e))] for i in range(qdim)],len(e))
    hs=[rowsum([x["z"] for x in seen],a) for a in nvec];thetas=[rowsum([x["theta"] for x in seen],a) for a in nvec];etas=[rowsum([x["eta"] for x in seen],a) for a in nvec]
    for h,t,eta in zip(hs,thetas,etas):require(h==mvec(case["D"],t) and not any(mvec(case["C"],eta)),"left kernel replay")
    require(case["terminal"] in ("MEMBER","NONMEMBER"),"terminal enum")
    target=vnorm(case["target"]);is_member=member(hs,target);expected=case["terminal"]=="MEMBER";require(is_member==expected,"terminal/member")
    if is_member:
        coeff=span_solve(hs,target);theta=rowsum(thetas,coeff);require(mvec(case["D"],theta)==target and not any(mvec(case["C"],rowsum(etas,coeff))),"member equations");dual_value=None
    else:
        dual_value=next((list(x) for x in itertools.product(range(3),repeat=zdim) if any(x) and all(sum(x[i]*h[i] for i in range(zdim))%3==0 for h in hs) and sum(x[i]*target[i] for i in range(zdim))%3==1),None);require(dual_value is not None,"dual")
        theta=[]
    return {"case":case["name"],"terminal":case["terminal"],"closure_rank":rank([x["flat"] for x in seen]),"rows":seen,"left_kernel_basis":nvec,"kernel_dim":len(nvec),"full_nonzero_kernel_cardinality":3**len(nvec)-1,"Hd1":hs,"Hd1_rank":rank(hs),"target":target,"member_theta":theta if is_member else None,"dual":dual_value,"slice_membership":is_member}
def mutate(case,owner):
    c=json.loads(json.dumps(case));baseline=digest(c)
    if owner=="field_modulus":c["modulus"]=9
    elif owner=="theta_seed":c["theta_seeds"][0][0]=(c["theta_seeds"][0][0]+1)%3
    elif owner=="theta_action":c["A_theta"][0][0]=2
    elif owner=="z_action":c["A_Z"][0][0]=2
    elif owner=="eta_action":c["A_E"][0][0]=2
    elif owner=="D_entry":c["D"][0][0]=2
    elif owner=="O_entry":c["O"][0][0]=2
    elif owner=="C_entry":c["C"][0][0]=2
    elif owner=="action_order":c["action_names"]=["mutated-action"]
    elif owner=="parent":c["parent_hint"]=1
    elif owner=="premature_C":c["C_phase"]="before-closure"
    elif owner=="left_kernel":c["left_kernel_method"]="image"
    elif owner=="target":c["target"]=[1,0]
    elif owner=="seed_index":c["seed_bindings"][0][0]=(c["seed_bindings"][0][0]+1)%3
    elif owner=="row_theta":c["theta_seeds"][0][0]=(c["theta_seeds"][0][0]+1)%3
    elif owner=="Hd1":c["C"][0][0]=2
    elif owner=="member_ancestry":c["seed_bindings"][0][0]=(c["seed_bindings"][0][0]+1)%3
    elif owner=="dual":c["terminal"]="MEMBER"
    elif owner=="terminal":c["terminal"]="MUTATED"
    else: raise RuntimeError("unknown mutation owner")
    require(digest(c)!=baseline,"mutation canonical unchanged")
    c["mutation_fixture_seal"]=mutation_seal(c)
    require(type(c["mutation_fixture_seal"]) is str and c["mutation_fixture_seal"]==mutation_seal(c),"mutation seal")
    try:return compile_case(c)
    except (RuntimeError,ValueError,KeyError,TypeError):return None
def selftest(fixture):
    f=parse_fixture(fixture);results=[compile_case(c) for c in f["cases"]]
    wrong_seal=dict(f);wrong_seal["fixture_seal"]="wrong-nonempty-seal";seal_rejected=False
    try:validate_fixture(wrong_seal)
    except RuntimeError:seal_rejected=True
    require(seal_rejected is True,"wrong nonempty fixture seal canary")
    for result in results:
        expected=f["expected_cases"][result["case"]]
        require(result["closure_rank"]==expected["closure_rank"] and result["kernel_dim"]==expected["kernel_dim"] and result["full_nonzero_kernel_cardinality"]==expected["full_nonzero_kernel_cardinality"] and result["Hd1_rank"]==expected["Hd1_rank"],"fixture expected rank")
        require(result["member_theta"]==expected["member_theta"] and result["dual"]==expected["dual"],"fixture expected equation")
    controls=[]
    for owner in OWNERS:
        rejected=mutate(f["cases"][1],owner) is None
        require(rejected is True,"mutation semantic rejection")
        controls.append({"owner":owner,"rejected":rejected})
    require(len(controls)==len(OWNERS) and all(x["rejected"] is True for x in controls),"mutation accepted")
    body={"schema":SELF,"status":"COMPLETE","terminal":PASS,"cases":results,"mutation_controls":controls,"mutation_attempted":len(controls),"mutation_rejected":sum(x["rejected"] is True for x in controls),"wrong_seal_rejected":seal_rejected,"production_input":False}
    return dict(body,self_digest_sha256=digest(body))
def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument("--mode",choices=("SELFTEST","PRODUCTION"),required=True);p.add_argument("--fixture",type=Path,default=ROOT/FIXTURE);p.add_argument("--output",type=Path,required=True);a=p.parse_args(argv)
    value=selftest(a.fixture) if a.mode=="SELFTEST" else {"schema":SCHEMA,"status":STATIC,"terminal":STATIC,"reason":"actual typed matrices are not staged"}
    a.output.write_bytes(canon(value)+b"\n");print(PASS if a.mode=="SELFTEST" else "R07_JOINT_SLICE_KERNEL_GENERAL_V9_PRODUCER_TERMINAL "+value["terminal"])
if __name__=="__main__":main()







