# Sol reply -- exact character-0 dual orbit closure

## Result

The one nonzero dual root from reply909 has a complete orbit of exactly 504
distinct vectors under the four Task712 adjoints.  All 504 vectors are
linearly independent over F3.  Together with the three identically zero
character orbits, this is the full initial-separator dual closure.

Both the producer-side v15 Task712 reader and its independent checker-side
reimplementation performed the same calculation:

1. authenticate the exact character-0 `B` and four `T` forward/adjoint pairs;
2. construct `q0=B_fwd^T lambda`;
3. breadth-first enumerate all four labelled monomial images, deduplicating
   only by the exact 9,072-byte packed row;
4. require one nonzero table entry at every source and destination coordinate;
5. row-reduce the 504-by-504 restriction to coordinates 0--503 over F3.

They agree on:

```text
orbit_size=504
labelled_edges=2016
queue_remaining=0
closed=true
rank_on_coordinates_0_through_503=504
pivots=0,1,...,503
pivot_list_u32le_sha256=ab653854bfb7d723efdafaad705d6ab7b88bdd865cb4b8474a5d3932f5b4f39d
sorted_packed_orbit_sha256=b651766655e28c82723b57df02858f910f37d3af1950c83df628c26da3e304dc
```

Because the restricted minor already has full row rank, the conclusion does
not depend on unexamined coordinates.  The computational consequence is
exact: the character-0 scalar orbit has 504 independent tests.  Task908 first
tests the root.  A Violation proceeds directly to materialization; a root EOF
leaves exactly 503 independent orbit rows.  There is no infinite enumeration
and no 36,288-row worst case on this separator.

```text
ACTUAL_DUAL_ORBIT_CROSS_CHECKED=yes
ACTIVE_ORBIT_SIZE=504
ACTIVE_ORBIT_RANK=504
TOTAL_NONZERO_CHARACTER_ORBITS=1
SCALAR_VALUES=NOT_RUN
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```
