---
name: progress-report
description: 進捗報告書を作成する。定期進捗報告、マイルストーンレビュー時に使う。
phase: executing
pmbok-area: communications
---

## 目的

プロジェクトの進捗状況を報告し、課題・リスクを共有する。

## トリガー語

- 「進捗報告書を作成」
- 「進捗をまとめる」
- 「ステータスレポート」

---

## 入力で最初に聞くこと

| # | 質問 | 必須 |
|---|------|------|
| 1 | **プロジェクト名**は？ | ✓ |
| 2 | **報告期間**は？ | ✓ |

---

## 手順

### Step 1: 進捗率の算出
### Step 2: 主要タスクの状況
### Step 3: 課題・リスクの更新
### Step 4: 保存
- `workspace/{ProjectName}/docs/ProgressReport_YYYYMMDD.md`

---

## 成果物

| 成果物 | 保存先 |
|--------|--------|
| 進捗報告書 | `workspace/{ProjectName}/docs/ProgressReport_YYYYMMDD.md` |

---

## 検証（完了条件）

- [ ] 進捗率が記載されている
- [ ] 予実差異がある場合は分析されている
- [ ] 次のアクションが明記されている

---

## 参照

- Command: `.claude/commands/02_aipjm_03_executing_03_progress_report.md`
