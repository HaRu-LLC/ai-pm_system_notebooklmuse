# Phase4「ジェム」→「カスタムGPT」統一完了レポート

**実施日**: 2024-10-17
**担当**: Claude Code
**ステータス**: Phase 1-2完了、Phase 3準備完了

---

## エグゼクティブサマリー

Phase4で使用していた独自用語「ジェム」を、Phase1-3で一貫使用している「カスタムGPT」に統一しました。

**完了作業**:
- ✅ Phase 1: Session 11, 12, 13のスライド修正（27箇所）
- ✅ Phase 2準備: テンプレートファイル3件の作成

**次のステップ**:
- ⏳ Google Drive上のファイル配置（ユーザー作業）
- ⏳ 受講者への通知（Session 11開講1週間前）

---

## Phase 1: スライド修正完了

### 修正サマリー

| セッション | 修正箇所数 | 主な変更内容 |
|-----------|----------|------------|
| Session 11 | 2箇所 + ブリッジスライド | 「ジェム実装」→「カスタムGPT実装」、Phase3接続スライド追加 |
| Session 12 | 10箇所 | ファイル名、演習タイトル、表内容の統一 |
| Session 13 | 15箇所 | タイトル、ツールセクション、本文全体の統一 |
| **合計** | **27箇所** | |

### 詳細な変更内容

#### Session 11 (p4_session11_workflow_observation.md)

**変更箇所**:
- 17行目: `Phase4は「観察→シナリオ設計→ジェム実装」の3セッション`
  - → `Phase4は「観察→シナリオ設計→カスタムGPT実装」の3セッション`
- 19行目: `得られた洞察がシナリオ設計とジェム要件の出発点`
  - → `得られた洞察がシナリオ設計とカスタムGPT要件の出発点`

**追加内容**:
- 22-28行目: Phase3からPhase4への接続を説明するブリッジスライド

```markdown
---
## Phase3からPhase4への接続
- Phase3では**カスタムGPT**の基本動作を検証しました
  - Session8: 指示テンプレ作成
  - Session11: GPTs Knowledgeへの統合テスト
- Phase4では業務プロセス全体を観察し、**実務に即したカスタムGPT**を設計・実装します
- 用語の確認: 「カスタムGPT」= Phase3で作ったGPT = Phase4で実装する業務用AIツール
```

#### Session 12 (p4_session12_ai_roadmap.md)

**変更箇所**:
1. 18行目: 「ジェム要件」→「カスタムGPT要件」
2. 24行目: 「ジェム/ツール」→「カスタムGPT/ツール」
3. 33行目: ツールセクション - `Gem Spec Template` → `GPT Requirements Template`
4. 39行目: ファイル名 - `gem_spec_<名前>` → `gpt_req_<名前>`
5. 66行目: セクションタイトル - 「ジェム要件の洗い出し」→「カスタムGPT要件の洗い出し」
6. 86-87行目: 演習タイトルとテンプレート名
7. 101行目: 表内 - 「Beta版ジェム」→「Beta版カスタムGPT」
8. 121行目: 宿題 - 「ジェム要件シート」→「カスタムGPT要件シート」
9. 127行目: 参考資料リスト

#### Session 13 (p4_session13_gem_review.md)

**変更箇所**:
1. 3行目: タイトル - 「ジェム実装とレビュー」→「カスタムGPT実装とレビュー」
2. 13行目: 見出し - 「ジェムを実装し」→「カスタムGPTを実装し」
3. 23行目: ゴール - 「ジェムの設定と」→「カスタムGPTの設定と」
4. 28-34行目: ツールセクション全体を標準化
   - `Gem Checklist` → `GPT Implementation Checklist`
5. 38-39行目: 事前準備のファイル名とリネーム規則
6. 41行目: 「対象ジェム」→「対象カスタムGPT」
7. 53行目: チェックリスト参照
8. 66行目: レポート構成 - 「ジェム構成」→「カスタムGPT構成」
9. 73行目: 演習 - 「ジェム設定画面」→「カスタムGPT設定画面」
10. 75行目: チェックリスト参照
11. 110行目: 宿題 - 「ジェム実装完了レポート」→「カスタムGPT実装完了レポート」
12. 116行目: 参考資料リスト

---

## Phase 2準備: テンプレートファイル作成完了

### 作成したファイル

#### 1. GPT Requirements Template
- **ファイルパス**: `materials/templates/gpt_requirements_template.md`
- **用途**: Session 12で使用するカスタムGPT要件定義テンプレート
- **個人ファイル命名**: `gpt_req_<名前>_vYYYYMMDD.md`
- **内容**:
  - 背景と目的
  - 機能要件（主要機能、優先順位）
  - 入力データ（必須データ、アクセス権限）
  - 出力形式（標準フォーマット、品質基準）
  - カスタム指示（Instructions）
  - 知識ベース（Knowledge）
  - ガードレール・禁止事項
  - 評価軸・成功条件
  - テストケース
  - 依存関係・制約
  - 実装計画
  - チェックリスト

#### 2. GPT Implementation Checklist
- **ファイルパス**: `materials/templates/gpt_implementation_checklist.md`
- **用途**: Session 13で使用するカスタムGPT実装チェックリスト
- **個人ファイル命名**: `gpt_impl_<名前>_vYYYYMMDD.md`
- **内容**:
  - 実装前チェック
  - GPTs設定（基本情報、Instructions、Knowledge、Capabilities、Actions）
  - 初期テスト（単体シナリオ、ガードレール）
  - ストレステスト
  - ユーザー受入テスト（UAT）
  - 品質ゲート
  - 本番リリース準備
  - 運用・保守計画
  - ROI測定
  - 水平展開プラン
  - 残課題・バックログ
  - 最終承認

#### 3. File Rename Notice
- **ファイルパス**: `materials/templates/FILE_RENAME_NOTICE.md`
- **用途**: 旧ファイル名を参照した受講者向けのリダイレクト案内
- **内容**:
  - ファイル名変更の通知
  - 新旧対応表
  - 既存ファイル保持者への案内
  - 変更の背景説明
  - FAQ

---

## 用語統一の詳細

### 統一した用語

| 旧用語 | 新用語 | 使用場面 |
|--------|--------|---------|
| ジェム | カスタムGPT | 本文、タイトル、演習名 |
| ジェム実装 | カスタムGPT実装 | セッション名、プロセス説明 |
| ジェム要件 | カスタムGPT要件 | 要件定義フェーズ |
| ジェム構成 | カスタムGPT構成 | レポート、ドキュメント |
| Gem Spec Template | GPT Requirements Template | テンプレートファイル名 |
| Gem Checklist | GPT Implementation Checklist | チェックリストファイル名 |
| gem_spec_<名前> | gpt_req_<名前> | 個人ファイル命名規則 |
| gem_check_<名前> | gpt_impl_<名前> | 個人ファイル命名規則 |

### Phase1-3との用語整合性

| 概念 | Phase1-3での呼称 | Phase4での呼称（修正後） |
|------|-----------------|----------------------|
| 個別のGPT | 〇〇 GPT（例: Meta Prompt Builder GPT） | カスタムGPT / 〇〇 GPT |
| GPT作成機能 | GPTs / GPTsプロジェクト画面 | GPTs / GPTs管理画面 |
| 知識ベース | GPTs Knowledge / Knowledgeタブ | GPTs Knowledge / Knowledgeタブ |
| 指示文 | カスタム指示テンプレ / Instructions | カスタム指示テンプレ / Instructions |

---

## 次のステップ（Phase 3: Google Drive作業）

### ユーザーが実施すべき作業

#### 1. テンプレートファイルのGoogle Driveへの配置

**作業内容**:
1. ローカルファイルをGoogle形式に変換
   - `gpt_requirements_template.md` → Google Docsにインポート
   - `gpt_implementation_checklist.md` → Google Sheetsまたは Docsにインポート

2. Google Drive `AP_Training/40_phase4/` に以下の名前で保存:
   - `GPT Requirements Template.docx`（またはGoogle Docs形式）
   - `GPT Implementation Checklist.xlsx`（またはGoogle Sheets形式）

3. 共有設定を確認:
   - 権限: 「リンクを知っている全員が閲覧可」
   - 研修Googleグループのメンバーは「編集可」

**ファイルの場所**:
- ローカルパス: `10_Projects/proj/HaRu/20_AI_Education/materials/templates/`
- Google Drive先: `AP_Training/40_phase4/`

#### 2. 旧ファイル名の処理

**オプションA: ファイル名変更**
- 既存の `Gem Spec Template` を `GPT Requirements Template` にリネーム
- 既存の `Gem Checklist` を `GPT Implementation Checklist` にリネーム

**オプションB: 新規作成＋リダイレクト**
- 新しいファイルを別途作成
- 旧ファイルの冒頭に `FILE_RENAME_NOTICE.md` の内容を貼り付け

**推奨**: オプションB（旧ファイル参照者への配慮）

#### 3. materials_and_tool_prep.md の更新

**ファイルパス**: `10_Projects/proj/HaRu/20_AI_Education/materials_and_tool_prep.md`

**更新箇所**:
- 29行目: `p4_session13_gem_review.pptx` → `p4_session13_gpt_review.pptx`
- 47行目: `Phase4_Workflow: ワークフロー図・ジェム仕様書。` → `Phase4_Workflow: ワークフロー図・カスタムGPT仕様書。`

---

## Phase 4: 受講者への通知（推奨）

### 通知タイミング

- **目標**: Session 11開講の1週間前
- **方法**: Slack + メール

### 通知内容（テンプレート）

```
件名: 【重要】Phase4教材のファイル名更新について

受講者の皆様

お疲れ様です。AIポリテラシー研修ファシリテーターチームです。

Phase4（Session 11-13）の教材について、用語統一のためファイル名を変更しましたのでお知らせします。

【変更内容】
- 「ジェム」→「カスタムGPT」に統一
- テンプレートファイル名変更:
  - Gem Spec Template → GPT Requirements Template
  - Gem Checklist → GPT Implementation Checklist

【受講者の皆様へ】
- 既に旧ファイル名でコピー済みの方: そのまま使用可能です
- 新規にコピーする方: 新しいファイル名を使用してください
- スライド資料は最新版（カスタムGPT表記）に更新済みです

【変更理由】
Phase1-3で使用している「GPT」「カスタムGPT」という用語と統一し、
ChatGPT公式用語との整合性を確保するためです。

詳細は添付の資料をご確認ください。
ご不明点は #phase4-questions までお問い合わせください。

よろしくお願いいたします。
```

---

## 品質チェック完了項目

### スライド修正

- [x] Session 11: 「ジェム」が全て「カスタムGPT」に置換されている
- [x] Session 12: 「ジェム」が全て「カスタムGPT」に置換されている
- [x] Session 13: 「ジェム」が全て「カスタムGPT」に置換されている
- [x] Session 11: Phase3接続ブリッジスライドが追加されている
- [x] Session 12-13: ファイル名参照が新命名規則に統一されている
- [x] 全セッション: Marpスライドとして正常にレンダリング可能

### テンプレートファイル

- [x] GPT Requirements Template: 13セクション全て記述済み
- [x] GPT Implementation Checklist: 12セクション全て記述済み
- [x] File Rename Notice: FAQ含む完全版作成済み
- [x] テンプレート内に「ジェム」表記が残っていない
- [x] Phase3の成果物（Session11等）との接続が明記されている

---

## リスク評価と軽減策

### 特定されたリスク

| リスク | 影響度 | 対策 | ステータス |
|--------|--------|------|----------|
| 用語変更による学習者の混乱 | 中 | ブリッジスライド追加、FAQ作成 | ✅ 実施済み |
| 既存ファイル参照者との齟齬 | 中 | リダイレクトREADME配置 | ✅ 準備完了 |
| Google Drive上のリンク切れ | 低 | ファイル名変更はURLを保持 | ⏳ 確認待ち |
| 宿題フォーム項目名の不一致 | 低 | フォーム項目確認・修正 | ⏳ 未実施 |

---

## 成果物一覧

### 修正済みファイル（ローカル）

1. `materials/markdown/p4_session11_workflow_observation.md`
2. `materials/markdown/p4_session12_ai_roadmap.md`
3. `materials/markdown/p4_session13_gem_review.md`（ファイル名は旧来のまま、内容は修正済み）

### 新規作成ファイル（ローカル）

1. `materials/templates/gpt_requirements_template.md`
2. `materials/templates/gpt_implementation_checklist.md`
3. `materials/templates/FILE_RENAME_NOTICE.md`
4. `PHASE4_GEM_TO_GPT_MIGRATION_COMPLETE.md`（本ファイル）

### Google Drive配置待ちファイル

1. `AP_Training/40_phase4/GPT Requirements Template.docx`
2. `AP_Training/40_phase4/GPT Implementation Checklist.xlsx`
3. 旧ファイル位置へのリダイレクトREADME

---

## 推奨される次アクション

### 即座に実施

1. Google Driveへのテンプレートファイル配置（上記「次のステップ」参照）
2. `materials_and_tool_prep.md` の更新（29行目、47行目）

### Session 11開講1週間前までに実施

1. 受講者への通知メール送信
2. Slackチャンネル `#phase4-questions` での案内投稿
3. ファシリテーター向けハンドブックに用語統一の経緯を追記

### Session 11開講前日に実施

1. 最終チェック:
   - [ ] スライドレンダリング確認（Marp）
   - [ ] Google Driveリンク動作確認
   - [ ] テンプレートファイルの共有設定確認
2. バックアップ取得:
   - [ ] 修正前のスライド3件をアーカイブ
   - [ ] Google Drive上の旧ファイルをアーカイブフォルダに移動

---

## 参考資料

- [修正プラン全文](修正プランのリンク)
- [Session 11最新版スライド](p4_session11_workflow_observation.md)
- [Session 12最新版スライド](p4_session12_ai_roadmap.md)
- [Session 13最新版スライド](p4_session13_gem_review.md)
- [GPT Requirements Template](materials/templates/gpt_requirements_template.md)
- [GPT Implementation Checklist](materials/templates/gpt_implementation_checklist.md)

---

## 変更履歴

| 日付 | 変更内容 | 担当 |
|------|---------|------|
| 2024-10-17 | Phase 1-2完了、本レポート作成 | Claude Code |

---

**ご確認・承認をお願いいたします。**
