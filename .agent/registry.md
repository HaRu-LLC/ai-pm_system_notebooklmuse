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
- (準備中)

### meta/
*テンプレ抽出・Skill生成等のメタ作業*
- **skills-creator** - 最高品質のSkillを設計・生成するメタスキル
- **template-miner** - 過去資料からテンプレ・スタイルガイド・チェックリストを抽出

---

## 更新履歴

| 日付 | 更新内容 |
|------|----------|
| 2025-12-28 | **skills-creator** 追加（メタSkill: Skill生成の専門家） |
| 2025-12-28 | 優先度「高」の3 Skills（template-miner, doc-from-examples, privacy-email-review）を作成 |
| 2025-12-28 | 初期作成。Workflows対応表を定義。 |
