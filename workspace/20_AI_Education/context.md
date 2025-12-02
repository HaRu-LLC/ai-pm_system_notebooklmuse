# AIポリテラシー研修 プロジェクトコンテクスト v20240914

## 概要
- 目的: ChatGPT/Gemini等の標準チャットツールを自走活用できる人材を育成し、最終的にGPTs構築・Cursor相当の文書生成・ワークフロー自動化まで習得させる13セッションの研修プログラムを設計。
- 対象: 企業内のPoC推進リーダー（選抜20名程度）。Google Workspace + ChatGPT Teamsを利用する前提。
- 成果物: プロンプト改善力、カスタムGPTs、業務課題解体とジェム実装、ROI報告。

## フェーズ構成（全13セッション）
- Phase1（3回）: 手書きプロンプト基礎。構造化→明確化→改善ループ。
- Phase2（2回）: AIと共創してプロンプト原案生成→ロール/ガードレール磨き込み。
- Phase3（5回）: カスタム指示・知識ベース作成（ブリーフ→指示テンプレ→共創ドキュメント→既存資料リファイン→統合検証）。
- Phase4（3回）: 業務観察→改善シナリオ→ジェム実装＆レビュー。

## 評価・運用方針
- セッション後アンケート（理解度5段階、曖昧点、サポート希望など7問）と宿題フォーム（リンク・自己評価・AIログ）で形成評価。
- ルーブリックでプロンプト品質・GPTs完成度・工数削減率・水平展開数・継続利用率を測定。
- Googleグループ＋ChatGPT Teamsで権限管理。Apps Script/Zapierで宿題トラッカーとリマインダを自動化。
- GPTs/ファイルログを週次バックアップ。ドライラン（Week-2, -1, 0）で導線と教材を検証。

## 教材・テンプレ構成
- `AP_Training/` 共有ドライブにPhase別フォルダを配置。各セッションごとにスライド（pptx）＋動画（mp4）＋テンプレ（Sheets/Docs）。
- スライド作成はMarkdown原稿→スライド生成ツール→Google Slides→PDF→AI動画化（音声付き）。
- ChatGPT Teams内に`AI-Politeracy-2025`ワークスペース。GPTs7種とPhase別プロジェクトを共有。
- `gpts_specs/<name>.md` にカスタム指示全文・知識ベース一覧・生成手順・テストケースを記載。プロジェクト仕様も`projects_specs/<name>.md`で管理。

## 今後のタスク（第2フェーズ）
1. セッション別Markdownドラフトとスライド/動画生成のパイプライン構築。
2. GPTsテンプレ（Prompt Refinement等）の指示文と知識ベース整備（残: Guardrail Checker / Instruction Reviewer / Doc Co-Author / Markdown Refiner / Workflow Assistant）。
3. Apps Scriptで宿題トラッカー自動化、Zapierで通知設定。
4. ドライラン用ダミーデータとレポートテンプレートの準備。

## 最近の更新（2024-09-18）
- Phase1〜Phase4の全セッション（1〜13）について、`materials/markdown/` に学習者向けMarpドラフトを作成。初心者向けのステップ・テンプレ複製・ChatGPT操作手順・宿題提出フローを明文化。
- Phase2以降は「設計チャット」「検証チャット」を分離し、プロンプト改善ループの進め方とログ記録方法を統一。セッション6では汎用ChatGPTによる試験整形 → セッション9で専用`Markdown Refiner` GPT導入予定である旨を追記。
- GPT仕様書 `gpts_specs/` に`prompt_refinement_gpt.md` と `meta_prompt_builder.md` を追加。材料準備ドキュメント `materials_and_tool_prep.md` の「7.3作成状況メモ」を更新し、残タスクの対象GPTを明示。
- `task.md` のタスク5メモをv0.2内容に合わせ更新済み。マテリアルフォルダは `10_Projects/proj/HaRu/20_AI_Education/materials/markdown/` へ集約。
