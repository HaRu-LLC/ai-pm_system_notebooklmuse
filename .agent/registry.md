# Skills Registry

Skills と Workflows の対応表。どのSkillがどのWorkflowに対応するかを管理する。

---

## Skills ⇄ Workflows 対応表

| Skill名 | 関連Workflow | 配置先 |
|---------|--------------|--------|
| skills-creator | （メタSkill） | `.agent/skills/meta/skills-creator/` |
| template-miner | `/05_meta_bootstrap_template_library` | `.agent/skills/meta/template-miner/` |
| doc-from-examples | `/05_meta_doc_from_examples` | `.agent/skills/business/doc-from-examples/` |
| privacy-email-review | `/05_meta_privacy_review_email` | `.agent/skills/pm/privacy-email-review/` |
| diagnostic-site-no-logs | `/05_meta_build_diagnostic_site` | `.agent/skills/engineering/diagnostic-site/` |
| sim-game-builder-email | `/05_meta_build_simulation_game` | `.agent/skills/engineering/simulation-game/` |
| codex-cli | （外部ツール連携） | `.agent/skills/engineering/codex-cli/` |
| docx | （Anthropic公式） | `.agent/skills/engineering/docx/` |
| pdf | （Anthropic公式） | `.agent/skills/engineering/pdf/` |
| pptx | （Anthropic公式） | `.agent/skills/engineering/pptx/` |
| xlsx | （Anthropic公式） | `.agent/skills/engineering/xlsx/` |
| playwright | （コミュニティ） | `.agent/skills/engineering/playwright/` |
| test-driven-development | （superpowers） | `.agent/skills/engineering/test-driven-development/` |
| systematic-debugging | （superpowers） | `.agent/skills/engineering/systematic-debugging/` |
| verification-before-completion | （superpowers） | `.agent/skills/engineering/verification-before-completion/` |
| writing-plans | （superpowers） | `.agent/skills/engineering/writing-plans/` |
| executing-plans | （superpowers） | `.agent/skills/engineering/executing-plans/` |
| subagent-driven-development | （superpowers） | `.agent/skills/engineering/subagent-driven-development/` |
| dispatching-parallel-agents | （superpowers） | `.agent/skills/engineering/dispatching-parallel-agents/` |
| using-git-worktrees | （superpowers） | `.agent/skills/engineering/using-git-worktrees/` |
| brainstorming | （superpowers） | `.agent/skills/engineering/brainstorming/` |
| workflow-designer | （メタSkill） | `.agent/skills/meta/workflow-designer/` |

---

## カテゴリ別 Skills一覧

### business/
*ビジネス文書作成・経営支援*
- **doc-from-examples** - 過去資料の「型」に合わせて新規ビジネス文書を作成

### pm/
*プロジェクト管理・リスク管理*
- **privacy-email-review** - メール取得を伴う機能のプライバシー設計レビュー

### engineering/
*開発・実装支援*

**ドキュメント処理（Anthropic公式）**
- **docx** - Word文書(.docx)の読み取り、作成、編集、トラッキング変更
- **pdf** - PDFファイルの読み取り、作成、マージ、注釈、OCR
- **pptx** - PowerPointプレゼンテーションの読み取り、作成、編集
- **xlsx** - Excelスプレッドシートの読み取り、作成、数式、チャート

**AI連携**
- **codex-cli** - OpenAI Codex CLIを起動・操作、マルチエージェント連携、ゴール達成までの自動ループ

**ブラウザ自動化**
- **playwright** - Playwrightによるブラウザ自動化、Webテスト、スクリーンショット

**開発プラクティス（superpowers）**
- **test-driven-development** - テスト駆動開発（TDD）の厳格な実践
- **systematic-debugging** - 体系的デバッグ、根本原因調査を先に行う
- **verification-before-completion** - 完了前検証、証拠なしに完了を主張しない

**計画＆実行（superpowers）**
- **writing-plans** - マルチステップ開発タスク向け実装計画作成
- **executing-plans** - 事前作成された計画の構造化実行
- **subagent-driven-development** - タスクごとにサブエージェント派遣、2段階レビュー
- **dispatching-parallel-agents** - 独立問題に複数エージェント同時割り当て
- **using-git-worktrees** - Git Worktreeで分離ワークスペース、並列ブランチ作業
- **brainstorming** - アイデアを仕様に変換する協調的デザインプロセス

### meta/
*テンプレ抽出・Skill生成等のメタ作業*
- **skills-creator** - 最高品質のSkillを設計・生成するメタスキル
- **template-miner** - 過去資料からテンプレ・スタイルガイド・チェックリストを抽出
- **workflow-designer** - 複数Skillsを連動させたワークフローを設計、チェックポイント付き

---

## 更新履歴

| 日付 | 更新内容 |
|------|----------|
| 2026-01-14 | **workflow-designer** 追加（meta: ワークフロー設計メタスキル） |
| 2026-01-14 | awesome-claude-skillsから14スキル追加（docx, pdf, pptx, xlsx, playwright, TDD, debugging等） |
| 2026-01-14 | **codex-cli** 追加（engineering: Codex CLI連携、オーケストレーターループ対応） |
| 2025-12-28 | **skills-creator** 追加（メタSkill: Skill生成の専門家） |
| 2025-12-28 | 優先度「高」の3 Skills（template-miner, doc-from-examples, privacy-email-review）を作成 |
| 2025-12-28 | 初期作成。Workflows対応表を定義。 |
