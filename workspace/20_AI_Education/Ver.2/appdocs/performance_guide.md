# パフォーマンスガイド

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 作成日: 2026-01-06
- 版: v1.0
- 関連文書: monitoring_spec.md, infrastructure_spec.md, test_plan.md

---

## 1. パフォーマンス目標

### 1.1 Core Web Vitals 目標

| 指標 | 目標 | 許容限界 | 測定方法 |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s | < 4.0s | Vercel Analytics |
| **FID** (First Input Delay) | < 100ms | < 300ms | Vercel Analytics |
| **CLS** (Cumulative Layout Shift) | < 0.1 | < 0.25 | Vercel Analytics |
| **INP** (Interaction to Next Paint) | < 200ms | < 500ms | Vercel Analytics |
| **TTFB** (Time to First Byte) | < 800ms | < 1.8s | Vercel Analytics |

### 1.2 API パフォーマンス目標

| API 種別 | 目標（P95） | 許容限界 | 備考 |
|---|---|---|---|
| 一覧取得 | < 200ms | < 500ms | ページネーション適用 |
| 詳細取得 | < 100ms | < 300ms | キャッシュ活用 |
| 作成・更新 | < 300ms | < 1s | DB書き込み含む |
| 課題評価（Gemini） | < 10s | < 30s | LLM処理時間含む |
| ファイルアップロード | < 5s | < 15s | 10MBまで |

### 1.3 その他の目標

| 項目 | 目標 | 測定方法 |
|---|---|---|
| 初期バンドルサイズ（JS） | < 150KB (gzip) | Bundle Analyzer |
| 初期バンドルサイズ（CSS） | < 30KB (gzip) | Bundle Analyzer |
| Lighthouse Performance | > 90 | Lighthouse CI |
| 同時接続ユーザー | 100人 | k6負荷テスト |

---

## 2. フロントエンド最適化

### 2.1 Next.js App Router 最適化

#### 2.1.1 サーバーコンポーネントの活用

```tsx
// ✅ Good: データフェッチはサーバーコンポーネントで
// app/sessions/[id]/page.tsx
export default async function SessionPage({ params }: { params: { id: string } }) {
  // サーバーサイドでデータ取得（クライアントにJSを送らない）
  const session = await getSession(params.id);
  const exercises = await getExercises(params.id);

  return (
    <div>
      <SessionHeader session={session} />
      <ExerciseList exercises={exercises} />
    </div>
  );
}

// ❌ Bad: クライアントで不要なデータフェッチ
'use client';
export default function SessionPage({ params }) {
  const [session, setSession] = useState(null);
  useEffect(() => {
    fetch(`/api/sessions/${params.id}`).then(...);
  }, []);
  // ...
}
```

#### 2.1.2 Streaming と Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';

export default function DashboardPage() {
  return (
    <div>
      {/* 即座に表示される部分 */}
      <DashboardHeader />

      {/* データ取得を待つ部分は Suspense で囲む */}
      <Suspense fallback={<ProgressSkeleton />}>
        <ProgressSection />
      </Suspense>

      <Suspense fallback={<SubmissionsSkeleton />}>
        <RecentSubmissions />
      </Suspense>
    </div>
  );
}
```

#### 2.1.3 動的インポート

```tsx
// 重いコンポーネントは動的インポート
import dynamic from 'next/dynamic';

// チャートライブラリは遅延読み込み
const ProgressChart = dynamic(() => import('@/components/charts/ProgressChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // クライアントのみでレンダリング
});

// PDFビューアは必要時のみ読み込み
const PdfViewer = dynamic(() => import('@/components/PdfViewer'), {
  loading: () => <div>Loading PDF viewer...</div>,
});
```

### 2.2 画像最適化

#### 2.2.1 next/image の使用

```tsx
import Image from 'next/image';

// ✅ Good: next/image で自動最適化
<Image
  src="/images/session-thumbnail.jpg"
  alt="Session 1"
  width={400}
  height={225}
  priority={true}  // LCP画像には priority
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>

// ❌ Bad: 通常のimg タグ
<img src="/images/session-thumbnail.jpg" />
```

#### 2.2.2 画像フォーマット・サイズ指針

| 用途 | フォーマット | 最大サイズ | 備考 |
|---|---|---|---|
| サムネイル | WebP | 50KB | 400x225px |
| アイコン | SVG/PNG | 10KB | 32x32〜64x64px |
| 背景 | WebP | 100KB | 圧縮品質75% |
| ユーザーアバター | WebP | 20KB | 100x100px |

### 2.3 コード分割

#### 2.3.1 ルートベースの分割

Next.js App Router は自動でルートベースの分割を行います。

```
app/
├── (auth)/          # 認証関連（別バンドル）
│   ├── login/
│   └── register/
├── (learner)/       # 受講者機能（別バンドル）
│   ├── dashboard/
│   ├── sessions/
│   └── submissions/
└── (admin)/         # 管理機能（別バンドル）
    ├── users/
    └── reports/
```

#### 2.3.2 共有コンポーネントの最適化

```tsx
// ❌ Bad: 全てを1つのファイルからエクスポート
export { Button, Card, Modal, Table, Chart, ... } from '@/components/ui';

// ✅ Good: 必要なものだけインポート
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
```

### 2.4 キャッシュ戦略

#### 2.4.1 ブラウザキャッシュ

```typescript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*.{js,css,woff2,ico,png,jpg,webp}',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/api/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'no-store, max-age=0',
          },
        ],
      },
    ];
  },
};
```

#### 2.4.2 React Query によるデータキャッシュ

```tsx
// lib/queries/sessions.ts
import { useQuery } from '@tanstack/react-query';

export function useSessions() {
  return useQuery({
    queryKey: ['sessions'],
    queryFn: fetchSessions,
    staleTime: 5 * 60 * 1000,    // 5分間はキャッシュを使用
    gcTime: 30 * 60 * 1000,      // 30分間キャッシュを保持
    refetchOnWindowFocus: false, // フォーカス時の再取得を無効化
  });
}

export function useSubmissions(userId: string) {
  return useQuery({
    queryKey: ['submissions', userId],
    queryFn: () => fetchSubmissions(userId),
    staleTime: 1 * 60 * 1000,    // 1分間はキャッシュを使用
  });
}
```

### 2.5 バンドルサイズ分析

**セットアップ**:

```bash
# @next/bundle-analyzer をインストール（devDependencies）
npm install --save-dev @next/bundle-analyzer
```

```typescript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // ...その他の設定
});
```

```json
// package.json に追加
{
  "scripts": {
    "analyze": "ANALYZE=true next build"
  }
}
```

**実行方法**:

```bash
# バンドル分析の実行（正しい方法）
npm run analyze

# または直接環境変数を指定
ANALYZE=true npm run build
```

**注意**: `npx @next/bundle-analyzer` は CLI ツールではないため動作しません。
必ず `ANALYZE=true npm run build` または `npm run analyze` で実行してください。

分析完了後、ブラウザで以下のレポートが自動的に開きます:
- `client.html`: クライアントサイドバンドル
- `server.html`: サーバーサイドバンドル

---

## 3. バックエンド最適化

### 3.1 データベースクエリ最適化

#### 3.1.1 N+1 問題の回避

```typescript
// ❌ Bad: N+1 問題
const submissions = await prisma.submission.findMany();
for (const sub of submissions) {
  const evaluation = await prisma.evaluation.findFirst({
    where: { submissionId: sub.id }
  });
}

// ✅ Good: include で一括取得
const submissions = await prisma.submission.findMany({
  include: {
    evaluation: {
      where: { isActive: true },
    },
    exercise: true,
  },
});
```

#### 3.1.2 必要なフィールドのみ取得

```typescript
// ❌ Bad: 全フィールド取得
const users = await prisma.user.findMany();

// ✅ Good: 必要なフィールドのみ
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    email: true,
  },
});
```

#### 3.1.3 ページネーション

```typescript
// 一覧取得は必ずページネーション
const submissions = await prisma.submission.findMany({
  where: { userId },
  take: 20,           // 1ページあたり20件
  skip: (page - 1) * 20,
  orderBy: { submittedAt: 'desc' },
  include: {
    exercise: { select: { id: true, title: true } },
    evaluation: { select: { score: true } },
  },
});

// 総件数も取得（カウントクエリを別で実行）
const total = await prisma.submission.count({
  where: { userId },
});
```

### 3.2 インデックス戦略

#### 3.2.1 既存インデックス（db_schema.md より）

```sql
-- users
CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_role ON users(role) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_status ON users(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_cohort_id ON users(cohort_id) WHERE deleted_at IS NULL;

-- submissions
CREATE INDEX idx_submissions_user_id ON submissions(user_id);
CREATE INDEX idx_submissions_exercise_id ON submissions(exercise_id);
CREATE INDEX idx_submissions_status ON submissions(status);
CREATE INDEX idx_submissions_submitted_at ON submissions(submitted_at);

-- evaluations
CREATE INDEX idx_evaluations_submission_id ON evaluations(submission_id);
CREATE INDEX idx_evaluations_is_active ON evaluations(is_active);
```

#### 3.2.2 追加推奨インデックス

```sql
-- 受講者進捗表示の高速化（複合インデックス）
CREATE INDEX idx_submissions_user_status
  ON submissions(user_id, status)
  WHERE status = 'evaluated';

-- 管理画面の受講者一覧（コホート + ステータス）
CREATE INDEX idx_users_cohort_status
  ON users(cohort_id, status)
  WHERE deleted_at IS NULL;

-- 評価待ち一覧の高速化
CREATE INDEX idx_submissions_pending
  ON submissions(status, submitted_at)
  WHERE status IN ('submitted', 'evaluating');
```

### 3.3 キャッシュ戦略

#### 3.3.1 Next.js のキャッシュ機能

```typescript
// app/api/sessions/route.ts
import { unstable_cache } from 'next/cache';

const getSessions = unstable_cache(
  async () => {
    return prisma.session.findMany({
      where: { isPublished: true },
      orderBy: { number: 'asc' },
    });
  },
  ['sessions'],
  {
    revalidate: 3600, // 1時間キャッシュ
    tags: ['sessions'],
  }
);

export async function GET() {
  const sessions = await getSessions();
  return Response.json(sessions);
}
```

#### 3.3.2 キャッシュ無効化

```typescript
// セッション公開時にキャッシュを無効化
import { revalidateTag } from 'next/cache';

export async function publishSession(sessionId: string) {
  await prisma.session.update({
    where: { id: sessionId },
    data: { isPublished: true, publishedAt: new Date() },
  });

  // キャッシュを無効化
  revalidateTag('sessions');
}
```

### 3.4 API レスポンス最適化

#### 3.4.1 レスポンス圧縮

```typescript
// next.config.js
module.exports = {
  compress: true, // gzip圧縮を有効化（デフォルトで有効）
};
```

#### 3.4.2 不要なデータの除去

```typescript
// ❌ Bad: 内部情報をレスポンスに含める
return Response.json({
  ...user,
  encryptedPassword: user.encryptedPassword,  // 危険！
  loginFailedCount: user.loginFailedCount,     // 不要
});

// ✅ Good: 必要なフィールドのみ返す
return Response.json({
  id: user.id,
  name: user.name,
  email: user.email,
  role: user.role,
});
```

---

## 4. Gemini API 最適化

### 4.1 トークン削減

#### 4.1.1 プロンプトの最適化

```typescript
// ❌ Bad: 冗長なプロンプト
const prompt = `
あなたは優秀な教育者です。生徒の提出物を評価してください。
評価する際は、以下の点に注意してください：
- 基本要素が含まれているか
- 実用性があるか
- 創意工夫があるか
- 完成度は高いか
それぞれ25点満点で採点し、詳細なフィードバックを...
（長い説明が続く）
`;

// ✅ Good: 簡潔で構造化されたプロンプト
const prompt = `
課題評価:
- 基本要素(25点): 4要素の有無
- 実用性(25点): 業務活用可能性
- 創意工夫(25点): 独自性
- 完成度(25点): 完成度

提出物:
${submission.content}

JSON形式で回答: {score, breakdown, goodPoints, improvements}
`;
```

#### 4.1.2 コンテキスト長の制限

```typescript
// 提出物の長さを制限
const MAX_CONTENT_LENGTH = 4000; // 約2000トークン相当

function truncateContent(content: string): string {
  if (content.length <= MAX_CONTENT_LENGTH) {
    return content;
  }
  return content.slice(0, MAX_CONTENT_LENGTH) + '\n...[以下省略]';
}
```

### 4.2 並列処理とバッチ

#### 4.2.1 評価の並列実行

```typescript
// 複数の提出物を並列評価（レート制限に注意）
async function evaluateSubmissions(submissions: Submission[]) {
  const BATCH_SIZE = 5;
  const results = [];

  for (let i = 0; i < submissions.length; i += BATCH_SIZE) {
    const batch = submissions.slice(i, i + BATCH_SIZE);
    const batchResults = await Promise.all(
      batch.map(sub => evaluateWithRetry(sub))
    );
    results.push(...batchResults);

    // レート制限対策: バッチ間で待機
    if (i + BATCH_SIZE < submissions.length) {
      await sleep(1000); // 1秒待機
    }
  }

  return results;
}
```

### 4.3 リトライとフォールバック

```typescript
// lib/gemini.ts
const MAX_RETRIES = 3;
const RETRY_DELAYS = [1000, 2000, 4000]; // 指数バックオフ

async function evaluateWithRetry(submission: Submission): Promise<EvaluationResult> {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
    try {
      return await callGeminiApi(submission);
    } catch (error) {
      lastError = error as Error;

      if (isRateLimitError(error)) {
        // レート制限: 長めに待機
        await sleep(RETRY_DELAYS[attempt] * 2);
      } else if (isTemporaryError(error)) {
        // 一時的エラー: 通常のリトライ
        await sleep(RETRY_DELAYS[attempt]);
      } else {
        // 永続的エラー: リトライしない
        break;
      }
    }
  }

  // リトライ失敗: 手動評価キューへ
  await queueForManualReview(submission, lastError);
  throw lastError;
}
```

---

## 5. 負荷テスト

### 5.1 k6 による負荷テスト

#### 5.1.1 インストールと設定

```bash
# macOS
brew install k6

# テストスクリプト作成
mkdir -p tests/load
```

#### 5.1.2 基本シナリオ

```javascript
// tests/load/basic.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 20 },   // 1分で20ユーザーに増加
    { duration: '3m', target: 20 },   // 3分間維持
    { duration: '1m', target: 50 },   // 1分で50ユーザーに増加
    { duration: '3m', target: 50 },   // 3分間維持
    { duration: '2m', target: 0 },    // 2分で0に減少
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95%が500ms以下
    http_req_failed: ['rate<0.01'],    // エラー率1%未満
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://staging.ai-politeracy.example.com';

export default function () {
  // セッション一覧取得
  const sessionsRes = http.get(`${BASE_URL}/api/v1/sessions`);
  check(sessionsRes, {
    'sessions status is 200': (r) => r.status === 200,
    'sessions response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);

  // ダッシュボード取得
  const dashboardRes = http.get(`${BASE_URL}/api/v1/learner/dashboard`, {
    headers: { Authorization: `Bearer ${__ENV.TEST_TOKEN}` },
  });
  check(dashboardRes, {
    'dashboard status is 200': (r) => r.status === 200,
  });

  sleep(2);
}
```

#### 5.1.3 課題提出シナリオ

```javascript
// tests/load/submission.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 20,
  duration: '5m',
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    http_req_failed: ['rate<0.05'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://staging.ai-politeracy.example.com';

export default function () {
  // 課題取得
  const exerciseRes = http.get(`${BASE_URL}/api/v1/exercises/ex-01`, {
    headers: { Authorization: `Bearer ${__ENV.TEST_TOKEN}` },
  });

  check(exerciseRes, {
    'exercise fetched': (r) => r.status === 200,
  });

  sleep(5); // ユーザーが課題を読む時間

  // 課題提出
  const submitRes = http.post(
    `${BASE_URL}/api/v1/submissions`,
    JSON.stringify({
      exerciseId: 'ex-01',
      content: generateTestContent(),
    }),
    {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${__ENV.TEST_TOKEN}`,
      },
    }
  );

  check(submitRes, {
    'submission created': (r) => r.status === 201 || r.status === 200,
    'submission response time < 1s': (r) => r.timings.duration < 1000,
  });

  sleep(10); // 次の操作まで待機
}

function generateTestContent() {
  return `
【指示】週次報告書を作成してください
【文脈】プロジェクトAの進捗報告、チームメンバー5名
【制約】箇条書き、300字以内
【出力形式】Markdown形式
  `.trim();
}
```

#### 5.1.4 テスト実行

```bash
# 基本テスト
k6 run tests/load/basic.js

# 環境変数を指定して実行
k6 run -e BASE_URL=https://staging.example.com \
       -e TEST_TOKEN=xxx \
       tests/load/submission.js

# 結果をJSONで出力
k6 run --out json=results.json tests/load/basic.js
```

### 5.2 パフォーマンステスト結果の目安

| シナリオ | VUs | 目標 RPS | 目標 P95 | 許容エラー率 |
|---|---|---|---|---|
| セッション一覧 | 50 | 100 | < 200ms | < 0.1% |
| ダッシュボード | 50 | 50 | < 500ms | < 0.5% |
| 課題提出 | 20 | 10 | < 1s | < 1% |
| 評価取得 | 30 | 30 | < 300ms | < 0.5% |

---

## 6. 監視とアラート

### 6.1 パフォーマンス監視項目

| 項目 | 測定方法 | アラート条件 | 対応 |
|---|---|---|---|
| LCP | Vercel Analytics | > 4s（5分間） | フロントチーム通知 |
| API P95 | Vercel Logs | > 1s（5分間） | バックエンドチーム通知 |
| エラー率 | Sentry | > 1%（10分間） | 即時調査 |
| DB接続数 | Supabase Dashboard | > 80% | 接続プール調整 |

### 6.2 Vercel Analytics でのモニタリング

```typescript
// lib/monitoring.ts
import { track } from '@vercel/analytics';

// カスタムパフォーマンス計測
export function measureApiCall(endpoint: string, startTime: number) {
  const duration = Date.now() - startTime;

  track('api_performance', {
    endpoint,
    duration_ms: duration,
    threshold_exceeded: duration > 500,
  });

  if (duration > 1000) {
    console.warn(`Slow API call: ${endpoint} took ${duration}ms`);
  }
}

// 使用例
export async function fetchWithTiming(url: string) {
  const start = Date.now();
  try {
    const response = await fetch(url);
    return response;
  } finally {
    measureApiCall(url, start);
  }
}
```

---

## 7. パフォーマンスバジェット

### 7.1 バジェット定義

```json
// .lighthouserc.json
{
  "ci": {
    "assert": {
      "budgets": [
        {
          "resourceSizes": [
            { "resourceType": "script", "budget": 150 },
            { "resourceType": "stylesheet", "budget": 30 },
            { "resourceType": "image", "budget": 200 },
            { "resourceType": "document", "budget": 50 },
            { "resourceType": "total", "budget": 500 }
          ],
          "resourceCounts": [
            { "resourceType": "script", "budget": 15 },
            { "resourceType": "third-party", "budget": 5 }
          ]
        }
      ],
      "preset": "lighthouse:recommended",
      "assertions": {
        "first-contentful-paint": ["error", { "maxNumericValue": 2000 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["error", { "maxNumericValue": 300 }]
      }
    }
  }
}
```

### 7.2 CI でのバジェットチェック

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI

on:
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm ci && npm run build

      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

---

## 8. 最適化チェックリスト

### 8.1 フロントエンド

```
□ Server Components をデフォルトで使用
□ 'use client' は必要な場合のみ追加
□ 重いコンポーネントは dynamic import
□ next/image で画像を最適化
□ Suspense でストリーミング
□ React Query でデータキャッシュ
□ バンドルサイズを定期的に分析
□ 不要な依存関係を削除
```

### 8.2 バックエンド

```
□ Prisma の include/select を適切に使用
□ N+1 クエリを排除
□ 一覧APIはページネーション必須
□ 適切なインデックスを設定
□ キャッシュを活用
□ 不要なフィールドを返さない
□ レスポンス圧縮を有効化
```

### 8.3 Gemini API

```
□ プロンプトを簡潔に
□ 入力長を制限
□ リトライロジックを実装
□ レート制限を考慮
□ 並列処理でバッチ化
□ 失敗時のフォールバック
```

### 8.4 本番デプロイ前

```
□ Lighthouse スコア > 90
□ バンドルサイズがバジェット内
□ 負荷テストで目標達成
□ Core Web Vitals が目標内
□ 主要APIのP95が目標内
□ エラー率が許容範囲内
```

---

## 更新履歴

| 日付 | バージョン | 変更内容 |
|---|---|---|
| 2026-01-06 | v1.0 | 初版作成 |
| 2026-01-06 | v1.1 | bundle-analyzer の正しい実行方法を追記 |
