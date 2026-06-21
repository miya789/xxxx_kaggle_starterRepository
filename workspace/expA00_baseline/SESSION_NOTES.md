# SESSION_NOTES — expA00_baseline

## セッション情報
- 日付: 2026-06-21
- 作業フォルダ: workspace/expA00_baseline
- 目標: PTCG AI Battle の Phase 1 ベースライン — 合法手から常に index 0 を選ぶ first-action エージェント。クラッシュしない提出パイプラインの確立と、ローカル評価ハーネスの動作確認が目的。

## ベース
- ベース: reference_sim/ (ConnectX template) → PTCG I/F へ適応
- 親 exp（あれば）: なし（expA00 が最初）

## エージェントI/F（PTCG）

```python
def agent(obs_dict: dict) -> list[int]:
    # obs_dict: cabt エンジンが提供するゲーム状態辞書
    # return: 合法手インデックスのリスト
```

- ConnectX の `agent(observation, configuration) -> int` と**全く異なる**ことに注意
- `submit_agent.py` を `main.py` にリネームして提出

## 提出形式
```
submission.tar.gz
├── main.py      # submit_agent.py をリネーム
├── deck.csv     # 使用デッキ（60枚）
└── cg/          # cabt エンジンライブラリ（datasets/cg/ からコピー）
```

## 未確認の重要項目
- [ ] `obs_dict` のキー一覧（`availableActions` / `legalActions` どちらか）
- [ ] `evaluate.py` の ENGINE 名（現在 "cabt" — 要確認）
- [ ] cabt エンジンのビルトイン対戦相手名
- [ ] deck.csv のフォーマット（カードID の形式）
- [ ] cg/ ライブラリの配置先（`datasets/cg/` を仮定）

## ファイル構成
```
expA00_baseline/
├── agent.py           # 開発用エントリ（パッケージ import あり）
├── submit_agent.py    # 提出用（self-contained、main.py にリネームして提出）
├── evaluate.py        # ローカル評価ハーネス（CLI）
├── run_local.sh       # evaluate.py のラッパ（cwd 非依存）
├── agents/
│   ├── __init__.py
│   └── heuristic.py   # Phase 1 baseline: 常に index 0 を選択
├── opponents/
│   ├── __init__.py
│   └── v1/            # 凍結相手プール v1（まだ空）
├── requirements.txt   # kaggle-environments == 1.30.1 等
└── SESSION_NOTES.md   # このファイル
```

## 試したアプローチと結果
<!-- 実験を回したら追記 -->

| 試行 | 変更点 | ローカル勝率 (vs random) | LB μ | 備考 |
|------|--------|--------------------------|------|------|
| Phase1 | first-action baseline | - | - | SDK インストール待ち |

## 重要な知見
<!-- 学習中に得られた知見 -->

## 次のステップ
- [ ] cabt エンジン SDK をインストールして ENGINE 名・obs_dict 構造を確認
- [ ] `run_local.sh` で 1 エピソード完走テスト
- [ ] 勝率を計測（vs random、最低 20 ゲーム）
- [ ] submit/v001_expA00_baseline/ を作成して submission.tar.gz を生成
- [ ] `/submit-check` で提出物を検証してから提出

## コマンド履歴
```bash
# 評価実行
bash run_local.sh --policy heuristic --opponents random --games 20

# 提出物の作成
cd submit/v001_expA00_baseline/
tar -czvf submission.tar.gz main.py deck.csv cg/
```
