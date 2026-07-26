// Class-4 structural test: solve  N(v) = -E_m  AND  (1+theta)v = 0  over Q,
// then inspect denominators.  If every solution denominator is a power of 3,
// the solution is 2-integral => the criterion holds mod 2^j for EVERY j
// (since 3 is invertible mod 2^j).  That upgrades the numeric run to a proof.
const D = 4;
const WORDS = []; (function g(s){WORDS.push(s); if(s.length<D){g(s+"0");g(s+"1");}})("");
const ONE=()=>({"":1n}), cl=(A)=>{const R={};for(const k in A) if(A[k]!==0n)R[k]=A[k];return R;};
const mul=(A,B)=>{const R={};for(const a in A)for(const b in B){if(a.length+b.length>D)continue;const k=a+b;R[k]=(R[k]||0n)+A[a]*B[b];}return cl(R);};
const sb=(A,B)=>{const R={...A};for(const b in B)R[b]=(R[b]||0n)-B[b];return cl(R);};
const ad=(A,B)=>{const R={...A};for(const b in B)R[b]=(R[b]||0n)+B[b];return cl(R);};
const iv=(A)=>{const u=sb(A,ONE());let R=ONE(),t=ONE();for(let i=1;i<=D;i++){t=mul(t,u);R=i%2?sb(R,t):ad(R,t);}return cl(R);};
const pw=(A,n)=>{if(n<0)return pw(iv(A),-n);let R=ONE();for(let i=0;i<n;i++)R=mul(R,A);return R;};
const cm=(a,b)=>mul(mul(iv(a),iv(b)),mul(a,b));
const x={"":1n,"0":1n}, y={"":1n,"1":1n}, z=iv(mul(x,y));
const w=cm(x,y), p=cm(w,x), q=cm(w,y);
const B=[["w",w,2],["p",p,3],["q",q,3],["r1",cm(p,x),4],["r2",cm(p,y),4],["r3",cm(q,y),4]];
const NM=B.map(b=>b[0]), EL=B.map(b=>b[1]), WT=B.map(b=>b[2]), R=6;
const dk=(A,k)=>WORDS.filter(s=>s.length===k).map(s=>A[s]||0n);
const gg=(u,v)=>{u=u<0n?-u:u;v=v<0n?-v:v;while(v){[u,v]=[v,u%v];}return u;};
function solveInt(cols,tg){const n=cols.length,L=tg.length,M=[];
 for(let i=0;i<L;i++)M.push([...cols.map(c=>c[i]),tg[i]]);
 const s=new Array(n).fill(0n),pv=[];let r=0;
 for(let c=0;c<n&&r<L;c++){let pr=-1;for(let i=r;i<L;i++)if(M[i][c]!==0n){pr=i;break;}
  if(pr<0)continue;[M[r],M[pr]]=[M[pr],M[r]];
  for(let i=0;i<L;i++)if(i!==r&&M[i][c]!==0n){const g0=gg(M[r][c],M[i][c]),fa=M[r][c]/g0,fb=M[i][c]/g0;
   for(let j=0;j<=n;j++)M[i][j]=M[i][j]*fa-M[r][j]*fb;}
  pv.push([r,c]);r++;}
 for(let i=r;i<L;i++)if(M[i][n]!==0n)return null;
 for(const[rr,cc]of pv){if(M[rr][n]%M[rr][cc])return null;s[cc]=M[rr][n]/M[rr][cc];}return s;}
function nf(g){const o=new Array(R).fill(0n);let h={...g};
 for(let k=2;k<=D;k++){const idx=[...Array(R).keys()].filter(i=>WT[i]===k);if(!idx.length)continue;
  const s=solveInt(idx.map(i=>dk(EL[i],k)),dk(h,k));if(s===null)throw new Error("nf");
  idx.forEach((i,j)=>o[i]=s[j]);for(const i of idx)h=mul(h,pw(EL[i],Number(-o[i])));}
 return o;}
const am=(IX,IY)=>{const W=cm(IX,IY),P=cm(W,IX),Q=cm(W,IY);
 const M={w:W,p:P,q:Q,r1:cm(P,IX),r2:cm(P,IY),r3:cm(Q,IY)};return NM.map(n=>nf(M[n]));};
const theta=am(y,x);
const sig=(m)=>{const cj=(g)=>mul(mul(pw(y,-m),g),pw(y,m));return am(cj(y),cj(z));};
const mm=(A,Bm)=>A.map(row=>{const o=new Array(R).fill(0n);row.forEach((c,i)=>Bm[i].forEach((v,j)=>o[j]+=c*v));return o;});
const ma=(...Ms)=>Ms[0].map((_,i)=>Ms[0][i].map((_,j)=>Ms.reduce((s,M)=>s+M[i][j],0n)));
const ID=[...Array(R).keys()].map(i=>[...Array(R).keys()].map(j=>(i===j?1n:0n)));

// --- exact rational Gaussian elimination (BigInt fractions) ---
const nrm=(a,b)=>{if(b<0n){a=-a;b=-b;}const g0=gg(a,b)||1n;return [a/g0,b/g0];};
const Q_=(a,b=1n)=>nrm(a,b);
const qa=(A,B2)=>Q_(A[0]*B2[1]+B2[0]*A[1],A[1]*B2[1]);
const qs=(A,B2)=>Q_(A[0]*B2[1]-B2[0]*A[1],A[1]*B2[1]);
const qm=(A,B2)=>Q_(A[0]*B2[0],A[1]*B2[1]);
const qd=(A,B2)=>Q_(A[0]*B2[1],A[1]*B2[0]);
function solveQ(rows,rhs){                 // rows: L x R rational, rhs: L
  const L=rows.length, M=rows.map((r,i)=>[...r.map(c=>Q_(c)),Q_(rhs[i])]);
  const pv=[];let r=0;
  for(let c=0;c<R&&r<L;c++){let pr=-1;for(let i=r;i<L;i++)if(M[i][c][0]!==0n){pr=i;break;}
   if(pr<0)continue;[M[r],M[pr]]=[M[pr],M[r]];
   const d=M[r][c];for(let k=c;k<=R;k++)M[r][k]=qd(M[r][k],d);
   for(let i=0;i<L;i++)if(i!==r&&M[i][c][0]!==0n){const f=M[i][c];
    for(let k=c;k<=R;k++)M[i][k]=qs(M[i][k],qm(f,M[r][k]));}
   pv.push([r,c]);r++;}
  for(let i=r;i<L;i++)if(M[i][R][0]!==0n)return null;
  const v=[...Array(R)].map(()=>Q_(0n));
  for(const[rr,cc]of pv)v[cc]=M[rr][R];
  return {sol:v, freeCols:[...Array(R).keys()].filter(c=>!pv.some(pp=>pp[1]===c))};
}
const v2=(n)=>{if(n===0n)return "inf";let v=0;n=n<0n?-n:n;while(n%2n===0n){n/=2n;v++;}return v;};
console.log("### class 4: solve  (1+theta)v=0 & N(v)=-E_m  over Q ; inspect denominators");
let bad2=false;
for(let m=0;m<=12;m++){
  const S=sig(m), N=ma(ID,S,mm(S,S)), OT=ma(ID,theta);
  const Em=nf(mul(mul(pw(x,m),pw(z,m)),pw(y,m)));
  const rows=[],rhs=[];
  for(let c=0;c<R;c++){rows.push([...Array(R).keys()].map(i=>OT[i][c]));rhs.push(0n);}
  for(let c=0;c<R;c++){rows.push([...Array(R).keys()].map(i=>N[i][c]));rhs.push(-Em[c]);}
  const res=solveQ(rows,rhs);
  if(!res){console.log(`  m=${m}: NO RATIONAL SOLUTION (obstructed over Q)`);bad2=true;continue;}
  const dens=res.sol.map(f=>f[1]);
  const odd=dens.every(d=>d%2n!==0n);
  console.log(`  m=${m}: sol=[${res.sol.map(f=>f[1]===1n?f[0]:f[0]+"/"+f[1]).join(", ")}]  free=${res.freeCols.length}  denominators ${odd?"ODD (2-integral)  OK":"EVEN  *** not 2-integral ***"}`);
  if(!odd)bad2=true;
}
console.log(bad2?"\n>>> NOT uniformly 2-integral -- structural proof does not follow"
                :"\n>>> every solution is 2-integral => criterion holds mod 2^j for ALL j (class 4 closed)");
