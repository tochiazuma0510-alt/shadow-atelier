# Luna task 153b — independent soundness audit of the Burau finite-fiber route

## Role

You are an independent Luna auditor.  Do not implement the producer and do not share helpers with task 153.  Read:

- `sol/luna_task_153_b5_burau_fiber.md`
- `sol/sol_reply_152_pushback.md` §§12.2–12.8
- `sol/luna_reply_152_b4_158_pentagon_semantics.md`
- the local paper `C:/Users/81905/Desktop/2607.05283v1.pdf`, especially Observation 2.1, Theorem 2.3, Proposition 6.4, Corollary 6.5, Theorem 6.6.

Report only to `sol/luna_reply_153b_burau_soundness.md`.  Do not edit code, workflows, or any other file.

## Questions to decide

1. Prove or refute the sound implication in task 153:

   For a finite Burau specialization and the combined map
   \(E:F_2\to P\times GL_4(\mathbf F_q)^5\), if the complete commutator fiber over a roof row is nonempty but has no element whose literal raw-A.18 defect is identity, then the row cannot be the reduction of any element of \(\widehat{GT}\).

   Check continuity/profinite completion, representative independence, the use of \([H,H]\) versus the image of \(\widehat F_2'\), paper/GAP opposite multiplication, and whether five component values really determine the raw defect.

2. Decide whether an explicit B4-normal NFI window or isolatedization is logically needed for this one-way A obstruction, or whether a finite quotient of the defining equations suffices.  If a window is needed, construct it exactly from the five kernels and prove its induced PB3 kernel is below the fixed roof M.

3. Decide what the 2026 Burau-faithfulness theorem actually adds.  Separate:
   - finite-specialization A semidecision;
   - discrete Brunnian detection;
   - detection in the profinite completion;
   - cofinality/compatible-lift requirements for B.
   Do not claim that discrete faithfulness alone gives profinite faithfulness.

4. Audit the terminal index-3 conclusion: explain why a zero fiber cannot be arithmetic and why one fake row forces all 648 outside rows fake under the fixed D972 dichotomy.  State every premise used.

5. Give a final verdict `SOUND`, `SOUND_WITH_REPAIRS`, or `UNSOUND`, with exact repairs if needed.  This is a paper audit only; no partial computation is an A/B result.
