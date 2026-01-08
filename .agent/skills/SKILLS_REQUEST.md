# Claude Code Skills 作成依頼書

**作成日**: 2025-12-28  
**依頼者**: AI-PM System 管理者  
**実行者**: Claude Code

---

## 1. 概要

本依頼書は、`.agent/skills/` 配下に Claude Code 用の Skills を作成するための要件を定義します。

### 前提条件
- 本リポジトリには既に `.agent/workflows/` に40個以上のワークフロー定義が存在
- Antigravity（Gemini）向けに Rules v2 と Workflows を整備済み
- Skills は Claude Code での運用を主目的とし、Antigravity とは `registry.md` で対応付け

### 期待する成果物
- `.agent/skills/<category>/<skill-name>/SKILL.md` 形式の Skill 定義ファイル
- 必要に応じて `REFERENCE.md` や関連テンプレート
- `.agent/registry.md` への登録

---

## 2. Skills 仕様

### ディレクトリ構造
```
.agent/skills/
├── business/       # ビジネス文書作成・経営支援
├── pm/             # プロジェクト管理・リスク管理
├── engineering/    # 開発・実装支援
└── meta/           # テンプレ抽出・Skill生成等のメタ作業
```

### SKILL.md フォーマット
```markdown
---
name: <skill-name>
description: <1行説明（トリガー語を含む）>
---

## 目的
<このSkillの目的>

## 入力で最初に聞くこと
- <質問1>
- <質問2>

## 手順
1. <ステップ1>
2. <ステップ2>
...

## 成果物
- <成果物1>
- <成果物2>

## 検証（完了条件）
- <条件1>
- <条件2>
```

---

## 3. 作成依頼 Skills 一覧

### 優先度：高（最初に作成）

| Skill名 | カテゴリ | 目的 | 対応Workflow |
|---------|----------|------|--------------|
| `template-miner` | meta | 過去資料からテンプレ・スタイルガイド・チェックリストを抽出 | `/05_meta_bootstrap_template_library` |
| `doc-from-examples` | business | 過去資料の型に合わせて新規ビジネス文書を作成 | `/05_meta_doc_from_examples` |
| `privacy-email-review` | pm | メール取得機能のプライバシー設計レビュー | `/05_meta_privacy_review_email` |

### 優先度：中（必要に応じて作成）

| Skill名 | カテゴリ | 目的 | 対応Workflow |
|---------|----------|------|--------------|
| `diagnostic-site` | engineering | ログ保存しない診断サイトの設計 | `/05_meta_build_diagnostic_site` |
| `sim-game-builder` | engineering | メール取得ありシミュレーションゲーム設計 | `/05_meta_build_simulation_game` |
| `proposal-writer` | business | 提案書作成支援 | `/02_aipjm_*` 系を参照 |
| `ringi-writer` | business | 稟議書作成支援 | 新規作成 |

---

## 4. 各 Skill の詳細要件

### 4.1 template-miner（最優先）

**配置先**: `.agent/skills/meta/template-miner/SKILL.md`

**トリガー語例**:
- 「テンプレを作りたい」
- 「過去資料からテンプレ抽出」
- 「スタイルガイドを作成」

**入力**:
- 過去資料 3〜10件
- 対象文書種別（提案書/稟議/議事録/PRD等）
- 読者（役員/部長/現場）

**手順**:
1. 各資料の章立てを抽出し、共通パターンを特定
2. 各章の役割（意思決定に必要な情報）を定義
3. 定型文スニペット（冒頭文、結論文、注意書き）を抽出
4. 禁止・注意表現（曖昧語、過度な断定、根拠なき数値）を抽出
5. DoDチェックリストを作成
6. 成果物を生成・保存

**成果物**:
- `STYLE_GUIDE.md`
- `TEMPLATE_<doc-type>.md`
- `CHECKLIST_<doc-type>.md`

**保存先**: `.agent/templates/docs/` または `workspace/{ProjectName}/docs/templates/`

---

### 4.2 doc-from-examples

**配置先**: `.agent/skills/business/doc-from-examples/SKILL.md`

**トリガー語例**:
- 「過去の○○と同じ形式で作って」
- 「この資料を参考に新しい文書を作成」
- 「型に合わせて提案書を書いて」

**入力**:
- 参考資料
- 新規テーマ（何を決めたいか）
- 意思決定者

**手順**:
1. 参考資料の章立て・トーンを抽出
2. 新規テーマを各章にマッピング
3. 不足情報は仮説で補完（仮説であることを明記）
4. DoDチェックを通す
5. 追加で必要な情報を質問

**成果物**:
- 新規文書（参考資料の型に準拠）
- 追加情報リスト（質問形式）

---

### 4.3 privacy-email-review

**配置先**: `.agent/skills/pm/privacy-email-review/SKILL.md`

**トリガー語例**:
- 「メール取得のレビュー」
- 「プライバシーチェック」
- 「PII設計確認」

**入力**:
- メール取得の目的
- 保存先
- 保持期間
- 削除要件

**手順（チェックリスト形式）**:
1. 目的の正当化（本当に必要か、代替はないか）
2. 同意（UI文言、通知、オプトイン、二重同意）
3. 露出経路遮断（URL、ログ、エラー、通知）
4. 保存と保護（分離保管、暗号化、アクセス制御）
5. 保持と削除（保持期間、削除導線、削除手順）
6. 実装チェック（POST、ログマスク、DBスキーマ）

**成果物**:
- メール取得設計メモ
- 実装上の注意点リスト

---

## 5. 作成手順

1. **Workflowの読み込み**: 対応する `.agent/workflows/05_meta_*.md` を読み込む
2. **SKILL.md生成**: 上記フォーマットに従ってSKILL.mdを作成
3. **配置**: `.agent/skills/<category>/<skill-name>/SKILL.md` に保存
4. **registry.md更新**: `.agent/registry.md` に対応を追記
5. **動作確認**: Skillが正しくトリガーされるか確認

---

## 6. 注意事項

### 既存資産との整合性
- 既存の `.agent/workflows/` はそのまま維持
- Skills は Workflows を補完・参照する形で設計
- 重複する手順定義は Workflows を正本とし、Skills から参照

### Rules v2 との整合性
以下のルールを Skills 内でも遵守すること：
- 出力構造：要約→提案→次の質問
- 文書品質：根拠レベル明示、仮説は仮説と明記
- PII配慮：ログ/URL/通知にPIIを載せない

### テスト方法
- Claude Code で「テンプレを作りたい」等のトリガー語を入力
- 対応するSkillが呼び出され、手順に従った動作が開始されることを確認

---

## 7. 完了基準

- [ ] 優先度「高」の3つのSkillsが作成されている
- [ ] 各SkillにSKILL.mdが存在する
- [ ] registry.mdに対応が記載されている
- [ ] トリガー語で正しくSkillが呼び出される

---

## 参照ドキュメント

| ドキュメント | 場所 |
|--------------|------|
| Rules v2 | `GEMINI.md` 内 "Rules v2" セクション |
| Workflows一覧 | `.agent/workflows/` |
| Skills構造 | `.agent/skills/` |
| 対応表 | `.agent/registry.md` |
| 設計元資料 | `rules_temp.md` |
