# Introduction
This is a repository for Kaggle competitions.
Please review the rules together with CLAUDE.md.

Target competition:
Competition name:


# Directory Structure

```
./                                # Primary working directory
├── myMemo.md                     # Personal notes
├── claudeSummary.md              # Aggregated notes and insights from each experiment
├── datasets/
│   └── distributed/              # Competition data download scripts
├── competition/                  # Competition details
├── tools/                        # Utility scripts
│   ├── kaggle_elapsed_time.py    # Submission status monitoring
│   └── kaggle_upload.sh          # Dataset upload/versioning script
├── survey                        # Research and investigation folder
│   ├── discussion                # Regular monitoring of Kaggle discussions
│   └── papers                    # Paper summaries
│── workspace/                    # Main development workspace
    └── expXXX                    # Experiment folders
```

# Experiment Method
Claude's experiment folders and human experiment folders are separated.
* Claude:
  * Create folders as exp(letter)(2-digit number)_(experiment name)
    workspace/expA00_baseline
  * Only change numbering for major experiment changes. Minor tweaks and parameter searches stay in the same folder.
* Human:
  * exp(3-digit number)_experiment_name

## Session Recording Rules

**Important**: Every experiment folder must have a `SESSION_NOTES.md`

### What SESSION_NOTES.md Should Include

1. **Session Info**
   - Date
   - Working folder
   - Goal

2. **Approaches Tried and Results**
   - Detailed description of each approach
   - File names used
   - Quantitative results (metrics, scores, etc.)
   - Issues and improvements

3. **File Structure**
   - List of created scripts
   - List of visualization outputs
   - List of data files

4. **Key Insights**
   - Important discoveries made during the session
   - Approaches to avoid
   - Techniques that worked

5. **Next Steps**
   - Tasks for next session
   - Ideas to explore
   - Prioritized

6. **Performance History**
   - Record of experiment names and performance changes
   - Overview of what was done and what happened

7. **Command History**
   - Major commands executed
   - For reproducibility

### Example
```
workspace/exp000_all_test/SESSION_NOTES.md
workspace/exp200_xxxxxxxx/SESSION_NOTES.md
```

### Purpose
- Resume work immediately after session interruption
- Never lose track of past attempts
- Documentation that others (or your future self) can understand

# Competition Workflow
- Always analyze the data first and proceed based on those findings
- Follow competition rules and improve performance according to the competition metric

# Training Code
1. Keep training logs. Things like learning curves. Structure it cleanly like this:
```
./exp000_all_test
├── SESSION_NOTES.md
├── results/
│   └── exp001_xxxx/
├── dataset/
│   └── v001_xxxx/
├── src
```
2. Training must be resumable from checkpoints. The PC may stop mid-training.
3. Use AMP for training.

# Survey Folder

## Discussion Folder
Keep scraping results organized in the folder for regular monitoring. Summarize what new information appeared in diffs separately.

### Discussion Collection Workflow

#### 1. Initial Setup
```bash
# Install Playwright
pip install playwright beautifulsoup4 lxml
playwright install chromium

# Create directories
mkdir -p survey/discussion
cd survey/discussion
```

#### 2. Get Discussion List

**Script**: `scrape_with_playwright.py`

```python
# Scrape discussion page using Playwright
# - Get HTML after JavaScript execution with headless browser
# - Extract discussion titles and URLs
# - Save to discussions_playwright.json
```

**Run**:
```bash
python scrape_with_playwright.py
```

#### 3. Get Detailed Info (Comment Count, etc.)

**Script**: `scrape_discussion_details.py`

```python
# Visit each discussion page
# - Get comment count
# - Get view count, vote count (when available)
# - Save to discussion_snapshot_YYYYMMDD_detailed.json
```

**Run**:
```bash
python scrape_discussion_details.py
```

#### 4. Snapshot Management

**File Structure**:
- `discussion_snapshot_YYYYMMDD.json` - Basic info snapshot
- `discussion_snapshot_YYYYMMDD_detailed.json` - Detailed info with comment counts
- `kaggle_discussions_organized.md` - Organized summary
- `discussion_activity_summary.md` - Activity analysis report
- `README.md` - Snapshot history and guide

#### 5. Diff Check (Next Run)

```bash
# Get new snapshot
python scrape_with_playwright.py
python scrape_discussion_details.py

# Check diffs (manual or scripted)
# - New topics
# - Increase in comment count
# - Changes in last updated timestamp
```

#### 6. Recommended Schedule

**Frequency**: 1-2 times per week
**Timing**: More frequent early in competition, weekly later on

**Checkpoints**:
- Check official announcements
- Important updates like data patches
- Discussions about evaluation metrics
- Shared effective solutions

### Notes

1. **Kaggle API Limitations**
   - Official Kaggle API has no discussion retrieval feature
   - Dynamic scraping with Playwright is required

2. **Scraping Etiquette**
   - 2-3 second wait between requests
   - Run in headless mode
   - Avoid excessive access

### MCP Tool Usage (Recommended)

**MCP (Model Context Protocol)** tools can simplify execution when available:

#### Check MCP Availability
```bash
# Check MCP tools
env | grep -i mcp
which mcp
```

#### Web Fetching with MCP
MCP tools may include `mcp__web_fetch` and `mcp__web_search`, potentially with fewer limitations than WebFetch.

**Available MCP Tool Examples**:
- `mcp__web_fetch` - Fetch webpage HTML
- `mcp__web_search` - Web search
- `mcp__browser` - Browser operations

**Usage**:
```
Tell Claude Code:
"Use MCP tools to fetch the Kaggle discussion page"
```

#### MCP vs Playwright Comparison

| Method | Pros | Cons |
|--------|------|------|
| **MCP** | - No setup needed<br>- Integration with Claude Code<br>- More concise | - Environment dependent<br>- Tools may be limited |
| **Playwright** | - Reliable<br>- Fine-grained control<br>- Versatile | - Setup required<br>- Environment setup needed |

**Recommended Approach**:
1. First check MCP tool availability
2. Fall back to Playwright if MCP unavailable
3. Try both and choose the more effective one

## Papers Folder
Summarize paper contents.

### Research Workflow

1. **Search Related Papers**
   - Search past competitions and related research via WebSearch
   - Retrieve papers from arXiv, Google Scholar, etc.

2. **Create Paper Summaries**
   - Summarize in `mabe_related_research.md`
   - Record methods, datasets, metrics, results

3. **Organize by Category**
   - Dataset papers
   - Method papers
   - Benchmark papers
   - Tools/Libraries

## Competition Folder
Summarize basic competition information.

### Information to Collect

1. **overview.md** - Competition overview
   - Background & purpose
   - Data format
   - Evaluation metric
   - Key challenges
   - Recommended approaches

2. **Data Sources**
   - Analysis of train.csv, test.csv
   - Understanding Parquet file structure
   - Metadata review

---

# Design Intent: Why These Rules

This section provides **judgment guidelines**, not step-by-step procedures.
For procedures, refer to Skills and Readme.md.

## Intent of "Safe + Bold"

Looking back at top Kaggle solutions, it's rare to win with incremental improvement (safe) alone. Many gold medal solutions contain a "nobody would normally do that" leap.

- Safe approaches alone lead to local optima. Encoder changes, hyperparameter tuning, augmentation additions... these are necessary but alone will plateau
- Bold alone is gambling. You need a solid baseline to properly measure bold ideas
- **By always presenting both, you separate "what to do now" from "what's worth trying"**
- Bold ideas are expected to fail. If 1 out of 10 hits, that's a huge jump
- Typical bold ideas: cross-domain transfer (NLP→CV, audio→time series), problem reframing (segmentation→detection), non-obvious external data usage
- The more you think "that would never work," the more likely no other participants have tried it

## Intent of Fold Design

How you split folds determines CV reliability. **If CV isn't reliable, every experiment decision is flawed.**

- Random KFold assumes "data is completely i.i.d." In real Kaggle data, this assumption rarely holds
- Group leakage (same patient/image/session split across train/val) inflates CV unfairly. Discovering this only on LB is too late
- Time series leakage (predicting past with future info) is even worse. Requires explicit prevention with Purged KFold etc.
- **Time spent on initial fold design determines the value of all subsequent experiments**
- Large variance in fold scores likely means you're missing a group structure in the data
- Weak CV/LB correlation means fold design doesn't reflect the real test distribution

## Intent of Preprocessing

- Normalizing with train statistics only prevents leakage. Within folds, likewise don't use val fold info for train normalization
- Starting with weak augmentation verifies the model's raw learning ability first. Strong augmentation is a symptomatic fix for overfitting that can mask root causes (insufficient data/model capacity)
- **Always judge augmentation effects quantitatively by CV. Don't add something because it "seems useful"**

## Intent of Evaluation Metrics

- Accurately reproducing the competition metric is fundamental. Default parameters in sklearn etc. often don't match the competition (average specification, thresholds, weighting, etc.)
- When loss and metric differ (e.g., BCELoss for training, F1 for evaluation), the optimal solution may diverge. Be aware of this gap and consider threshold optimization or custom losses as needed
- **"CV improved" only holds if the metric implementation is correct**

## Intent of Submission & Ensemble

- Recording single model scores before ensembling helps understand each model's contribution. Ensembling is "combining the best models," not "mixing everything"
- Pre-submission checks seem obvious, but wasting time on submission errors from row count mismatches or column name typos is avoidable. Always check after modifying post-processing
