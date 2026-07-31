# prediction check: counts on the CORRECTED fiber for the Kummer coarse class
exec(open('scratchpad/pent_atomic_v2b.py').read().split('# ---------- third-party')[0])
import json, io
d = json.load(io.open('search/certs/pent_thirdparty_gt_20260731.json', encoding='utf-8'))
rows = d['coarse_reduction']['charming']['per_entry_rows']
lets = {0:('x',1), 1:('y',1), 2:('c',1)}
# word-of section for elements of QP (WordOf equivalent): BFS over generators
gens = {'x': Psi(X), 'y': Psi(Y), 'c': Psi(C)}
word = {ONE5: []}
fr = [ONE5]
while fr:
    nf = []
    for a in fr:
        for n, g in gens.items():
            b = mul5(a, g)                      # Psi is anti-hom: Psi(w)*Psi(g) = Psi(g*w)
            if b not in word:
                word[b] = [(n, 1)] + word[a]    # so prepend the letter
                nf.append(b)
    fr = nf
assert len(word) == 7500
bad = sum(1 for q, w in word.items() if Psi(w) != q)
print("word-section check: mismatches =", bad)

for target, m, label in ((3, 0, "Kummer class (2,3,4): corrected fiber (pr1 = (1,3,5))"),):
    # fiber over the coarse image carried by the author's witness for that class
    w_auth = red([lets[i] for i in rows[10]['word']])       # row 11 = the Kummer entry
    tgt = PsiAt(w_auth, 0)
    fib = [q for q in word if q[0] == tgt]
    cnt = [0]*6
    for q in fib:
        r = chk(m, word[q])
        for i, b in enumerate(r): cnt[i] += 1 if b else 0
    print(f"{label}\n  |fiber|={len(fib)}  c1={cnt[0]} c2={cnt[1]} c3={cnt[2]} c4={cnt[3]} c5={cnt[4]} all={cnt[5]}")
