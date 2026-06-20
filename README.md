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
> 注: Claude Code on the web には専用シークレット保管庫が無く、環境変数はその環境を
> 編集できる人に見える。Kaggle トークンは随時ローテート可能な前提で扱う。

1. Kaggle UI でコンペのルールに同意（Join）。
   <https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks>
2. Kaggle の Settings → API → **Generate New Token** を発行（`KGAT_...` 形式）。
3. Claude Code on the web の環境設定（クラウドアイコン → 環境 → 設定）で:
   - **Network access** → **Custom** →「Also include default list...」にチェック →
     Allowed domains に `*.kaggle.com` を追加（`storage.googleapis.com` は既定で許可済み）。
   - **Environment variables**（`.env` 形式・引用符なし）に
     `KAGGLE_API_TOKEN=KGAT_...` を登録。
   - **Setup script** に `pip install --upgrade kaggle` を追加。
4. 設定を保存し、**新規セッションを開始**（ネットワーク/環境変数は再起動で反映）。
5. データ/SDK を取得:
   ```bash
   bash scripts/fetch_data.sh
   ```
   取得物は `data/`（`.gitignore` 済み）に展開される。
