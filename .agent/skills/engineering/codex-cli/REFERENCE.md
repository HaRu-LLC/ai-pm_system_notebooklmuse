# codex-cli Reference

詳細なコマンドリファレンス、設定オプション、トラブルシューティングガイド。

---

## 目次

1. [インストールガイド](#1-インストールガイド)
2. [認証方法](#2-認証方法)
3. [実行モード詳細](#3-実行モード詳細)
4. [承認モード詳細](#4-承認モード詳細)
5. [マルチエージェント連携パターン](#5-マルチエージェント連携パターン)
6. [セッション管理](#6-セッション管理)
7. [セキュリティ考慮事項](#7-セキュリティ考慮事項)
8. [トラブルシューティング](#8-トラブルシューティング)
9. [コマンドリファレンス](#9-コマンドリファレンス)
10. [tmux永続セッションモード](#10-tmux永続セッションモード)
11. [オーケストレーターループ詳細](#11-オーケストレーターループ詳細)
12. [既存ツール/プロジェクト参照](#12-既存ツールプロジェクト参照)

---

## 1. インストールガイド

### macOS（Homebrew推奨）

```bash
brew install --cask codex
```

### npm（クロスプラットフォーム）

```bash
npm install -g @openai/codex
```

### アップグレード

```bash
codex --upgrade
```

### インストール確認

```bash
which codex
# 期待出力: /usr/local/bin/codex または /opt/homebrew/bin/codex

codex --version
# 期待出力: codex version x.x.x
```

### 対応プラットフォーム

| プラットフォーム | 対応状況 | 備考 |
|-----------------|---------|------|
| macOS | ✅ | Homebrew推奨 |
| Linux | ✅ | npm推奨 |
| Windows | ⚠️ | WSL2推奨 |

---

## 2. 認証方法

### OAuth認証（推奨）

```bash
codex login
```

ブラウザが開き、ChatGPTアカウントでログイン。

### APIキー認証

```bash
codex login --with-api-key
# プロンプトでAPIキーを入力
```

### 環境変数

```bash
export OPENAI_API_KEY="sk-..."
```

### 認証状態確認

```bash
codex --version
# エラーなく表示されれば認証済み
```

---

## 3. 実行モード詳細

### モード選択ガイド

| モード | 用途 | 推奨度 | 特徴 |
|--------|------|:------:|------|
| **完全自動** | Claude委譲、CI/CD | ⭐⭐⭐ | シンプル、安定、結果のみ取得 |
| **対話観察** | デバッグ、学習 | ⭐⭐ | tmuxで対話を観察可能 |
| **インタラクティブTUI** | 手動探索 | ⭐ | ユーザーが直接操作 |

---

### 完全自動モード（推奨）

```bash
codex exec "タスク内容" --approval-mode auto-edit
```

**Claudeからの委譲に最適。** 結果のみ返却され、対話プロセスは内部で処理される。

```bash
# 例
codex exec "このコードをレビューして改善点を指摘してください"
codex exec "Pythonでファイル名一括変更スクリプトを作成"
```

---

### 対話観察モード（tmux使用）

対話の過程をターミナルで観察したい場合に使用。詳細は [セクション10](#10-tmux永続セッションモード) を参照。

---

### インタラクティブTUI

```bash
codex
```

- フルスクリーンターミナルUI
- リアルタイム対話
- ファイル編集のプレビュー
- 操作の承認/拒否

**TUI内スラッシュコマンド**:
- `/model` - モデル切り替え
- `/mode` - 承認モード変更
- `/exit` または `Ctrl+C` - 終了

### スクリプト実行（codex exec）

```bash
codex exec "<タスク説明>"
```

**例**:
```bash
codex exec "Create a Python function that sorts a list" --approval-mode auto-edit
```

**用途**:
- CI/CDパイプライン
- 自動化スクリプト
- 単発タスク

### MCPサーバーモード

```bash
codex mcp
```

他のAIツール（Claude Desktop等）との統合用。

---

## 4. 承認モード詳細

### 決定マトリックス

| シナリオ | 推奨モード | 理由 |
|---------|-----------|------|
| 初めて使う | `--suggest` | 全操作を確認して学習 |
| 信頼できるコード編集 | `--auto-edit` | ファイル編集は自動化 |
| CI/CDパイプライン | `--full-auto` | 人間介入なし（制約付き） |
| テスト環境のみ | `--yolo` | 最大自動化（本番禁止） |

### モード比較

| モード | ファイル編集 | コマンド実行 | ネットワーク | リスク |
|--------|-------------|-------------|-------------|--------|
| `--suggest` | 確認必要 | 確認必要 | 確認必要 | 最低 |
| `--auto-edit` | 自動 | 確認必要 | 確認必要 | 低 |
| `--full-auto` | 自動 | 自動 | 自動 | 中 |
| `--yolo` | 自動 | 自動 | 自動 | 高 |

### コマンド例

```bash
# 最も安全
codex --suggest

# 開発時推奨
codex --auto-edit

# 自動化用
codex --full-auto

# テスト環境のみ（本番禁止）
codex --yolo
```

---

## 5. マルチエージェント連携パターン

### パターンA: Claude as Orchestrator

```
User Request
    │
    ▼
Claude (分析・計画)
    │
    ▼
Codex (コード生成・実行)
    │
    ▼
Claude (レビュー・統合)
    │
    ▼
User Response
```

**使用例**: 複雑な機能実装、リファクタリング

### パターンB: 並列実行

```
          ┌─ Claude (ドキュメント作成)
User ─────┤
          └─ Codex (コード生成)
                    │
                    ▼
              結果マージ
```

**使用例**: コードとドキュメントの同時生成

### パターンC: 反復改善

```
Claude → Codex → Claude → Codex → ... → 完了
  │        │        │        │
  ▼        ▼        ▼        ▼
要件定義  実装   レビュー  修正
```

**使用例**: コード品質向上、バグ修正

---

## 6. セッション管理

### セッション一覧

```bash
codex sessions
```

### セッション再開

```bash
codex resume
# または
codex resume <session-id>
```

### セッションフォーク

```bash
codex --fork <session-id>
```

既存セッションのコンテキストを継承して新セッション作成。

---

## 7. セキュリティ考慮事項

### サンドボックス

- Codexはデフォルトで作業ディレクトリ内のみアクセス
- `--full-auto`でもファイルシステム境界は維持
- センシティブファイル（`.env`, `credentials.json`等）は自動的にスキップ

### 推奨プラクティス

1. **本番環境では`--suggest`を使用**
2. **機密情報を含むディレクトリで実行しない**
3. **生成されたコードは必ずレビュー**
4. **CI/CDでは制約付き`--full-auto`**

### 禁止事項

- 本番環境での`--yolo`使用
- 機密情報を含むプロンプト送信
- 未レビューコードの本番デプロイ

---

## 8. トラブルシューティング

### よくある問題

| 問題 | 原因 | 解決策 |
|------|------|--------|
| `codex: command not found` | 未インストール | `brew install --cask codex` |
| 認証エラー | トークン期限切れ | `codex login` |
| Permission denied | 承認モード制限 | `--auto-edit`以上に変更 |
| セッション消失 | 予期せぬ終了 | `codex resume` |
| タイムアウト | 長時間タスク | tmux永続モード使用 |
| tmux起動時 `[exited]` | 直接コマンド渡し | 2段階起動: `tmux new -s codex` → `codex` |
| 送信が入力欄に溜まる | `Enter`が改行扱い | `C-m` (Ctrl-M) を使用 |

### デバッグ

```bash
# 詳細ログ出力
codex --debug

# 設定確認
cat ~/.codex/config.toml
```

---

## 9. コマンドリファレンス

### 基本コマンド

| コマンド | 説明 |
|---------|------|
| `codex` | インタラクティブTUI起動 |
| `codex exec "<task>"` | タスク実行 |
| `codex resume` | セッション再開 |
| `codex login` | 認証 |
| `codex mcp` | MCPサーバー起動 |
| `codex --upgrade` | アップグレード |

### オプション

| オプション | 説明 |
|-----------|------|
| `--suggest` | 全操作確認モード |
| `--auto-edit` | ファイル編集自動モード |
| `--full-auto` | 完全自動モード |
| `--yolo` | 無制限自動モード |
| `--model <name>` | モデル指定 |
| `--debug` | デバッグ出力 |
| `-c key=value` | 設定オーバーライド |
| `--search` | Web検索有効化 |

---

## 10. tmux永続セッションモード

> **推奨**: 通常の `codex exec` （完全自動モード）で十分な場合が多い。対話観察が必要な場合のみtmuxを使用。

### セットアップ（実証済み）

```bash
# セッション名は固定 "codex" を使用（シンプル化）
SESSION="codex"

# 1. tmuxセッション作成（コマンドを渡さない - 重要）
tmux new -s $SESSION

# 2. tmux内でcodex起動
codex --approval-mode auto-edit

# 3. 離脱（Codexは動作継続）
# Ctrl+B → D
```

### セッション操作

```bash
# セッション確認
tmux has-session -t codex 2>/dev/null && echo "EXISTS"

# セッション一覧
tmux ls

# セッションに接続（対話を観察）
tmux attach -t codex

# セッション終了
tmux kill-session -t codex
```

### プロンプト送信（実証済み）

> **重要**: `C-m` (Ctrl-M) を使用する。`Enter` は改行として解釈される場合がある。

```bash
# 正しい送信方法（実証済み）
tmux send-keys -t codex "プロンプト" && sleep 0.5 && tmux send-keys -t codex C-m

# 応答待ち＆キャプチャ
sleep 10 && tmux capture-pane -t codex -p -S -50
```

**避けるべきパターン**:
```bash
# NG: Enter は改行として解釈される場合がある
tmux send-keys -t codex "プロンプト" Enter

# NG: 直接コマンド渡しは [exited] になる
tmux new -s codex 'codex --approval-mode auto-edit'
```

### 出力キャプチャ

```bash
# 最新200行取得
tmux capture-pane -t codex -p -S -200

# 全履歴取得
tmux capture-pane -t codex -p -S -10000
```

### 完了検出

> **注意**: `❯` プロンプト検出はCodex CLIのバージョン/テーマに依存する可能性あり。安定運用には `codex exec` を推奨。

```bash
# プロンプト復帰（❯）を待つ
while ! tmux capture-pane -t codex -p | grep -q "❯"; do
    sleep 2
done
```

### マルチペイン構成（上級）

複数のCodexセッションを並列で運用する場合:

```bash
# 複数セッション作成
tmux new -s codex1
# (codex起動後、Ctrl+B → D)

tmux new -s codex2
# (codex起動後、Ctrl+B → D)

# 特定セッションに送信
tmux send-keys -t codex1 "タスク1" && sleep 0.5 && tmux send-keys -t codex1 C-m
tmux send-keys -t codex2 "タスク2" && sleep 0.5 && tmux send-keys -t codex2 C-m
```

---

## 11. オーケストレーターループ詳細

> **推奨**: 単発タスクには `codex exec` を使用。複雑な反復タスクのみ以下のループパターンを検討。

### 完全なループ実装

```bash
#!/bin/bash
# codex-orchestrator-loop.sh
# 注意: このスクリプトはtmuxセッションが事前に起動済みであることを前提とする

GOAL="$1"                    # ユーザー定義ゴール
MAX_LOOPS=${2:-10}           # デフォルト10回
TIMEOUT_MIN=${3:-30}         # デフォルト30分
POLL_INTERVAL=2              # 2秒間隔

SESSION="codex"              # 固定セッション名
START_TIME=$(date +%s)

# 前提: tmuxセッション "codex" が起動済み
# 起動方法: tmux new -s codex → codex --approval-mode auto-edit → Ctrl+B D
if ! tmux has-session -t $SESSION 2>/dev/null; then
    echo "ERROR: tmux session '$SESSION' not found. Start it first."
    exit 1
fi

loop_count=0
goal_achieved=false
prev_output=""
stuck_count=0

while [ "$goal_achieved" = false ] && [ $loop_count -lt $MAX_LOOPS ]; do
    elapsed=$(( ($(date +%s) - START_TIME) / 60 ))
    [ $elapsed -ge $TIMEOUT_MIN ] && break  # タイムアウト

    echo "=== Loop $((loop_count + 1))/$MAX_LOOPS (elapsed: ${elapsed}min) ==="

    # 2. Claudeが次の指示を決定（ここはClaude側で実行）
    # → capture-pane結果を分析し、next_promptを生成
    # next_prompt="..."

    # 3. Codexにプロンプト送信（C-m推奨）
    tmux send-keys -t $SESSION "$next_prompt" && sleep 0.5 && tmux send-keys -t $SESSION C-m

    # 4. 完了待ち（プロンプト復帰検出）
    echo "Waiting for Codex to complete..."
    timeout_count=0
    while ! tmux capture-pane -t $SESSION -p | grep -q "❯"; do
        sleep $POLL_INTERVAL
        timeout_count=$((timeout_count + 1))
        [ $timeout_count -gt 300 ] && break  # 10分でタイムアウト
    done

    # 5. 出力取得 → Claudeが評価
    output=$(tmux capture-pane -t $SESSION -p -S -500)

    # スタック検出（同一出力3回）
    if [ "$output" = "$prev_output" ]; then
        stuck_count=$((stuck_count + 1))
        [ $stuck_count -ge 3 ] && echo "STUCK: Same output 3 times" && break
    else
        stuck_count=0
    fi
    prev_output="$output"

    # → Claudeが$outputを見てgoal_achievedを判定
    # goal_achieved=true/false

    loop_count=$((loop_count + 1))
done

# 7. 最終報告
echo ""
echo "=== Final Report ==="
if [ "$goal_achieved" = true ]; then
    echo "SUCCESS: Goal achieved in $loop_count iterations"
else
    echo "INCOMPLETE: Stopped after $loop_count iterations"
    [ $elapsed -ge $TIMEOUT_MIN ] && echo "Reason: Timeout (${TIMEOUT_MIN}min)"
    [ $loop_count -ge $MAX_LOOPS ] && echo "Reason: Max loops reached ($MAX_LOOPS)"
    [ $stuck_count -ge 3 ] && echo "Reason: Stuck (same output 3 times)"
fi

# セッション維持（resumeのため）
echo "Session preserved at: $SOCKET (session: $SESSION)"
```

### ゴール判定パターン

| パターン | 検出方法 | 例 |
|---------|---------|---|
| テスト成功 | `grep -q "All tests passed"` | pytest, jest |
| ビルド成功 | `grep -q "Build successful"` | npm build, cargo build |
| エラーなし | `! grep -q "error\|Error\|ERROR"` | 汎用 |
| ファイル生成 | `test -f <expected_file>` | 特定ファイル確認 |
| カスタム | `grep -q "<custom_marker>"` | Codexに出力させる |

---

## 12. 既存ツール/プロジェクト参照

### 公式/準公式ツール

| ツール | 用途 | URL |
|--------|------|-----|
| Codex CLI | 本体 | https://developers.openai.com/codex/cli/ |
| Codex MCP | ツール統合 | `codex mcp` |

### コミュニティツール

| ツール | 用途 | 特徴 |
|--------|------|------|
| cld-tmux | 永続セッション | シンプル、tmux統合 |
| claude-code-tools | ターミナル自動化 | アイドル検出、遅延処理 |
| Agent Conductor | マルチエージェント | REST API、SQLite永続化 |
| Tmux Orchestrator | 24/7自律実行 | 自己トリガー、プロジェクト管理 |
| Agent Deck | セッション管理 | Go製、セッションフォーク |
| libtmux | Python制御 | プログラマティックtmux操作 |

### 参考リソース

- [Claude Code + tmux: The Ultimate Terminal Workflow](https://www.blle.co/blog/claude-code-tmux-beautiful-terminal)
- [Forking subagents in an AI coding session with tmux](https://kau.sh/blog/agent-forking/)
- [Tmux Orchestrator - Run AI agents 24/7](https://ktwu01.github.io/posts/2025/08/tmux-orchestrator/)

---

## 更新履歴

| バージョン | 日付 | 内容 |
|-----------|------|------|
| 1.0 | 2026-01-14 | 初版作成 |
| 1.1 | 2026-01-14 | tmux連携の実証済み手順追加（2段階起動、C-m送信） |
| 1.2 | 2026-01-14 | Codexレビュー反映: モード分離、完全自動を推奨に変更 |
| 1.3 | 2026-01-14 | Codex最終レビュー反映: SESSION/SOCKET統一、Enter→C-m統一 |
