# Task948 -- bounded paper audit of Sol163's next-root decision

Read mail163, reply162 sections0/5/19, Tasks944/945/947 and reply944.
Independently audit the fixed44 primal-packet algebra against v541 and the
retained complete-P1/Conn assumptions. Read v542/v543/v546/v547/v548 as
needed for the rank bound and alternative oracle; no historical numerical
re-audit is requested.

Answer concretely:

- Is the packet independent of lambda with exactly the declared source?
- What is a rigorously justified bound on NEW successful appends from the
  saved rank1356 state? Separate the conservative176 list bound, the effect
  of already included seed30/34 if their packet bytes match, the ambient
  physical bound, and any sharper bound actually justified by v546.
- Explain why sets of nonzero root seeds need not decrease monotonically,
  and why ROOT_SEEDS_ZERO for one current lambda does not prove all root
  vectors lie in the state nor full-image nonmembership.
- State exact conditions for switching to a newly authenticated dual orbit
  or the v548/v543 cochain criterion. Identify any mathematical gap that
  must block packet execution (do not invent optional prerequisites).
- Audit M3-1's DERIVED option by writing its short implication precisely.

Write ONLY `sol/luna_reply_948_r07_packet_bounds_audit.md`, using F# findings.
No implementation, numerical execution, network, credentials, git, or
further agents. Existing numerical receipts remain cited premises; do not
declare external cross-checked grading. Root owns the final decision.
