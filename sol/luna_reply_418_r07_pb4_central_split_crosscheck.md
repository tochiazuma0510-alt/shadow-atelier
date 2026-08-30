# Luna reply 418 — PB4 central-split independent replay

Completed the bounded task418 replay and created only the three authorized
outputs:

- `crosscheck/check_d972_r07_pb4_central_split_v1.py`
- `search/certs/d972_r07_pb4_central_split_v1_20260830.json`
- this reply

The checker byte-pins and independently loads only
`search/check_d972_b345_q3_chief_v1.py`; it does not import or execute the
producer-side `search/d972_b345_seedspan_triple4_v1.py`, and it does not
enumerate the matched group.

All bounded gates passed:

- frozen q3 schema/terminal, PB4 PC width/order/class/exponent/relative
  orders, and Q4 degree/order;
- `z=[1,2,4,3,5,6]` has coarse identity, nontrivial PC image, cube identity,
  and commutes with all six marked generators;
- `pc(z)=(1,1,1,1,1,1,0,0,0,0)` and the five noncentral marked generators
  have first coordinate zero;
- all 10 power, 45 conjugate, and 45 inverse-conjugate presentation rows
  descend under the first-coordinate map to F3;
- six literal Artin substitutions, fixation of `w=p*q*r`, and the
  `z3`-conjugation-by-`w` action;
- the source identity
  `A12=z*A34^-1*A24^-1*A14^-1*A23^-1*A13^-1` in both PC and coarse models;
- adversarial rejection of a wrong central order, a nonhomomorphic
  coordinate, and a dropped noncentral generator.

The certificate records the theorem consequence
`H=H0 direct_product <z>` as a finite central-split replay result. It sets
`cross_checked=true` and `verified=false`, and explicitly makes no A0,
fake, Ihara-witness, compatible-lift, or A0 MEMBER/NONMEMBER claim.

Replay command:

```text
python crosscheck/check_d972_r07_pb4_central_split_v1.py --output search/certs/d972_r07_pb4_central_split_v1_20260830.json
```

Result: PASS, wall time `0.309369 s`.

Pins:

- q3 receipt: 231570 bytes,
  `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`;
- proof v402: 9753 bytes,
  `7945c953db3a5b4dbbedb683a7c2e77ba19354bb2f5c0d76e98a5a550dafe8e9`;
- independent q3 checker: 89082 bytes,
  `ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73`;
- task418: 3735 bytes,
  `c91186486ae89ceb051b7f992b7452a757c6880ec902abbb8815fbe1784632b0`;
- central-split checker: 13575 bytes,
  `413717cebf6319b3a54926f40d71e2308e7ab773374af3f3f797627e35d371b0`;
- output certificate: 3774 bytes,
  `e1588853db01d196a9bf60ed29d3073bdc71ad25f2aca4c706e51f6f593b4866`.

Local gates run: `py_compile` and the bounded independent replay. No heavy
production run, workflow edit, commit, push, or dispatch was performed.
