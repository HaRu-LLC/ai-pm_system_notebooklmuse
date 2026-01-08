# 監視・ログ設計書

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 作成日: 2026-01-05
- 版: v1.0
- 関連文書: infrastructure_spec.md (v1.0), api_spec.md (v1.3), runbook.md

---

## 1. 概要

### 1.1 監視方針

| 方針 | 説明 |
|---|---|
| **オブザーバビリティ** | ログ・メトリクス・トレースの3本柱で可視化 |
| **プロアクティブ監視** | 問題発生前に異常を検知・アラート |
| **コスト効率** | 無料枠・低コストサービスを最大活用 |
| **シンプル構成** | 小規模チームで運用可能な設計 |

### 1.2 監視スタック

| 領域 | サービス | 用途 | 費用 |
|---|---|---|---|
| **APM** | Vercel Analytics | Webパフォーマンス | 無料（Hobby） |
| **エラー追跡** | Sentry | エラー検知・通知 | 無料（5K events/月） |
| **ログ** | Vercel Logs | アプリケーションログ | 無料 |
| **稼働監視** | Vercel（組み込み） | デプロイ・稼働状況 | 無料 |
| **外形監視** | UptimeRobot | 死活監視 | 無料（50モニター） |
| **DB監視** | Supabase Dashboard | PostgreSQL監視 | 無料 |

---

## 2. APM（Application Performance Monitoring）

### 2.1 Vercel Analytics設定

**有効化**:
```typescript
// next.config.js
module.exports = {
  experimental: {
    instrumentationHook: true,
  },
};

// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

### 2.2 監視メトリクス

| メトリクス | 説明 | 目標値 | アラート閾値 |
|---|---|---|---|
| **LCP** | Largest Contentful Paint | < 2.5s | > 4.0s |
| **FID** | First Input Delay | < 100ms | > 300ms |
| **CLS** | Cumulative Layout Shift | < 0.1 | > 0.25 |
| **TTFB** | Time to First Byte | < 800ms | > 1.8s |
| **INP** | Interaction to Next Paint | < 200ms | > 500ms |

### 2.3 カスタムイベント追跡

```typescript
// lib/analytics.ts
import { track } from '@vercel/analytics';

// 動画視聴トラッキング
export function trackVideoView(sessionId: number, partNumber: number, progress: number) {
  track('video_view', {
    session_id: sessionId,
    part: partNumber,
    progress_percent: progress,
  });
}

// 課題提出トラッキング
export function trackExerciseSubmission(exerciseId: number, timeSpent: number) {
  track('exercise_submission', {
    exercise_id: exerciseId,
    time_spent_minutes: timeSpent,
  });
}

// エラートラッキング
export function trackError(errorType: string, context: Record<string, unknown>) {
  track('error_occurred', {
    error_type: errorType,
    ...context,
  });
}
```

---

## 3. エラー追跡（Sentry）

### 3.1 Sentry設定

**インストール**:
```bash
npm install @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

**設定ファイル**:
```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,

  // パフォーマンストレース
  tracesSampleRate: 0.1, // 10%サンプリング

  // リプレイ（エラー時のみ）
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,

  integrations: [
    Sentry.replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],

  // 無視するエラー
  ignoreErrors: [
    'ResizeObserver loop limit exceeded',
    'Non-Error exception captured',
  ],
});
```

```typescript
// sentry.server.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
});
```

### 3.2 カスタムエラーコンテキスト

```typescript
// lib/sentry.ts
import * as Sentry from '@sentry/nextjs';

// ユーザーコンテキスト設定
export function setUserContext(user: { id: string; email: string; role: string }) {
  Sentry.setUser({
    id: user.id,
    email: user.email,
    role: user.role,
  });
}

// カスタムタグ追加
export function setSessionContext(sessionId: number, exerciseId?: number) {
  Sentry.setTags({
    session_id: sessionId,
    exercise_id: exerciseId,
  });
}

// 手動エラー送信
export function captureApiError(endpoint: string, error: Error, context?: Record<string, unknown>) {
  Sentry.withScope((scope) => {
    scope.setTag('api_endpoint', endpoint);
    scope.setContext('request_context', context || {});
    Sentry.captureException(error);
  });
}
```

### 3.3 エラー分類

| 重要度 | 分類 | 例 | 対応 |
|---|---|---|---|
| **Critical** | サービス停止 | DB接続失敗、認証基盤障害 | 即時対応 |
| **Error** | 機能障害 | API 500エラー、評価失敗 | 1時間以内 |
| **Warning** | 品質低下 | レスポンス遅延、リトライ発生 | 24時間以内 |
| **Info** | 情報 | 設定変更、デプロイ完了 | 定期確認 |

---

## 4. ログ設計

### 4.1 ログレベル

| レベル | 用途 | 出力先 |
|---|---|---|
| **ERROR** | 例外、障害 | Sentry + Vercel Logs |
| **WARN** | 警告、リトライ | Vercel Logs |
| **INFO** | 重要イベント | Vercel Logs |
| **DEBUG** | 詳細情報 | 開発環境のみ |

### 4.2 構造化ログ

```typescript
// lib/logger.ts
type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogContext {
  userId?: string;
  sessionId?: number;
  exerciseId?: number;
  requestId?: string;
  [key: string]: unknown;
}

function log(level: LogLevel, message: string, context?: LogContext) {
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    message,
    ...context,
  };

  if (level === 'error') {
    console.error(JSON.stringify(entry));
  } else if (level === 'warn') {
    console.warn(JSON.stringify(entry));
  } else {
    console.log(JSON.stringify(entry));
  }
}

export const logger = {
  debug: (message: string, context?: LogContext) => log('debug', message, context),
  info: (message: string, context?: LogContext) => log('info', message, context),
  warn: (message: string, context?: LogContext) => log('warn', message, context),
  error: (message: string, context?: LogContext) => log('error', message, context),
};
```

### 4.3 ログ出力ポイント

| イベント | ログレベル | 出力内容 |
|---|---|---|
| ユーザーログイン | INFO | user_id, ip, user_agent |
| 動画視聴開始 | INFO | user_id, session_id, part |
| 動画視聴完了 | INFO | user_id, session_id, part, duration |
| 課題提出 | INFO | user_id, exercise_id, content_length |
| 評価開始 | INFO | submission_id, evaluator (gemini/manual) |
| 評価完了 | INFO | submission_id, score, processing_time |
| 評価失敗 | ERROR | submission_id, error_type, error_message |
| API呼び出し（Gemini） | INFO | request_id, model, token_count |
| APIエラー | ERROR | endpoint, status_code, error_body |
| 認証失敗 | WARN | email, failure_reason, ip |

---

## 5. アラート設定

### 5.1 アラートチャネル

| チャネル | 用途 | 設定先 |
|---|---|---|
| **Slack** | 即時通知（Critical/Error） | #alerts-ai-politeracy |
| **Email** | 日次サマリー | admin@example.com |
| **PagerDuty** | オンコール（本番Critical） | 将来対応 |

### 5.2 Sentryアラートルール

```yaml
# Critical: サービス停止
- name: "Critical - Service Down"
  conditions:
    - event.type == "error"
    - event.tags.level == "critical"
  actions:
    - notify: slack-channel
    - notify: email
  frequency: immediate

# Error: API障害
- name: "Error - API Failure Spike"
  conditions:
    - count(events) > 10 in 5 minutes
    - event.tags.category == "api"
  actions:
    - notify: slack-channel
  frequency: 5 minutes

# Warning: パフォーマンス低下
- name: "Warning - Slow Response"
  conditions:
    - avg(transaction.duration) > 3000ms in 10 minutes
  actions:
    - notify: slack-channel
  frequency: 30 minutes
```

### 5.3 UptimeRobot設定

| モニター | URL | 間隔 | アラート条件 |
|---|---|---|---|
| 本番ヘルスチェック | /api/health | 5分 | 2回連続失敗 |
| 本番ログイン画面 | /login | 5分 | 2回連続失敗 |
| Staging環境 | staging.../api/health | 15分 | 3回連続失敗 |

---

## 6. ダッシュボード設計

### 6.1 運用ダッシュボード（Vercel）

**URL**: `https://vercel.com/{team}/{project}/analytics`

**表示項目**:
- リアルタイムアクセス数
- Core Web Vitals（LCP/FID/CLS）
- ページ別パフォーマンス
- デバイス・ブラウザ分布
- 地域分布

### 6.2 エラーダッシュボード（Sentry）

**URL**: `https://sentry.io/organizations/{org}/issues/`

**表示項目**:
- 未解決エラー一覧
- エラートレンド
- 影響ユーザー数
- リリース別エラー率

### 6.3 ビジネスダッシュボード（カスタム）

**実装**: 管理画面内 `/admin/dashboard`

| KPI | 説明 | 更新頻度 |
|---|---|---|
| アクティブ受講者数 | 過去7日間にログインしたユーザー | リアルタイム |
| 動画視聴完了率 | 全セッションの平均視聴完了率 | 日次 |
| 課題提出率 | 必須課題の平均提出率 | 日次 |
| 平均評価スコア | 全課題の平均スコア | 日次 |
| 自動評価成功率 | Gemini評価の成功率 | 日次 |
| 修了予測 | 現在のペースでの修了見込み人数 | 週次 |

### 6.4 ダッシュボードSQL例

```sql
-- アクティブ受講者数
SELECT COUNT(DISTINCT user_id) AS active_learners
FROM viewing_logs
WHERE created_at > NOW() - INTERVAL '7 days';

-- 動画視聴完了率（チェックイン方式）
-- Note: 現行スキーマではviewing_logsはchecked_in_at（視聴完了時に記録）のみ
SELECT
  s.id AS session_id,
  s.title,
  COUNT(DISTINCT vl.user_id) AS completed_count,
  (SELECT COUNT(*) FROM users WHERE role = 'learner' AND deleted_at IS NULL) AS total_learners,
  ROUND(
    100.0 * COUNT(DISTINCT vl.user_id) /
    NULLIF((SELECT COUNT(*) FROM users WHERE role = 'learner' AND deleted_at IS NULL), 0),
    1
  ) AS completion_rate
FROM sessions s
LEFT JOIN viewing_logs vl ON vl.session_id = s.id
GROUP BY s.id, s.title
ORDER BY s.id;

-- 自動評価成功率（過去7日）
-- Note: evaluationsテーブルではevaluator_typeカラムを使用
SELECT
  COUNT(*) AS total_evaluations,
  COUNT(CASE WHEN evaluator_type = 'gemini' THEN 1 END) AS gemini_evaluations,
  COUNT(CASE WHEN evaluator_type = 'manual' THEN 1 END) AS manual_evaluations,
  ROUND(
    100.0 * COUNT(CASE WHEN evaluator_type = 'gemini' THEN 1 END) /
    NULLIF(COUNT(*), 0),
    1
  ) AS auto_evaluation_rate
FROM evaluations
WHERE created_at > NOW() - INTERVAL '7 days';
```

---

## 7. インシデント対応フロー

### 7.1 重要度別対応

| 重要度 | 定義 | 初動 | 対応時間 | エスカレーション |
|---|---|---|---|---|
| **P1 (Critical)** | サービス全停止 | 即時 | 30分以内 | 開発責任者→講師 |
| **P2 (High)** | 主要機能障害 | 15分以内 | 2時間以内 | 開発責任者 |
| **P3 (Medium)** | 一部機能障害 | 1時間以内 | 24時間以内 | 担当者 |
| **P4 (Low)** | 軽微な問題 | 翌営業日 | 1週間以内 | 担当者 |

### 7.2 インシデント対応手順

```
1. 検知・確認
   └─ アラート受信
   └─ 影響範囲の特定
   └─ 重要度判定

2. 初動対応
   └─ Slackでインシデント宣言
   └─ ステータスページ更新（該当する場合）
   └─ 応急処置の実施

3. 原因調査
   └─ ログ・メトリクス確認
   └─ 直近の変更（デプロイ）確認
   └─ 再現手順の特定

4. 復旧
   └─ 修正実装 or ロールバック
   └─ 動作確認
   └─ 監視強化

5. 事後対応
   └─ ポストモーテム作成
   └─ 再発防止策の実施
   └─ ドキュメント更新
```

### 7.3 ロールバック手順

```bash
# Vercelでの即時ロールバック
# Dashboard: Deployments → 前回成功デプロイ → Promote to Production

# または CLI
vercel rollback [deployment-url]

# Supabaseマイグレーションのロールバック
supabase db reset --linked
```

---

## 8. データ保持・アーカイブ

### 8.1 ログ保持期間

| ログ種別 | 保持期間 | 根拠 |
|---|---|---|
| Vercel Logs | 7日 | 無料プラン制限 |
| Sentry Events | 90日 | 無料プラン制限 |
| 視聴ログ（DB） | 永続 | 助成金要件 |
| 課題提出履歴 | 永続 | 助成金要件 |
| アクセスログ | 1年 | セキュリティ監査 |

### 8.2 助成金対応ログ

厚労省助成金申請に必要なログは永続保存:

```sql
-- 視聴証跡
-- Note: 現行スキーマではviewing_logsはchecked_in_atのみ（詳細視聴ログなし）
SELECT
  u.name,
  u.email,
  s.title AS session_title,
  vl.checked_in_at,
  vl.ip_address
FROM viewing_logs vl
JOIN users u ON u.id = vl.user_id
JOIN sessions s ON s.id = vl.session_id
WHERE u.id = $1
ORDER BY vl.checked_in_at;

-- 課題提出証跡
-- Note: evaluationsテーブルにはevaluated_atカラムなし（created_atを使用）
SELECT
  u.name,
  e.title AS exercise_title,
  sub.submitted_at,
  eval.score,
  eval.created_at AS evaluated_at
FROM submissions sub
JOIN users u ON u.id = sub.user_id
JOIN exercises e ON e.id = sub.exercise_id
LEFT JOIN evaluations eval ON eval.submission_id = sub.id AND eval.is_active = true
WHERE u.id = $1
ORDER BY sub.submitted_at;
```

---

## 9. セキュリティ監視

### 9.1 監視項目

| 項目 | 検知方法 | アラート条件 |
|---|---|---|
| ブルートフォース攻撃 | 認証失敗ログ | 同一IPから10回/分 |
| 不正アクセス | 403/401ログ | 同一ユーザーから5回/分 |
| SQLインジェクション | WAFログ | パターンマッチ |
| 大量データアクセス | APIログ | 通常の10倍以上 |

### 9.2 Supabase RLS監視

```sql
-- RLS違反の検出（監査ログ）
SELECT
  auth.uid() AS user_id,
  current_timestamp AS attempted_at,
  current_query() AS query
FROM audit_log
WHERE action = 'RLS_VIOLATION';
```

---

## 10. 定期レビュー

### 10.1 週次レビュー

| 確認項目 | 担当 | 時間 |
|---|---|---|
| エラー率トレンド | 開発者 | 毎週月曜 |
| パフォーマンス推移 | 開発者 | 毎週月曜 |
| 未解決アラート | 開発者 | 毎週月曜 |

### 10.2 月次レビュー

| 確認項目 | 担当 | 時間 |
|---|---|---|
| SLA達成状況 | PM | 月初 |
| コスト推移 | PM | 月初 |
| 容量計画 | 開発者 | 月初 |
| セキュリティ監査 | 開発者 | 月初 |

---

## 11. SLA目標

| 指標 | 目標 | 測定方法 |
|---|---|---|
| **可用性** | 99.5% | UptimeRobot |
| **レスポンスタイム（P95）** | < 2秒 | Vercel Analytics |
| **エラー率** | < 1% | Sentry |
| **MTTR（平均復旧時間）** | < 2時間 | インシデント記録 |

---

## 12. 変更履歴

| 日付 | バージョン | 変更内容 |
|---|---|---|
| 2026-01-05 | v1.0 | 初版作成 |
