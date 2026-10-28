# Literature Notes

For each paper: Problem / Method / Result / Limitation (mine or theirs).

## Paper title (year)

- Problem:
- Method:
- Result:
- Limitation:

## ApacheJIT: A Large Dataset for Just-In-Time Defect Prediction (Keshavarz & Nagappan, MSR 2022)

- Problem: JIT datasets are small, so models (especially deep ones) generalize poorly.
- Method: 106,674 commits from 14 Apache Java projects; bug-inducing commits found with a modified SZZ plus filtering; Kamei-style change metrics.
- Result: 28,239 bug-inducing (about 26%) vs 78,435 clean commits.
- Limitation: SZZ label noise (design favors false negatives), Java only, no commit text or code in the data, extrinsic bugs not handled.
