# ASK_ADIR - algorithms-1

Open questions for Adir. One entry per item; the orchestrator moves it to Resolved when answered.

## Open

### 26A-A Q3 - printed sub-points sum to 20, not 25
- Path: 26A-A exam booklet (course sources, 2026 folder)
- Page: 9-10 (Q3a and Q3b print 10 points each)
- Question: every other question is 25 points (cover says 25 per question, cap 115). Q3 prints 10 + 10. Transcribed as printed.
- Needed: nothing blocking; confirm if the grading key counts Q3 as 20 or 25 when the points matter.
- Status: note only (not held)

### 26A-A Q3a - tie in the Huffman run
- Page: solution p.6
- Question: weights 15 (leaf b) and 15 (internal node) tie. The official tree merges 10 with leaf b; merging 10 with the internal 15 gives a different code with the same cost (219). The official answer is kept.
- Needed: a step-author rule that either code is accepted when a student gives it.
- Status: note only (not held)

### 22A-A Q5 - two options fit the approximation algorithm
- Page: 4 (the unnumbered graph box after Q4)
- Question: options c and e are both possible outputs of the vertex-cover 2-approximation (checked by enumeration); the page shows only e pre-marked.
- Needed: which options the original quiz accepted (or accept both c and e).
- Status: resolved by solver, pending refuter (2026-10-24; the stem asks which set CAN be an output, so both are accepted: correctId e, acceptedIds [e, c]; checks in tools/verify/22A-A/solve_22A-A.py)

### 22A-B Q5 - bonus question text missing
- Page: 5
- Question: the file prints only the header (15 points, bonus) and "question + solution in Moodle". No text.
- Needed: the question and solution, if wanted; otherwise leave out.
- Status: hold

### 22A-B Q1, Q4 - headers say 3 parts, one or two printed
- Page: 1 and 3
- Question: Q1 and Q4 headers say "3 סעיפים"; the file prints one request (Q1) and two (Q4 a,b).
- Needed: nothing blocking.
- Status: note only (not held)

### SAMP-1 Q4a - official sets are not disjoint
- Page: solution p.8
- Question: official answer lists {c1,c3,c7} and {c1,c3,c6}; with the printed data c1 meets c3 and c3 meets c6. The example also says n=6 but lists 7 circles, and c5 is printed with r_4. "Not unique" is true (e.g. {c1,c2,c5}, {c1,c2,c7}).
- Needed: the intended circle data, or accept the corrected answer.
- Status: resolved by solver, pending refuter (2026-10-24; typo ruling: verdict "not unique" kept, sets corrected to {c1,c2,c5} and {c1,c2,c7}, the only optimal sets; tools/verify/SAMP-1/solve_SAMP-1.py)

### 22A-C Q3b, Q4, Q5 - no key in the student paper
- Page: 16 (Q3b), 20 (Q4), 22 (Q5)
- Question: Q3b proof marked not proven (-10); Q4 student test uses == instead of "at least"; Q5 table incomplete (3/15) and the graph cannot be cropped from a student page.
- Needed: route to the solver; Q5 needs the graph redrawn as new art.
- Status: resolved by solver, pending refuter (2026-10-24; Q5 graph redrawn from data by tools/verify/22A-C/draw_graph.py -> images/exams/22A-C-Q5-graph.png, no crop; checks in tools/verify/22A-C/solve_22A-C.py)

### 25B-A Q1a - official total weight is 13, the printed weights give 11
- Page: solution p.2
- Question: the counterexample (DFS from c) lists tree edges cb and ab with total 13; with w(ab)=7 and w(cb)=4 the total is 11. Verdict (false, MST = 9) is unaffected. Official text kept, flagged inside the solution.
- Needed: nothing blocking; the step-author should use 11 (or avoid the number).
- Status: note only (not held)

### 25B-A Q3a(ii) - d = 5 or 6 also give an optimal-cost code
- Page: solution p.8
- Question: official answer d = 7 (the only frequency for which the Huffman algorithm itself builds this tree). d = 5 or 6 give the same shape with optimal cost, but the algorithm would not build it. Official answer kept.
- Needed: step-author rule: accept only 7.
- Status: note only (not held)

### 25A-C Q2a - points not printed
- Page: 2
- Question: Q2a has no printed points (Q2b prints 10) and the Q2 header has no total. Omitted, not inferred.
- Status: note only; the sitting (all 8 items) is resolved by solver, pending refuter

### 26A-B, 26B-A, 25A-C - no answer source
- Question: all items held "no-key" for the solver. 26B-A is the new choose-2-of-3 form (Q3 and Q4 parts, items per part). Reference facts (not an official key) are printed by tools/verify/26B-A/checks.py.
- 26A-B (12 items) and 25A-C (8 items): resolved by solver, pending refuter (2026-10-24). Checks: tools/verify/26A-B/solve_all.py, tools/verify/25A-C/solve_all.py. 25A-C transcription re-verified against the page renders (Q1a answer skeleton has four cases, not three; fixed). 25A-C Q3 assumes distinct values (as in the example).
- 26B-A (16 of 17 items): resolved by solver, pending refuter (2026-10-24). Transcription re-verified against renders of all 20 pages (texts, tables, BFS example, the 14 edges of the Q4b graph): no changes needed. Checks: tools/verify/26B-A/solve_q1_q2.py, solve_q3.py, solve_q4.py. Q4a(ii) asks for "the" frequency of e, but both 6 and 7 fit the given code and sibling rule; the solution gives both.
- Status: 26A-B, 25A-C and 26B-A resolved by solver, pending refuter, except 26B-A Q4b(ii) (item Q4d), below.

### 26B-A Q4b(ii) (item Q4d) - Prim order is not unique
- Page: p.15
- Question: with X=3 (the answer of Q4b(i)), Prim from C meets two ties: C-B and D-F weigh 3, and D-E and F-H weigh 4. Four edge orders and two different MSTs (weight 18) are valid; the exam states no tie-breaking rule. A solved draft listing the branches is in the generator.
- Needed: accept every valid order, or name a tie-breaking rule.
- Status: hold (two-answer)

### 25A-A Q1c - official answer returns the average, not the r-th smallest
- Page: solution p.1
- Question: the official answer Return(mid(A[1..r],B[1..r])) gives the average of the two middle elements of the 2r chosen elements (A=[1,2], B=[3,4], r=2 gives 2.5; the r-th smallest is 2).
- Needed: a correct solution (looking only at the first r elements of each array is right).
- Status: resolved by solver, pending refuter (2026-10-24; typo ruling, binary search over A[1..r], B[1..r]; tools/verify/25A-A/solve_25A-A.py)

### 25A-A Q2a - printed recurrence is wrong or undefined
- Page: solution p.2
- Question: rows 3 and 8 of the official piecewise recurrence write T(i,j-1,k) (k should drop to k-1) and no row covers S1[i]!=S3[k] with S2[j]!=S3[k]. Checked against brute force (tools/verify/25A-A/checks.py).
- Needed: a corrected recurrence for the solver; Q2b (the worked example) is held with it.
- Status: resolved by solver, pending refuter (2026-10-24; typo ruling, k-1 in both rows plus "false otherwise"). Q2b stays held: its printed input gives only S1=ebc and S2=dec, S3 is missing.
- 25A-A bonus c stays held: "linear in the size of the graph" with an adjacency matrix is ambiguous (with D, F, Pi the classification is O(V^2) = linear in the matrix, statement false; but not O(V+E), statement true). Bonus a (false) and b (true) are solved. Needed: Adir's reading.

### 25A-A Q4a - the official note is not an algorithm and is unsafe
- Page: solution p.4
- Question: the solution gives only a remark (compute the KMP pi array, return its maximum). max(pi) differs from pi[n-1] (abcabcd). The question examples also conflict with its wording (aaaa gives 4, aabcdaabc gives 4).
- Needed: a solver answer (pi[n-1], proper-border reading); confirm which reading the lecturer intends.
- Status: resolved by solver, pending refuter (2026-10-24; typo ruling: return pi[n] instead of max(pi); both official readings stated)

### 24B-B Q2b - question text missing from the booklet
- Page: 6
- Question: the page shows only a stray "A. ..." line and the empty answer box for part b. No answer source either.
- Needed: the printed wording of part b (10 points inferred from 25 - 15), or drop it.
- Status: hold

### 25A-B, 24B-B - no answer source
- Question: no key for any item of either sitting; all items are held no-key for the solver. The 24B-B cover says "מועד א" (14.8.24), treated as 24B-B per GATE1.
- Status: hold (no-key)
- 25A-B (2026-10-24): all 12 items resolved by solver, pending refuter (solutionSource "solved", checks in tools/verify/25A-B/solve_25AB.py). Bonus item b (adjacency list, number of neighbours in O(1)): ruled by orchestrator, pending refuter: false under the course's (CLRS) linked-list convention, O(deg v); the solution opens with a visible "הערה:" that the claim becomes true if each list also stores its length. Adir may still override the convention.
- 24B-B: resolved by solver, pending refuter (11 of 12 items solved; Q2b stays held, see above). Assumptions stated in the solutions: Q1b no self-loops (with loops the claim fails), Q2a every coded letter occurs (c=0 would add (0,4)). Bonus: the tree forces T = ?ATATAT with ? not A/T (read R); the answer ATAT does not depend on it.

### 23A-A - no answer source
- Question: no key for any item; all 11 items were held no-key.
- Status: resolved by solver, pending refuter (all 11 solved; checks in tools/verify/23A-A/solve_all.py).

### 22B-A Q2 - official code wrong for even n
- Page: solution p.4
- Question: the official pseudo-code tests CountL+CountM > n/2 but the task needs >= ceil(n/2). For even n it misses pairs whose total is exactly n/2 (A=[1,2,3,4]: true answer True, code False). Brute force over all arrays n<=8 confirms the idea is right with >= ceil(n/2).
- Needed: decide whether to ship the official text with the note, or let the solver write a corrected version.
- Status: resolved by solver, pending refuter (2026-10-24; typo ruling). New finding: the idea is also incomplete for even n, testing only Select(A,(n+1)/2) misses A=[1,2,3,4,5,5] (pair 4,5 has 3 = n/2 occurrences, the median 3 is in no such pair; the earlier brute force used values 1..4 only). The fix also tests the element at position n/2+1; brute force over all arrays n<=8 with values 1..n (tools/verify/22B-A/solve_22B-A.py).

### 22B-B Q2a, Q2b - official split algorithm wrong when k > n-k
- Page: 6, 8
- Question: the official code always splits into the k smallest vs the n-k largest, optimal only when k <= n-k (A=[13,5,7], k=2: best 15, code 1); in the else branch the sizes of B and C are also swapped. Q2b analyses that code, so it is held with it.
- Needed: the solver may write the correct algorithm (the bigger group takes the large values).
- Status: resolved by solver, pending refuter (2026-10-24; typo ruling: the else branch pivots on Select(A,n,n-k); Q2b adds the correctness argument; tools/verify/22B-B/solve_22B-B.py)

### 22B-B Q4c - two wrong cells in the official table
- Page: 13
- Question: row 2 / column 6 is printed 2 (recurrence gives 1) and row 6 / column 8 is printed 1 (recurrence gives 0). Final answer 3 is right.
- Needed: confirm shipping with the corrected cells.
- Status: resolved by solver, pending refuter (2026-10-24; typo ruling, the two cells corrected)

### 22B-B Q1a, Q1c, Q1d - weak official solutions (notes only)
- Page: 2, 4, 5
- Question: Q1a counterexample has the same tree shape (mirror only); Q1c suffix tree lacks the leaf of the suffix "$"; Q1d never states the answer ABABA. Shipped with a visible transcription note.
- Status: note only (not held)

### 23A-B Q4a, Q4b - official side errors (notes only)
- Page: solution Q4.1, Q4.2
- Question: Q4a option 1 uses f=(13,0,0,0) although f>0 is required (option 2 is valid); Q4b says the drawn graph has 6 spanning trees, it has 8 (still >= 5). Shipped with visible notes. Q4 has only two parts, so no Q4.3 exists (the triage note was a misreading).
- Status: note only (not held)

<!-- Entry format:
### <exam code> Q<number> - <short title>
- Path: <absolute file path>
- Page: <page number>
- Question: <what is unclear or missing>
- Needed: <what Adir must provide or decide>
- Status: hold
-->

### 24A-A Q1a, Q1b, Q4c, Q5 - no key in the partial solution file
- Page: solution p.1 (Q1 "solution in Moodle"), p.4 (Q4c time only, bonus "see homework")
- Question: Q1a/b (walk / shortest path through z) and the bonus have no answer in the file; Q4c states only the time O(n^2), not the space. Held as no-key for the solver. Q4 in the solution file is a variant (example table, width sorted descending, different parts b/c); Q4a is kept with confidence med, Q4b (space O(n) from "one-dimensional array") with med.
- Needed: route to the solver; optionally the Moodle model solution for Q1.
- Status: resolved by solver, pending refuter (2026-10-24; all four solved, bonus false; tools/verify/24A-A/solve_24A-A.py)

### 24A-B Q3c, Q4c - weak key in the student paper
- Page: 18 (Q3c), 24 (Q4c)
- Question: Q3c handwriting is partly unreadable (idea kept: independent repeated runs) and its printed hypothesis reads "at least 1/4"; Q4c (listing the combinations) was graded full for time and space O(m*n), although the output itself can be exponentially large.
- Needed: refuter decision; confidence is low on both.
- Status: note only (not held)

### 24A-B Q4a/Q4b - grader deductions
- Page: 20 (Q4a: -3 for missing edge cases), 22 (Q4b: space O(m*n) got half credit)
- Question: Q4a is shipped with the full base cases, Q4b with O(n*m) time and O(m) space (two rows) as "solved".
- Needed: nothing blocking.
- Status: note only (not held)

### 23B-C Q1-Q4 - blank booklet, no key
- Page: 3-20
- Question: no solution source exists for this sitting; all 8 items are held with reason no-key. Q1 and Q3 print one point total per question (30 each), not per part.
- Needed: route to the solver.
- Status: resolved by solver, pending refuter (2026-10-24; all 8 items solved, checks in tools/verify/23B-C/solve_23BC.py). Q4 assumes c and d occur in S (frequency >= 1); with frequency 0 allowed, (0,7) would be one extra pair, noted in the solution.

## Resolved
