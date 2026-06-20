#!/usr/bin/env bash
# Kaggle コンペ「AI Agent Security - Multi-Step Tool Attacks」のデータ/SDK 取得。
#
# 前提:
#   1. Kaggle UI でコンペのルールに同意済み（Join）
#   2. kaggle CLI 導入済み（pip install --upgrade kaggle）
#   3. 認証: KAGGLE_API_TOKEN=KGAT_... を設定（環境変数）。
#      互換: ~/.kaggle/access_token / kaggle.json / KAGGLE_USERNAME+KAGGLE_KEY も可。
#   4. ネットワーク許可: *.kaggle.com（www/api 両方）への egress が必要。
#      （Claude Code on the web では環境のネットワーク設定で Custom + *.kaggle.com）
#
# 取得物は data/ 配下（.gitignore 済み）に展開する。コミットしない。
set -euo pipefail

COMP="ai-agent-security-multi-step-tool-attacks"
DEST="data/${COMP}"

if ! command -v kaggle >/dev/null 2>&1; then
  echo "ERROR: kaggle CLI が見つかりません。'pip install --upgrade kaggle' を実行してください。" >&2
  exit 1
fi

have_creds=0
[[ -n "${KAGGLE_API_TOKEN:-}" ]] && have_creds=1
[[ -f "${HOME}/.kaggle/access_token" || -f "${HOME}/.kaggle/kaggle.json" ]] && have_creds=1
[[ -n "${KAGGLE_USERNAME:-}" && -n "${KAGGLE_KEY:-}" ]] && have_creds=1
if [[ "${have_creds}" -ne 1 ]]; then
  echo "ERROR: Kaggle 認証が未設定です。KAGGLE_API_TOKEN=KGAT_... を環境変数に設定してください。" >&2
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
