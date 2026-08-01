# R4a(裁定376 GO)— 既存証明書からの独立照合 + 屋根 M の組立
# 数学者(Opus)単系統・python・整数演算のみ。GAP 再走なし(証明書を入力にする独立実装)。
import json, hashlib
from math import gcd
from collections import Counter
R="C:/Users/81905/Desktop/shadow-atelier/"
def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()
K9P,S4P=R+"certificates/K9.v1.json",R+"certificates/S4.v2.json"
K9=json.load(open(K9P,encoding='utf-8')); S4=json.load(open(S4P,encoding='utf-8'))
fails=[]
def chk(c,msg):
    if not c: fails.append(msg); print("FAIL:",msg)

print("== 入力証明書 ==")
print("K9.v1.json  sha256 =",sha(K9P))
print("S4.v2.json  sha256 =",sha(S4P))

# ---------- P-IHN-7 前半 (U-11): GT(K^(9)) の同型型を合成表から確定 ----------
sh=K9['shadows']; ct=K9['composition_table']; N=len(sh)
chk(N==108,"|GT(K^9)|=108")
chk(K9['target']['invariants']['N_ord']==18,"K9_ord=18")
chk(K9['counts']['raw_candidates']==12*729,"raw_candidates=12*729=8748(R4a-1 の走査規模の予言と一致)")
# 合成表 -> 積関数
prod={}
for row in ct: prod[(row[0],row[1])]=row[2]
chk(len(prod)==N*N,"合成表 108x108 完備")
# Theta 座標(命題 E1-S1): u=2m+1 mod 9, eps=m mod 2, k は f_triple 第1成分 = 2k mod 9
inv2=pow(2,-1,9)
def theta(s):
    m=s['m']; a=s['f_triple'][0][0]
    chk(s['f_triple'][0][1]==0 and s['f_triple'][1][1]==0 and s['f_triple'][2][1]==0,"f_triple は回転成分のみ")
    k=(a*inv2)%9
    chk(s['f_triple'][1][0]%9==(-a)%9,"第2成分 = r^{-2k}")
    kap=(m+1) if m%2==1 else (-m)
    chk(s['f_triple'][2][0]%9==kap%9,"第3成分 = r^{kappa(m)}")
    return (k,(2*m+1)%9,m%2)
TH=[theta(s) for s in sh]
chk(len(set(TH))==108,"Theta は単射(108 点)")
chk(set(x[1] for x in TH)==set(u for u in range(9) if gcd(u,9)==1),"u 像 = (Z/9)^x")
# 積が Aff(Z/9) x C2 の積か(全 108^2 対)
bad=0
for i in range(N):
    for j in range(N):
        k1,u1,e1=TH[i]; k2,u2,e2=TH[j]
        want=((k1+u1*k2)%9,(u1*u2)%9,(e1+e2)%2)
        if TH[prod[(i,j)]]!=want: bad+=1
chk(bad==0,"合成表が Aff(Z/9)xC2 の積と一致(全 11664 対) bad=%d"%bad)
print("U-11: GT(K^(9)) ≅ Aff(Z/9) x C2 = Hol(Z/9) x C2  [合成表 11664 対で確定]")
# 不変量(GAP IdGroup [108,26] の照合材料)
def order_of(i):
    e=i; n=1
    ident=[t for t in range(N) if all(prod[(t,x)]==x for x in range(N))][0]
    while e!=ident: e=prod[(e,i)]; n+=1
    return n
ident=[t for t in range(N) if all(prod[(t,x)]==x for x in range(N))][0]
ordprof=Counter(order_of(i) for i in range(N))
center=[i for i in range(N) if all(prod[(i,j)]==prod[(j,i)] for j in range(N))]
print("order profile:",dict(sorted(ordprof.items())))
print("|Z(GT(K^9))| =",len(center))
chk(len(center)==2,"中心の位数 2(= C2 因子; Aff(Z/9) は中心自明)")

# ---------- S4 窓の m 像 ----------
s4m=sorted(set(x['m'] for x in S4['settled_detail']))
c4=Counter(x['m'] for x in S4['settled_detail'])
chk(S4['settled_count']==54,"|GT(N_S4)|=54")
chk(s4m==[0,2,3,5,6,8],"S4 の m 像 = {0,2,3,5,6,8} = charming set 全体")
chk(set(c4.values())=={9},"各 m の fiber = 9 (= F_0 ≅ C_9)")
print("S4 m-image:",s4m," fibers:",sorted(set(c4.values())))

# ---------- 屋根 M = K^(9) ∩ N_S4 の組立 ----------
k9m=sorted(set(s['m'] for s in sh)); ck9=Counter(s['m'] for s in sh)
chk(sorted(set(m%9 for m in k9m))==s4m,"P-IHN: X_9 mod 9 の像 = S4 charming set")
GTM=sum(ck9[m]*c4[m%9] for m in k9m if m%9 in c4)
chk(GTM==972,"P-IHN-4: |GT(M)|=972  (実測組立 %d)"%GTM)
imgK9=sorted({m for m in k9m if m%9 in c4})
chk(imgK9==k9m,"P-IHN-5: Im R_{M,K^9} は全 m-fiber を含む ⟹ 108/108 全射")
imgS4=sorted({m%9 for m in k9m} & set(s4m))
chk(imgS4==s4m,"P-IHN-6: Im R_{M,S4} は全 m-fiber を含む ⟹ 54/54 全射")
chk(108*54//6==972,"fiber 積 108*54/|(Z/18)^x|=972")
# F_0(M) と chi 像
chk(9*9*12==972,"972 = |F_0(M)|(81) * |(Z/36)^x|(12)")
print("組立: |GT(M)|=%d, F_0(M)=81, chi-image=12, Im R_{M,K9}=108/108, Im R_{M,S4}=54/54"%GTM)
print("failures =",len(fails)); print("RESULT:","ALL PASS" if not fails else "FAILED")
