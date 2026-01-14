# 3-Step Orchestration Framework

Skills-First Orchestrator の実行フレームワーク。

---

## Step 1: Goal Clarification (Plan Mode)

**目的**: ユーザー要求を正確に理解し、成功基準を定義

### プロセス

1. **要求受信**: ユーザーからのタスク依頼
2. **明確化質問**（最大3つ）:
   - 何を達成したいか？
   - 成功の定義は？
   - 制約や前提は？
3. **成功基準定義**: 定量的・定性的基準を明文化
4. **ユーザー合意**: 進める前に確認

### 成功基準テンプレート

```yaml
goal:
  description: "XXXを達成する"
  success_criteria:
    - テスト全件パス
    - ファイル X, Y, Z が生成されている
    - エラー 0
  constraints:
    - 既存コードを破壊しない
    - 30分以内に完了
```

---

## Step 2: Plan Creation (Plan Mode)

**目的**: ゴール達成のための具体的計画を作成

### プロセス

1. **Skills確認**: 利用可能な Skills をリストアップ
2. **タスク分解**: 大きなタスクを小さなステップに分割
3. **Skill割当**: 各ステップに適した Skill を選定
4. **順序設計**: 依存関係と並列実行可能部分を整理
5. **制約設定**: タイムアウト、試行回数上限

### 計画テンプレート

```yaml
plan:
  name: "実装計画: XXX"
  created: YYYY-MM-DD

  steps:
    - id: 1
      skill: brainstorming
      description: "設計方針を決定"
      success: "設計ドキュメント作成完了"

    - id: 2
      skill: codex-cli
      description: "コード生成"
      depends_on: [1]
      success: "ファイル生成完了"

    - id: 3
      skill: test-driven-development
      description: "テスト作成・実行"
      depends_on: [2]
      success: "テスト全件パス"

  limits:
    max_attempts: 10
    timeout_minutes: 60
```

---

## Step 3: Execution Loop

**目的**: 計画に基づき、ゴール達成まで Skills を呼び出し続ける

### ループロジック

```
attempts = 0
MAX_ATTEMPTS = 10
TIMEOUT = 60 minutes

while (goal not achieved):
    if attempts >= MAX_ATTEMPTS:
        report_failure("Max attempts reached")
        break

    if elapsed_time >= TIMEOUT:
        report_failure("Timeout")
        break

    # 1. 現状評価
    current_state = evaluate_progress()

    # 2. 次のアクション決定
    next_skill, params = select_next_action(current_state, plan)

    # 3. Skill 実行
    result = execute_skill(next_skill, params)

    # 4. 結果評価
    if result.success:
        if goal_achieved(result):
            report_success()
            break
        else:
            continue  # 次のステップへ
    else:
        if same_error_count >= 3:
            escalate_to_user()
        else:
            adjust_approach()

    attempts++
```

### 評価基準マトリックス

| 状態 | 条件 | アクション |
|------|------|-----------|
| ゴール達成 | 成功基準全て満たす | ループ終了、成功報告 |
| 進捗あり | 一部完了 | 次のステップへ継続 |
| エラー | Skill実行失敗 | 修正試行 or 別Skill選択 |
| スタック | 同一エラー3回 | ユーザーに介入要請 |

---

## 制限パラメータ

```yaml
limits:
  max_attempts: 10        # 最大試行回数
  timeout_minutes: 60     # タイムアウト
  stuck_threshold: 3      # 同一エラー許容回数
  escalation_trigger: 3   # ユーザー介入トリガー
```

---

## Orchestrator Principles

### DO
- Skills を選択・実行する
- 実行結果を評価する
- 次のアクションを判断する
- ユーザーへ進捗報告する

### DON'T
- 直接コードを書く（→ `codex-cli` を使う）
- 直接ファイルを編集する（→ 適切な Skill を使う）
- 手動でテストを実行する（→ `test-driven-development` を使う）

### 例外
以下の場合のみ、直接作業を許可:
1. 利用可能な Skill がない単純タスク
2. Skill 実行のオーバーヘッドが大きすぎる軽微な修正
3. ユーザーが明示的に「直接やって」と指示した場合
