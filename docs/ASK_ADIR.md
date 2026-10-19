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
- Status: hold

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
- Status: hold

### 22A-C Q3b, Q4, Q5 - no key in the student paper
- Page: 16 (Q3b), 20 (Q4), 22 (Q5)
- Question: Q3b proof marked not proven (-10); Q4 student test uses == instead of "at least"; Q5 table incomplete (3/15) and the graph cannot be cropped from a student page.
- Needed: route to the solver; Q5 needs the graph redrawn as new art.
- Status: hold

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
- Status: note only; the whole sitting is held no-key

### 26A-B, 26B-A, 25A-C - no answer source
- Question: all items held "no-key" for the solver. 26B-A is the new choose-2-of-3 form (Q3 and Q4 parts, items per part). Reference facts (not an official key) are printed by tools/verify/26B-A/checks.py.
- Status: hold (no-key)

<!-- Entry format:
### <exam code> Q<number> - <short title>
- Path: <absolute file path>
- Page: <page number>
- Question: <what is unclear or missing>
- Needed: <what Adir must provide or decide>
- Status: hold
-->

## Resolved
