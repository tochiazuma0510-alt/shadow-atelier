# Luna task 273 - task232 SELFTEST envelope seal v1

Role: bounded one-owner implementation repair. Read current task232 files and
GHA run 33148048757. Do not run Python, Node, GAP, git, GHA, or network. Edit
only producer, driver pin, and existing task232 Luna reply.

Run 33148048757 emitted the exact producer SELFTEST success terminal after all
57 producer mutations were rejected. The independent checker then stopped at
`producer self digest`: production envelopes are sealed by `envelope`, but
the plain dictionary returned by `selftest` has no `self_digest_sha256`.

Seal the complete SELFTEST receipt with the same canonical digest convention:
compute the digest over every receipt field before adding the digest field.
Do not change the SELFTEST contents, mutation roster/evidence, checker rule,
production envelope, any roof/projection/K mathematics, caps, terminals, or
conclusions. Refresh driver/reply pins and report UNEXECUTED. Parent Sol will
rerun the full serial GHA SELFTEST.

A4 remains 0/3 because actual task198 K has not been run.
