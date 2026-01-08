# インフラ・デプロイ設計書

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 作成日: 2026-01-05
- 版: v1.0
- 関連文書: development_roadmap.md, auth_design.md, db_schema.md

---

## 1. 概要

### 1.1 インフラ構成

```
┌─────────────────────────────────────────────────────────────────┐
│                          Internet                                │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Vercel Edge Network                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      CDN / Edge                          │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Vercel Functions                            │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐        │
│  │  Next.js App  │  │  API Routes   │  │  Server Comp  │        │
│  └───────────────┘  └───────────────┘  └───────────────┘        │
└─────────────────────────────┬───────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│    Supabase     │  │   Gemini API    │  │  Resend/SMTP    │
│  ┌───────────┐  │  │                 │  │                 │
│  │PostgreSQL │  │  │  LLM評価        │  │  メール送信     │
│  │  + RLS    │  │  │                 │  │                 │
│  ├───────────┤  │  └─────────────────┘  └─────────────────┘
│  │  Storage  │  │
│  ├───────────┤  │
│  │   Auth    │  │
│  └───────────┘  │
└─────────────────┘
```

### 1.2 サービス選定

| コンポーネント | サービス | 選定理由 |
|---|---|---|
| **ホスティング** | Vercel | Next.js最適化、Edge Functions、無料枠 |
| **データベース** | Supabase (PostgreSQL) | RLS、リアルタイム、認証統合 |
| **ファイルストレージ** | Supabase Storage | 統合管理、RLS対応 |
| **認証** | Supabase Auth | JWT、RLS連携 |
| **LLM** | Gemini API | コスト効率、Structured Output |
| **メール** | Resend | 開発者フレンドリー、無料枠 |
| **監視** | Vercel Analytics + Sentry | パフォーマンス + エラー追跡 |

---

## 2. 環境構成

### 2.1 環境一覧

| 環境 | 用途 | URL | Supabaseプロジェクト |
|---|---|---|---|
| **development** | ローカル開発 | localhost:3000 | ai-politeracy-dev |
| **staging** | テスト・検証 | staging.ai-politeracy.example.com | ai-politeracy-staging |
| **production** | 本番 | ai-politeracy.example.com | ai-politeracy-prod |

### 2.2 環境変数

```bash
# .env.local (development)
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

GEMINI_API_KEY=AIzaSy...
RESEND_API_KEY=re_...

NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 2.3 環境変数管理

| 変数種別 | 管理方法 | アクセス |
|---|---|---|
| 公開変数（NEXT_PUBLIC_*） | Vercel環境変数 | クライアント |
| 秘密変数 | Vercel環境変数（暗号化） | サーバーのみ |
| ローカル開発 | .env.local（gitignore） | 開発者のみ |

---

## 3. CI/CD パイプライン

### 3.1 ワークフロー概要

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Push    │───▶│  Build   │───▶│  Test    │───▶│  Deploy  │
│  (Git)   │    │  (CI)    │    │  (CI)    │    │(Vercel)  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │                                               │
     │ PR作成/更新                                   │
     └───────────────────────────────────────────────┘
                    Preview Deploy
```

### 3.2 GitHub Actions設定

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Unit tests
        run: npm run test
        env:
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.SUPABASE_URL_TEST }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY_TEST }}

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  e2e-test:
    runs-on: ubuntu-latest
    needs: lint-and-test

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e
        env:
          BASE_URL: ${{ secrets.STAGING_URL }}

      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

### 3.3 Vercel設定

```json
// vercel.json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm ci",
  "framework": "nextjs",
  "regions": ["hnd1"],
  "git": {
    "deploymentEnabled": {
      "main": true,
      "develop": true
    }
  },
  "env": {
    "NEXT_PUBLIC_SUPABASE_URL": "@supabase-url",
    "NEXT_PUBLIC_SUPABASE_ANON_KEY": "@supabase-anon-key"
  }
}
```

### 3.4 ブランチ戦略

| ブランチ | 用途 | デプロイ先 |
|---|---|---|
| `main` | 本番コード | Production |
| `develop` | 開発統合 | Staging |
| `feature/*` | 機能開発 | Preview |
| `hotfix/*` | 緊急修正 | Preview → Production |

---

## 4. データベース管理

### 4.1 マイグレーション

```bash
# Supabase CLIを使用
supabase db push          # スキーマ適用（開発）
supabase db reset         # DBリセット（開発）
supabase migration new    # 新規マイグレーション作成
supabase migration up     # マイグレーション適用
```

### 4.2 マイグレーションファイル管理

```
supabase/
├── migrations/
│   ├── 20260101000000_initial_schema.sql
│   ├── 20260102000000_add_rls_policies.sql
│   ├── 20260103000000_add_calibration_samples.sql
│   └── ...
├── seed.sql
└── config.toml
```

### 4.3 バックアップ戦略

| 項目 | 設定 |
|---|---|
| 自動バックアップ | 日次（Supabase標準） |
| 保持期間 | 7日（Pro Plan） |
| Point-in-time Recovery | 有効（Pro Plan） |
| 手動バックアップ | リリース前に実施 |

---

## 5. 監視・ログ

### 5.1 監視構成

```
┌─────────────────────────────────────────────────────────────────┐
│                        監視ダッシュボード                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ Vercel Analytics│  │     Sentry      │  │  Supabase       │  │
│  │                 │  │                 │  │  Dashboard      │  │
│  │ - ページビュー  │  │ - エラー追跡    │  │ - DBメトリクス  │  │
│  │ - Core Web     │  │ - パフォーマンス│  │ - API使用量     │  │
│  │   Vitals       │  │ - リリース追跡  │  │ - ストレージ    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Sentry設定

```typescript
// sentry.client.config.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.VERCEL_ENV || "development",
  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  integrations: [
    new Sentry.Replay({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],
});
```

### 5.3 ログ設計

| ログ種別 | 出力先 | 保持期間 |
|---|---|---|
| アプリケーションログ | Vercel Logs | 7日 |
| エラーログ | Sentry | 90日 |
| 監査ログ | Supabase (audit_logs) | 7年 |
| APIアクセスログ | Vercel Logs | 7日 |

### 5.4 アラート設定

| 条件 | 重要度 | 通知先 |
|---|---|---|
| エラー率 > 1% | Critical | Slack + Email |
| レスポンスタイム > 3秒 | High | Slack |
| Gemini API障害 | Critical | Slack + Email |
| DB接続エラー | Critical | Slack + Email |

---

## 6. セキュリティ

### 6.1 セキュリティ対策

| 対策 | 実装 |
|---|---|
| **HTTPS** | Vercel自動（Let's Encrypt） |
| **WAF** | Vercel Edge Middleware |
| **DDoS対策** | Vercel標準保護 |
| **SQLインジェクション** | Supabase RLS + パラメータ化クエリ |
| **XSS** | React自動エスケープ + CSP |
| **CSRF** | SameSite Cookie |

### 6.2 セキュリティヘッダー

```typescript
// next.config.js
const securityHeaders = [
  {
    key: "X-DNS-Prefetch-Control",
    value: "on",
  },
  {
    key: "Strict-Transport-Security",
    value: "max-age=63072000; includeSubDomains; preload",
  },
  {
    key: "X-Content-Type-Options",
    value: "nosniff",
  },
  {
    key: "X-Frame-Options",
    value: "DENY",
  },
  {
    key: "X-XSS-Protection",
    value: "1; mode=block",
  },
  {
    key: "Referrer-Policy",
    value: "origin-when-cross-origin",
  },
  {
    key: "Content-Security-Policy",
    value: "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://*.supabase.co https://generativelanguage.googleapis.com;",
  },
];

module.exports = {
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ];
  },
};
```

---

## 7. スケーリング

### 7.1 現在のキャパシティ

| リソース | 制限 | 想定使用量 |
|---|---|---|
| Vercel Functions | 無制限（Hobby/Pro） | - |
| Supabase DB | 500MB（Free） | ~50MB |
| Supabase Storage | 1GB（Free） | ~200MB |
| Supabase Auth | 50,000 MAU（Free） | ~100 MAU |
| Gemini API | 60 QPM（Free） | ~10 QPM |

### 7.2 スケールアップ計画

| フェーズ | 想定規模 | アップグレード |
|---|---|---|
| パイロット | 30名 | Free Tier |
| 本格展開 | 100名 | Supabase Pro |
| 拡大期 | 300名+ | Vercel Pro + Supabase Pro |

---

## 8. 障害対応

### 8.1 障害レベル定義

| レベル | 定義 | 対応時間 |
|---|---|---|
| **Critical** | サービス全停止 | 30分以内 |
| **High** | 主要機能停止 | 2時間以内 |
| **Medium** | 一部機能制限 | 24時間以内 |
| **Low** | 軽微な問題 | 次回リリース |

### 8.2 障害対応フロー

```
障害検知（アラート/ユーザー報告）
        │
        ▼
┌───────────────────┐
│  影響範囲確認     │
│  ・ログ確認       │
│  ・メトリクス確認 │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  原因特定         │
│  ・Sentry確認     │
│  ・Vercel Logs    │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  復旧対応         │
│  ・ロールバック   │
│  ・ホットフィックス│
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  事後対応         │
│  ・原因分析       │
│  ・再発防止策     │
└───────────────────┘
```

### 8.3 ロールバック手順

```bash
# Vercelでのロールバック
# 1. Vercel Dashboardからデプロイ履歴を確認
# 2. 前回の正常デプロイを選択
# 3. "Promote to Production" をクリック

# または CLI
vercel rollback
```

---

## 9. コスト試算

### 9.1 月間コスト（想定30名）

| サービス | プラン | 月額 |
|---|---|---|
| Vercel | Hobby（Free） | $0 |
| Supabase | Free | $0 |
| Gemini API | 従量課金 | ~$1 |
| Resend | Free（100通/日） | $0 |
| ドメイン | 年額按分 | ~$1 |
| **合計** | | **~$2/月** |

### 9.2 本格展開時（100名）

| サービス | プラン | 月額 |
|---|---|---|
| Vercel | Pro | $20 |
| Supabase | Pro | $25 |
| Gemini API | 従量課金 | ~$3 |
| Resend | Pro | $20 |
| **合計** | | **~$68/月** |

---

## 10. 変更履歴

| バージョン | 日付 | 変更内容 |
|---|---|---|
| v1.0 | 2026-01-05 | 初版作成 |

---

## 承認

| 役割 | 氏名 | 承認日 |
|---|---|---|
| プログラムマネージャー | AI-PgM | 2026-01-05 |
| インフラ担当 | - | - |
