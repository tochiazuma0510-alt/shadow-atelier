To: Commander / Luna

Please run `sol/luna_task_162_r07_normalizer_bfs_and_residual.md` now and reply
to `sol/luna_reply_162_r07_normalizer_bfs_and_residual.md`.  The construction
is reduced to one 504-state local BFS for the inversion involution
`s0=[1,7,6,9,8,3,2,5,4]`, followed by
`ftilde07=chi07*[u^-4,S]`.  No GHA is needed for the BFS.  If the subsequent
residual stage crosses the pinned resource threshold, return a checkpoint so
the parent broker can dispatch the heavy continuation on GHA.
