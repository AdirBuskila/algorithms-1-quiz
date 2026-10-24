# Build report - אלגוריתמים 1 (open engine)

- Raw exam files: **21**
- **Final questions: 233**
- Shared context blocks: **65**
- Math spans rendered (distinct): **3135**
- Guided steps: **749** {'numeric': 331, 'choice': 222, 'findbug': 50, 'text': 92, 'fillblank': 8, 'order': 46}
- Graph visualizers (graph): **0** questions, **32** steps
- includeDrafts: **False**
- **ai-draft parts stripped: 0** 
- **On hold (not in bank): 4**

  - 22A-B-Q5: no-text: the file prints only the header (15 points, bonus) and 'question + solution in Moodle'
  - 24B-B-Q2b: no-key: the question text of Q2b is missing from the booklet (p.6 shows only a stray 'A. ...' line and the empty answer box); no answer source either
  - 25A-A-Q2b: no-text: the printed input gives only S1=ebc and S2=dec; S3 is missing, so the demonstration cannot be written (the solution file only says that similar demonstrations were done in the course)
  - 25A-A-Q5c: ambiguous: the answer depends on what 'linear in the size of the graph' means for an adjacency matrix. With D, F and Pi every edge is classified in O(1), so the classification is linear in the matrix size Theta(V^2) (statement false); but listing the edges of a matrix takes Theta(V^2), not O(V+E) (statement true). No key; see docs/ASK_ADIR.md

## By kind

- computation: 90
- proof: 30
- algorithm: 78
- code: 0
- mcq: 1
- truefalse: 34

## By topic

| topic | label | n |
|---|---|---|
| `complexity_recurrence` | סיבוכיות ונוסחאות נסיגה | 19 |
| `divide_conquer` | הפרד ומשול ו-Select | 16 |
| `dp_sequences` | תכנות דינמי: סדרות ותת-סדרות | 17 |
| `dp_optimization` | תכנות דינמי: תרמיל, מסלולים ומטריצות | 32 |
| `graphs_search` | גרפים: ייצוג, BFS ו-DFS | 12 |
| `graph_proofs` | גרפים: טענות והוכחות | 11 |
| `mst` | עצים פורשים מינימליים | 16 |
| `greedy` | אלגוריתמים חמדניים | 37 |
| `huffman` | קוד הופמן | 17 |
| `randomized` | אלגוריתמים הסתברותיים | 18 |
| `kmp_strings` | מחרוזות: KMP ופונקציית רישא | 23 |
| `suffix_structures` | עצי סיפות ומערכי סיפות | 11 |
| `approximation` | אלגוריתמי קירוב | 4 |

## By exam

- SAMP-1: 15
- 22A-A: 7
- 22A-B: 6
- 22A-C: 6
- 22B-A: 10
- 22B-B: 11
- 23A-A: 11
- 23A-B: 11
- 23B-C: 8
- 24A-A: 12
- 24A-B: 12
- 24A-C: 13
- 24B-A: 12
- 24B-B: 11
- 25A-A: 12
- 25A-B: 12
- 25A-C: 8
- 25B-A: 14
- 26A-A: 13
- 26A-B: 12
- 26B-A: 17

## Warnings

- 24A-B-Q3c: confidence low
- 24A-B-Q4c: confidence low
