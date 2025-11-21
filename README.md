# AI-PM System Template

## 概要
本リポジトリは、PMBOK第7版に準拠した「全社横断プロジェクトマネージャー」AIエージェントを稼働させるためのテンプレートシステムです。
あらゆるプロジェクトの計画・実行・監視・終結を、AIとの対話を通じて効率的に管理します。

## 特徴
- **PMBOK準拠**: 12の原理・原則と8つのパフォーマンス・ドメインに基づいたマネジメント支援。
- **動的エージェント生成**: プロジェクト憲章に基づき、必要な専門家エージェントやワークフローを自動生成。
- **NotebookLM連携**: プロジェクト固有のナレッジベースとしてNotebookLMを活用可能（オプション）。

## 対応CLI
本システムは、以下のAI CLIツールでの動作を想定しています：
- **Claude Code** (`CLAUDE.md` を参照)
- **Gemini CLI** (`GEMINI.md` を参照)
- **Codex** (OpenAI Codex CLI)

### インストール・アップデート

環境に合わせて、`npm` または `Homebrew` を使用してインストールしてください。

#### npmを使用する場合
```bash
# Claude Code
npm install -g @anthropic-ai/claude-code@latest

# Gemini CLI
npm install -g @google/gemini-cli@latest

# Codex CLI
npm install -g @openai/codex@latest
```

#### Homebrewを使用する場合
```bash
# Claude Code
brew install claude-code

# Gemini CLI
brew install google-gemini-cli

# Codex CLI
# Homebrew版は提供されていないため、npmを使用してください
npm install -g @openai/codex@latest
```

## ディレクトリ構造
- `.agent/`: エージェント定義とワークフロー
    - `personas/`: 動的に生成されるエージェント人格
    - `workflows/`: PMBOK標準ワークフロー + 動的生成ワークフロー
- `workspace/`: プロジェクト作業領域（初期状態は空）
- `AGENTS.md`: AI-PMのコアロジック定義
- `CLAUDE.md` / `GEMINI.md`: 各CLI向けのエントリーポイント

## 使い方
1. 本リポジトリをクローンまたはテンプレートとして使用。
2. 対応するCLIツールでプロジェクトを開く。
3. 「プロジェクトを立ち上げたい」と話しかける。
4. AI-PMの案内に従い、プロジェクト憲章を作成。

## Slash Commands（Claude Code）

Claude Codeでは、以下のSlash Commandsが利用可能です：

### プロジェクト管理（PMBOK準拠）
- `/project-charter` - PMBOK第7版準拠のプロジェクト憲章を生成
- `/requirements` - 要件定義書を生成（業務/機能/非機能要件）
- `/risk-register` - リスク登録簿を生成・更新
- `/weekly-status` - 週次統合ステータスレポートを生成
- `/meeting-minutes` - 会議議事録を生成

### 経営層向け
- `/corporate-strategy` - 経営戦略の策定と壁打ち支援
- `/hr-strategy` - 採用・人事・組織戦略を立案
- `/marketing-strategy` - マーケティング戦略を立案

各コマンドの詳細は `.claude/commands/` ディレクトリ内の各ファイルを参照してください。

## オーケストレーション機能（Claude Code）

Claude Codeでは、AIが**オーケストレーター（指揮者）**として機能し、ユーザーの要求を理解して**自律的に**適切なSlash Commandsを選択・実行します。

### 主な特徴

#### 1. 自律的なコマンド実行
ユーザーが明示的にコマンドを指定しなくても、Claudeが状況を判断して適切なコマンドを実行します。

**例:**
```
ユーザー: 「プロジェクトを始めたい」
Claude: 「プロジェクト憲章を作成します。」
        [/project-charterを自動実行]
```

#### 2. プロアクティブな提案
会話開始時にプロジェクト状態を確認し、必要なアクションを提案します。

**例:**
```
Claude: 「プロジェクトAの週次レポートが先週から更新されていません。
         最新の状況を整理しましょうか？」
        [/weekly-statusを自動実行]
```

#### 3. 連鎖実行
一つのタスクに複数のコマンドが必要な場合、順次自動実行します。

**例:**
```
プロジェクト立ち上げ:
  /project-charter → /requirements → /risk-register
```

### オーケストレーション成熟度レベル

- **Level 0**: 手動実行（ユーザーが`/project-charter`と入力）
- **Level 1**: 提案型（Claudeが「作成しますか？」と確認）
- **Level 2**: 自律実行 ✅ **目標**（Claudeが自動的に実行）
- **Level 3**: 完全自律 ⭐ **理想**（全プロセスを自動化）

### クイックスタート

オーケストレーション機能を試すには：

```
「新規プロジェクトを始めたい」
```

Claudeが自動的に以下を実行します：
1. プロジェクト状態の確認
2. プロジェクト憲章の生成
3. 次のステップ（要件定義）の提案

詳細は `QUICKSTART_ORCHESTRATION.md` を参照してください。
