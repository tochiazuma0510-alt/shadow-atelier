# rank over F_7 of the images of the 6 PB4 generators in (P^ab)^4 = F_7^8
p=7
# P^ab basis (x,y):  x12->(1,0)  x23->(0,1)  x13->(-1,-1)
V={'x12':(1,0),'x23':(0,1),'x13':(-1,-1),'1':(0,0)}
P={1:{'x12':'1','x13':'1','x14':'1','x23':'x12','x24':'x13','x34':'x23'},
   2:{'x12':'1','x23':'1','x24':'1','x13':'x12','x14':'x13','x34':'x23'},
   3:{'x13':'1','x23':'1','x34':'1','x12':'x12','x14':'x13','x24':'x23'},
   4:{'x14':'1','x24':'1','x34':'1','x12':'x12','x13':'x13','x23':'x23'}}
gens=['x12','x13','x14','x23','x24','x34']
rows=[]
for g in gens:
    r=[]
    for i in [1,2,3,4]:
        a,b=V[P[i][g]]
        r+= [a%p,b%p]
    rows.append(r)
    print(g, r)
# gaussian elimination over F_7
M=[row[:] for row in rows]; rank=0; ncol=8
for c in range(ncol):
    piv=None
    for r in range(rank,len(M)):
        if M[r][c]%p: piv=r;break
    if piv is None: continue
    M[rank],M[piv]=M[piv],M[rank]
    inv=pow(M[rank][c],p-2,p)
    M[rank]=[(v*inv)%p for v in M[rank]]
    for r in range(len(M)):
        if r!=rank and M[r][c]%p:
            f=M[r][c]
            M[r]=[(M[r][k]-f*M[rank][k])%p for k in range(ncol)]
    rank+=1
print("F_7-rank of abelianized image =",rank)
print("=> |image in (P^ab)^4| = 7^%d ; |(P^ab)^4| = 7^8"%rank)
print("=> |PB4 : N_core| divides 7^%d * (7^6)^4 = 7^%d   [ab rank + 4 x dim[P,P] ]"%(rank,rank+24))
print("   crude lower bound: >= |P| = 7^8 (each coordinate onto)")
