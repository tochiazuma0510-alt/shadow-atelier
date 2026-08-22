"""Decisive check of the A2 v2 cond3 predicate at p=2, from raw rows+witness jsonl.
Correct charming at K_p:  (A,B) in p*Lambda_N  <=>  p|A and p|B and 3 | (A+B)/p.
Implemented (script line 'gotcond3'): 3 | (S/3 + (a_w+b_w)/3)  <=>  9 | (A+B)   [the p=3 predicate]."""
import json, io, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
B = r"C:\Users\81905\Desktop\shadow-atelier\search\certs\koubou83_A2_48sweep_v2_20260822"

def linking(word):
    pos = [1, 2, 3]; L = {(1,2):0, (1,3):0, (2,3):0}
    for a in word:
        i = abs(a); s = 1 if a > 0 else -1
        j, k = pos[i-1], pos[i]
        L[(min(j,k), max(j,k))] += s
        pos[i-1], pos[i] = k, j
    if pos != [1,2,3]: return None
    if any(v % 2 for v in L.values()): return None
    return (L[(1,2)]//2, L[(1,3)]//2, L[(2,3)]//2)

def abg_sigma(word):
    lk = linking(word)
    if lk is None: return None
    l12, l13, l23 = lk
    return (l12-l13, l23-l13, l13)

def ab_xy(word):
    a = b = 0
    for t in word:
        if abs(t) == 1: a += (1 if t > 0 else -1)
        else: b += (1 if t > 0 else -1)
    return (a, b)

rows = [json.loads(l) for l in io.open(B+"_rows.jsonl", encoding='utf-8') if l.strip()]
wits = {}
for l in io.open(B+"_witness.jsonl", encoding='utf-8'):
    if not l.strip(): continue
    r = json.loads(l)
    wits[(tuple(r['window']), r['shadow_idx'], r['p'])] = r['witness_sigma_word']

bad_S = 0; bad_W = 0; mism_impl = 0; mism_corr = 0; n = 0
dead = []
print("%-14s %3s %1s | %-9s %-14s | cond1/2/3(cert) | correct-cond3 | 9|(A+B)" % ("window","idx","p","ab(f0)","abg(w)"))
for r in rows:
    n += 1
    key = (tuple(r['window']), r['shadow_idx'], r['p'])
    w = wits.get(key)
    if w is None: print("  MISSING WITNESS", key); continue
    a0, b0 = ab_xy(r['f_xyword'])
    aw, bw, gw = abg_sigma(w)
    S = a0 + b0; Ws = aw + bw
    A, Bv = a0+aw, b0+bw
    p = r['p']
    if S % 3: bad_S += 1
    if Ws % 3: bad_W += 1
    c1 = (A % p == 0); c2 = (Bv % p == 0)
    corr3 = c1 and c2 and (((A+Bv)//p) % 3 == 0)
    impl3 = ((A+Bv) % 9 == 0)
    if c1 != r['cond1'] or c2 != r['cond2']: mism_corr += 1
    if impl3 != r['cond3']: mism_impl += 1
    if not r['cond3']:
        dead.append((r['window'][1], r['shadow_idx'], p, (a0,b0), (aw,bw,gw), A+Bv, corr3, impl3))
print("rows=%d ; rows with 3 nmid S: %d ; rows with 3 nmid (a_w+b_w): %d" % (n, bad_S, bad_W))
print("cert cond1/cond2 reproduced exactly: %s (mismatches=%d)" % (mism_corr == 0, mism_corr))
print("cert cond3 == [9 | (A+B)] : %s (mismatches=%d)" % (mism_impl == 0, mism_impl))
allcorr = all(((a0+aw+b0+bw) // r['p']) % 3 == 0
              for r in rows
              for (a0, b0) in [ab_xy(r['f_xyword'])]
              for (aw, bw, gw) in [abg_sigma(wits[(tuple(r['window']), r['shadow_idx'], r['p'])])]
              if (a0+aw) % r['p'] == 0 and (b0+bw) % r['p'] == 0)
print("CORRECT cond3 (3 | (A+B)/p) holds on every row where cond1&cond2 hold: %s" % allcorr)
print("\ncond3=false rows: %d" % len(dead))
for d in dead[:8]:
    print("   win=%d idx=%d p=%d ab(f0)=%s abg(w)=%s A+B=%d  correct_cond3=%s  9|(A+B)=%s"
          % d)
print("   ... (showing first 8)")
print("\nprimes among cond3=false rows:", sorted(set(d[2] for d in dead)))
print("A+B values mod 9 among dead rows:", sorted(set((d[5] % 9) for d in dead)))
print("A+B values mod 6 among dead rows:", sorted(set((d[5] % 6) for d in dead)))
# the positive control [11,1]: f0 = empty word
pc = [d for d in dead if d[3] == (0, 0)]
print("\ndead rows with f0 = 1 (identity f, includes the [11,1] arithmetic control):", len(pc))
for d in pc: print("   ", d)
