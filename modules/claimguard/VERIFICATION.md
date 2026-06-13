# Verification status

This library was extracted from a working Android/Kotlin engine whose verification
tests pass. Because this sandbox has **no Kotlin compiler and no network**, the Gradle
build was not executed here. Instead, the **ported logic** was verified empirically with
a reference harness (`VERIFICATION_harness.py`) that reproduces the original engine's
test vectors (from `Tier0Gse85047ReplayV30392Test`):

| Behavior | Original test | Result |
|----------|---------------|--------|
| Tier-0 blocks COMPUTATIONAL_KILL / SURVIVING_COMPUTATIONAL | tier0Blocks… | PASS |
| Tier-1 blocks kill, allows lab-upgrade | (matrix) | PASS |
| Tier-2 allows kill | (matrix) | PASS |
| transform hash changes when declared genes change | transformContractHash… | PASS |
| transform hash stable under gene reorder (canonical) | — (added) | PASS |
| tier classification 0/1/2 from signals | bridgeKeepsSelectedMatrix… | PASS |
| selected-matrix kill → BLOCKED, no promotion | bridgeKeepsSelectedMatrix… | PASS |
| CD276 rewrite (adapter preset) | sanitizerRewritesCd276… | PASS |
| kill downgraded below Tier-2 / preserved at Tier-2 | sanitizerBlocks… | PASS |

Run it:

```bash
python3 VERIFICATION_harness.py
```

To confirm the Kotlin itself in your environment:

```bash
./gradlew :claimguard-core:test
```

The harness verifies the **algorithm**; the Gradle run verifies the **Kotlin
compilation**. Both should be green before tagging a release.
