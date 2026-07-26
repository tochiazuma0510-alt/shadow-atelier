// ===========================================================================
// metab_rank.mjs  --  E19-b' の検算(数学者 Opus・委嘱 10)
//
// 目的: docs/scout/metab.mjs と同じ自由 metabelian モデルで、各 m について
//         rank_Q M(m),  rank_F2 M(m),  rank_Q [M(m) | b(m)]
//   を計算し、「全ての非零 Smith 因子が奇数」 <=> rank_Q = rank_F2 を
//   m の剰余類ごとに追跡する。Smith 形は計算しない(rank だけで判定できる)。
//
//   これは 系 E19-b(便 13 F10 で FAIL)の修理案 命題 E19-b'(v3 §4)の
//   前提データ: 「多項式行列の小行列式は次数 <= (r+1)d ゆえ、十分多くの
//   標本点で rank <= r なら恒等的に rank <= r」という有限判定の入力。
//
//   usage: node metab_rank.mjs [class c] [mMax]      (defaults 5, 200)
// ===========================================================================
const CC = Number(process.argv[2] || 5), MMAX = Number(process.argv[3] || 200);

// ---------- truncated polynomial arithmetic in Z[S,T]/(S,T)^{DG+1} ----------
// (docs/scout/metab.mjs と同一。モデルは意図的に共有 — 本スクリプトは
//  第二系統ではなく、同一モデル上の別量(rank)を測る補助計算である。)
let DG = 0;
const key = (a,b)=>a+","+b;
const P0 = ()=>new Map();
const Pc = (c)=>{const m=new Map(); if(c!==0n)m.set("0,0",c); return m;};
const padd=(A,B)=>{const R=new Map(A);for(const[k,v]of B){const u=(R.get(k)||0n)+v;if(u===0n)R.delete(k);else R.set(k,u);}return R;};
const psub=(A,B)=>{const R=new Map(A);for(const[k,v]of B){const u=(R.get(k)||0n)-v;if(u===0n)R.delete(k);else R.set(k,u);}return R;};
const pscal=(A,c)=>{const R=new Map();if(c===0n)return R;for(const[k,v]of A)R.set(k,v*c);return R;};
function pmul(A,B){const R=new Map();
  for(const[k1,v1]of A){const[a1,b1]=k1.split(",").map(Number);
    for(const[k2,v2]of B){const[a2,b2]=k2.split(",").map(Number);
      if(a1+a2+b1+b2>DG)continue; const k=key(a1+a2,b1+b2);
      const u=(R.get(k)||0n)+v1*v2; if(u===0n)R.delete(k); else R.set(k,u);}}
  return R;}
function ppow(A,n){let R=Pc(1n),b=new Map(A);while(n>0){if(n&1)R=pmul(R,b);b=pmul(b,b);n>>=1;}return R;}
function pinvUnit(A){const u=psub(A,Pc(1n)); let R=Pc(1n),t=Pc(1n);
  for(let i=1;i<=DG;i++){t=pmul(t,u); R = i%2 ? psub(R,t) : padd(R,t);} return R;}
const S=()=>{const m=new Map();m.set("1,0",1n);return m;};
const T=()=>{const m=new Map();m.set("0,1",1n);return m;};
const s_=()=>padd(Pc(1n),S()), t_=()=>padd(Pc(1n),T());
function psubst(f,U,V){ let R=P0();
  const Up=[Pc(1n)],Vp=[Pc(1n)];
  for(let i=1;i<=DG;i++){Up.push(pmul(Up[i-1],U));Vp.push(pmul(Vp[i-1],V));}
  for(const[k,v]of f){const[a,b]=k.split(",").map(Number); if(a+b>DG)continue;
    R=padd(R,pscal(pmul(Up[a],Vp[b]),v));}
  return R;}

let BASIS=[], IDX=new Map();
function setClass(c){ DG=c-2; BASIS=[]; IDX=new Map();
  for(let d=0;d<=DG;d++)for(let a=d;a>=0;a--){const b=d-a;IDX.set(key(a,b),BASIS.length);BASIS.push([a,b]);} }
const toVec=(f)=>{const v=new Array(BASIS.length).fill(0n);for(const[k,c]of f){const i=IDX.get(k);if(i!==undefined)v[i]=c;}return v;};
const fromVec=(v)=>{const f=new Map();v.forEach((c,i)=>{if(c!==0n)f.set(key(...BASIS[i]),c);});return f;};
const thetaP=(f)=>pscal(psubst(f,T(),S()),-1n);
function tauP(f){ const invs=pinvUnit(s_()), invt=pinvUnit(t_());
  const rho=psub(pmul(invs,invt),Pc(1n));
  return pmul(psubst(f,T(),rho),invs); }
const sigmaP=(f,m)=>pmul(ppow(t_(),m),tauP(f));
function Em(m){ if(m===0)return P0();
  const s=s_(),t=t_(),st=pmul(s,t);
  const A=(u,n)=>{let R=P0(),p=Pc(1n);for(let i=0;i<n;i++){R=padd(R,p);p=pmul(p,u);}return R;};
  let c=P0();
  for(let k=2;k<=m;k++) c=padd(pmul(t,A(st,k-1)),pmul(t,c));
  const inv_sm=ppow(pinvUnit(s),m);
  return psub(c, pmul(inv_sm,pmul(A(s,m),A(st,m)))); }
const matOf=(op)=>BASIS.map((_,i)=>{const e=new Array(BASIS.length).fill(0n);e[i]=1n;return toVec(op(fromVec(e)));});
const mm=(A,B)=>A.map(r=>{const o=new Array(A.length).fill(0n);r.forEach((c,i)=>B[i].forEach((v,j)=>o[j]+=c*v));return o;});
const ma=(...M)=>M[0].map((_,i)=>M[0][i].map((_,j)=>M.reduce((s,X)=>s+X[i][j],0n)));
const idm=(n)=>[...Array(n)].map((_,i)=>[...Array(n)].map((_,j)=>i===j?1n:0n));

// ---------- ranks ----------
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b];}return a;};
function rankQ(Min){                       // fraction-free elimination over Z (= rank over Q)
  const A=Min.map(r=>r.slice()); const n=A.length, mc=A[0].length; let r=0;
  for(let c=0;c<mc&&r<n;c++){
    let p=-1; for(let i=r;i<n;i++) if(A[i][c]!==0n){p=i;break;}
    if(p<0) continue;
    [A[r],A[p]]=[A[p],A[r]];
    for(let i=r+1;i<n;i++) if(A[i][c]!==0n){
      const a=A[r][c], b=A[i][c];
      for(let j=c;j<mc;j++) A[i][j]=a*A[i][j]-b*A[r][j];
      let g=0n; for(let j=c;j<mc;j++) g=gcd(g,A[i][j]);
      if(g>1n) for(let j=c;j<mc;j++) A[i][j]/=g;
    }
    r++;
  }
  return r;
}
function rankF2(Min){
  const A=Min.map(r=>r.map(x=>((x%2n)+2n)%2n===1n?1:0));
  const n=A.length, mc=A[0].length; let r=0;
  for(let c=0;c<mc&&r<n;c++){
    let p=-1; for(let i=r;i<n;i++) if(A[i][c]){p=i;break;}
    if(p<0) continue;
    [A[r],A[p]]=[A[p],A[r]];
    for(let i=0;i<n;i++) if(i!==r&&A[i][c]) for(let j=c;j<mc;j++) A[i][j]^=A[r][j];
    r++;
  }
  return r;
}

// ---------- main ----------
setClass(CC);
const n=BASIS.length, d=2*(CC-2);
const th=matOf(thetaP), OT=ma(idm(n),th);
console.log(`class c=${CC}  rank A_c = n = ${n}   entry-degree bound d = 2(c-2) = ${d}`);
console.log(`m   rank_Q(M)  rank_F2(M)  rank_Q[M|b]   all-divisors-odd?  Q-solvable?`);
const byRes = new Map();               // residue mod 8 -> {rQ:Set, rF:Set, rAug:Set, count}
for(let m=0;m<=MMAX;m++){
  const sm=matOf(f=>sigmaP(f,m)); const N=ma(idm(n),sm,mm(sm,sm));
  const b=toVec(Em(m));
  const rows=[],rhs=[];
  for(let i=0;i<n;i++){const r=new Array(n).fill(0n);for(let k=0;k<n;k++)r[k]=OT[k][i];rows.push(r);rhs.push(0n);}
  for(let i=0;i<n;i++){const r=new Array(n).fill(0n);for(let k=0;k<n;k++)r[k]=N[k][i];rows.push(r);rhs.push(-b[i]);}
  const aug=rows.map((r,i)=>r.concat([rhs[i]]));
  const rQ=rankQ(rows), rF=rankF2(rows), rA=rankQ(aug);
  const res=m%8;
  if(!byRes.has(res)) byRes.set(res,{rQ:new Set(),rF:new Set(),rA:new Set(),count:0});
  const e=byRes.get(res); e.rQ.add(rQ); e.rF.add(rF); e.rA.add(rA); e.count++;
  if(m<=23||m%8===0) console.log(`${String(m).padStart(3)}     ${rQ}         ${rF}          ${rA}          ${rQ===rF?"YES":"NO "}              ${rA===rQ?"YES":"NO "}`);
}
console.log("\n--- per residue class mod 8 ---");
console.log("res | #samples | rank_Q values | rank_F2 values | rank[M|b] values | needed #samples (E19-b')");
let ok=true;
for(const res of [...byRes.keys()].sort((a,b)=>a-b)){
  const e=byRes.get(res);
  const rQ=[...e.rQ], rF=[...e.rF], rA=[...e.rA];
  const rmax=Math.max(...rQ);
  const need1=(rmax+1)*d+1, need2=(rmax+1)*d+CC+1;      // strict: > degree bound
  const pass = rQ.length===1 && rF.length===1 && rA.length===1 && rQ[0]===rF[0] && rA[0]===rQ[0]
               && e.count>=need2;
  if(!pass) ok=false;
  console.log(` ${res}  |   ${String(e.count).padStart(4)}   | ${rQ.join(",")}            | ${rF.join(",")}             | ${rA.join(",")}              | ${need1} (M) / ${need2} ([M|b])  ${pass?"=> CLOSED":"=> not yet"}`);
}
console.log(ok ? `\n*** E19-b' criterion MET for c=${CC} on m=0..${MMAX} (all residues) ***`
               : `\n*** E19-b' criterion NOT yet met for c=${CC} with mMax=${MMAX} ***`);
