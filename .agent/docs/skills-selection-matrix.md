# Skills Selection Matrix

タスク種別に応じた Skills 選定ガイド。

---

## カテゴリ別 Skills 一覧

### Engineering - コード生成・開発

| Skill | 用途 | トリガー語 |
|-------|------|-----------|
| `codex-cli` | コード生成、マルチエージェント連携 | 「Codexで生成」「コード作成」 |
| `test-driven-development` | TDD 強制、テストファースト | 「TDDで」「テスト駆動」 |
| `systematic-debugging` | 根本原因分析、デバッグ | 「デバッグ」「原因調査」 |
| `verification-before-completion` | 完了前検証 | 「検証して」「確認して」 |

### Engineering - 計画・実行

| Skill | 用途 | トリガー語 |
|-------|------|-----------|
| `brainstorming` | 協調的設計プロセス | 「設計を練る」「アイデア出し」 |
| `writing-plans` | 実装計画書作成 | 「計画を作成」「プラン作成」 |
| `executing-plans` | 計画に基づく実行 | 「計画を実行」「プラン実行」 |
| `subagent-driven-development` | タスク分割、2段階レビュー | 「サブエージェントで」 |
| `dispatching-parallel-agents` | 並列エージェント派遣 | 「並列で調査」「同時に処理」 |
| `using-git-worktrees` | 分離ワークスペース作成 | 「worktree作成」「並列ブランチ」 |

### Engineering - ドキュメント処理

| Skill | 用途 | トリガー語 |
|-------|------|-----------|
| `docx` | Word ファイル操作 | 「Word作成」「.docx」 |
| `pdf` | PDF ファイル操作 | 「PDF作成」「.pdf」 |
| `pptx` | PowerPoint 操作 | 「スライド作成」「.pptx」 |
| `xlsx` | Excel ファイル操作 | 「Excel作成」「.xlsx」 |

### Engineering - その他

| Skill | 用途 | トリガー語 |
|-------|------|-----------|
| `playwright` | ブラウザ自動化、Webテスト | 「ブラウザ操作」「スクレイピング」 |

### PM - プロジェクト管理

| Skill | 用途 | トリガー語 |
|-------|------|-----------|
| `project-charter` | プロジェクト憲章作成 | 「プロジェクト立ち上げ」「憲章作成」 |
| `requirements` | 要件定義書作成 | 「要件定義」「仕様書作成」 |
| `risk-register` | リスク登録簿作成 | 「リスク管理」「リスク登録」 |
| `weekly-status` | 週次レポート作成 | 「週次報告」「進捗レポート」 |
| `meeting-minutes` | 議事録作成 | 「議事録」「会議メモ」 |

---

## タスク→Skills マッピング

| ユーザー要求 | 推奨 Skills | 備考 |
|-------------|------------|------|
| 「コードを書いて」 | `codex-cli` | Codex に委譲 |
| 「テストを作成して」 | `test-driven-development` | TDD 強制 |
| 「バグを調査して」 | `systematic-debugging` | 根本原因分析 |
| 「設計を考えて」 | `brainstorming` | 協調的設計 |
| 「計画を立てて」 | `writing-plans` | 実装計画書 |
| 「複数のことを同時に」 | `dispatching-parallel-agents` | 並列処理 |
| 「プロジェクト開始」 | `project-charter` | PM 立ち上げ |
| 「要件をまとめて」 | `requirements` | 要件定義 |
| 「リスクを洗い出して」 | `risk-register` | リスク管理 |
| 「今週の進捗は」 | `weekly-status` | 週次レポート |
| 「会議の内容をまとめて」 | `meeting-minutes` | 議事録 |
| 「Word で出力」 | `docx` | Office 出力 |
| 「スライドを作成」 | `pptx` | PowerPoint |
| 「Webサイトを確認」 | `playwright` | ブラウザ操作 |

---

## 組み合わせパターン

### パターン1: 設計→実装→テスト

```
brainstorming → codex-cli → test-driven-development
```

新機能開発の標準フロー。

### パターン2: 並列調査→統合

```
dispatching-parallel-agents → (複数 Skill 並列) → 統合
```

複数の独立した問題を同時調査。

### パターン3: 委譲→レビュー→修正

```
subagent-driven-development → (実装+レビュー) → 修正
```

2段階レビュー付きの品質保証フロー。

### パターン4: PM プロジェクト立ち上げ

```
project-charter → requirements → risk-register
```

新規プロジェクトの標準初期化フロー。

### パターン5: 週次定例

```
weekly-status → (issue 確認) → risk-register 更新
```

定期的な進捗管理フロー。

---

## Skills 選定の判断基準

1. **タスクの性質**: コード? ドキュメント? 調査?
2. **複雑さ**: 単一 Skill で完結? 組み合わせ必要?
3. **並列性**: 独立したタスク? 依存関係あり?
4. **品質要件**: レビュー必要? 検証必要?

### 選定フローチャート

```
タスク受信
    ↓
コード関連? → YES → codex-cli, TDD, debugging
    ↓ NO
ドキュメント? → YES → docx, pptx, pdf, xlsx
    ↓ NO
PM タスク? → YES → project-charter, requirements, etc.
    ↓ NO
調査・分析? → YES → playwright, parallel-agents
    ↓ NO
設計・計画? → YES → brainstorming, writing-plans
```
