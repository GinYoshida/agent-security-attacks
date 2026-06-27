# 共通ルール（個人プリファレンス）

<!--
claude-md リポジトリを claude-shared として submodule 参照し、単一の真実源とする。
別環境/別セッションで submodule 未取得だと下記 import は無言でスキップされるため、
.claude/settings.json の SessionStart フックで `git submodule update --init` を自動実行している。
-->
@claude-shared/CLAUDE.md

## agent-security-attacks 固有ルール

### プロジェクト概要
- Kaggle: AI Agent Security - Multi-Step Tool Attacks（OpenAI 主催 Code Competition）
- 目的: ツール利用 AI エージェントの、再現可能なマルチステップ失敗を見つける攻撃アルゴリズムの開発

### Kaggle 運用メモ
- データ取得は kaggle CLI で行う（手動 UI ダウンロードはしない）
- push 可能物（submission / kernel など）も kaggle CLI で行う
- Web UI 操作が必須の作業（同意・チーム設定など CLI 不可のもの）は私に依頼する

### Superpowers プラグイン
- Superpowers プラグインは `.claude/settings.json` の `enabledPlugins` で有効化している
- 各環境（ローカル / Codespaces / Claude Code on the web）の初回セッションで
  ワークスペース信頼の確認ダイアログが一度だけ出る場合がある（リポジトリ側では抑止不可）
