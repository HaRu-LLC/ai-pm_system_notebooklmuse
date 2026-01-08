# デプロイガイド

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 作成日: 2026-01-06
- 版: v1.0
- 関連文書: infrastructure_spec.md, runbook.md, cicd_pipeline.md

---

## 1. デプロイ概要

### 1.1 環境構成

| 環境 | 用途 | URL | Supabase | デプロイトリガー |
|---|---|---|---|---|
| **development** | ローカル開発 | localhost:3000 | ai-politeracy-dev | - |
| **staging** | テスト・検証 | staging.ai-politeracy.example.com | ai-politeracy-staging | `develop` ブランチ push |
| **production** | 本番 | ai-politeracy.example.com | ai-politeracy-prod | `main` ブランチ push |

### 1.2 デプロイフロー図

```
┌──────────────────────────────────────────────────────────────────────┐
│                        開発フロー                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   feature/xxx ──┬──▶ PR作成 ──▶ Preview Deploy（自動）               │
│                 │                  ↓                                  │
│                 │              レビュー・テスト                        │
│                 │                  ↓                                  │
│                 └──▶ develop にマージ ──▶ Staging Deploy（自動）     │
│                                                                       │
│   develop ─────────▶ main にマージ ──▶ Production Deploy（自動）     │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Vercel 設定

### 2.1 プロジェクト作成

1. [Vercel Dashboard](https://vercel.com/dashboard) にログイン
2. **Add New...** → **Project** をクリック
3. GitHub リポジトリを選択（`ai-politeracy-app`）
4. **Framework Preset**: `Next.js` を選択
5. **Root Directory**: `.`（デフォルト）
6. **Build Command**: `npm run build`（デフォルト）
7. **Install Command**: `npm ci`
8. **Deploy** をクリック

### 2.2 環境変数設定

**Settings** → **Environment Variables** で以下を設定:

| 変数名 | Production | Staging | Preview | 説明 |
|---|:---:|:---:|:---:|---|
| `NEXT_PUBLIC_SUPABASE_URL` | ✅ | ✅ | ⚠️ | Supabase プロジェクトURL（Preview: 開発用プロジェクト） |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | ✅ | ✅ | ⚠️ | Supabase anon key（Preview: 開発用プロジェクト） |
| `SUPABASE_SERVICE_ROLE_KEY` | ✅ | ✅ | ❌ | Supabase service role key（**重要: Previewには配布禁止**） |
| `DATABASE_URL` | ✅ | ✅ | ⚠️ | PostgreSQL接続文字列（Preview: **開発用DB必須**） |
| `DIRECT_URL` | ✅ | ✅ | - | PostgreSQL接続文字列（直接接続、マイグレーション用） |
| `GEMINI_API_KEY` | ✅ | ✅ | ❌ | Gemini API キー（**Previewには配布禁止**） |
| `RESEND_API_KEY` | ✅ | ✅ | - | Resend API キー |
| `EMAIL_FROM` | ✅ | ✅ | - | 送信元メールアドレス |
| `NEXT_PUBLIC_APP_URL` | ✅ | ✅ | - | 各環境のURL |
| `NEXT_PUBLIC_SENTRY_DSN` | ✅ | ✅ | - | Sentry DSN |
| `SENTRY_AUTH_TOKEN` | ✅ | - | - | Sentry リリース用トークン |

**凡例**: ✅ 本番/Staging用、⚠️ 開発専用（本番データ禁止）、❌ 配布禁止

**重要: Preview環境のセキュリティとDB分離**:

| 環境 | DATABASE_URL | データ | 注意事項 |
|---|---|---|---|
| **Production** | 本番Supabase | 本番データ | RLS有効、監査ログ有効 |
| **Staging** | Staging Supabase | 本番に近いテストデータ | 本番と同一設定 |
| **Preview/PR** | **開発用Supabase** | テストデータのみ | **本番データ禁止** |

- `SUPABASE_SERVICE_ROLE_KEY` は**本番・Stagingのみ**に設定（Preview/PRからの管理権限漏洩を防止）
- `GEMINI_API_KEY` は**本番・Stagingのみ**に設定（API課金リスク軽減）
- **DATABASE_URL（Preview）は開発専用プロジェクトを指定すること**
  - Prisma は DB に直接接続するため、**Supabase の RLS をバイパス**します
  - Preview に本番/Staging の DATABASE_URL を設定すると、PR コードから全データにアクセス可能になります
  - 開発用 Supabase プロジェクト（`ai-politeracy-dev`）を作成し、テストデータのみを配置してください
- Preview環境でのテストはモックまたは開発用テストデータで実施

**注意**: 環境ごとに異なる値を設定するには、変数追加時に環境を選択

### 2.3 vercel.json 設定

```json
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
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store" }
      ]
    }
  ],
  "crons": [
    {
      "path": "/api/cron/cleanup",
      "schedule": "0 0 * * *"
    }
  ]
}
```

### 2.4 カスタムドメイン設定

1. **Settings** → **Domains** を開く
2. **Add** をクリック
3. ドメインを入力（例: `ai-politeracy.example.com`）
4. DNS設定:
   - **CNAME**: `cname.vercel-dns.com`
   - または **A Record**: Vercel指定のIP
5. SSL証明書は自動発行

---

## 3. Supabase 本番設定

### 3.1 プロジェクト作成

1. [Supabase Dashboard](https://supabase.com/dashboard) にログイン
2. **New Project** をクリック
3. 設定:
   - **Organization**: 組織を選択
   - **Project name**: `ai-politeracy-prod`
   - **Database Password**: 強力なパスワードを生成
   - **Region**: `Northeast Asia (Tokyo)` → `ap-northeast-1`
   - **Pricing Plan**: `Pro` を推奨（本番用）
4. **Create new project** をクリック

### 3.2 RLS ポリシー確認

本番デプロイ前に、以下のRLSポリシーが有効か確認:

```sql
-- 確認クエリ
SELECT schemaname, tablename, policyname, cmd, qual
FROM pg_policies
WHERE schemaname = 'public';
```

**必須ポリシー**:
- `users`: learner は自分のデータのみ閲覧可
- `submissions`: learner は自分の提出のみ閲覧可
- `evaluations`: learner は自分の評価のみ閲覧可
- `viewing_logs`: learner は自分のログのみ閲覧可
- `cohorts`: admin のみ作成・編集可

### 3.3 バックアップ設定

| 設定 | 値 | 備考 |
|---|---|---|
| 自動バックアップ | 有効（Pro Plan） | 日次 |
| 保持期間 | 7日 | Pro Plan標準 |
| Point-in-time Recovery | 有効 | Pro Plan |
| 手動バックアップ | リリース前に実施 | Dashboard から |

**手動バックアップ手順**:
1. **Settings** → **Database** → **Backups**
2. **Create backup** をクリック
3. ダウンロードして安全な場所に保存

### 3.4 接続プール設定

```
Settings → Database → Connection Pooling
```

| 設定 | 値 |
|---|---|
| Mode | Transaction |
| Pool Size | 15 |

**接続文字列の使い分け（重要）**:

| 用途 | 環境変数 | 接続タイプ | ポート | 説明 |
|---|---|---|---|---|
| **ランタイム（アプリ）** | `DATABASE_URL` | Pooler（Transaction） | 6543 | サーバーレス環境での接続枯渇を防止 |
| **マイグレーション** | `DIRECT_URL` | Direct | 5432 | トランザクション必須の操作に使用 |

```bash
# Vercel環境変数の設定例
DATABASE_URL=postgres://postgres.xxxx:[PASSWORD]@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres?pgbouncer=true
DIRECT_URL=postgresql://postgres:[PASSWORD]@db.xxxx.supabase.co:5432/postgres
```

```prisma
// prisma/schema.prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")  // マイグレーション用
}
```

**注意**: サーバーレス環境（Vercel Functions）では Pooler 経由を必須とし、接続枯渇を防止する

---

## 4. 初回デプロイ手順

### 4.1 事前準備チェックリスト

- [ ] Supabase 本番プロジェクト作成完了
- [ ] Supabase 接続情報を Vercel 環境変数に設定
- [ ] Gemini API キー（本番用）を設定
- [ ] Resend API キー（本番用）を設定
- [ ] ドメインの DNS 設定完了
- [ ] SSL 証明書発行完了

### 4.2 データベースマイグレーション

```bash
# Prisma マイグレーションを本番に適用
# 注意: マイグレーションには DIRECT_URL（直接接続）を使用

# 1. 本番接続文字列を一時的に設定
# DATABASE_URL: Pooler経由（ランタイム用、schema.prismaのurl）
# DIRECT_URL: 直接接続（マイグレーション用、schema.prismaのdirectUrl）
export DATABASE_URL="postgres://postgres.xxxx:[PASSWORD]@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres?pgbouncer=true"
export DIRECT_URL="postgresql://postgres:[PASSWORD]@db.xxxx.supabase.co:5432/postgres"

# 2. マイグレーション適用（DIRECT_URLを使用）
npx prisma migrate deploy

# 3. RLS/関数/ビュー適用（オプション、CIで自動実行される場合は不要）
# ./scripts/apply-db-objects.sh

# 4. 環境変数をクリア
unset DATABASE_URL DIRECT_URL
```

**重要**: Prisma は `schema.prisma` の `directUrl` を参照してマイグレーションを実行するため、`DIRECT_URL` の設定が必須です。

### 4.3 シードデータ投入

```bash
# 必要な初期データを投入（セッション、課題定義など）
npx prisma db seed

# 投入されるデータ:
# - 12セッション（sessions テーブル）
# - 26課題（exercises テーブル）
# - 初期管理者アカウント（users テーブル）
```

### 4.4 Vercel デプロイ実行

```bash
# main ブランチにプッシュして自動デプロイ
git checkout main
git merge develop
git push origin main

# または Vercel CLI で手動デプロイ
npx vercel --prod
```

### 4.5 デプロイ後の動作確認

| 確認項目 | 手順 | 期待結果 |
|---|---|---|
| トップページ表示 | `https://ai-politeracy.example.com` にアクセス | ランディングページが表示 |
| ログイン | `/login` で管理者ログイン | ダッシュボードに遷移 |
| API 動作 | `/api/health` にアクセス | `{ "status": "ok" }` |
| DB 接続 | 受講者一覧を表示 | データが表示される |
| Gemini API | 課題を提出して評価 | 自動評価が完了 |
| メール送信 | 招待メールを送信 | メールが届く |

---

## 5. 継続デプロイ

### 5.1 自動デプロイ（通常フロー）

1. `feature/xxx` ブランチで開発
2. PR を作成 → Preview Deploy が自動実行
3. レビュー・テスト完了後、`develop` にマージ → Staging Deploy
4. 検証完了後、`main` にマージ → Production Deploy

### 5.2 Preview Deploy

PRを作成すると自動的に Preview Deploy が実行される:
- URL: `https://ai-politeracy-app-xxx-org.vercel.app`
- 環境変数: Preview 設定を使用
- 用途: レビュー時の動作確認

### 5.3 手動デプロイ（緊急時）

```bash
# Vercel CLI をインストール
npm i -g vercel

# ログイン
vercel login

# 手動デプロイ（本番）
vercel --prod

# 手動デプロイ（プレビュー）
vercel
```

---

## 6. ロールバック手順

### 6.1 Vercel Dashboard からのロールバック

1. [Vercel Dashboard](https://vercel.com/dashboard) → プロジェクト選択
2. **Deployments** タブを開く
3. ロールバックしたいデプロイを選択
4. **...** → **Promote to Production** をクリック
5. 確認ダイアログで **Promote** をクリック

**所要時間**: 約1-2分

### 6.2 Vercel CLI からのロールバック

```bash
# デプロイ一覧を確認
vercel ls

# 特定のデプロイにロールバック
vercel promote <deployment-url> --prod

# 例
vercel promote ai-politeracy-xxx-yyy.vercel.app --prod
```

### 6.3 Git からのロールバック

**推奨: revert による安全なロールバック**

```bash
# 前のコミットを打ち消す新しいコミットを作成（推奨）
git revert HEAD
git push origin main

# 複数のコミットをまとめてrevert
git revert HEAD~3..HEAD --no-commit
git commit -m "revert: 直前3コミットをロールバック"
git push origin main
```

**非推奨: force pushによるロールバック**

```bash
# ⚠️ 警告: 監査性・安全性を損なうため、原則使用禁止
# やむを得ず使用する場合は、チームへの事前共有が必須
# git reset --hard <commit-hash>
# git push origin main --force
```

**ロールバック方針**:
- 原則として `git revert` または Vercel Dashboard からの Promote を使用
- `git reset --hard` + force push は監査ログが失われるため**非推奨**
- 緊急時でも可能な限り revert で対応し、履歴を保持する

### 6.4 データベースのロールバック

**Prisma マイグレーションのロールバック**:
```bash
# 1つ前のマイグレーションに戻す
# 注意: down マイグレーションが必要
npx prisma migrate resolve --rolled-back <migration-name>
```

**Supabase Point-in-time Recovery（最終手段）**:
1. Supabase Dashboard → **Settings** → **Database** → **Backups**
2. **Restore** をクリック
3. 復元したい時点を選択
4. 新しいプロジェクトとして復元

---

## 7. デプロイ前チェックリスト

### 7.1 コード品質

- [ ] ESLint エラーなし（`npm run lint`）
- [ ] TypeScript エラーなし（`npm run type-check`）
- [ ] 単体テスト通過（`npm run test`）
- [ ] E2Eテスト通過（`npm run test:e2e`）
- [ ] ビルド成功（`npm run build`）

### 7.2 機能確認

- [ ] 主要機能の手動テスト完了
- [ ] 新機能のテストケース追加済み
- [ ] 既存機能への影響確認済み

### 7.3 セキュリティ

- [ ] 機密情報がコードに含まれていない
- [ ] 環境変数が適切に設定されている
- [ ] APIキーがローテーションされていない

### 7.4 パフォーマンス

- [ ] バンドルサイズが許容範囲内
- [ ] Core Web Vitals の悪化なし
- [ ] 不要なログ出力の削除

### 7.5 ドキュメント

- [ ] CHANGELOG 更新済み
- [ ] 必要に応じて README 更新済み
- [ ] 破壊的変更がある場合は告知済み

---

## 8. 環境別設定値

### 8.1 Supabase

| 項目 | Development | Staging | Production |
|---|---|---|---|
| Project | ai-politeracy-dev | ai-politeracy-staging | ai-politeracy-prod |
| Region | ap-northeast-1 | ap-northeast-1 | ap-northeast-1 |
| Plan | Free | Pro | Pro |
| Pool Size | 10 | 15 | 15 |

### 8.2 Vercel

| 項目 | Staging | Production |
|---|---|---|
| Branch | develop | main |
| Domain | staging.ai-politeracy.example.com | ai-politeracy.example.com |
| Region | hnd1 (Tokyo) | hnd1 (Tokyo) |
| Functions | Edge | Edge |

### 8.3 外部サービス

| サービス | Development | Staging | Production |
|---|---|---|---|
| Gemini API | 共通キー | 共通キー | 本番キー |
| Resend | テストドメイン | テストドメイン | 本番ドメイン |
| Sentry | - | staging | production |

---

## 9. トラブルシューティング

### 9.1 ビルドエラー

**症状**: Vercel ビルドが失敗

**対処**:
1. ローカルで `npm run build` を実行して同じエラーか確認
2. 環境変数が Vercel に設定されているか確認
3. `package-lock.json` がコミットされているか確認

### 9.2 データベース接続エラー

**症状**: `Error: P1001: Can't reach database server`

**対処**:
1. `DATABASE_URL` が正しいか確認
2. Supabase でプロジェクトが停止していないか確認
3. 接続プールの設定を確認

### 9.3 環境変数が反映されない

**症状**: 新しい環境変数が動作しない

**対処**:
1. Vercel で環境変数を追加/変更後、再デプロイが必要
2. `NEXT_PUBLIC_` プレフィックスの有無を確認
3. デプロイログで環境変数が読み込まれているか確認

### 9.4 Edge Function タイムアウト

**症状**: API が 10秒以上かかりタイムアウト

**対処**:
1. Gemini API 呼び出しを非同期処理に変更
2. バックグラウンドジョブに分離
3. Vercel Pro Plan でタイムアウトを延長（最大 60秒）

---

## 10. 参考リンク

| リソース | URL |
|---|---|
| Vercel ドキュメント | https://vercel.com/docs |
| Vercel CLI | https://vercel.com/docs/cli |
| Supabase ドキュメント | https://supabase.com/docs |
| Prisma Migrate | https://www.prisma.io/docs/concepts/components/prisma-migrate |

---

## 更新履歴

| 日付 | バージョン | 変更内容 |
|---|---|---|
| 2026-01-06 | v1.0 | 初版作成 |
| 2026-01-06 | v1.1 | Preview環境のキー分離、DB接続プール指針、ロールバック方針を追記 |
| 2026-01-06 | v1.2 | 初回デプロイ手順をDATABASE_URL/DIRECT_URL両方設定する方針に修正 |
| 2026-01-06 | v1.3 | Preview環境のDB分離方針を明確化（PrismaはRLSバイパスのため開発専用DB必須） |
