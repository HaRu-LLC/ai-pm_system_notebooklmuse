---
description: Skills仕様化・生成のためのワークフロー（./agent/skills配下にSKILL.mdを生成）
---

# Skill Factory（Skills生成ワークフロー）

新しいSkillを設計・生成するためのワークフロー。

---

## 入力

1. **Skill名**（英語、ハイフン区切り推奨）
2. **想定ユーザー発話**（トリガー語句のリスト）
3. **成果物**（何を生成するか）
4. **禁止事項**（やってはいけないこと）
5. **カテゴリ**（business / pm / engineering / meta）

---

## 手順

### Step 1: name / description確定
- トリガー精度を最優先
- description は「何をするSkillか」を1行で

### Step 2: SKILL.md雛形生成

```markdown
---
name: <skill-name>
description: <1行説明>
---

## 目的
<このSkillの目的>

## 入力で最初に聞くこと
- <質問1>
- <質問2>

## 手順
1. <ステップ1>
2. <ステップ2>
...

## 成果物
- <成果物1>
- <成果物2>

## 検証（完了条件）
- <条件1>
- <条件2>
```

### Step 3: 詳細情報の分離
- 詳細な参照情報は `REFERENCE.md` に分離
- テンプレートは `templates/` に配置

---

## 成果物

| 成果物 | 配置先 |
|--------|--------|
| `SKILL.md` | `.agent/skills/<category>/<skill-name>/SKILL.md` |
| `REFERENCE.md`（任意） | 同ディレクトリ |
| テンプレート（任意） | `.agent/templates/<category>/` |

---

## 完了条件

- [ ] SKILL.mdが作成されている
- [ ] name / description がYAMLフロントマターで定義されている
- [ ] registry.md に対応情報が追記されている() 

---

## registry.mdへの登録

Skill作成後、以下を `.agent/registry.md` に追記：

```markdown
| <skill-name> | /05_meta_skill_factory | .agent/skills/<category>/<skill-name>/ |
```
