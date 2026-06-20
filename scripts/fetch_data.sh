#!/usr/bin/env bash
# Kaggle コンペ「AI Agent Security - Multi-Step Tool Attacks」のデータ/SDK 取得。
#
# 前提:
#   1. Kaggle UI でコンペのルールに同意済み（Join）
#   2. kaggle CLI 導入済み（pip install --upgrade kaggle）
#   3. 環境シークレットに KAGGLE_USERNAME / KAGGLE_KEY が設定済み
#
# 取得物は data/ 配下（.gitignore 済み）に展開する。コミットしない。
set -euo pipefail

COMP="ai-agent-security-multi-step-tool-attacks"
DEST="data/${COMP}"

if ! command -v kaggle >/dev/null 2>&1; then
  echo "ERROR: kaggle CLI が見つかりません。'pip install --upgrade kaggle' を実行してください。" >&2
  exit 1
fi

if [[ -z "${KAGGLE_USERNAME:-}" || -z "${KAGGLE_KEY:-}" ]]; then
  echo "ERROR: KAGGLE_USERNAME / KAGGLE_KEY が未設定です。環境シークレットに設定してください。" >&2
  exit 1
fi

mkdir -p "${DEST}"
echo "Downloading competition files into ${DEST} ..."
kaggle competitions download -c "${COMP}" -p "${DEST}"

echo "Unzipping ..."
(
  cd "${DEST}"
  for z in *.zip; do
    [[ -e "$z" ]] || continue
    unzip -o "$z" && rm -f "$z"
  done
)

echo "Done. Files under ${DEST}:"
ls -la "${DEST}"
