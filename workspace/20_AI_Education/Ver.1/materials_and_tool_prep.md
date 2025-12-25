# 教材・ツール準備仕様 v0.2

## 1. 教材ファイル構成（Scribe・Customer Success協議）
- ルート: `AP_Training/` 共有ドライブ
  - `00_guides/`
    - `overview_slide_deck.pptx`（全体オリエン）
    - `facilitator_runbook.docx`
  - `10_phase1/`
    - `p1_session1_mindset.pptx` / `p1_session1_mindset.mp4`
    - `p1_session2_prompt_basics.pptx` / `p1_session2_prompt_basics.mp4`
    - `p1_session3_ambiguity.pptx` / `p1_session3_ambiguity.mp4`
    - `p1_session4_loop_demo.pptx` / `p1_session4_loop_demo.mp4`
    - `prompt_skeleton_sheet.xlsx`
  - `20_phase2/`
    - `p2_session5_meta_prompt.pptx` / `p2_session5_meta_prompt.mp4`
    - `p2_session6_role_guardrail.pptx` / `p2_session6_role_guardrail.mp4`
    - `meta_prompt_builder.gpts`（ChatGPT Teams）
    - `prompt_refinement_gpt.gpts`
  - `30_phase3/`
    - `p3_session7_kb_brief.pptx` / `p3_session7_kb_brief.mp4`
    - `p3_session8_instruction_lab.pptx` / `p3_session8_instruction_lab.mp4`
    - `p3_session9_doc_coauthor.pptx` / `p3_session9_doc_coauthor.mp4`
    - `p3_session10_markdown_refine.pptx` / `p3_session10_markdown_refine.mp4`
    - `p3_session11_test_review.pptx` / `p3_session11_test_review.mp4`
    - `doc_coauthor_gpt.gpts`
    - `markdown_refiner_gpt.gpts`
  - `40_phase4/`
    - `p4_session12_workflow_observation.pptx` / `p4_session12_workflow_observation.mp4`
    - `p4_session13_ai_roadmap.pptx` / `p4_session13_ai_roadmap.mp4`
    - `p4_session14_gem_review.pptx` / `p4_session14_gem_review.mp4`
    - `roi_calculator.xlsx`
  - `90_templates/`
    - 各種Google Docs/Sheets/Slidesのテンプレ（Docs版を保存）

## 2. GPTs / プロジェクト準備（Lead Engineer協議）
- ChatGPT Teams内に研修専用ワークスペース`AI-Politeracy-2025`を作成。
- GPTsテンプレ一覧
  1. `Prompt Refinement GPT`
  2. `Meta Prompt Builder`
  3. `Guardrail Checker`
  4. `Instruction Reviewer`
  5. `Doc Co-Author`
  6. `Markdown Refiner`
  7. `Workflow Assistant`
- プロジェクト構成
  - `Phase1_Prompts`: サンプル課題・改善ログを格納。
  - `Phase3_KnowledgeBase`: 知識ベース整備用ドキュメントのリンク集。
  - `Phase4_Workflow`: ワークフロー図・ジェム仕様書。
- 共有設定: 研修Googleグループのメンバー全員を`Editor`に。ワークスペース管理者=ファシリテーター。
- GPTs仕様ドキュメント
  - 各GPTごとに `gpts_specs/<name>.md` を作成。記載内容:
    - タイトル・目的
    - カスタムプロンプト（インストラクション）全文
    - 参照する知識ベースファイル一覧と更新手順
    - 知識ベース作成方法（Markdown整形ルール、タグ、更新頻度）
    - テストケースと期待出力
  - プロジェクト用にも `projects_specs/<name>.md` を用意し、構成するGPTs・知識ファイル・権限ルールを明示。

## 3. 自動化/ログ管理（QA・Security協議）
- Googleフォーム提出→Apps Scriptで`homework_tracker`シートに自動記録。
- ChatGPTログ: 研修期間終了後にエクスポートし、`logs/chatgpt/YYYYMMDD.zip`として保管。
- Slack/メール通知: 宿題提出・レビュー締切のリマインダをZapierで週次送信。

## 4. ドライラン計画
- Week-2: ファシリテーター内でPhase1〜2を通し練習。AI応答ログを確認。
- Week-1: テスト受講者2名でPhase3〜4の要所を試行。アンケート・宿題導線を検証。
- Week0: チェックリストを用いた最終リハーサル、資料配布、権限付与。

## 5. 残タスク
1. 各プレゼン資料および解説動画のドラフト作成（PPTX/MP4）
   - 対象: Phase1〜4の13セッション。素材管理=`materials/markdown/<phase>_session<no>.md`。
   - 依頼フロー: Markdownドラフト完成→ファシリ一次チェック→Slides変換→動画化→QAレビュー。
- 直近ToDo: Session2〜4のMarkdownを2024-09-25までにドラフト化、Session5〜7は2024-10-02までに骨子作成。
2. GPTsテンプレの初版をファシリが作成し、QAが検証。
   - 対象: `Prompt Refinement`〜`Workflow Assistant`の7種。
   - 依存: Phase別教材ドラフトで示す用語・評価指標を反映すること。
   - 直近ToDo: `Prompt Refinement GPT`と`Meta Prompt Builder`の指示文ドラフトを2024-09-27までに作成、QAレビュー枠を2024-09-30に設定。
3. Google Apps Scriptの実装・レビュー。
   - スコープ: 宿題フォーム連携、リマインダ送信、提出状況ダッシュボード更新。
   - 依存: `homework_tracker`シート列定義、Zapierフロー要件確定。
   - 直近ToDo: フォーム回答→シート書込のサンプルスクリプトを作成し、2024-09-24の定例でレビュー。
4. ドライラン実施レポートのテンプレ作成。
   - スコープ: Week-2〜0の実施ログ、改善点、アクションアイテム、リスク記録。
   - 依存: Phase別チェックリスト、QA観点、Apps Scriptログ仕様。
   - 直近ToDo: `dryrun_report_template.md`のアウトラインを2024-09-26までに作成。

## 6. 教材作成手順（Docs→Slides→Video）
1. マークダウンドラフト
   - `materials/markdown/`に各セッション用の`.md`ファイルを作成（講義要点・演習手順・図表指示を記述）。
   - ChatGPT Teams内の`Doc Co-Author` GPTを利用して内容を整える。
2. スライド生成
   - マークダウンをスライド生成ツール（例: Marp, Deckset, SlidesAI）へインポートし、体裁調整。
   - Googleスライドにエクスポートし、`AP_Training/...` のPPTXに同期。
3. 動画化
   - 完成スライドをPDF出力。
   - AI動画作成ツール（例: Synthesia, HeyGen 等）にPDFを読み込み、ナレーション付き動画に変換。
   - 必要に応じて音声を調整し、MP4を格納。
4. 品質チェック
   - スライド/動画ともにファシリテーターとQAで確認。
   - 修正点はマークダウンにフィードバックし、再生成。
5. 公開
   - 共有ドライブの該当フォルダにPPTX/MP4を配置し、Slackで周知。
   - バージョンタグ（`vYYYYMMDD`）をファイル名末尾に付与。

### 6.1 Markdownドラフトテンプレ
- ファイル命名: `materials/markdown/p<phase>_session<no>_<keyword>.md`
- 推奨構成:
  1. Front Matter（セッション名／Phase／作成日／担当）
  2. `Learning Objectives`
  3. `Session Flow`（タイムボックス）
  4. `Key Concepts`（箇条書き）
  5. `Demo Script`（講師用指示）
  6. `Hands-on Exercise`
  7. `Homework`（課題内容・提出形式）
  8. `Reference Materials`
- スタイル: H2見出しで大項目、演習手順は番号付きリスト、Tipsはブロック引用。

### 6.2 スライド生成チェックリスト
- マスター: タイトル・本文・箇条書きレイアウトを事前に設定し、Marpからの出力差異を吸収。
- 配色: 統一カラーパレット（Primary: #004A8F, Accent: #00A0DC, Neutral: #F3F5F7）。
- 図表: 演習フローは3ステップ図、評価基準はテーブル、リスク/対策は2列比較。
- ナレーション用スクリプトはスライドの`Speaker Notes`に貼り付け、動画化ツールへインポート。
- QA項目: 誤字脱字／図の解像度／AI用語の整合性／演習時間の合計。

### 6.3 動画化ワークフロー
- `Synthesia`（第一候補）: テンプレート「Learning & Development」を使用。字幕自動生成を有効化。
- `HeyGen`（代替案）: 日本語話者アバター`Sakura`を利用。固有名詞はカスタム辞書に登録。
- 音声校正: 読み替えが必要な固有名詞は`Pronunciation`機能で調整し、試写後にトーン／間を再確認。
- 出力設定: 1080p, mp4, 30fps。クラウド保存→`AP_Training/<phase>/`へダウンロード配置。

## 7. GPTsテンプレ仕様

### 7.1 共通テンプレート骨子（`gpts_specs/<name>.md`）
- Metadata: タイトル、最終更新日、作成者、適用フェーズ（例: Phase3 Session9）。
- Purpose: 目的と利用シナリオ（3〜4文）。
- Instructions: カスタム指示（セクションごとに箇条書き）。
- Knowledge Base: 参照ファイル、更新手順、品質チェック。
- Input/Output Formats: 期待する入力形式、レスポンスフォーマット例。
- Test Cases: 最低3ケース（正常2／例外1）。
- Maintenance Notes: 改修フロー、権限、バージョンタグ付け。

### 7.2 初版ドラフト方針
- `Prompt Refinement GPT`: Phase1で使う骨組み質問リストを初期プロンプトへ埋め込み、改善ループの終了条件を明示。
- `Meta Prompt Builder`: 利用者の業界・目的・制約をヒアリングする質問群を先に提示。生成物はMarkdown形式。
- `Guardrail Checker`: リスク分類（情報公開/倫理/法規制）を網羅したチェック表を出力。
- `Instruction Reviewer`: テンプレの必須項目が欠落した場合に警告文を返すロジックを盛り込む。
- `Doc Co-Author`: セクションごとに要約→問い返し→アウトライン提案の順で返答するよう設定。
- `Markdown Refiner`: 表形式への変換ルール、メタデータタグ（`tags:[]`）の付与を自動化。
- `Workflow Assistant`: TODOリストとリスクログを同時に出力し、Phase4での業務整理を支援。

### 7.3 作成状況メモ（2024-09-18）
- ✅ `gpts_specs/prompt_refinement_gpt.md` 初版作成済み（Phase1用）
- ✅ `gpts_specs/meta_prompt_builder.md` 初版作成済み（Phase2用）
- ⏳ 次ステップ: Guardrail Checker / Instruction Reviewer / Doc Co-Author / Markdown Refiner / Workflow Assistant の仕様ドラフト

### 7.4 カスタム指示テンプレ生成フロー
- 入力整理: 受講者はSession7の素材ブリーフを基に、業務目的・利用資料・ガードレールを`Meta Prompt Builder`へ入力。
- 初稿生成: `Meta Prompt Builder`が「ロール/ゴール/入力/出力/ガードレール/改善ループ」の6ブロックを含むドラフトを返す。
- 人による整備: 受講者がドラフトを`Custom Instruction Template`へ転記し、固有条件や社内ポリシーを追記。
- 自動レビュー: 完成版を`Instruction Reviewer`に渡し、欠落項目・曖昧表現・ガードレール不足を抽出。
- ログ更新: 指摘と修正内容を`Instruction Log`へ記録し、確定版を`gpts_specs/<name>.md`へ反映。

## 8. Apps Script 自動化設計
- リポジトリ: `AP_Training/apps_script/homework_tracker.gs`
- 構成
  - `onFormSubmit(e)`: フォーム回答から`homework_tracker`に書き込み、提出IDを発行。
  - `syncStatusToDashboard()`: 受講者ごとの進捗を`dashboard`シートに集計。
  - `postReminder()`: Zapier WebhookまたはGmail送信APIを呼び出してリマインダ送信。
- 権限: 宿題フォームのオーナーがApps Scriptを公開し、研修Googleグループに「編集者」を付与。
- テスト: テスト用フォームで3件のダミー投稿→シート記録→Zapier通知まで確認。
- ログ: エラーは`Logs/app_script/YYYYMMDD.log`に記録。Slack通知は重大エラーのみ。

## 9. ドライランレポートテンプレ概要
- ファイル: `AP_Training/90_templates/dryrun_report_template.md`
- 構成案
  1. `Session Scope`（実施範囲、日付、参加者）
  2. `Preparation Checklist`（完了/未完）
  3. `Observations`（良かった点／課題／AIログ抜粋）
  4. `Action Items`（担当・期限・フォロー方法）
  5. `Risk & Mitigation`（重要度ABC分類）
  6. `Tooling Feedback`（GPTs、Apps Script、Slides/Video）
  7. `Next Step Approval`（承認者、コメント）
- 運用: Week-2〜0の各ドライラン終了当日に記入、翌日のスタンドアップでレビュー。
