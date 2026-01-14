# Skill テンプレート

新しいSkillを作成する際の雛形。

---

## 使用方法

1. 対象ディレクトリにコピー（例: `planning/requirements/`）
2. ファイル名を `SKILL.md` に変更
3. 以下のプレースホルダを実際の内容に置換

---

## テンプレート本体

```markdown
---
name: <skill-name>
description: <1行説明（トリガー語を含む）>
phase: initiating | planning | executing | closing | cross-cutting
pmbok-area: <知識エリア>
---

## 目的

<このSkillが解決する課題・提供する価値>

## トリガー語

- 「〇〇を作成」
- 「〇〇を生成」

---

## 入力で最初に聞くこと

| # | 質問 | 目的 |
|---|------|------|
| 1 | <質問1> | <目的> |
| 2 | <質問2> | <目的> |

---

## 手順

### Step 1: <ステップ名>
<具体的なアクション>

### Step 2: <ステップ名>
<具体的なアクション>

---

## 出力テンプレート

```
# <成果物タイトル>

## 1. セクション1
<内容>

## 2. セクション2
<内容>
```

---

## 成果物

| 成果物 | 保存先 |
|--------|--------|
| <成果物名> | `workspace/{ProjectName}/docs/<filename>.md` |

---

## 検証（完了条件）

- [ ] <条件1>
- [ ] <条件2>

---

## 参照

- Command: `.claude/commands/<command-name>.md`
- Workflow: `.agent/workflows/<workflow>.md`
```

---

## ベストプラクティス

1. **500行以下**に保つ
2. 詳細は `REFERENCE.md` に分離
3. テンプレートは `templates/` に配置
4. 参照は1レベル深いまで
