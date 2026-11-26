# Reproduce the checks

From the repository root run the standard-library replay and archive verifier.

```sh
python3 -I verification/src/replay.py
python3 -I scripts/verify_repository.py
```

The replay constructs private signals with exact rational probabilities, evaluates receiver incentives including sender-favorable ties, and reconstructs payoffs from the message mass vectors. It checks 64 small clause patterns and the worked pair. On the unsatisfiable instance it samples 4,225 balanced test choices and 1,024 two-message policies. The manuscript proves the bound over all schemes.

With an existing Lean 4.30.0 distribution run the partial arithmetic certificate.

```sh
lean -DwarningAsError=true formal/Q587Certificate.lean
```

[Exact replay output](verification/logs/replay.txt) · [Lean output](verification/logs/lean.txt) · [Build the manuscript](paper/BUILD.md) · [Render the example](visualization/README.md)
