# claimguard-core

An independent, verifiable **claim-verification layer** for AI-generated research hypotheses.

> AI proposes. Evidence disposes.

Hypothesis generation is getting cheap (Google Co-Scientist and others). Hypothesis
*discipline* is becoming the bottleneck: which proposed mechanism actually deserves a
dataset, and which deserves the lab? `claimguard-core` is the layer that sits **between
a generator and the lab** and answers that — with a receipt anyone can check.

It does **not** generate hypotheses, and it is **independent of whatever produced the
claim**. That independence is the point: a generator grading its own output is not
credible; an external, open, versioned engine that says "not supported at this tier,
here's why" is.

This is **research-use only**. It makes no clinical, causal, or therapeutic claims, and
it never emits "proof".

---

## What it does

Given a run (a proposed hypothesis + a claimed result + your dataset/reproducibility
signals), it returns a receipt whose **enforced verdict can never exceed the
verification tier**, plus a firewall report that flags any surface that overclaims.

### The three-tier contract (the governing fence)

```
Tier-0 proves replayability, not source truth.
Tier-1 proves source extraction, not biological truth.
Tier-2 is required before any computational evidence claim.
```

| Tier | Proves | Allowed verdicts |
|------|--------|------------------|
| Tier-0 | deterministic slice replay only | Inconclusive only |
| Tier-1 | source-certified extraction | + Lab-Upgrade (exploratory) |
| Tier-2 | + full mapping audit + independent replication | + Killed / Survived |

This matrix is enforced **in code** (`VerificationTierVerdictPolicy`), not in prose. A
Tier-0 run cannot emit a kill, even if asked.

### Anti-cherry-picking

The slice's feature set, sample rule, covariates, and model formula are hashed into a
single `transform_contract_sha256` **before** the verdict is read. Change the declared
genes and the hash changes; reorder them and it doesn't. Selection-after-result is
detectable.

---

## The ten classes

| Class | Role |
|-------|------|
| `EvidenceVerificationTier` | classifies a run into Tier-0/1/2 |
| `VerificationTierVerdictPolicy` | the mechanical fence: tier → allowed verdict |
| `EvidenceClaimLevel` | claim level, kept separate from reproducibility tier |
| `HypothesisProvenanceContract` | hashes the hypothesis + records its source (e.g. which LLM) |
| `SliceSelectionContract` | records why this slice exists + redistribution gate |
| `TransformContractHash` | the anti-cherry-picking contract hash |
| `VerificationReceiptBridge` | assembles the full receipt |
| `GlobalClaimSanitizer` | the claim firewall over all output surfaces |
| `ClaimRewriteRule` | configurable, tier-gated rewrites (domain rules live here) |
| `EngineIdentity` | injectable runtime identity (App vs CLI/CI receipts kept honest) |

`ClaimGuard` is a one-call facade over the bridge + sanitizer.

---

## Usage

```kotlin
import io.claimguard.core.*
import org.json.JSONObject
import org.json.JSONArray

val run = JSONObject()
    .put("hypothesis_contract", JSONObject()
        .put("hypothesisId", "MICA_LOWNK_PFS")
        .put("hypothesisText", "MICA-high + low NK effector predicts worse PFS independent of MYCN")
        .put("declaredGenes", JSONArray(listOf("MICA", "NKG7", "GZMB", "MYCN")))
        .put("covariates", JSONArray(listOf("MYCN")))
        .put("outcome", "PFS")
        .put("dataset", "GSE85047")
        .put("locked", true)
        .put("source", JSONObject()        // provenance: which generator proposed it
            .put("system", "Google Co-Scientist")
            .put("captured_at", "2026-06-10T16:40:00Z")))
    .put("prior_receipt", JSONObject().put("verdict", "COMPUTATIONAL_KILL"))
    // no source_certification / mapping / replication signals -> stays Tier-0

val result = ClaimGuard.assess(run, EngineIdentity(host = RuntimeHost.CLI))

result.verificationTier   // TIER0_SLICE_REPRODUCIBLE_REVIEW_ONLY
result.enforcedVerdict    // BLOCKED_COMPUTATIONAL_CLAIM_REQUIRES_TIER2
result.promotionAllowed   // false
result.overclaiming       // false (no surface leaked a kill)
```

Run a whole batch of Co-Scientist proposals through it unfiltered and publish the
distribution (how many killed / inconclusive / lab-upgrade) — that batch is itself an
unbiased calibration board.

---

## Domain adapters

The core mentions no disease. Anything specific (CD276, GSE85047, GPL5175, MYCN) lives
in an adapter. See `adapters/neuroblastoma/NeuroblastomaAdapter.kt`, where the CD276
"computational null → selected-matrix null-like; official kill blocked" rewrite that the
original engine hardwired is now a single portable `ClaimRewriteRule` preset.

---

## Build & test

```bash
./gradlew :claimguard-core:test
```

Pure Kotlin/JVM + `org.json` only. No Android, no network.

> Note on verification: the porting was logic-verified with a reference harness
> (`VERIFICATION.md`) reproducing the original engine's test vectors. Compile/run the
> Gradle tests in your environment to confirm against your toolchain.

## License

Apache-2.0 (recommended for the core).
