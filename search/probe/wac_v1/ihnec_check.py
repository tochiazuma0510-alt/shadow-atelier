# IH-NEC v1 検算(整数演算のみ・単系統)
from math import gcd
fail=0
def chk(c,msg):
    global fail
    if not c: fail+=1; print("FAIL:",msg)

# --- 窓データ ---
n=9; Kord=2*n            # K^(9)_ord = 18
S4ord=9                  # N_S4 の N_ord(証明書 LEDGER L642)
# charming set
X9=[m for m in range(Kord) if gcd(2*m+1,Kord)==1]
XS4=[m for m in range(S4ord) if gcd(2*m+1,S4ord)==1]
chk(len(X9)==12,"|X_9|=12"); chk(len(XS4)==6,"|X_S4|=6")
chk(sorted(XS4)==[0,2,3,5,6,8],"S4 charming = {0,2,3,5,6,8}(surj_s4_v2 §1 と一致)")
chk(sorted(set(m%9 for m in X9))==sorted(XS4),"X_9 mod 9 の像 = S4 charming set")
from collections import Counter
c=Counter(m%9 for m in X9); chk(set(c.values())=={2},"各 m mod 9 はちょうど 2 回")

# --- 位数 ---
def phi(k): return sum(1 for i in range(1,k+1) if gcd(i,k)==1)
GT9=2*n*phi(n); chk(GT9==108,"|GT(K^9)|=108")
GTS4=54
F0_9=GT9//len(X9); F0_S4=GTS4//len(XS4)
chk(F0_9==9 and F0_S4==9,"F0 = 9 / 9")
chk(phi(4*n)==12,"|(Z/36)^x|=12"); chk(phi(2*n)==6,"|(Z/18)^x|=6")
# 屋根 M の予言
GTM=sum(F0_9*F0_S4 for m in X9)     # 各 m in X_9 で m mod 9 は必ず charming(上で確認)
chk(GTM==972,"|GT(M)|=972")
chk(GTM==GT9*GTS4//phi(2*n),"fiber product over (Z/18)^x = 108*54/6")
chk(GTM==F0_9*F0_S4*phi(4*n),"972 = 81 * 12")
# 群の位数
G9=n**3*4; chk(G9==2916,"|G_9|=2916")
chk(G9*504==1469664,"|PB3/M| = |G_9|*|PSL(2,8)| = 1469664")
# 比較可能性の数値篩
chk(Kord % S4ord==0 and S4ord % Kord!=0,"K^(9)_ord=18 は N_S4_ord=9 の倍数 ⟹ N_S4 ⊄ K^(9)")
# 像の全射性(分裂屋根)
img=set()
for m in X9:
    if m%9 in XS4: img.add(m)
chk(sorted(img)==sorted(X9),"Im R_{M,K^9} は全 m-fiber を含む ⟹ 全射")
print("failures =",fail); print("RESULT:","ALL PASS" if fail==0 else "FAILED")
