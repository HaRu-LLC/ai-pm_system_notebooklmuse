# Gemini API統合仕様書

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 作成日: 2026-01-05
- 版: v1.0
- 関連文書: api_spec.md (v1.1), db_schema.md (v1.1), exercises/Chapter1-4_Rubrics.md

---

## 1. 概要

### 1.1 目的

本仕様書は、Gemini APIを使用した課題自動評価機能の実装詳細を定義する。

### 1.2 システム構成

```
┌──────────────────────────────────────────────────────────────┐
│                        受講者                                 │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼ 課題提出
┌──────────────────────────────────────────────────────────────┐
│                      Webアプリ (Next.js)                      │
│  ┌─────────────────┐    ┌─────────────────┐                  │
│  │  提出API         │───▶│  評価Job Queue   │                  │
│  └─────────────────┘    └────────┬────────┘                  │
└──────────────────────────────────│───────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────┐
│                   Gemini API (gemini-1.5-flash)              │
│  ┌─────────────────────────────────────────────┐             │
│  │  Structured Output (response_schema)        │             │
│  └─────────────────────────────────────────────┘             │
└──────────────────────────────────────────────────────────────┘
                                   │
                                   ▼ 評価結果
┌──────────────────────────────────────────────────────────────┐
│                      Supabase                                │
│  ┌─────────────────┐    ┌─────────────────┐                  │
│  │  evaluations     │    │  notifications   │                 │
│  └─────────────────┘    └─────────────────┘                  │
└──────────────────────────────────────────────────────────────┘
```

### 1.3 使用モデル

| 項目 | 設定 |
|---|---|
| モデル | gemini-1.5-flash |
| 選定理由 | コスト効率、高速応答（評価用途に最適） |
| 出力形式 | Structured Output (response_schema) |
| 最大トークン | 8,192 tokens |
| 温度 | 0.3（一貫性重視） |

---

## 2. 評価プロンプト設計

### 2.1 共通評価基準（4軸 × 25点 = 100点）

| 評価軸 | 配点 | 評価観点 |
|---|---|---|
| **elements** | 25点 | 4要素の充足度（指示・文脈・制約・出力形式） |
| **practicality** | 25点 | 実践性（業務で使えるか、具体的で再現可能か） |
| **creativity** | 25点 | 創意工夫（独自の工夫、効果的なテクニック） |
| **completeness** | 25点 | 完成度（必要な要素が揃っているか、論理的整合性） |

### 2.2 Phase別評価プロンプトテンプレート

#### Phase 1: 手書きプロンプト基礎（Session 1-3）

```markdown
# プロンプト評価アシスタント - Phase 1

あなたは「AIポリテラシー育成プログラム Ver.2」のPhase 1課題評価担当AIです。
受講者が提出したプロンプトを評価し、建設的なフィードバックを提供します。

## 評価対象課題
課題ID: {{exercise_code}}
課題タイトル: {{exercise_title}}

## 提出内容
{{submission_content}}

## 評価基準

### 1. 4要素の充足度（25点）
- **指示（Instruction）**: 何をしてほしいかが明確か
- **文脈（Context）**: 状況や背景が適切に設定されているか
- **制約（Constraints）**: 具体的な条件や制限が明示されているか
- **出力形式（Format）**: 期待する出力形式が指定されているか

### 2. 実践性（25点）
- 実際の業務で使えるレベルか
- 具体的で再現可能か
- 曖昧さがないか

### 3. 創意工夫（25点）
- 独自の工夫があるか
- 課題の意図を超えた発展があるか
- 効果的なテクニックを使っているか

### 4. 完成度（25点）
- 必要な要素が揃っているか
- 誤字脱字がないか
- 論理的に整合しているか

## 評価ガイドライン
- 初学者向けに励ましを含めたフィードバックを心がける
- 具体的な改善例を1つ以上示す
- 「し・ぶ・せ・だ」（指示・文脈・制約・出力形式）の観点で評価

## 出力
指定されたJSON形式で評価結果を出力してください。
```

#### Phase 2: メタプロンプト設計（Session 4-5）

```markdown
# プロンプト評価アシスタント - Phase 2

あなたは「AIポリテラシー育成プログラム Ver.2」のPhase 2課題評価担当AIです。
メタプロンプト設計に焦点を当てた評価を行います。

## 評価対象課題
課題ID: {{exercise_code}}
課題タイトル: {{exercise_title}}

## 提出内容
{{submission_content}}

## Phase 2特有の評価観点

### 1. メタプロンプトの構造（elements: 25点）
- 汎用性のあるテンプレート構造か
- 変数化が適切か（{{目的}}、{{条件}}など）
- 再利用可能な形式か

### 2. 生成されるプロンプトの品質（practicality: 25点）
- メタプロンプトから生成されるプロンプトの品質
- 様々な用途に対応できるか
- 出力の一貫性があるか

### 3. 設計の工夫（creativity: 25点）
- メタプロンプト設計の独自性
- 効率的なテンプレート構造
- エッジケースへの対応

### 4. 完成度（completeness: 25点）
- メタプロンプトとして完成しているか
- 使用方法が明確か
- テスト例が含まれているか

## 評価ガイドライン
- 「プロンプトを生成するプロンプト」としての価値を評価
- 汎用性と具体性のバランスを重視
- 実際にメタプロンプトを使った例を想像して評価

## 出力
指定されたJSON形式で評価結果を出力してください。
```

#### Phase 3: GPTs構築（Session 6-10）

```markdown
# プロンプト評価アシスタント - Phase 3

あなたは「AIポリテラシー育成プログラム Ver.2」のPhase 3課題評価担当AIです。
GPTs設計・構築に焦点を当てた評価を行います。

## 評価対象課題
課題ID: {{exercise_code}}
課題タイトル: {{exercise_title}}

## 提出内容
{{submission_content}}

## Phase 3特有の評価観点

### 1. GPTs設計の妥当性（elements: 25点）
- Instructions設計の適切さ
- 知識ベースの構成
- ユーザー体験の設計

### 2. 業務適用性（practicality: 25点）
- 実際の業務課題を解決できるか
- ターゲットユーザーに適しているか
- 運用を考慮した設計か

### 3. 設計の工夫（creativity: 25点）
- GPTs設計の独自性
- メタプロンプトを活用した設計プロセス
- 知識ベースの効果的な活用

### 4. 仕様書の完成度（completeness: 25点）
- 必要な設計要素が網羅されているか
- テストケースが含まれているか
- 運用ガイドラインがあるか

## 評価ガイドライン
- GPTsとしての実用性を重視
- メタプロンプトを使った設計プロセスを評価
- 「使える」GPTsかどうかを判断

## 出力
指定されたJSON形式で評価結果を出力してください。
```

#### Phase 4: 業務GPTs実運用（Session 11-12）

```markdown
# プロンプト評価アシスタント - Phase 4

あなたは「AIポリテラシー育成プログラム Ver.2」のPhase 4課題評価担当AIです。
業務GPTsの実運用と最終成果物に焦点を当てた評価を行います。

## 評価対象課題
課題ID: {{exercise_code}}
課題タイトル: {{exercise_title}}

## 提出内容
{{submission_content}}

## Phase 4特有の評価観点

### 1. 業務課題の分析力（elements: 25点）
- 業務フローの理解度
- ボトルネックの特定
- AI適用ポイントの妥当性

### 2. GPTs運用の実践性（practicality: 25点）
- 5回以上の使用ログ
- 実際のフィードバックと改善
- 運用上の課題と対策

### 3. 改善と工夫（creativity: 25点）
- フィードバックに基づく改善
- 運用を通じた発見
- 独自の活用方法

### 4. 成果物の完成度（completeness: 25点）
- GPTs仕様書の完成度
- 運用ログの詳細さ
- 振り返りの深さ

## 評価ガイドライン
- 「作って終わり」ではなく「使って改善」を評価
- 運用ログの質を重視
- 最終発表に向けた準備状況を確認

## 出力
指定されたJSON形式で評価結果を出力してください。
```

---

## 3. Structured Output スキーマ

### 3.1 response_schema定義

```json
{
  "type": "object",
  "properties": {
    "score": {
      "type": "integer",
      "description": "総合スコア（0-100）",
      "minimum": 0,
      "maximum": 100
    },
    "breakdown": {
      "type": "object",
      "description": "評価軸別スコア",
      "properties": {
        "elements": {
          "type": "integer",
          "description": "4要素の充足度（0-25）",
          "minimum": 0,
          "maximum": 25
        },
        "practicality": {
          "type": "integer",
          "description": "実践性（0-25）",
          "minimum": 0,
          "maximum": 25
        },
        "creativity": {
          "type": "integer",
          "description": "創意工夫（0-25）",
          "minimum": 0,
          "maximum": 25
        },
        "completeness": {
          "type": "integer",
          "description": "完成度（0-25）",
          "minimum": 0,
          "maximum": 25
        }
      },
      "required": ["elements", "practicality", "creativity", "completeness"]
    },
    "good_points": {
      "type": "array",
      "description": "良かった点（1-3項目）",
      "items": { "type": "string" },
      "minItems": 1,
      "maxItems": 3
    },
    "improvements": {
      "type": "array",
      "description": "改善のアドバイス（1-3項目）",
      "items": { "type": "string" },
      "minItems": 1,
      "maxItems": 3
    },
    "next_step": {
      "type": "string",
      "description": "次のステップへのヒント"
    }
  },
  "required": ["score", "breakdown", "good_points", "improvements", "next_step"]
}
```

### 3.2 レスポンス例

```json
{
  "score": 85,
  "breakdown": {
    "elements": 22,
    "practicality": 21,
    "creativity": 20,
    "completeness": 22
  },
  "good_points": [
    "4要素（指示・文脈・制約・出力形式）が明確に構成されています",
    "業務シーンが具体的で、実際に使えるプロンプトになっています",
    "出力形式の指定が詳細で、期待通りの結果が得やすい設計です"
  ],
  "improvements": [
    "制約条件に「〇〇の場合は△△する」のような条件分岐を加えると、より堅牢になります",
    "ペルソナ設定をより具体的にすると、応答の一貫性が向上します"
  ],
  "next_step": "Session 2では、今回作成したプロンプトにペルソナ設定を追加してみましょう。「あなたは〇〇の専門家です」のような役割設定を加えることで、より専門的な応答を引き出せます。"
}
```

---

## 4. API呼び出し実装

### 4.1 TypeScript実装例

```typescript
import { GoogleGenerativeAI, SchemaType } from "@google/generative-ai";

// 評価結果の型定義
interface EvaluationResult {
  score: number;
  breakdown: {
    elements: number;
    practicality: number;
    creativity: number;
    completeness: number;
  };
  good_points: string[];
  improvements: string[];
  next_step: string;
}

// Gemini APIクライアント初期化
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);

// response_schema定義
const evaluationSchema = {
  type: SchemaType.OBJECT,
  properties: {
    score: { type: SchemaType.INTEGER },
    breakdown: {
      type: SchemaType.OBJECT,
      properties: {
        elements: { type: SchemaType.INTEGER },
        practicality: { type: SchemaType.INTEGER },
        creativity: { type: SchemaType.INTEGER },
        completeness: { type: SchemaType.INTEGER },
      },
      required: ["elements", "practicality", "creativity", "completeness"],
    },
    good_points: {
      type: SchemaType.ARRAY,
      items: { type: SchemaType.STRING },
    },
    improvements: {
      type: SchemaType.ARRAY,
      items: { type: SchemaType.STRING },
    },
    next_step: { type: SchemaType.STRING },
  },
  required: ["score", "breakdown", "good_points", "improvements", "next_step"],
};

// 評価実行関数
async function evaluateSubmission(
  exerciseCode: string,
  exerciseTitle: string,
  submissionContent: string,
  phase: number
): Promise<EvaluationResult> {
  const model = genAI.getGenerativeModel({
    model: "gemini-1.5-flash",
    generationConfig: {
      temperature: 0.3,
      maxOutputTokens: 8192,
      responseMimeType: "application/json",
      responseSchema: evaluationSchema,
    },
  });

  // Phase別プロンプトを取得
  const systemPrompt = getPhasePrompt(phase);

  // プロンプトに変数を埋め込み
  const prompt = systemPrompt
    .replace("{{exercise_code}}", exerciseCode)
    .replace("{{exercise_title}}", exerciseTitle)
    .replace("{{submission_content}}", submissionContent);

  const result = await model.generateContent(prompt);
  const response = result.response;
  const text = response.text();

  return JSON.parse(text) as EvaluationResult;
}

// Phase別プロンプト取得
function getPhasePrompt(phase: number): string {
  const prompts: Record<number, string> = {
    1: PHASE1_PROMPT,
    2: PHASE2_PROMPT,
    3: PHASE3_PROMPT,
    4: PHASE4_PROMPT,
  };
  return prompts[phase] || PHASE1_PROMPT;
}
```

### 4.2 API設定パラメータ

| パラメータ | 値 | 説明 |
|---|---|---|
| model | gemini-1.5-flash | コスト効率重視 |
| temperature | 0.3 | 一貫性を高める |
| maxOutputTokens | 8192 | 十分な出力長 |
| responseMimeType | application/json | JSON形式を強制 |
| responseSchema | evaluationSchema | Structured Output |

---

## 5. エラーハンドリング

### 5.1 リトライ戦略

```typescript
interface RetryConfig {
  maxRetries: number;
  initialDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
}

const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxRetries: 3,
  initialDelayMs: 1000,
  maxDelayMs: 30000,
  backoffMultiplier: 2,
};

async function evaluateWithRetry(
  submission: Submission,
  config: RetryConfig = DEFAULT_RETRY_CONFIG
): Promise<EvaluationResult | null> {
  let lastError: Error | null = null;
  let delay = config.initialDelayMs;

  for (let attempt = 1; attempt <= config.maxRetries; attempt++) {
    try {
      const result = await evaluateSubmission(
        submission.exercise_code,
        submission.exercise_title,
        submission.content,
        submission.phase
      );

      // バリデーション
      if (validateEvaluationResult(result)) {
        return result;
      }
      throw new Error("Invalid evaluation result structure");

    } catch (error) {
      lastError = error as Error;
      console.error(`Attempt ${attempt} failed:`, error);

      if (attempt < config.maxRetries) {
        await sleep(delay);
        delay = Math.min(delay * config.backoffMultiplier, config.maxDelayMs);
      }
    }
  }

  // 全リトライ失敗 → 手動評価キューへ
  await addToManualQueue(submission, lastError?.message || "Unknown error");
  return null;
}

function validateEvaluationResult(result: any): result is EvaluationResult {
  return (
    typeof result.score === "number" &&
    result.score >= 0 && result.score <= 100 &&
    typeof result.breakdown === "object" &&
    typeof result.breakdown.elements === "number" &&
    typeof result.breakdown.practicality === "number" &&
    typeof result.breakdown.creativity === "number" &&
    typeof result.breakdown.completeness === "number" &&
    Array.isArray(result.good_points) &&
    Array.isArray(result.improvements) &&
    typeof result.next_step === "string"
  );
}
```

### 5.2 エラー種別と対応

| エラー種別 | HTTPステータス | 対応 |
|---|---|---|
| 認証エラー | 401 | APIキー確認、即時通知 |
| レート制限 | 429 | 指数バックオフでリトライ |
| サーバーエラー | 500/503 | リトライ（最大3回） |
| タイムアウト | - | 30秒でタイムアウト、リトライ |
| スキーマ不正 | - | リトライ、失敗時は手動キューへ |

### 5.3 手動評価キューへのフォールバック

```typescript
async function addToManualQueue(
  submission: Submission,
  reason: string
): Promise<void> {
  // 1. submissionsテーブルのstatusを更新
  await supabase
    .from("submissions")
    .update({ status: "manual_queue" })
    .eq("id", submission.id);

  // 2. 管理者へ通知メール送信
  await sendEmail({
    to: ADMIN_EMAIL,
    subject: `[手動評価必要] ${submission.exercise_code}`,
    body: `
      提出ID: ${submission.id}
      受講者: ${submission.user_name}
      課題: ${submission.exercise_title}
      失敗理由: ${reason}

      管理画面から手動評価を行ってください。
    `,
  });

  // 3. 受講者へ待機通知
  await sendEmail({
    to: submission.user_email,
    subject: "【評価中】課題の評価について",
    body: `
      ${submission.user_name}様

      提出いただいた課題「${submission.exercise_title}」は
      現在評価中です。評価完了までもう少々お待ちください。

      評価完了後、改めてご連絡いたします。
    `,
  });
}
```

---

## 6. コスト管理

### 6.1 想定コスト試算

| 項目 | 数値 | 備考 |
|---|---|---|
| 受講者数 | 30名 | 初期想定 |
| 課題数/人 | 24課題 | 必須12 + 任意12 |
| 総提出数/期 | 720件 | 30 × 24（全員全提出時） |
| 入力トークン/件 | ~2,000 | プロンプト + 提出内容 |
| 出力トークン/件 | ~500 | JSON評価結果 |
| 総トークン/期 | ~1.8M | (2,000 + 500) × 720 |

### 6.2 gemini-1.5-flash 料金

| 項目 | 単価 | 想定コスト |
|---|---|---|
| 入力 | $0.075 / 1M tokens | ~$0.11 |
| 出力 | $0.30 / 1M tokens | ~$0.11 |
| **合計** | - | **~$0.22/期** |

> **注**: 実際のコストは提出頻度やリトライ回数により変動。月間$30以内を目標。

### 6.3 コスト監視

```typescript
// コスト追跡用の監視関数
async function trackApiUsage(
  inputTokens: number,
  outputTokens: number,
  submissionId: string
): Promise<void> {
  await supabase.from("api_usage_logs").insert({
    submission_id: submissionId,
    input_tokens: inputTokens,
    output_tokens: outputTokens,
    estimated_cost_usd: calculateCost(inputTokens, outputTokens),
    created_at: new Date().toISOString(),
  });
}

function calculateCost(inputTokens: number, outputTokens: number): number {
  const inputCost = (inputTokens / 1_000_000) * 0.075;
  const outputCost = (outputTokens / 1_000_000) * 0.30;
  return inputCost + outputCost;
}
```

---

## 7. モデル更新時の再校正

### 7.1 校正プロセス

Geminiモデルのアップデート時は以下の再校正を実施：

1. **校正用サンプル準備**（5件固定）
   - 高スコア例（85点以上）: 2件
   - 中スコア例（60-84点）: 2件
   - 低スコア例（59点以下）: 1件

2. **再評価実行**
   - 5件のサンプルを新モデルで再評価
   - 旧モデルとのスコア差を計測

3. **ドリフト判定**
   - 平均スコア差が±15点以内: 許容
   - ±15点超: プロンプト調整が必要

### 7.2 校正用サンプル管理

```sql
-- 校正用サンプルテーブル
CREATE TABLE calibration_samples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exercise_code VARCHAR(10) NOT NULL,
    content TEXT NOT NULL,
    expected_score INT NOT NULL,
    expected_breakdown JSONB NOT NULL,
    category VARCHAR(20) NOT NULL, -- 'high', 'medium', 'low'
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 8. セキュリティ考慮事項

### 8.1 プロンプトインジェクション対策

```typescript
function sanitizeSubmissionContent(content: string): string {
  // 制御文字の除去
  let sanitized = content.replace(/[\x00-\x1F\x7F]/g, "");

  // 過度に長い入力の切り詰め
  const MAX_LENGTH = 10000;
  if (sanitized.length > MAX_LENGTH) {
    sanitized = sanitized.substring(0, MAX_LENGTH) + "\n[以下省略]";
  }

  return sanitized;
}
```

### 8.2 APIキー管理

| 環境 | 管理方法 |
|---|---|
| 開発 | .env.local（gitignore） |
| ステージング | Vercel環境変数 |
| 本番 | Vercel環境変数（暗号化） |

---

## 9. 変更履歴

| バージョン | 日付 | 変更内容 |
|---|---|---|
| v1.0 | 2026-01-05 | 初版作成 |

---

## 承認

| 役割 | 氏名 | 承認日 |
|---|---|---|
| プログラムマネージャー | AI-PgM | 2026-01-05 |
| バックエンドエンジニア | - | - |
