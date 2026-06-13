import hashlib, re

def sha256(t): return hashlib.sha256(t.encode("utf-8")).hexdigest()
def canonical(arr): return "|".join(sorted([x.strip() for x in arr if x.strip()]))

TIER0="TIER0_SLICE_REPRODUCIBLE_REVIEW_ONLY"; TIER1="TIER1_SOURCE_CERTIFIED_REVIEW_GRADE"; TIER2="TIER2_REPLICATION_CERTIFIED_COMPUTATIONAL_EVIDENCE"
BLOCKED="BLOCKED_COMPUTATIONAL_CLAIM_REQUIRES_TIER2"

def is_comp_claim(v):
    v=v.upper()
    return ("COMPUTATIONAL_KILL" in v or "COMPUTATIONAL_SURVIVE" in v or "SURVIVING_COMPUTATIONAL" in v
            or v=="COMPUTATIONAL_SUPPORT_CANDIDATE" or v.startswith("KILLED_") or v=="KILLED"
            or v.startswith("SURVIVED_") or v=="SURVIVED")

def enforce(tier, verdict):
    comp=is_comp_claim(verdict); lab=("LAB_UPGRADE" in verdict.upper() or "LAB-UPGRADE" in verdict.upper())
    allowed = True if tier==TIER2 else (not comp) if tier==TIER1 else (not comp and not lab)
    return allowed, (verdict if allowed and verdict else ("INCONCLUSIVE" if allowed else BLOCKED)) if allowed else BLOCKED

def classify(source_certified, mapping_pass, replication):
    if source_certified and mapping_pass and replication: return TIER2
    if source_certified: return TIER1
    return TIER0

def transform_hash(hyp_text, genes, sample_rule, covs, model_formula, code_id):
    parts = {
        "hypothesis_text_hash": sha256(hyp_text),
        "declared_gene_set_hash": sha256(canonical(genes)),
        "sample_inclusion_rule_hash": sha256(sample_rule),
        "covariate_rule_hash": sha256(canonical(covs)),
        "model_formula_hash": sha256(model_formula),
        "transform_code_hash": sha256(code_id),
    }
    canon="\n".join(f"{k}={v}" for k,v in parts.items())
    return sha256(canon)

# default tier-gated rewrite (domain-agnostic)
def sanitize(text, tier):
    if tier==TIER2: return text
    for pat in ["COMPUTATIONAL_KILL","COMPUTATIONAL_SURVIVE","SURVIVING_COMPUTATIONAL"]:
        text=re.sub(pat, BLOCKED, text, flags=re.IGNORECASE)
    return text

# neuroblastoma adapter rewrite (preset, NOT in core)
CD276_CANON="CD276 selected-matrix null-like signal; official computational kill blocked pending full GPL5175 mapping."
def sanitize_neuroblastoma(text, tier):
    text=re.sub(r"CD276 computational null", CD276_CANON, text, flags=re.IGNORECASE)
    return sanitize(text, tier)

fails=0
def check(name, cond):
    global fails
    print(("PASS" if cond else "FAIL")+": "+name)
    if not cond: fails+=1

# T1: Tier-0 blocks kill + surviving-computational  (mirror of tier0BlocksComputationalKillAndSurviveLanguage)
a,v=enforce(TIER0,"COMPUTATIONAL_KILL"); check("Tier0 blocks COMPUTATIONAL_KILL", (a==False and v==BLOCKED))
a,v=enforce(TIER0,"SURVIVING_COMPUTATIONAL_EVIDENCE"); check("Tier0 blocks SURVIVING_COMPUTATIONAL", (a==False and v==BLOCKED))
# Tier-1 blocks computational claim but allows lab-upgrade; Tier-2 allows kill
a,v=enforce(TIER1,"COMPUTATIONAL_KILL"); check("Tier1 blocks computational kill", (a==False and v==BLOCKED))
a,v=enforce(TIER1,"LAB_UPGRADE_CANDIDATE"); check("Tier1 allows lab-upgrade", (a==True and v=="LAB_UPGRADE_CANDIDATE"))
a,v=enforce(TIER2,"COMPUTATIONAL_KILL"); check("Tier2 allows kill", (a==True and v=="COMPUTATIONAL_KILL"))
a,v=enforce(TIER0,"INCONCLUSIVE"); check("Tier0 allows inconclusive", (a==True and v=="INCONCLUSIVE"))

# T2: transform hash changes when declared genes change (mirror of transformContractHashChangesWhenDeclaredGenesChange)
base=transform_hash("topic",["CD276","GZMB","MYCN","NKG7"],"sampleRule",["MYCN"],"modelFormula","code")
alt =transform_hash("topic",["CD276","GZMB","MYCN","NKG7","ODC1"],"sampleRule",["MYCN"],"modelFormula","code")
check("transform hash changes when genes change", base!=alt)
# and is stable under gene reordering (canonical)
reordered=transform_hash("topic",["NKG7","MYCN","GZMB","CD276"],"sampleRule",["MYCN"],"modelFormula","code")
check("transform hash stable under gene reorder", base==reordered)

# T3: tier classification (mirror of bridgeKeepsSelectedMatrixAsTier0ReviewOnly path)
check("no source cert -> Tier0", classify(False,False,False)==TIER0)
check("source cert only -> Tier1", classify(True,False,False)==TIER1)
check("full chain -> Tier2", classify(True,True,True)==TIER2)
# bridge: selected matrix (Tier0) with requested COMPUTATIONAL_KILL -> enforced BLOCKED, promotion not allowed
tier=classify(False,False,False); a,v=enforce(tier,"COMPUTATIONAL_KILL")
check("selected-matrix kill -> BLOCKED + no promotion", (v==BLOCKED and (tier==TIER2)==False))

# T4: sanitizer (mirror of sanitizerRewritesCd276 + downgrade below Tier-2)
out=sanitize_neuroblastoma("CD276 computational null from selected matrix", TIER0)
check("CD276 rewrite contains null-like", "selected-matrix null-like signal" in out)
check("CD276 rewrite contains kill blocked", "official computational kill blocked" in out)
out2=sanitize("verdict=COMPUTATIONAL_KILL", TIER0); check("kill downgraded below Tier2", BLOCKED in out2 and "COMPUTATIONAL_KILL" not in out2)
out3=sanitize("verdict=COMPUTATIONAL_KILL", TIER2); check("kill preserved at Tier2", "COMPUTATIONAL_KILL" in out3)

print("\n=== %s ===" % ("ALL LOGIC CHECKS PASS" if fails==0 else f"{fails} FAILURE(S)"))
