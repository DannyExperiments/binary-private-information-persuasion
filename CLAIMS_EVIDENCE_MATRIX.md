# Claims and evidence

| Claim | Evidence |
| --- | --- |
| Payoff-threshold problem is in NP | Rational posterior vertices and a basic solution with at most one positive weight per state in the [paper](paper/manuscript.pdf). |
| Hardness with state-independent sender payoff | 3-SAT test forms, stochastic private channel, and analytic completeness and soundness. |
| No deterministic additive FPTAS unless P = NP | Inverse-polynomial threshold gap in the paper. |
| Finite replay | Exact rational channels, worked bounds and sample message policies in [replay output](verification/logs/replay.txt). |
| Partial formal verification | Seven rational inequalities in the [Lean source](formal/Q587Certificate.lean). |
