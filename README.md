# AI-PM System Template

## 概要
本リポジトリは、PMBOK第7版に準拠した「全社横断プロジェクトマネージャー」AIエージェントを稼働させるためのテンプレートシステムです。
あらゆるプロジェクトの計画・実行・監視・終結を、AIとの対話を通じて効率的に管理します。

## 特徴
- **PMBOK準拠**: 12の原理・原則と8つのパフォーマンス・ドメインに基づいたマネジメント支援
- **動的エージェント生成**: プロジェクト憲章に基づき、必要な専門家エージェントやワークフローを自動生成
- **30+ Skills搭載**: PM、エンジニアリング、ビジネス、メタスキルを網羅
- **マルチエージェント連携**: Claude × Codex の協調動作に対応
- **NotebookLM連携**: プロジェクト固有のナレッジベースとしてNotebookLMを活用可能（オプション）

---

## 前提条件

### 必須
| ツール | 用途 | インストール |
|--------|------|-------------|
| **Claude Code** | メインAI CLI | `npm install -g @anthropic-ai/claude-code@latest` または `brew install claude-code` |
| **Node.js** | CLI実行環境 | https://nodejs.org/ |
| **Git** | バージョン管理 | https://git-scm.com/ |

### オプション（機能拡張用）
| ツール | 用途 | インストール |
|--------|------|-------------|
| **Codex CLI** | マルチエージェント連携 | `npm install -g @openai/codex@latest` または `brew install --cask codex` |
| **tmux** | Codex対話観察モード | `brew install tmux` |
| **Gemini CLI** | Geminiモデル利用 | `npm install -g @google/gemini-cli@latest` または `brew install google-gemini-cli` |
| **Python 3.8+** | NotebookLM連携、スクリプト実行 | https://www.python.org/ |

### CLI一括インストール
```bash
# npm版（クロスプラットフォーム）
npm install -g @anthropic-ai/claude-code@latest @openai/codex@latest @google/gemini-cli@latest

# Homebrew版（macOS）
brew install claude-code google-gemini-cli tmux
brew install --cask codex  # Codexはcask
```

### Codex CLI認証（マルチエージェント連携を使用する場合）
```bash
# OAuth認証（推奨）
codex login

# APIキー認証
codex login --with-api-key
```

---

## 対応CLI
本システムは、以下のAI CLIツールでの動作を想定しています：
- **Claude Code** (`CLAUDE.md` を参照) - メインオーケストレーター
- **Gemini CLI** (`GEMINI.md` を参照) - Geminiモデル利用
- **Codex CLI** - マルチエージェント連携、コード生成委譲

## ディレクトリ構造
```
.
├── .agent/                    # エージェント定義
│   ├── skills/                # 利用可能なスキル（30+）
│   │   ├── business/          # ビジネス文書作成、NotebookLM連携
│   │   ├── engineering/       # 開発・実装支援（14スキル）
│   │   ├── pm/                # プロジェクト管理
│   │   └── meta/              # メタスキル（スキル生成等）
│   ├── docs/                  # フレームワーク詳細ガイド
│   ├── templates/             # 成果物テンプレート
│   ├── workflows/             # PMBOK標準ワークフロー
│   ├── registry.md            # スキル登録簿
│   └── ORCHESTRATION_GUIDE.md # オーケストレーション設計
├── .claude/commands/          # Slash Commands（40+）
├── workspace/                 # プロジェクト作業領域
├── AGENTS.md                  # PMロール定義（PMBOK v7）
├── CLAUDE.md                  # Claude Code設定
└── GEMINI.md                  # Gemini CLI設定
```

## 使い方
1. 本リポジトリをクローンまたはテンプレートとして使用。
2. 対応するCLIツールでプロジェクトを開く。
3. 「プロジェクトを立ち上げたい」と話しかける。
4. AI-PMの案内に従い、プロジェクト憲章を作成。

## Slash Commands（Claude Code）

Claude Codeでは、40以上のSlash Commandsが利用可能です：

### 経営層向け（Executive）
| コマンド | 説明 |
|----------|------|
| `/corporate-strategy` | 経営戦略の策定と壁打ち支援 |
| `/hr-strategy` | 採用・人事・組織戦略を立案 |
| `/marketing-strategy` | マーケティング戦略を立案 |
| `/new-biz-dev` | 新規事業・新商品開発 |
| `/financial-strategy` | 財務戦略 |
| `/research-report` | 調査・レポート作成 |

### プロジェクト管理（PMBOK準拠）
| フェーズ | コマンド例 |
|----------|-----------|
| **立上げ** | `/project-charter`, `/stakeholder-reg` |
| **計画** | `/pm-plan`, `/wbs`, `/schedule`, `/cost-estimate`, `/risk-reg`, `/requirements`, `/test-plan`, `/quality-plan` |
| **実行** | `/meeting-minutes`, `/test-report`, `/progress-report`, `/weekly-status` |
| **終結** | `/closing-report`, `/handover` |

### 特殊コマンド
| コマンド | 説明 |
|----------|------|
| `/agents-maker` | AIエージェント作成スペシャリスト |
| `/strategy-analysis` | 戦略分析ワークフロー |
| `/case-study` | 事例作成 |
| `/seminar-architect` | セミナー企画・準備・運営 |

詳細は `.claude/commands/` ディレクトリを参照してください。

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

---

## Skills一覧

本システムには30以上のスキルが搭載されています。

### Engineering（開発・実装支援）

| スキル | 説明 |
|--------|------|
| **codex-cli** | OpenAI Codex CLI連携、マルチエージェント協調 |
| **docx / pdf / pptx / xlsx** | Office文書処理（Anthropic公式） |
| **playwright** | ブラウザ自動化、Webテスト |
| **test-driven-development** | テスト駆動開発の厳格な実践 |
| **systematic-debugging** | 体系的デバッグ、根本原因調査 |
| **verification-before-completion** | 完了前検証 |
| **writing-plans / executing-plans** | 計画作成と実行 |
| **subagent-driven-development** | サブエージェント派遣 |
| **dispatching-parallel-agents** | 並列エージェント実行 |
| **using-git-worktrees** | Git Worktreeで並列ブランチ作業 |
| **brainstorming** | アイデアを仕様に変換 |

### Business / PM / Meta

| カテゴリ | スキル |
|----------|--------|
| **Business** | doc-from-examples, **notebooklm**（ナレッジベース連携） |
| **PM** | privacy-email-review（プライバシー設計レビュー） |
| **Meta** | skills-creator, template-miner, workflow-designer |

詳細は `.agent/registry.md` を参照してください。

---

## NotebookLM連携（オプション）

Google NotebookLMをナレッジベースとして活用できます。

### セットアップ
```bash
cd .agent/skills/business/notebooklm
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 認証
Claude Codeで以下を実行：
```
「NotebookLMの認証をセットアップして」
```

### 使用例
```
「私のReactドキュメントでhooksについて調べて」
「このNotebookLMをライブラリに追加: [リンク]」
```

詳細は `.agent/skills/business/notebooklm/README.md` を参照してください。

---

## マルチエージェント連携（Claude × Codex）

ClaudeからCodex CLIを操作し、異なる視点でのコード生成・レビューが可能です。

### 完全自動モード（推奨）
```bash
codex exec "タスク内容"
```

### 対話観察モード（tmux使用）
```bash
# tmuxセッション作成
tmux new -s codex

# codex起動
codex --approval-mode auto-edit

# 離脱（Ctrl+B → D）
```

詳細は `.agent/skills/engineering/codex-cli/SKILL.md` を参照してください。
