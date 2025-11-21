---
description: "Cursor Command: 週次コンテキスト生成（NotebookLM連携）"
---

# Cursor Command: 週次コンテキスト生成（NotebookLM連携）

## 説明
NotebookLMから情報を収集し、週次コンテキストを生成します。
生成したコンテキストは各ノートブックのソースとして追加され、次週以降の情報源となります。

**実行タイミング**: 毎週金曜日（週次更新フロー Step3）

---

## プロンプトテンプレート

あなたはPMBOK第7版準拠の全社横断AIプロジェクトマネージャー（AI-PgM）です。

**週次コンテキスト生成フロー**:
1. NotebookLMから今週の情報を収集
2. マスター指示書（CLAUDE.md）に基づいて整理
3. 標準フォーマットで週次コンテキストを生成
4. 各ノートブック用のコンテキストファイルを保存

---

## 実行手順（ステップバイステップ）

### Step 1: NotebookLMから情報収集

```bash
# 1-1: EB ALLから全体状況を取得
python scripts/run.py ask_question.py \
  --question "今週（YYYY-MM-DD～YYYY-MM-DD）の全体状況を以下の観点でまとめてください：\
1. 全体ステータス（緑/黄/赤）\
2. 横断依存の変化\
3. 統合リスクの状況\
4. 全体KPIの実績\
5. 次週の重点事項" \
  --notebook-id "eb-all"

# 1-2: EB PL定例から決定事項・アクションを取得
python scripts/run.py ask_question.py \
  --question "今週のPL定例で決定した事項、合意されたアクション、スケジュール変更を報告してください" \
  --notebook-id "eb-pl-meeting"

# 1-3: 全サブPJから進捗・課題を収集
python scripts/run.py ask_multiple.py \
  --question "今週の進捗率、完了タスク、課題、次週予定を簡潔に報告してください" \
  --all-notebooks
```

### Step 2: コンテキスト生成

取得した情報を基に、以下の3種類のコンテキストファイルを生成：

#### 2-1: Context_EB_Global（EB ALL用）
```markdown
# Context_EB_Global_{{YYYY-MM-DD}}.md

- 生成日: {{YYYY-MM-DD}}
- 対象期間: {{From～To}}
- 生成者: AI-PgM（マスター指示書準拠）

## 全体状況
- 全体ステータス: {{緑/黄/赤}}（理由）
- サマリ: {{一言}}

## サブプロジェクト進捗サマリー
| サブPJ | ステータス | 進捗率 | 主要課題 | 次アクション |
|---|---|---|---|---|
{{NotebookLMから取得した情報}}

## 横断依存・統合リスク
{{NotebookLMから取得した情報}}

## 全体KPI実績
{{NotebookLMから取得した情報}}

## 次週重点事項
- [ ] {{項目1}}
- [ ] {{項目2}}

---
**このコンテキストは次週のEB ALL質問時に参照されます**
```

#### 2-2: Context_PL（EB PL定例用）
```markdown
# Context_PL_{{YYYY-MM-DD}}.md

- 生成日: {{YYYY-MM-DD}}
- 対象: PL定例議事録
- 生成者: AI-PgM（マスター指示書準拠）

## 決定事項
{{NotebookLMから取得}}

## アクション
| アクション | 担当 | 期限 | ステータス |
|---|---|---|---|
{{NotebookLMから取得}}

## スケジュール変更
{{NotebookLMから取得}}

## 次回議題
- {{項目}}

---
**このコンテキストは次週のEB PL定例質問時に参照されます**
```

#### 2-3: Context_SP-XX（各サブPJ用）
```markdown
# Context_SP-{{XX}}_{{YYYY-MM-DD}}.md

- 生成日: {{YYYY-MM-DD}}
- 対象サブPJ: {{SubPJName}}
- 生成者: AI-PgM（マスター指示書準拠）

## 今週の進捗
- 進捗率: {{N}}%
- 完了タスク: {{リスト}}
- 課題: {{リスト}}

## 横断依存（他サブPJとの連携）
{{NotebookLMから取得}}

## リスク
{{NotebookLMから取得}}

## 次週予定
- [ ] {{タスク1}}
- [ ] {{タスク2}}

---
**このコンテキストは次週のサブPJ質問時に参照されます**
```

### Step 3: コンテキスト保存

```bash
# EB ALL用コンテキストを保存
保存先: /{ProjectName}/context/eb_all/Context_EB_Global_YYYY-MM-DD.md

# EB PL定例用コンテキストを保存
保存先: /{ProjectName}/context/eb_pl/Context_PL_YYYY-MM-DD.md

# 各サブPJ用コンテキストを保存
保存先: /{ProjectName}/context/subprojects/sp-XX/Context_SP-XX_YYYY-MM-DD.md
```

### Step 4: NotebookLMへのソース追加（手動）

生成したコンテキストファイルを各NotebookLMノートブックのソースとして追加：
1. EB ALLノートブック → Context_EB_Global_YYYY-MM-DD.md を追加
2. EB PL定例ノートブック → Context_PL_YYYY-MM-DD.md を追加
3. 各サブPJノートブック → Context_SP-XX_YYYY-MM-DD.md を追加

---

## 使用例

**毎週金曜日の定型作業**:

```
# ステップ1: NotebookLMから情報収集（上記コマンド実行）

# ステップ2: コンテキスト生成
/週次コンテキスト生成

対象期間: "2025-11-03～2025-11-09"

# 以下、NotebookLMから取得した情報を入力してエージェント実行
```

---

## 備考
- **原則**: システム思考（過去のコンテキストを未来の判断材料に）
- **ドメイン**: 測定、プロジェクト作業
- **フィードバックループ**: 週次コンテキスト保存により、NotebookLMの回答品質が向上
- **マスター指示書**: CLAUDE.mdセクション14.6参照
