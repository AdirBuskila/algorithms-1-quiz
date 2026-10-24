import json, pathlib
RAW = pathlib.Path(__file__).resolve().parents[2] / 'raw'


def A(ans=None, agrees=True, note="", flags=None, steps="all steps agree"):
    d = {"agrees": agrees, "confident": True, "transcriptionIssues": "", "stepsVerdict": steps, "note": note}
    if ans is not None:
        d["answer"] = ans
    if flags:
        d["flags"] = flags
    return d


POS = "positional citation"
v = {}
v['22A-A'] = {"derivation": "Blind: Q1 LCS3 DP (brute-forced on 300 random triples); Q2 A periodic iff A occurs >=3 times in A*A (all binary strings n<=12 vs pi-method and brute force); Q3 Monte Carlo evaluate P,G at random t, Horner O(n), k rounds; Q4 greedy from A_m downward, max element < previous (2000 random vs brute force, example 35); Q5 enumerated all 27 outputs of the 2-approx on the 11-edge graph: c and e are reachable, a/b/f/d not.",
 "answers": {
  "1": A(note="LCS3 recurrence correct; abcab/bcbab/cabba=3 confirmed"),
  "2": A(note="t>=3 threshold correct incl. n=1; counts 5 and 2 confirmed"),
  "3a": A(note="Algorithm sound. One-round error can be n/(n+1) (difference has degree <=n), so k must be about n; solution leaves k free. Step 1 answer 3 confirmed.", flags=["note: 'בדוגמה הקודמת' in step 2 explain refers to the previous step by position"]),
  "3b": A(note="Theta(kn) matches lecturer"),
  "4a": A(note="greedy = brute force on 2000 random inputs; TEMPMAX=17, sum 35, [4,5],[1,3],[2] -> 0 confirmed"),
  "4b": A(note="exchange argument valid (A_m is the last array so the swap keeps strict increase); findbug index 2 is the only changed line"),
  "5": A(ans="e", note="Exhaustive enumeration of all 27 possible outputs: e and c are both reachable (e.g. (1,9),(6,5),(3,8) and (4,9),(1,6),(3,8)); a (2 and 7 need 6), b (not a cover, edge 5-8 uncovered), f (0 needs 9) unreachable; d false. acceptedIds [e,c] correct; graph image matches page 4 (11 edges). The page marks e only.")}}
v['22A-B'] = {"derivation": "Blind: Q1 min-cut DP C(i)=min C(j)+T(j+1,i) (brute force 300 random); Q2a majority on slope classes / SELECT n/2; Q2b SELECT at ceil(n/3), ceil(2n/3) (verified for all n<400 with ceilings; floor fails for small n); Q3 complement P (a<->b) then KMP (2000 random vs brute force); Q4 Huffman merge cost (29 for 4,3,2,6, equals brute force over all merge orders). Typo 'P=p_1..p_n' on page 3 is p_n in the source; p_m in the item is right (m=|P|).",
 "answers": {
  "1": A(note="agree; C(4)=2, C(6)=2 confirmed"),
  "2a": A(agrees=False, note="Algorithm and steps correct (max-on-line=3 < 3.06 confirmed). Divergences: (1) points: the part carries 25 but the source gives 25 for the whole 2-part question (same for Q4); (2) the point (0,0) lies on every line and 0/0 is undefined: plain slope-majority is wrong on 199 of 6000 random inputs that include the origin; official ignores it, item says nothing; (3) step-2 explain 'מתאים לסעיף אחר' cites a sub-part by position.", flags=[POS, "points double-count", "origin point unhandled (official gap, add a note)"]),
  "2b": A(agrees=False, note="Algorithm correct; steps (17, 4, positions n/3 and 2n/3 with ceil) confirmed. Divergences: points 25 again (should split Q2's 25); rubric[0] 'כמו בסעיף הקודם' and pitfall 3 'מהסעיף הקודם' cite a sub-part by position.", flags=[POS, "points double-count"]),
  "3": A(note="P' = swap a<->b, KMP on T and P', Theta(n). Text, solution, steps and rubric are consistent about the swap; P=aabab -> bbaba, count 2 for T=abbaabba confirmed; p_m vs p_n typo handled correctly."),
  "4a": A(agrees=False, note="Official Huffman pseudocode and numbers (29, 15, 38/34/31) confirmed; bugIndex 4 correct. Divergences: points 25 for a part of a 25-point question; rubric[4] and pitfall 3 say the result is the total merge cost, but the official pseudocode returns EXTRACT-MIN(Q), the root node (f = total rope length, not the cost), so the pitfall would penalize the official solution; add a note that the cost is the sum of internal f values.", flags=["points double-count", "rubric/pitfall vs official return"]),
  "4b": A(agrees=False, note="Proof and steps confirmed (B(T)=47, B(T')=39, diff 8; findbug index 2). Divergence: points 25 for a part of a 25-point question."),
  "5": {"agrees": False, "confident": True, "transcriptionIssues": "", "note": "held: the page prints only the header (15-pt bonus, 'question + solution in Moodle'); nothing to verify; the hold is correct"}}}
v['22A-C'] = {"derivation": "Blind: Q1 F(i)=1+min F(i-j^2) (BFS check N<200); Q2 pi(S#S^R) last value (exhaustive n<=7, random to 11; aabaac -> 5); Q3a sort and pair neighbours (500 random vs all pairings; 5,1,4,2,8,3 -> 14); Q4 Select at multiples of ceil(n/2), ceil(n/3) + count (40000 random vs brute force); Q5 redraw edges read from page 22: 15 edges, OPT=4, all 17 possible outputs have size 6 or 8.",
 "answers": {
  "1": A(note="standard recurrence, F(12)=3, F(13)=2, greedy gives 4. Labelled student-solution although the stored formula is the standard one (docstring says so)."),
  "2": A(agrees=False, note="Algorithm, numeric steps (5, 3, 5) and sizes confirmed. Divergence: step[1] prompt says 'המחרוזת שבסעיף הקודם' (cites the previous step by position; breaks if steps are reordered).", flags=[POS]),
  "3a": A(note="agree"),
  "3b": A(note="exchange argument valid; findbug index 3 is the only changed line; saving 2=min(5,9)-3 confirmed. Rubric split 10/15 (a/b) is reasonable."),
  "4": A(note="candidate algorithm matches brute force on 40000 random arrays incl. NIL cases; step answers 5 and 3 confirmed; at most 5 Select calls"),
  "5": A(note="Redraw matches the page-22 figure: edges ab ah af hg gf bi ih id bc cd de gd dj jf fe (15), same as the student's E' list. After (a,b),(h,g),(i,d),(f,e): E' sizes 10,6,2,0 and C sizes 2,4,6,8; OPT=4 (unique cover {b,d,f,h}). Steps fix the edge order. Text only, no crop, no name/ID in the raw JSON.")}}
v['SAMP-1'] = {"derivation": "Blind: Q1 LPS DP (brute force 500 random; BARCAR=3, longest are RAR, ARA, RCR, ACA); Q2 T2 in T1*T1 (all binary pairs n<=8); Q3 Freivalds, worst-case error exactly 1/2 (D with one nonzero entry); Q4a brute force over the printed circle data: with r5=2 the maximum is 3 with exactly {c1,c2,c5} and {c1,c2,c7} (intervals strictly disjoint); with r5=4 only {c1,c2,c7}; the printed {c1,c3,c7},{c1,c3,c6} are not disjoint (c1,c3 overlap); Q5 trie of the six suffixes: 21 non-root nodes, 6 leaves, 3 root children.",
 "answers": {
  "1a": A(note="agree; P(1,4)=1, P(2,6)=3"),
  "1b": A(note="agree; findbug index 1 is the only changed line. Minor: source mixes m (length) and n in 's_1=s_n', carried as is."),
  "1c": A(note="Theta(n^2) time and space confirmed. Rubric split 12/8/5 reasonable."),
  "2a": A(note="KMP(T1*T1,T2); count 4 confirmed (k=n allowed)"),
  "2b": A(note="agree (explanation is the official one, slightly garbled about the empty suffix)"),
  "2c": A(note="Theta(n); minor inconsistency: step 2 explain says input size 3n, solution says 2n (both linear)"),
  "3a": A(note="naive Theta(n^1.5) in input size n=k^2, 1000 mults for 10x10"),
  "3b": A(agrees=False, note="Freivalds correct, but 'טועה בהסתברות שקטנה מ-50%' is not strictly true: worst-case error is exactly 1/2 (the item's own 3d step 1 gives 4 of 8 liars). Should read 'לכל היותר 1/2'; rubric[3] repeats 'קטנה מ-1/2'."),
  "3c": A(note="Theta(n), 300 mults confirmed"),
  "3d": A(agrees=False, note="Proof (flip a fixed bit j with d_ij!=0, injective) is right but concludes 'קטנה מ-1/2' while it proves <=1/2; step 1 of the item shows exactly 1/2. Claim should be 'לכל היותר 1/2'."),
  "4a": A(agrees=False, note="Answer confirmed by brute force: exactly {c1,c2,c5} and {c1,c2,c7} (max 3), not unique; the correction note is visible. Divergences: (1) no visible note on the printed typos (n=6 with seven circles; c5 printed with r_4, value 2 read as r5=2; with r=4 {c1,c2,c5} would NOT be disjoint, so the reading matters); they are only in the generator docstring and the context shows the text verbatim; (2) the picture is a rough sketch, right-hand circles do not match the numbers (largest reaches x~9.5, c6 would reach 12); (3) the solution text cites 'מסעיף ב'' and 'בסעיפים ג'-ד'' by position.", flags=["add visible note n=6/r_4/sketch", POS]),
  "4b": A(agrees=False, note="Algorithm (sort by right end, remove left<=right) gives {c1,c2,c5}; second pick c2 confirmed. Divergence: step 3 explain claims that with '<' 'בדוגמה' the answer exceeds the optimum (נבדק), but on the printed example '<' also returns [c1,c2,c5]; true only on a tangent example that is not given."),
  "4c": A(agrees=False, note="Exchange argument valid; findbug index 2 is the only changed line; step answer 2 confirmed. Divergence: pitfall[1] 'שמוכח בסעיף הבא' cites a sub-part by position.", flags=[POS]),
  "4d": A(note="agree; 5 circles remain after c1, max 2 in the sub-problem"),
  "5": A(note="Image (slide, six-suffix trie) checked: 21 non-root nodes, 6 leaves, 3 root children. The image carries the lecturer slide footer (Moshe Lewenstein, Bar-Ilan): attribution note only. Rubric split 5/7/3 fine.")}}
for c, d in v.items():
    (RAW / f"_verify_{c}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
