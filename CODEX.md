# AI-PM System (CODEX.md)

**Role**: `AGENTS.md` で定義されたPMBOK第7版準拠の全社横断プロジェクトマネージャーとして動作します。まず `AGENTS.md` を読み込み、プロジェクト憲章がなければユーザーへ初期ヒアリングを行って生成してください。

## Codex CLIでの使い方
- 前提: `npm install -g @openai/codex@latest` でCodex CLIを導入。
- 起動: リポジトリ直下で `codex` を起動し、`AGENTS.md` を読み込んだうえで対話を開始（例: 「プロジェクトを立ち上げたい」）。
- 標準ワークフロー: `.agent/workflows/` にPMBOK準拠の雛形（立上げ/計画/実行・監視/終結/NotebookLM）があるので、必要に応じて参照・生成指示を行う。
- 成果物の保存先: `/{ProjectName}/docs|minutes|context/` を既定とし、Markdownで出力する。

## オーケストレーション（自律実行）利用のポイント
- 参考ドキュメント: `QUICKSTART_ORCHESTRATION.md` と `.agent/ORCHESTRATION_GUIDE.md` を参照。
- CodexにはClaudeのSlash Command相当がないため、以下を推奨:
  - 初期化: `workspace/` の状態確認を自動で提案し、必要なら `ls workspace/` などを実行。
  - 実行: 「プロジェクト憲章を作成」「要件定義書を作成」「週次レポートを作成」などを自然文で指示し、`.agent/workflows/` の記法に沿ってMarkdownを生成・保存する。
  - 連鎖: 憲章→要件→リスクの連続生成や週次レポート生成後の次アクション提案を自律的に行う。
- サンドボックス/ネットワーク制限がある場合は、実行可否をユーザーに確認してからコマンドを走らせる。

## NotebookLM連携（オプション・ネットワーク必須）
`.agent/skills/business/notebooklm` はClaude Code Skill由来のブラウザ自動化スクリプト群です。Codexから利用する場合はPythonスクリプトを直接呼び出します。
- 事前準備（ネットワークとChrome導入が必要）:
  1. `cd .agent/skills/business/notebooklm`
  2. `python scripts/setup_environment.py` （.venv作成・依存/Chromeインストールを自動実行）
  3. 認証: `python scripts/auth_manager.py setup` でブラウザが開くのでGoogleアカウントでNotebookLMにログイン
- クエリ実行の例:
  - 単票照会: `python scripts/ask_question.py --notebook-url "<共有URL>" --question "<質問>"`
  - 複数ノート: `python scripts/ask_multiple.py --library-file data/library.json --question "<質問>"`
- 注意: ブラウザ自動化のためネットワーク/GUIアクセスが必要。`data/` 配下に認証情報が保存されるのでGitコミット禁止（.gitignore済み）。

## 推奨初期プロンプト
```
あなたはPMBOK第7版準拠の全社横断PMです。AGENTS.mdを読み、プロジェクト憲章が無ければヒアリングから開始してください。
```

---
詳細な行動規範・テンプレートは `AGENTS.md` を参照してください。***
