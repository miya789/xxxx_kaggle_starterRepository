---
name: survey-papers
description: Search for papers and similar competition solutions related to the competition, and summarize in survey/papers/. Use during the research phase or when exploring new approaches.
argument-hint: "[search keywords or leave blank to auto-search from competition name]"
context: fork
agent: Explore
---

# Paper & Solution Research Skill

## Steps

1. **Determine Search Query**:
   - Use `$ARGUMENTS` if provided
   - Otherwise extract related keywords from the competition name in `KAGGLE_DIRECTION.md`

2. **Research via WebSearch** (search the following in parallel):
   - Related papers on arXiv
   - Top solutions from similar past Kaggle competitions
   - Related methods on Papers With Code
   - Related implementations on GitHub

3. **Summarize each paper/solution**:
   - Title, authors, URL
   - Method summary (3-5 lines)
   - Model/architecture used
   - Dataset & evaluation metrics
   - Key results
   - Applicability to this competition

4. **Save results**:
   - Append to `survey/papers/maybe_related_research.md`
   - Organize by category (dataset papers, method papers, benchmark papers, tools/libraries)

5. **Propose transfer ideas**:
   - List methods potentially applicable to this competition
   - Evaluate implementation difficulty and expected impact
