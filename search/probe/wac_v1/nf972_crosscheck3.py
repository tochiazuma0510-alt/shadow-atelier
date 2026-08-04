# NF-972 third fourth-party set comparison (commander, 2026-08-04, ruling 456)
# A v2 (python fiber-product, witness->q4(f) repair) vs B v3 (GAP direct roof, sigma=id)
# Result recorded in LEDGER: SET EQUAL True, 972/972, dup 0, (m,can9) proj 108=108, (m,can4) proj 108=108
import json
A = json.load(open('search/certs/nf972_sourcemap_a_tuples_v2_20260804.json', encoding='utf-8'))
B = json.load(open('search/certs/nf972_sourcemap_b_tuples_v3_20260804.json', encoding='utf-8'))
ta = A['tuples'] if isinstance(A, dict) else A
tb = B['tuples'] if isinstance(B, dict) else B

def normA(t):
    m0, pairs, ol = t[0], t[1], t[2]
    return (int(m0), tuple((int(a) % 9, int(e) % 2) for a, e in pairs), tuple(int(x) for x in ol))

def normB(s):
    m0, mid, ol = s.strip('()').split(';')
    v = [int(x) for x in mid.split(',')]
    return (int(m0), tuple((v[2*i] % 9, v[2*i+1] % 2) for i in range(3)), tuple(int(x) for x in ol.split(',')))

SA = set(map(normA, ta)); SB = set(map(normB, tb))
assert len(ta) == len(tb) == 972 and len(SA) == len(SB) == 972
assert SA == SB
assert set((t[0], t[1]) for t in SA) == set((t[0], t[1]) for t in SB)
assert set((t[0], t[2]) for t in SA) == set((t[0], t[2]) for t in SB)
print('NF972_CROSSCHECK3: SET EQUAL, 972/972, dup 0, projections match')
