# agent-security-attacks

Kaggle 実験リポジトリ — **AI Agent Security: Multi-Step Tool Attacks**（OpenAI 主催 Code Competition）。
ツール利用 AI エージェントの、再現可能なマルチステップ失敗を見つける攻撃アルゴリズムを開発する。

## 開発環境
- ローカル CLI / GitHub Codespaces / Claude Code on the web に対応。
- Codespaces では `.devcontainer/devcontainer.json` により Python 3.11 + kaggle CLI が用意される。

## Claude Code 連携
- [Superpowers](https://github.com/obra/Superpowers) プラグインを `.claude/settings.json` で有効化済み。
  初回セッションでワークスペース信頼の確認が一度だけ出る場合がある。
- プロジェクト固有ルールは `CLAUDE.md` を参照。

## Kaggle 運用
- データ取得・submission は `kaggle` CLI で行う。
- 認証情報（`kaggle.json`）はコミットしない（`.gitignore` 済み）。

## セットアップ（データ取得）
1. Kaggle UI でコンペのルールに同意（Join）。
   <https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks>
2. Kaggle の Settings → API → Create New API Token を発行（`username` と `key`）。
3. Claude Code on the web の環境設定で、環境シークレットを登録:
   - `KAGGLE_USERNAME`
   - `KAGGLE_KEY`
4. 環境のセットアップスクリプトに `pip install --upgrade kaggle` を追加（各セッションで CLI を用意）。
5. 新規セッション開始後、データ/SDK を取得:
   ```bash
   bash scripts/fetch_data.sh
   ```
   取得物は `data/`（`.gitignore` 済み）に展開される。
