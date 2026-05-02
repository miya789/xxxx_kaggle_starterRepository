---
name: onboard
description: Walks through the 7-item competition onboarding checklist interactively and saves it to survey/competition/overview.md. Use first when starting a new competition.
argument-hint: "[competition URL or blank to infer from KAGGLE_DIRECTION.md]"
---

# Competition Onboarding Skill

Mechanical procedure for CLAUDE.md's "Competition Onboarding Phase (Do this before writing any training code)".

## Steps

1. **Identify the input**:
   - Use `$ARGUMENTS` if it contains a competition URL
   - Otherwise infer from the "Competition name" line in `KAGGLE_DIRECTION.md`
   - WebFetch the overview / data / rules / timeline pages in parallel

2. **Fill in the 7 items** (ask the user for unknowns; mark inferences as "Inference:"):
   1. **Platform**: Kaggle / grand-challenge.org / CodaBench / custom
   2. **Task definition**: inputs, outputs, number of classes, evaluation unit (per-image / per-pixel / per-patient)
   3. **Data location**: download URLs, size, format, license, local target path
   4. **Metric**: exact definition (average / threshold / background class treatment / per-class vs micro/macro)
   5. **Submission format**: CSV / prediction-file zip / Docker container
   6. **Timeline**: validation phase / test phase / final deadline, submission quota
   7. **Rules**: team size, external data, pretrained models, commercial license

3. **Save**:
   - Create `survey/competition/overview.md` (merge with existing, never overwrite)
   - Use this template:

```markdown
# Competition Overview — <name>

Last updated: YYYY-MM-DD

## 1. Platform
- ...

## 2. Task Definition
- Input: ...
- Output: ...
- Classes: ...
- Evaluation unit: ...

## 3. Data Location
- URL: ...
- Size: ...
- Format: ...
- License: ...
- Local path: `datasets/...`

## 4. Metric
- Name: ...
- Definition: ...
- Implementation notes: ...

## 5. Submission Format
- Type: (A) CSV / (B) Prediction-file zip / (C) Docker
- Filename / naming rules: ...
- Row count / file count: ...
- Value range / dtype: ...

## 6. Timeline
- Start: ...
- Deadline: ...
- Submission quota: ...

## 7. Rules
- Team size: ...
- External data: ...
- Pretrained models: ...
- License constraints: ...

## Unknowns / Awaiting Confirmation
- [ ] ...
```

4. **Check**:
   - Confirm all 7 items are filled
   - List any unknowns under "Unknowns"
   - **Tell the user not to start implementation until all 7 are filled**

5. **Suggest next actions**:
   - Metric implementation plan (which sklearn function? custom?)
   - Fold design plan (candidate grouping keys)
   - One safe + one bold approach to consider
