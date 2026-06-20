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
