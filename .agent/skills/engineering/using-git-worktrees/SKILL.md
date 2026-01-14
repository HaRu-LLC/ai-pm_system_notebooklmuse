---
name: using-git-worktrees
description: Git Worktreeスキル。共有リポジトリ内で分離されたワークスペースを作成し、並列ブランチ作業を可能に。
source: https://github.com/obra/superpowers/tree/main/skills/using-git-worktrees
---

## 目的

共有リポジトリ内で分離されたワークスペースを作成。コンテキスト切り替えなしで並列ブランチ作業を可能にする。

---

## トリガー語

- 「worktreeを作成」
- 「並列ブランチで作業」
- 「分離ワークスペース」
- 「Git worktree」

---

## ディレクトリ選択優先順位

1. 既存の `.worktrees/` または `worktrees/` ディレクトリ
2. CLAUDE.md で指定された設定
3. ユーザー入力（プロジェクトローカル or グローバル選択）

---

## 重要なセーフティステップ

> **プロジェクトローカルディレクトリの場合、worktree作成前にgitignore登録を確認必須**

「worktreeコンテンツの誤コミット」を防ぐ。

---

## セットアップシーケンス

worktree作成後：

1. **プロジェクトタイプ自動検出**
   - Node, Rust, Python, Go 等

2. **依存関係インストール実行**
   - 適切なパッケージマネージャーを使用

3. **ベースラインテスト実行**
   - クリーンな開始点を確立

4. **レポート**
   - worktree場所とテストステータスを報告

---

## メインレッドフラグ

| 警告 | 対応 |
|------|------|
| プロジェクトローカルでgitignore未確認 | 確認してから作成 |
| ベースラインテスト失敗 | 続行前に明示的許可を要求 |

---

## 関連スキル

- **brainstorming**: ワークフロー統合
- **finishing-a-development-branch**: クリーンアップ用

---

## ライセンス

MIT License (superpowers repository)
