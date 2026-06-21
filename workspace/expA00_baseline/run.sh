#!/bin/bash
# ローカル評価・提出物生成を一発で回すスクリプト
# 使い方:
#   bash run.sh                              # デフォルト（heuristic vs random, 20 games）
#   bash run.sh --opponents random --games 50
#   引数は evaluate.py に渡る（--policy / --opponents / --games / --seed / --run-name）
set -e

cd "$(dirname "$0")"

bash run_local.sh "$@"
