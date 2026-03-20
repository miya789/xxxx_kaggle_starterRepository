# Kaggle Competition Experiment Template

**v2.1.1**

[日本語 (default)](#日本語) | [English](#english)
　
---

## English

This repository is an **experiment management template for Kaggle competitions**.
Built for Claude Code, it provides rules and workflows for the full pipeline: **data acquisition → EDA → research (papers/similar competitions) → experiments (exp management) → submission**, with high reproducibility.

### Quick Start

```bash
# 1. Fork this repository

# 2. Set language to English
./setup.sh en

# 3. Set target competition URL in KAGGLE_DIRECTION.md

# 4. Start working with Claude Code
```

### Language Setup

This template supports **Japanese** and **English**. Run the setup script to switch:

```bash
./setup.sh en   # English
./setup.sh ja   # Japanese (default)
```

This updates: `CLAUDE.md`, `KAGGLE_DIRECTION.md`, agent definitions, skill definitions, and templates.

### Features

#### Instructions & Rules
- **CLAUDE.md** — Instructions for Claude Code: training code rules, fold design, error analysis, submission workflow
- **KAGGLE_DIRECTION.md** — Competition-specific settings + design intent (safe + bold, fold design, preprocessing, metric guidelines)

#### Custom Agents (`.claude/agents/`)
| Agent | Model | Purpose |
|---|---|---|
| kaggle-researcher | sonnet | Paper, similar competition, and discussion research (low cost) |
| data-analyst | sonnet | EDA, visualization, feature analysis |
| code-reviewer | sonnet | ML/DL code quality review (read-only) |

#### Skills (`.claude/skills/`)
| Skill | Description |
|---|---|
| `/survey-papers [keyword]` | Paper/solution research (`context: fork` keeps main context clean) |

#### Tools (`tools/`)
| File | Description |
|---|---|
| `kaggle_elapsed_time.py` | Submission status monitoring & elapsed time |
| `kaggle_upload.sh` | Folder upload to Kaggle Dataset with versioning |

#### Reference Code (`reference/`)
- **2.5D segmentation template** based on PyTorch Lightning + timm + smp
- Based on [yu4u/kaggle-czii-4th](https://github.com/yu4u/kaggle-czii-4th)

#### Experiment Management
- **Folder naming**: Claude `expA00_xxx`, Human `exp200_xxx`
- **SESSION_NOTES.md**: Required in each experiment folder
- **Daily reports** (`daily_reports/YYYYMMDD.md`): Central record; append insights as they emerge
- **Submission history** (`submit/SUBMISSIONS.md`): CV/LB scores and parameters for all submissions
- **claudeSummary.md**: Cross-experiment insights and best score history

#### Training Code Rules
- AMP (Mixed Precision) always ON
- Checkpoint resume mandatory
- Seed fixed
- Hyperparameters in config (no hardcoding)
- `logging` module for output (`print` prohibited)
- All outputs to `results/{experiment_name}/foldN/`

### Repository Structure

```
./
├── CLAUDE.md                         # Claude Code instructions
├── KAGGLE_DIRECTION.md               # Competition settings + design intent
├── claudeSummary.md                  # Cross-experiment insights
├── myMemo.md                         # Personal notes
├── setup.sh                          # Language setup script
├── locales/                          # Language files
│   ├── ja/                           # Japanese
│   └── en/                           # English
├── .claude/
│   ├── agents/                       # Custom Agents (3 types)
│   └── skills/                       # Skills (/survey-papers)
├── reference/                        # Reference code (2.5D Seg)
├── tools/
│   ├── kaggle_elapsed_time.py        # Submission monitoring
│   └── kaggle_upload.sh              # Dataset upload
├── submit/
│   └── SUBMISSIONS.md                # Submission history
├── datasets/                         # Competition data
├── competition/                      # EDA & competition overview
├── survey/                           # Paper & discussion research
│   ├── discussion/
│   └── papers/
├── daily_reports/                    # Daily reports
└── workspace/                        # Experiment folders
    └── expXXX... / expA00...
```

---

## 日本語

このリポジトリは **Kaggle コンペ用の実験管理テンプレート**です。
Claude Code を前提に、**データ取得 → EDA → 調査（論文/類似コンペ） → 実験（exp管理） → 提出**までを、再現性高く回すためのルールと作業手順をまとめています。

詳細はこの記事に記載してあります。[リンク](https://zenn.dev/sugupoko/articles/1c985219823589)

### クイックスタート
1. このリポジトリをfork
2. KAGGLE_DIRECTION.md に対象コンペURLを記入
3. Claude Code で作業開始

### 機能一覧

#### 指示書・ルール
- **CLAUDE.md** — Claude Code への指示書。学習コードの鉄則、Fold設計、エラー分析、提出ワークフローなど
- **KAGGLE_DIRECTION.md** — コンペ固有の設定 + 設計意図（堅実＋爆発、Fold設計、前処理、評価指標の判断指針）

#### Custom Agents（`.claude/agents/`）
| エージェント | モデル | 用途 |
|---|---|---|
| kaggle-researcher | sonnet | 論文・類似コンペ解法・ディスカッション調査（低コスト） |
| data-analyst | sonnet | EDA・可視化・特徴量分析 |
| code-reviewer | sonnet | ML/DLコード品質レビュー（読み取り専用） |

#### Skills（`.claude/skills/`）
| スキル | 説明 |
|---|---|
| `/survey-papers [キーワード]` | 論文・解法調査（`context: fork` でメインコンテキストを汚さない） |

#### ツール（`tools/`）
| ファイル | 説明 |
|---|---|
| `kaggle_elapsed_time.py` | 提出状況の監視・経過時間計測 |
| `kaggle_upload.sh` | フォルダを Kaggle Dataset にアップロード・バージョン管理 |

#### リファレンスコード（`reference/`）
- PyTorch Lightning + timm + smp ベースの **2.5Dセグメンテーションテンプレート**
- [yu4u/kaggle-czii-4th](https://github.com/yu4u/kaggle-czii-4th) ベース

#### 実験管理
- **実験フォルダ命名規則**: Claude用 `expA00_xxx`、人間用 `exp200_xxx`
- **SESSION_NOTES.md**: 各実験フォルダに必須。仮説・結果・次アクションを記録
- **日報** (`daily_reports/YYYYMMDD.md`): 全記録の中心。知見が出たら都度追記
- **提出履歴** (`submit/SUBMISSIONS.md`): 全提出のCV/LBスコア・パラメータを記録
- **claudeSummary.md**: 実験横断の知見・ベストスコア履歴を集約

#### 学習コードの鉄則
- AMP (Mixed Precision) 常にON
- チェックポイント再開必須
- シード固定
- ハイパーパラメータは config 管理（ハードコーディング禁止）
- `logging` モジュールで出力（`print` 禁止）
- 全出力は `results/{experiment_name}/foldN/` に集約

### リポジトリ構造

```
./
├── CLAUDE.md                         # Claude Code 指示書
├── KAGGLE_DIRECTION.md               # コンペ固有設定 + 設計意図
├── claudeSummary.md                  # 実験横断の知見集約
├── myMemo.md                         # 個人メモ
├── setup.sh                          # 言語設定スクリプト
├── locales/                          # 言語ファイル
│   ├── ja/                           # 日本語
│   └── en/                           # English
├── .claude/
│   ├── agents/                       # Custom Agents (3種)
│   └── skills/                       # Skills (/survey-papers)
├── reference/                        # リファレンスコード (2.5D Seg)
├── tools/
│   ├── kaggle_elapsed_time.py        # 提出監視
│   └── kaggle_upload.sh              # Dataset アップロード
├── submit/
│   └── SUBMISSIONS.md                # 提出履歴
├── datasets/                         # コンペデータ
├── competition/                      # EDA・コンペ概要
├── survey/                           # 論文・ディスカッション調査
│   ├── discussion/
│   └── papers/
├── daily_reports/                    # 日報
└── workspace/                        # 実験フォルダ
    └── expXXX... / expA00...
```

### 実験フォルダ命名規則

* **Claude用**: `workspace/exp(アルファベット)(数字2桁)_(実験名)`
  * 例: `workspace/expA00_baseline`
  * 大きく方針が変わる時だけ番号を増やす（微調整は同じexp内）
* **人間用**: `workspace/exp(数字3桁)_(実験名)`
  * 例: `workspace/exp200_try_unet`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v2.1.1 | 2026-03-20 | Change kaggle-researcher agent from haiku to sonnet |
| v2.1.0 | 2026-03-20 | Add English language support (`locales/`, `setup.sh`), bilingual README |
| v2.0.1 | - | Initial public release with full experiment management template |
