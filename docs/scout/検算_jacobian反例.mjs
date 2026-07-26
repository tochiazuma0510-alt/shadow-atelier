// Exact verification of the Alpöge–Claude Jacobian counterexample (n=3).
// Polynomials over Z in x,y,z: Map "a,b,c" -> BigInt coefficient.
const P = (obj={}) => { const m = new Map(); for (const [k,v] of Object.entries(obj)) if (v!==0n) m.set(k, v); return m; };
const key = (a,b,c) => `${a},${b},${c}`;
const mono = (c,a,b,cc) => P({[key(a,b,cc)]: c});
const add = (p,q) => { const r = new Map(p); for (const [k,v] of q) { const w = (r.get(k)||0n)+v; if (w===0n) r.delete(k); else r.set(k,w); } return r; };
const neg = p => { const r = new Map(); for (const [k,v] of p) r.set(k,-v); return r; };
const sub = (p,q) => add(p, neg(q));
const mul = (p,q) => { const r = new Map(); for (const [k1,v1] of p) for (const [k2,v2] of q) {
  const [a1,b1,c1]=k1.split(',').map(Number), [a2,b2,c2]=k2.split(',').map(Number);
  const k3 = key(a1+a2,b1+b2,c1+c2); const w = (r.get(k3)||0n)+v1*v2; if (w===0n) r.delete(k3); else r.set(k3,w); } return r; };
const diff = (p,i) => { const r = new Map(); for (const [k,v] of p) { const e = k.split(',').map(Number); if (e[i]===0) continue;
  const c = v * BigInt(e[i]); const e2=[...e]; e2[i]-=1; const k2=key(...e2); const w=(r.get(k2)||0n)+c; if (w===0n) r.delete(k2); else r.set(k2,w); } return r; };
const C = n => mono(BigInt(n),0,0,0);
const X = mono(1n,1,0,0), Y = mono(1n,0,1,0), Z = mono(1n,0,0,1);

// u = 1+xy
const u = add(C(1), mul(X,Y));
const u2 = mul(u,u), u3 = mul(u2,u);
const fourPlus3xy = add(C(4), mul(C(3), mul(X,Y)));
// F1 = u^3 z + y^2 u (4+3xy)
const F1 = add(mul(u3,Z), mul(mul(mul(Y,Y),u), fourPlus3xy));
// F2 = y + 3 x u^2 z + 3 x y^2 (4+3xy)
const F2 = add(Y, add(mul(C(3),mul(X,mul(u2,Z))), mul(C(3),mul(X,mul(mul(Y,Y),fourPlus3xy)))));
// F3 = 2x - 3x^2 y - x^3 z
const F3 = sub(sub(mul(C(2),X), mul(C(3),mul(mul(X,X),Y))), mul(mul(X,mul(X,X)),Z));

// Jacobian determinant (exact symbolic)
const J = [[diff(F1,0),diff(F1,1),diff(F1,2)],[diff(F2,0),diff(F2,1),diff(F2,2)],[diff(F3,0),diff(F3,1),diff(F3,2)]];
const det = sub(add(add(mul(J[0][0],sub(mul(J[1][1],J[2][2]),mul(J[1][2],J[2][1]))),
                        mul(J[0][2],sub(mul(J[1][0],J[2][1]),mul(J[1][1],J[2][0])))),C(0)),
                mul(J[0][1],sub(mul(J[1][0],J[2][2]),mul(J[1][2],J[2][0]))));
const detEntries = [...det.entries()];
console.log("det J terms:", detEntries.length, "->", JSON.stringify(detEntries.map(([k,v])=>[k,v.toString()])));
console.log("det J === -2 identically:", detEntries.length===1 && det.get("0,0,0")===-2n);

// Exact rational evaluation: points scaled to avoid fractions — evaluate with fractions via BigInt pairs
const gcd = (a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b];}return a;};
const F_ = (num, den) => { const g = gcd(num,den)||1n; num/=g; den/=g; if (den<0n){num=-num;den=-den;} return [num,den]; };
const fadd=([a,b],[c,d])=>F_(a*d+c*b, b*d), fmul=([a,b],[c,d])=>F_(a*c,b*d);
const evalP = (p, pt) => { let s=[0n,1n]; for (const [k,v] of p) { const [a,b,c]=k.split(',').map(Number);
  let t=[v,1n]; for(let i=0;i<a;i++) t=fmul(t,pt[0]); for(let i=0;i<b;i++) t=fmul(t,pt[1]); for(let i=0;i<c;i++) t=fmul(t,pt[2]); s=fadd(s,t);} return s; };
const pts = [ [[0n,1n],[0n,1n],[-1n,4n]], [[1n,1n],[-3n,2n],[13n,2n]], [[-1n,1n],[3n,2n],[13n,2n]] ];
for (const pt of pts) {
  const v = [evalP(F1,pt), evalP(F2,pt), evalP(F3,pt)];
  console.log("F(", pt.map(([n,d])=>`${n}/${d}`).join(", "), ") =", v.map(([n,d])=>`${n}/${d}`).join(", "));
}
