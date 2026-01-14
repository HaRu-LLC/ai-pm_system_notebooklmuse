---
name: codex-cli
description: OpenAI Codex CLIを起動・操作するスキル。マルチエージェント連携、コード生成の委譲、サブエージェントとしてCodexを活用したいときに使う。
---

## 目的

ClaudeからOpenAI Codex CLIを起動・操作し、マルチエージェント協調を実現する。

- **マルチエージェント連携**: ClaudeとCodexで異なる視点からコード生成・レビュー
- **コード生成の委譲**: 特定のコーディングタスクをCodexに任せ、結果を統合
- **オーケストレーターループ**: ゴール達成までClaudeがCodexと自動的に対話を繰り返す

---

## トリガー語

- 「Codex CLIを起動」
- 「Codexでコード生成」
- 「Codexに委譲」
- 「Codexに任せて」
- 「マルチエージェントで作業」
- 「ClaudeとCodexで連携」
- 「Codexセッションを再開」
- 「Codexをtmuxで起動」
- 「ゴール達成までCodexでループ」

---

## 入力で最初に聞くこと

| # | 質問 | 目的 |
|---|------|------|
| 1 | **実行モード**: インタラクティブTUI / スクリプト実行 / オーケストレーターループ | 適切な実行方式を選択 |
| 2 | **タスク内容**: Codexに何をやらせたいか（自然言語で） | プロンプト準備、ゴール定義 |
| 3 | **承認モード**: suggest / auto-edit / full-auto | セキュリティレベル決定 |
| 4 | **永続モード（オプション）**: tmuxで永続化するか | セッション管理方式決定 |
| 5 | **制限設定（オプション）**: 最大ループ回数、タイムアウト | 無限ループ防止 |

---

## 手順

### Step 1: Pre-flight Check

```bash
# Codex CLIインストール確認
which codex || echo "NOT_INSTALLED"

# バージョン確認（認証状態も確認）
codex --version
```

**未インストールの場合**:
```bash
# Homebrew（macOS推奨）
brew install --cask codex

# npm（クロスプラットフォーム）
npm install -g @openai/codex
```

**未認証の場合**:
```bash
# OAuth認証（推奨）
codex login

# APIキー認証
codex login --with-api-key
```

### Step 2: モード選択

| モード | 用途 | コマンド | 推奨度 |
|--------|------|---------|:------:|
| **完全自動（推奨）** | Claude委譲、CI/CD | `codex exec "タスク"` | ⭐⭐⭐ |
| 対話観察 | デバッグ、学習 | `tmux` + `send-keys` | ⭐⭐ |
| インタラクティブTUI | 手動探索 | `codex` | ⭐ |
| MCPサーバー | ツール統合 | `codex mcp` | - |

### Step 3: 承認モード設定

| モード | リスク | 用途 | コマンド |
|--------|--------|------|---------|
| `--suggest` | 低 | 全操作を確認（推奨デフォルト） | `codex --suggest` |
| `--auto-edit` | 中 | ファイル編集は自動、実行は確認 | `codex --auto-edit` |
| `--full-auto` | 高 | ネットワーク含め自動 | `codex --full-auto` |
| `--yolo` | 危険 | 全て自動（要注意） | `codex --yolo` |

### Step 4: 実行

**A. インタラクティブTUI（手動操作）**
```bash
codex --approval-mode auto-edit
```
ユーザーが直接対話する場合に使用。

---

**B. 完全自動モード（推奨）**
```bash
codex exec "タスク内容" --approval-mode auto-edit
```
**Claudeからの委譲に最適。** シンプルで安定。結果のみ取得。

```bash
# 例: レビュー依頼
codex exec "SKILL.mdとREFERENCE.mdをレビューして改善点を指摘してください"

# 例: コード生成
codex exec "Pythonでファイル名一括変更スクリプトを作成"
```

---

**C. 対話観察モード（tmux使用）**

対話の過程をターミナルで観察したい場合に使用。

> **セットアップ（ユーザーが実行）**
```bash
# 1. tmuxセッション作成
tmux new -s codex

# 2. tmux内でcodex起動
codex --approval-mode auto-edit

# 3. セッションから離脱（Codexは動作継続）
# Ctrl+B → D
```

> **Claudeからの操作**
```bash
# メッセージ送信（C-m推奨）
tmux send-keys -t codex "タスク内容" && sleep 0.5 && tmux send-keys -t codex C-m

# 応答キャプチャ
sleep 10 && tmux capture-pane -t codex -p -S -50
```

> **セッション管理**
```bash
tmux ls                      # セッション確認
tmux attach -t codex         # 接続（対話を観察）
# Ctrl+B → D                 # 離脱
tmux kill-session -t codex   # 終了
```

**実証済みの注意点**:
- `tmux new -s codex 'codex'` は `[exited]` になるため、2段階で起動
- `Enter` より `C-m` (Ctrl-M) を推奨（実証で安定動作を確認）
- テキスト送信と `C-m` の間に `sleep 0.5` を挟む

**完了検出の制限**:
- `❯` プロンプト検出はCodex CLIのバージョン/テーマに依存する可能性あり
- 安定運用には **完全自動モード（B）** を推奨

### Step 5: オーケストレーターループ詳細

**ループフロー**:
```
while (ゴール未達成 && ループ < MAX && 時間 < TIMEOUT):
    1. Claudeが次の指示を決定（前回出力を分析）
    2. tmux send-keysでCodexに送信
    3. capture-paneで完了待ち
    4. Claudeが出力を評価
       - ゴール達成 → ループ終了
       - 進捗あり → 次の指示生成
       - エラー → 修正指示生成
       - スタック（3回同一エラー） → 介入要求
    5. ループカウンタ++
```

**ゴール判定ロジック（Claude判断）**:

| 判定 | 条件例 | アクション |
|------|--------|-----------|
| ゴール達成 | テスト全パス、ファイル生成完了、エラー0 | ループ終了、成功報告 |
| 進捗あり | 一部完了、次ステップ明確 | 次の指示を生成して継続 |
| エラー発生 | コンパイルエラー、テスト失敗 | 修正指示を生成して継続 |
| スタック | 同じエラー3回連続、進捗なし | 介入要求 or 戦略変更 |

**制限パラメータ**:
```yaml
limits:
  max_loops: 10          # 最大ループ回数
  timeout_minutes: 30    # タイムアウト（分）
  poll_interval_sec: 2   # ポーリング間隔（秒）
  max_output_lines: 500  # capture-pane取得行数
  stuck_threshold: 3     # 同一エラー許容回数
```

### Step 6: 結果統合

1. Codex出力をキャプチャ
2. 変更されたファイル一覧を取得
3. セッション情報を記録（再開用）
4. Claudeワークフローに結果を統合

---

## 成果物

| 成果物 | 必須 | 説明 |
|--------|:----:|------|
| 実行ログ | Yes | Codexのターミナル出力 |
| 変更ファイル一覧 | Yes | Codexが作成/編集したファイル |
| セッションID | Optional | `codex resume`用のID |
| tmuxセッション情報 | Optional | ソケットパス、セッション名 |
| ループ履歴 | Optional | 各イテレーションの指示と結果 |
| ゴール達成証拠 | Yes | テスト結果、生成物の確認 |

---

## 検証（完了条件）

- [ ] Codex CLIがインストールされている
- [ ] 認証が成功している
- [ ] 指定したタスクが実行された
- [ ] 出力/変更が文書化されている
- [ ] Claudeへのハンドオフが完了している
- [ ] （オーケストレーターループの場合）ゴールが達成されている

---

## 参照

- Reference: [REFERENCE.md](./REFERENCE.md) - 詳細なコマンドリファレンス、トラブルシューティング
- OpenAI Codex CLI: https://developers.openai.com/codex/cli/
- tmux: https://github.com/tmux/tmux
