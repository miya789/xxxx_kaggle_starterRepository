# Kaggle Competition Experiment Template

**v2.0.1**

このリポジトリは **Kaggle コンペ用の実験管理テンプレート**です。
Claude Code を前提に、**データ取得 → EDA → 調査（論文/類似コンペ） → 実験（exp管理） → 提出**までを、再現性高く回すためのルールと作業手順をまとめています。

詳細はこの記事に記載してあります。[リンク](https://zenn.dev/sugupoko/articles/1c985219823589)

---

## 機能一覧

### 指示書・ルール
- **CLAUDE.md** — Claude Code への指示書。学習コードの鉄則、Fold設計、エラー分析、提出ワークフローなど
- **KAGGLE_DIRECTION.md** — コンペ固有の設定 + 設計意図（堅実＋爆発、Fold設計、前処理、評価指標の判断指針）

### Custom Agents（`.claude/agents/`）
| エージェント | モデル | 用途 |
|---|---|---|
| kaggle-researcher | haiku | 論文・類似コンペ解法・ディスカッション調査（低コスト） |
| data-analyst | sonnet | EDA・可視化・特徴量分析 |
| code-reviewer | sonnet | ML/DLコード品質レビュー（読み取り専用） |

### Skills（`.claude/skills/`）
| スキル | 説明 |
|---|---|
| `/survey-papers [キーワード]` | 論文・解法調査（`context: fork` でメインコンテキストを汚さない） |

### ツール（`tools/`）
| ファイル | 説明 |
|---|---|
| `kaggle_elapsed_time.py` | 提出状況の監視・経過時間計測 |
| `kaggle_upload.sh` | フォルダを Kaggle Dataset にアップロード・バージョン管理 |

### リファレンスコード（`reference/`）
- PyTorch Lightning + timm + smp ベースの **2.5Dセグメンテーションテンプレート**
- [yu4u/kaggle-czii-4th](https://github.com/yu4u/kaggle-czii-4th) ベース
- 新しい実験のベースとして活用可能

### 実験管理
- **実験フォルダ命名規則**: Claude用 `expA00_xxx`、人間用 `exp200_xxx`
- **SESSION_NOTES.md**: 各実験フォルダに必須。仮説・結果・次アクションを記録
- **日報** (`daily_reports/YYYYMMDD.md`): 全記録の中心。知見が出たら都度追記
- **提出履歴** (`submit/SUBMISSIONS.md`): 全提出のCV/LBスコア・パラメータを記録
- **claudeSummary.md**: 実験横断の知見・ベストスコア履歴を集約

### 学習コードの鉄則
- AMP (Mixed Precision) 常にON
- チェックポイント再開必須
- シード固定
- ハイパーパラメータは config 管理（ハードコーディング禁止）
- `logging` モジュールで出力（`print` 禁止）
- 全出力は `results/{experiment_name}/foldN/` に集約

---

## Quickstart

最短で「このレポでコンペを回し始める」ための手順です。

### 1) 対象コンペを確定する
* `KAGGLE_DIRECTION.md` の冒頭に **対象コンペURL** を記入

### 2) データを揃える
* プロンプト:「データセットをダウンロードしてきて。`datasets/` に保存、展開まで。再現コマンドも残して。」
* 注意：kaggle APIのセットアップは済ませておくこと。

### 4) まず全体像を掴む（EDA）
* プロンプト：「EDAして `competition/overview.md` にまとめて。データ構造、サイズ、指標、提出形式、注意点込み。」

### 5) 先行知見を集める（調査）
* プロンプト：「関連論文を探して `survey/papers/maybe_related_research.md` にまとめて。転用アイデアも。」
* プロンプト：「類似コンペを探して `competition/related_competitions.md` にまとめて。流用点/差分も。」

### 6) 実験を開始する（最初のベースライン）
* プロンプト：「`workspace/expA00_baseline` を作って最小ベースライン。`SESSION_NOTES.md` を必ず作成して記録。」

---

## リポジトリ構造

```
./
├── CLAUDE.md                         # Claude Code 指示書
├── KAGGLE_DIRECTION.md               # コンペ固有設定 + 設計意図
├── claudeSummary.md                  # 実験横断の知見集約
├── myMemo.md                         # 個人メモ
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

---

## 実験フォルダ命名規則

* **Claude用**: `workspace/exp(アルファベット)(数字2桁)_(実験名)`
  * 例: `workspace/expA00_baseline`
  * 大きく方針が変わる時だけ番号を増やす（微調整は同じexp内）
* **人間用**: `workspace/exp(数字3桁)_(実験名)`
  * 例: `workspace/exp200_try_unet`
