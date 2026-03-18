# Kaggle Competition Workspace

このリポジトリはKaggleコンペ用の実験管理テンプレートです。
**判断に迷ったら `KAGGLE_DIRECTION.md` の設計意図を確認すること。**

## アイデア提案の原則（堅実＋爆発）

**アプローチやアイデアを提案するときは、必ず「堅実案」と「爆発案」の両方を出すこと。**

- **堅実案**: 既知の手法、定石、段階的改善。確実にスコアが上がる見込みがあるもの
- **爆発案**: 常識外れ、異分野からの転用、誰もやらなそうなアプローチ。失敗リスクは高いが当たれば大きいもの

例:
```
堅実: encoder を efficientnet_b0 → b4 に変更（+0.5%程度の改善見込み）
爆発: セグメンテーションを捨てて物体検出で解く / 全く別のモダリティの事前学習済みモデルを転用
```

局所解に陥らないために、爆発案は「それは普通やらないだろう」くらいがちょうどいい。

## 基本ルール

- 実験は `workspace/` 以下で行う
- Claude用: `expA00_baseline` (アルファベット+数字2桁)、人間用: `exp200_name` (数字3桁)
- 各実験フォルダには必ず `SESSION_NOTES.md` を作成する
- 大きく方針が変わる時だけ新しいexp番号にする。微調整は同じフォルダ内で
- 結果・知見・戦略はすべて日報 `daily_reports/YYYYMMDD.md` に集約する（個別planファイルは作らない）

## 学習コードの鉄則

- **AMP (Mixed Precision) は常にON** (`precision: 16-mixed`)
- **チェックポイント再開は必須** (`save_last=True` + `ckpt_path`)
- **シード固定** (`pl.seed_everything(seed, workers=True)`)
- ハイパーパラメータはすべてconfigで管理（ハードコーディング禁止）
- **ログはPythonの `logging` モジュールで出力する**（`print`禁止）
  - コンソール（INFO）とファイル（DEBUG）の両方に出力する
  - ログファイルは `results/{experiment_name}/foldN/` にタイムスタンプ付きで保存する
  - フォーマット: `%(asctime)s | %(levelname)s | %(message)s`
- **全出力は `results/{experiment_name}/foldN/` に集約する**
  - best_model, checkpoint, log, training_log.json, **config.yaml** を全て同一ディレクトリに保存する
  - **config.yamlは学習開始時に自動コピーされる**（再現性のため）
  - `experiment.name` をconfigに定義し、パラメータ変更時は名前を変える
  - 同名の実験ディレクトリが存在する場合は `_001`, `_002` とナンバリングして上書きしない
- 実行は `run.sh` 経由で行う（各実験フォルダに `run.sh` を作成し、学習・推論はすべてこのスクリプト経由）
- **日報 `daily_reports/YYYYMMDD.md` がすべての記録の中心**
  - 1日1ファイル。戦略・ロードマップ・知見・実験結果をすべてここに書く
  - **知見が出たら都度追記する**（学習完了、エラー発見、スコア変化など、待たずに即記録）
  - 実験結果（CVスコア等）は数値で明記する
  - 過去分は編集せず履歴として保持
  - **セッション開始時に最新の日報を読んで状況を把握する**
  - テンプレート:
    ```markdown
    # 日報 YYYY-MM-DD

    ## コンペ情報
    - **コンペ**: コンペ名
    - **締切**: YYYY-MM-DD（残りN日）
    - **評価指標**:
    - **LB状況**:

    ## 今日やったこと
    ### 1. ...

    ## 数値まとめ
    | 実験 | データ量 | CV | LB | 状態 |
    |------|---------|-----|-----|------|

    ## 戦略・ロードマップ

    ## 判断・知見
    <!-- 今日得られた重要な判断や知見 -->

    ## データ在庫
    <!-- 利用可能なデータソースの整理 -->

    ## 次にやること
    - [ ] TODO
    ```

## Fold設計（最重要）

**安易にランダムKFoldにしない。データの性質を先に確認する。**

- 時系列 → TimeSeriesSplit
- グループ構造あり → GroupKFold
- クラス不均衡 → StratifiedKFold
- グループ+不均衡 → StratifiedGroupKFold
- fold設計の理由と各foldの分布はSESSION_NOTES.mdに記録する
- CV/LBの相関を確認し、相関が弱ければfold設計を見直す

**fold割り当ての永続化（`workspace/fold/`）:**
- fold割り当ては `workspace/fold/{version}/folds.csv` に保存し、全実験で共有する
- `generate_folds.py` で生成。バージョン管理付き
- 前処理やデータを変更した場合は新バージョンを作る。古いバージョンは削除しない
- config.yamlの `cv.folds_csv` で使用バージョンを指定する
- 設計意図・切り方の詳細は `workspace/fold/README.md` に記載

## 提出ノートブック（`submit/`）

提出用ノートブックは `submit/` 以下で管理する。

- **命名**: `v001_説明`, `v002_説明`, ... の連番形式
- **構成**:
  ```
  submit/v001_baseline/
  ├── notebook.py          # 推論スクリプト（自己完結）
  └── model/               # 学習済みモデル一式をコピー
      ├── model.safetensors
      ├── config.json
      └── ...
  ```
- **notebook.py のルール**:
  - 前処理・後処理をファイル内に自己完結させる（外部モジュールに依存しない）
  - Kaggle環境とローカル環境を自動判別してパスを切り替える
  - 推論パラメータをファイル冒頭の定数で管理
  - submission.csvの検証（行数一致、NaNなし）を必ず行う
- **モデル**: `workspace/` の学習結果から `best_model/` をコピーする
- **出典記録**: notebook.py冒頭のdocstringに `Source: workspace/expXXX/.../best_model/` とコピー元パス・CVスコアを明記する
- **ローカルテスト**: 必ずローカルでsubmission.csv生成まで動作確認してからKaggleに提出
- **gitには `notebook.py` のみコミット**（model/は.gitignoreまたは手動除外。サイズが大きいため）
- **アップロード**: Kaggle Datasetへのアップロードはユーザーが手動で行う（Claudeは実行しない）
- **提出履歴**: `submit/SUBMISSIONS.md` に全提出を記録する。実験フォルダ、モデル元パス、fold定義、学習データ、学習/推論パラメータ、前処理、CV/LBスコアを必ず記載

## エラー分析の原則（スコアの前に出力を見ろ）

**スコアを上げようとする前に、まず出力を観察して「何が悪いか」を特定する。**

- 実験後は必ず prediction vs ground truth を目視確認する（最低20件）
- エラーの種類を分類し、パターンを把握する（分類はタスク依存。事前にリスト化せず、出力から帰納的に発見する）
- エラーの種類に応じた対策を打つ（前処理・後処理・推論戦略・学習データ・モデル変更）
- スコアという数字だけ見てパラメータを変える盲目的な探索をしない

順序: 出力を読む → 何が悪いか特定 → 原因に対処する → スコアで検証

## 前処理・評価

- 正規化はtrainデータの統計量で計算する（testの情報を使わない）
- コンペの評価指標を正確に再現する（既存実装のパラメータも確認）
- Augmentationはまず弱めで、過学習が確認されてから強める
- single modelのCV/LBを記録してからアンサンブルする
- 提出前に行数・カラム名・欠損値・値の範囲を確認する

## リファレンスコード

- `reference/` に2.5Dセグメンテーションのテンプレートコード（PyTorch Lightning + timm + smp）がある
- 新しい実験のベースとして活用すること
- 詳細は `reference/README.md` を参照

## 利用可能なSkills

- `/survey-papers [キーワード]` - 論文・解法調査（メインコンテキストを汚さず別コンテキストで実行）

## Custom Agents

状況に応じて自動的にサブエージェントに委譲される。並列実行も可能。

- **kaggle-researcher** (haiku) - 論文・類似コンペ解法・ディスカッション調査。コスト節約のためhaiku使用
- **data-analyst** (sonnet) - EDA・可視化・特徴量分析。データの全体像把握に
- **code-reviewer** (sonnet) - ML/DLコード品質レビュー。読み取り専用で安全
