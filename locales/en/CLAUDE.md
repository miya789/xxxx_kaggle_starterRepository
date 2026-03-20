# Kaggle Competition Workspace

This repository is an experiment management template for Kaggle competitions.
**When in doubt, check the design intent in `KAGGLE_DIRECTION.md`.**

## Idea Proposal Principles (Safe + Bold)

**When proposing approaches or ideas, always present both a "safe" and a "bold" option.**

- **Safe**: Known methods, established practices, incremental improvements. Expected to reliably improve scores
- **Bold**: Unconventional, cross-domain transfers, approaches nobody would normally try. High failure risk, but huge upside if successful

Example:
```
Safe: Switch encoder from efficientnet_b0 to b4 (expected ~+0.5% improvement)
Bold: Drop segmentation entirely and solve with object detection / Transfer a pretrained model from a completely different modality
```

To avoid local optima, bold ideas should be "nobody would normally do that" level.

## Basic Rules

- Experiments go under `workspace/`
- Claude: `expA00_baseline` (letter + 2-digit number), Human: `exp200_name` (3-digit number)
- Every experiment folder must have a `SESSION_NOTES.md`
- Only increment exp numbers for major direction changes. Minor tweaks stay in the same folder
- All results, insights, and strategy go in daily reports `daily_reports/YYYYMMDD.md` (no separate plan files)

## Training Code Rules

- **AMP (Mixed Precision) always ON** (`precision: 16-mixed`)
- **Checkpoint resume is mandatory** (`save_last=True` + `ckpt_path`)
- **Seed fixed** (`pl.seed_everything(seed, workers=True)`)
- All hyperparameters managed via config (no hardcoding)
- **Use Python `logging` module for output** (`print` is prohibited)
  - Output to both console (INFO) and file (DEBUG)
  - Log files saved to `results/{experiment_name}/foldN/` with timestamps
  - Format: `%(asctime)s | %(levelname)s | %(message)s`
- **All outputs go to `results/{experiment_name}/foldN/`**
  - Save best_model, checkpoint, log, training_log.json, **config.yaml** all in the same directory
  - **config.yaml is auto-copied at training start** (for reproducibility)
  - Define `experiment.name` in config; change the name when parameters change
  - If an experiment directory with the same name exists, append `_001`, `_002` numbering (never overwrite)
- Run via `run.sh` (create `run.sh` in each experiment folder; all training/inference goes through this script)
- **Daily reports `daily_reports/YYYYMMDD.md` are the central record**
  - One file per day. Strategy, roadmap, insights, experiment results all go here
  - **Append as insights emerge** (training complete, error found, score change — write immediately, don't wait)
  - Record experiment results (CV scores etc.) with exact numbers
  - Don't edit past reports; keep them as history
  - **Read the latest daily report at session start to understand current status**
  - Template:
    ```markdown
    # Daily Report YYYY-MM-DD

    ## Competition Info
    - **Competition**: Competition name
    - **Deadline**: YYYY-MM-DD (N days remaining)
    - **Metric**:
    - **LB Status**:

    ## What was done today
    ### 1. ...

    ## Numerical Summary
    | Experiment | Data Size | CV | LB | Status |
    |------------|-----------|-----|-----|--------|

    ## Strategy & Roadmap

    ## Decisions & Insights
    <!-- Important decisions and insights from today -->

    ## Data Inventory
    <!-- Organize available data sources -->

    ## Next Steps
    - [ ] TODO
    ```

## Fold Design (Critical)

**Do not default to random KFold. Check data characteristics first.**

- Time series → TimeSeriesSplit
- Group structure → GroupKFold
- Class imbalance → StratifiedKFold
- Group + imbalance → StratifiedGroupKFold
- Record fold design rationale and per-fold distributions in SESSION_NOTES.md
- Check CV/LB correlation; if weak, revisit fold design

**Fold assignment persistence (`workspace/fold/`):**
- Save fold assignments in `workspace/fold/{version}/folds.csv`, shared across all experiments
- Generate with `generate_folds.py`. Version controlled
- Create new version when preprocessing or data changes. Never delete old versions
- Specify version in config.yaml via `cv.folds_csv`
- Document design intent and split details in `workspace/fold/README.md`

## Submission Notebooks (`submit/`)

Submission notebooks are managed under `submit/`.

- **Naming**: Sequential format `v001_description`, `v002_description`, ...
- **Structure**:
  ```
  submit/v001_baseline/
  ├── notebook.py          # Inference script (self-contained)
  └── model/               # Copy of trained model files
      ├── model.safetensors
      ├── config.json
      └── ...
  ```
- **notebook.py rules**:
  - All preprocessing/postprocessing self-contained in the file (no external module dependencies)
  - Auto-detect Kaggle vs local environment and switch paths accordingly
  - Inference parameters managed as constants at the top of the file
  - Always validate submission.csv (row count match, no NaN)
- **Models**: Copy `best_model/` from `workspace/` training results
- **Source tracking**: Include `Source: workspace/expXXX/.../best_model/` and CV score in the notebook.py docstring
- **Local test**: Always verify submission.csv generation locally before submitting to Kaggle
- **Only commit `notebook.py` to git** (model/ is .gitignored or manually excluded due to size)
- **Upload**: Upload to Kaggle Dataset is done manually by the user (Claude does not execute this)
- **Submission history**: Record all submissions in `submit/SUBMISSIONS.md`. Include experiment folder, model source path, fold definition, training data, training/inference parameters, preprocessing, CV/LB scores

## Error Analysis Principles (Look at Outputs Before Scores)

**Before trying to improve scores, first observe outputs to identify "what's wrong."**

- After each experiment, visually inspect prediction vs ground truth (at least 20 samples)
- Classify error types and identify patterns (categories are task-dependent; discover inductively from outputs, don't predefine lists)
- Apply targeted fixes based on error types (preprocessing, postprocessing, inference strategy, training data, model changes)
- Don't blindly search by tweaking parameters based on score numbers alone

Order: Read outputs → Identify what's wrong → Address the cause → Verify with scores

## Preprocessing & Evaluation

- Normalization uses statistics from train data only (never use test data info)
- Accurately reproduce the competition metric (check parameters of existing implementations)
- Start with weak augmentation; strengthen only after overfitting is confirmed
- Record single model CV/LB before ensembling
- Before submission, verify row count, column names, missing values, and value ranges

## Reference Code

- `reference/` contains a template for 2.5D segmentation (PyTorch Lightning + timm + smp)
- Use as a base for new experiments
- See `reference/README.md` for details

## Available Skills

- `/survey-papers [keyword]` - Paper/solution survey (runs in separate context without polluting main context)

## Custom Agents

Automatically delegates to subagents as needed. Parallel execution supported.

- **kaggle-researcher** (sonnet) - Paper, similar competition solution, and discussion research
- **data-analyst** (sonnet) - EDA, visualization, feature analysis. For understanding overall data picture
- **code-reviewer** (sonnet) - ML/DL code quality review. Read-only and safe
