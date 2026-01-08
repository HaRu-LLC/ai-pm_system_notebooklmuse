# データベースマイグレーション手順書

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 作成日: 2026-01-06
- 版: v1.0
- 関連文書: db_schema.md, local_dev_setup.md, deployment_guide.md

---

## 1. 概要

### 1.1 マイグレーションツール

| 項目 | 選定 | 用途 |
|---|---|---|
| **Prisma Migrate** | 開発〜本番 | スキーマ変更管理の標準ツール |
| **Prisma Client** | アプリケーション | 型安全なDBアクセス |
| **Supabase CLI** | 補助 | RLSポリシー・関数の直接適用 |

### 1.2 環境構成

| 環境 | 用途 | DATABASE_URL |
|---|---|---|
| **Development** | 開発・テスト | `postgresql://...@db.xxx-dev.supabase.co:5432/postgres` |
| **Staging** | 本番前検証 | `postgresql://...@db.xxx-staging.supabase.co:5432/postgres` |
| **Production** | 本番 | `postgresql://...@db.xxx-prod.supabase.co:5432/postgres` |

---

## 2. Prisma Migrate 基本コマンド

### 2.1 開発環境でのマイグレーション

```bash
# スキーマ変更後、マイグレーションを作成
npx prisma migrate dev --name add_user_profile

# 出力例:
# Environment variables loaded from .env
# Prisma schema loaded from prisma/schema.prisma
# Datasource "db": PostgreSQL database "postgres"
#
# Applying migration `20260106123456_add_user_profile`
#
# The following migration(s) have been created and applied:
# migrations/
#   └─ 20260106123456_add_user_profile/
#     └─ migration.sql
#
# Your database is now in sync with your schema.
# ✔ Generated Prisma Client
```

### 2.2 マイグレーションのみ作成（適用しない）

```bash
# マイグレーションSQLを作成のみ（レビュー用）
npx prisma migrate dev --name add_cohort_settings --create-only

# 生成されたSQLを確認・編集
cat prisma/migrations/20260106123456_add_cohort_settings/migration.sql

# 確認後、適用
npx prisma migrate dev
```

### 2.3 本番環境へのデプロイ

```bash
# 本番環境へマイグレーション適用
npx prisma migrate deploy

# 出力例:
# Prisma schema loaded from prisma/schema.prisma
# Datasource "db": PostgreSQL database "postgres"
#
# 1 migration found in prisma/migrations
#
# Applying migration `20260106123456_add_user_profile`
#
# The following migration(s) have been applied:
# migrations/
#   └─ 20260106123456_add_user_profile/
#     └─ migration.sql
```

### 2.4 スキーマの直接適用（開発用）

```bash
# マイグレーションファイルを作らず直接適用（開発初期のみ）
npx prisma db push

# 警告: 本番では使用禁止
# - マイグレーション履歴が残らない
# - ロールバックできない
```

### 2.5 その他のコマンド

```bash
# マイグレーション状態を確認
npx prisma migrate status

# Prisma Client を再生成
npx prisma generate

# Prisma Studio でDB確認
npx prisma studio

# スキーマを既存DBから生成（リバースエンジニアリング）
npx prisma db pull
```

---

## 3. マイグレーションファイル管理

### 3.1 ディレクトリ構造

```
prisma/
├── schema.prisma              # Prismaスキーマ定義
├── migrations/
│   ├── 20260103100000_init/
│   │   └── migration.sql      # 初期スキーマ
│   ├── 20260105120000_add_cohorts/
│   │   └── migration.sql      # コホート追加
│   ├── 20260106123456_add_user_profile/
│   │   └── migration.sql      # ユーザープロファイル追加
│   └── migration_lock.toml    # マイグレーションロック
└── seed.ts                    # シードデータ
```

### 3.2 命名規則

| 形式 | 例 | 説明 |
|---|---|---|
| `YYYYMMDDHHMMSS_description` | `20260106123456_add_user_profile` | 自動生成タイムスタンプ + 説明 |

**推奨の description パターン**:
| パターン | 例 | 用途 |
|---|---|---|
| `init` | `20260103100000_init` | 初期スキーマ作成 |
| `add_{table}` | `add_cohorts` | 新テーブル追加 |
| `add_{table}_{column}` | `add_users_terms_agreed_at` | カラム追加 |
| `alter_{table}_{change}` | `alter_users_add_index` | テーブル変更 |
| `drop_{table}` | `drop_legacy_logs` | テーブル削除 |
| `create_index_{name}` | `create_index_submissions_status` | インデックス追加 |

### 3.3 Git 管理ルール

```bash
# マイグレーションファイルは必ずコミット
git add prisma/migrations/
git commit -m "feat: add cohorts table migration"

# schema.prisma と migrations は同時にコミット
git add prisma/schema.prisma prisma/migrations/
git commit -m "feat: add cohort management feature"
```

**重要なルール**:
- ✅ マイグレーションファイルはコミット必須
- ✅ 本番適用前に必ず PR レビュー
- ❌ 適用済みマイグレーションの編集禁止
- ❌ マイグレーションファイルの削除禁止（開発環境リセット時を除く）

---

## 4. スキーマ変更パターン

### 4.1 カラム追加（非破壊的）

```prisma
// schema.prisma
model User {
  id            String   @id @default(uuid())
  email         String   @unique
  name          String
  // 新規追加（NULL許容）
  phoneNumber   String?  @map("phone_number")

  @@map("users")
}
```

```sql
-- 生成されるSQL
ALTER TABLE "users" ADD COLUMN "phone_number" TEXT;
```

### 4.2 カラム追加（NOT NULL + デフォルト値）

```prisma
model User {
  // 新規追加（デフォルト値あり）
  isVerified    Boolean  @default(false) @map("is_verified")
}
```

```sql
-- 生成されるSQL
ALTER TABLE "users" ADD COLUMN "is_verified" BOOLEAN NOT NULL DEFAULT false;
```

### 4.3 カラム名変更

```prisma
model User {
  // 旧: name → 新: fullName
  fullName      String   @map("full_name")  // DB上のカラム名
}
```

```sql
-- ⚠️ Prisma は RENAME を生成しない
-- 手動で migration.sql を編集:
ALTER TABLE "users" RENAME COLUMN "name" TO "full_name";
```

### 4.4 テーブル追加

```prisma
model Cohort {
  id            String   @id @default(uuid())
  name          String
  organization  String
  startDate     DateTime @map("start_date")
  endDate       DateTime @map("end_date")
  status        String   @default("active")
  createdAt     DateTime @default(now()) @map("created_at")
  updatedAt     DateTime @updatedAt @map("updated_at")

  users         User[]

  @@map("cohorts")
}
```

### 4.5 インデックス追加

```prisma
model Submission {
  id          String   @id @default(uuid())
  userId      String   @map("user_id")
  status      String
  submittedAt DateTime @map("submitted_at")

  // 複合インデックス
  @@index([userId, status])
  @@index([submittedAt])
  @@map("submissions")
}
```

### 4.6 外部キー追加

```prisma
model User {
  id        String   @id @default(uuid())
  cohortId  String?  @map("cohort_id")

  // リレーション定義
  cohort    Cohort?  @relation(fields: [cohortId], references: [id])
}
```

---

## 5. 本番マイグレーション手順

### 5.1 事前準備チェックリスト

```
【マイグレーション前チェック】
□ PRがレビュー・承認済み
□ ステージング環境で検証済み
□ マイグレーションSQLの内容を確認
□ 破壊的変更がないことを確認
□ 本番DBのバックアップを取得
□ ロールバック手順を確認
□ メンテナンス時間を調整済み（必要な場合）
```

### 5.2 バックアップ取得

```bash
# Supabase Dashboard からバックアップ
# 1. Project Settings → Database → Backups
# 2. "Create backup" をクリック
# 3. バックアップ完了を確認

# または pg_dump（CLI）
pg_dump -h db.xxx-prod.supabase.co -U postgres -d postgres \
  -F c -f backup_20260106.dump
```

### 5.3 本番適用手順

```bash
# Step 1: 環境変数を本番用に設定
export DATABASE_URL="postgresql://postgres:[PASSWORD]@db.xxx-prod.supabase.co:5432/postgres"

# Step 2: マイグレーション状態を確認
npx prisma migrate status

# 出力例:
# Database schema is up to date!
# または
# Following migration have not yet been applied:
# 20260106123456_add_user_profile

# Step 3: 本番適用
npx prisma migrate deploy

# Step 4: Prisma Client を再生成
npx prisma generate

# Step 5: アプリケーションを再起動（Vercel は自動）
```

### 5.4 デプロイ後確認

```bash
# 接続確認
npx prisma db execute --stdin < /dev/null

# テーブル構造確認（Prisma Studio）
npx prisma studio

# または SQL で確認
psql $DATABASE_URL -c "\d users"
```

---

## 6. ロールバック手順

### 6.1 Prisma Migrate のロールバック

**注意**: Prisma Migrate は自動ロールバックをサポートしていません。手動で逆操作を行います。

```bash
# Step 1: 問題のマイグレーションを特定
npx prisma migrate status

# Step 2: 逆操作のマイグレーションを作成
npx prisma migrate dev --name rollback_add_user_profile --create-only

# Step 3: migration.sql を手動編集（逆操作を記述）
```

**逆操作の例**:
```sql
-- 元のマイグレーション: カラム追加
-- ALTER TABLE "users" ADD COLUMN "phone_number" TEXT;

-- ロールバック: カラム削除
ALTER TABLE "users" DROP COLUMN "phone_number";
```

### 6.2 バックアップからの復元

```bash
# Supabase Dashboard からリストア
# 1. Project Settings → Database → Backups
# 2. 復元したいバックアップを選択
# 3. "Restore" をクリック

# または pg_restore（CLI）
pg_restore -h db.xxx-prod.supabase.co -U postgres -d postgres \
  -c backup_20260106.dump
```

### 6.3 _prisma_migrations テーブルの操作

**⚠️ 緊急時のみ使用**

```sql
-- 適用済みマイグレーションを「未適用」に戻す
DELETE FROM _prisma_migrations
WHERE migration_name = '20260106123456_add_user_profile';

-- その後、手動で逆操作SQLを実行
ALTER TABLE "users" DROP COLUMN "phone_number";
```

---

## 7. データ移行を伴う変更

### 7.1 2段階デプロイ戦略

データ移行が必要な変更は、2段階に分けて実施します。

**例: カラム名変更（name → full_name）**

**Phase 1: 新カラム追加 + データコピー**
```sql
-- Migration 1: 新カラム追加
ALTER TABLE "users" ADD COLUMN "full_name" VARCHAR(100);

-- データ移行
UPDATE "users" SET "full_name" = "name";

-- NOT NULL 制約追加
ALTER TABLE "users" ALTER COLUMN "full_name" SET NOT NULL;
```

**アプリケーション対応**:
- 読み取り: `full_name` を優先、なければ `name`
- 書き込み: 両方に書き込み

**Phase 2: 旧カラム削除**
```sql
-- Migration 2: 旧カラム削除（Phase 1 デプロイ後）
ALTER TABLE "users" DROP COLUMN "name";
```

### 7.2 大量データの移行

```sql
-- バッチ処理で移行（ロック時間を短縮）
DO $$
DECLARE
  batch_size INT := 1000;
  total_rows INT;
  processed INT := 0;
BEGIN
  SELECT COUNT(*) INTO total_rows FROM users WHERE full_name IS NULL;

  WHILE processed < total_rows LOOP
    UPDATE users
    SET full_name = name
    WHERE id IN (
      SELECT id FROM users
      WHERE full_name IS NULL
      LIMIT batch_size
    );

    processed := processed + batch_size;
    RAISE NOTICE 'Processed % / % rows', processed, total_rows;

    -- 小休止（他のトランザクションに譲る）
    PERFORM pg_sleep(0.1);
  END LOOP;
END $$;
```

---

## 8. RLS ポリシー・関数のマイグレーション

### 8.1 Prisma での制限

Prisma Migrate は以下をサポートしていません:
- RLS ポリシー
- PostgreSQL 関数・トリガー
- カスタムビュー

これらは Supabase CLI または SQL ファイルで管理します。

### 8.2 SQL ファイルでの管理

```
prisma/
├── schema.prisma
├── migrations/
└── sql/
    ├── rls/
    │   ├── users_policies.sql
    │   ├── submissions_policies.sql
    │   └── evaluations_policies.sql
    ├── functions/
    │   ├── update_updated_at.sql
    │   └── log_audit.sql
    └── views/
        ├── learner_progress.sql
        └── session_completion_stats.sql
```

### 8.3 デプロイスクリプト（RLS/関数/ビュー専用）

```bash
#!/bin/bash
# scripts/apply-db-objects.sh
#
# 用途: RLS ポリシー、関数、ビューを適用する（migrate は含まない）
#
# 使用方法:
#   DIRECT_URL=postgresql://... ./scripts/apply-db-objects.sh
#
# 注意:
#   - このスクリプトは Prisma migrate とは別に実行
#   - DIRECT_URL（直接接続）を使用すること（Pooler経由ではDDL操作が失敗する可能性あり）
#   - migrate は CI の別ステップで `npx prisma migrate deploy` として実行

set -e

# 直接接続URLを使用
DB_URL="${DIRECT_URL}"

if [ -z "$DB_URL" ]; then
  echo "Error: DIRECT_URL is required"
  echo "Usage: DIRECT_URL=postgresql://... ./scripts/apply-db-objects.sh"
  exit 1
fi

echo "=== RLS Policies ==="
if compgen -G "prisma/sql/rls/*.sql" > /dev/null; then
  for file in prisma/sql/rls/*.sql; do
    echo "Applying $file..."
    psql "$DB_URL" -f "$file"
  done
else
  echo "No RLS policy files found, skipping..."
fi

echo "=== Functions ==="
if compgen -G "prisma/sql/functions/*.sql" > /dev/null; then
  for file in prisma/sql/functions/*.sql; do
    echo "Applying $file..."
    psql "$DB_URL" -f "$file"
  done
else
  echo "No function files found, skipping..."
fi

echo "=== Views ==="
if compgen -G "prisma/sql/views/*.sql" > /dev/null; then
  for file in prisma/sql/views/*.sql; do
    echo "Applying $file..."
    psql "$DB_URL" -f "$file"
  done
else
  echo "No view files found, skipping..."
fi

echo "=== Done ==="
```

**責務分離**:
- `npx prisma migrate deploy`: Prisma マイグレーション（CI で個別に実行）
- `apply-db-objects.sh`: RLS/関数/ビューの適用（migrate 後に実行）

**重要**: このスクリプトは CI/CD パイプラインで自動実行されます。詳細は次のセクション（9. CI/CD でのマイグレーション）を参照。

---

## 9. CI/CD でのマイグレーション

### 9.1 GitHub Actions ワークフロー

```yaml
# .github/workflows/migrate.yml
name: Database Migration

on:
  push:
    branches: [main]
    paths:
      - 'prisma/migrations/**'
      - 'prisma/schema.prisma'

jobs:
  migrate-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: Run migrations on staging
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}
          DIRECT_URL: ${{ secrets.STAGING_DIRECT_URL }}
        run: npx prisma migrate deploy

      - name: Apply RLS/Functions/Views on staging
        env:
          DIRECT_URL: ${{ secrets.STAGING_DIRECT_URL }}
        run: ./scripts/apply-db-objects.sh

      - name: Generate Prisma Client
        run: npx prisma generate

  migrate-production:
    runs-on: ubuntu-latest
    needs: migrate-staging
    environment: production
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: Run migrations on production
        env:
          DATABASE_URL: ${{ secrets.PRODUCTION_DATABASE_URL }}
          DIRECT_URL: ${{ secrets.PRODUCTION_DIRECT_URL }}
        run: npx prisma migrate deploy

      - name: Apply RLS/Functions/Views on production
        env:
          DIRECT_URL: ${{ secrets.PRODUCTION_DIRECT_URL }}
        run: ./scripts/apply-db-objects.sh

      - name: Notify Slack
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Migration ${{ job.status }}: ${{ github.repository }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Migration Status*: ${{ job.status }}\n*Repo*: ${{ github.repository }}\n*Ref*: ${{ github.ref }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### 9.2 PR でのマイグレーション検証

```yaml
# .github/workflows/pr-check.yml
name: PR Migration Check

on:
  pull_request:
    paths:
      - 'prisma/**'

jobs:
  check-migration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: Validate schema
        run: npx prisma validate

      - name: Check for drift
        env:
          DATABASE_URL: ${{ secrets.DEV_DATABASE_URL }}
        run: |
          # スキーマとDBの差分をチェック
          npx prisma migrate diff \
            --from-schema-datamodel prisma/schema.prisma \
            --to-schema-datasource prisma/schema.prisma \
            --exit-code || {
              echo "⚠️ Schema drift detected! Please run 'npx prisma migrate dev' locally."
              exit 1
            }

      - name: Dry run migration
        env:
          DATABASE_URL: ${{ secrets.DEV_DATABASE_URL }}
        run: |
          npx prisma migrate status
          echo "Migration files to be applied:"
          ls -la prisma/migrations/
```

---

## 10. ベストプラクティス

### 10.1 破壊的変更の回避

| 変更 | 破壊的？ | 対策 |
|---|---|---|
| カラム追加（NULL許容） | ❌ No | そのまま適用 |
| カラム追加（NOT NULL） | ⚠️ 条件付き | デフォルト値を設定 |
| カラム削除 | ✅ Yes | 2段階デプロイ |
| カラム名変更 | ✅ Yes | 2段階デプロイ |
| テーブル削除 | ✅ Yes | 2段階デプロイ |
| 型変更（互換あり） | ⚠️ 条件付き | テスト必須 |
| 型変更（互換なし） | ✅ Yes | 2段階デプロイ |

### 10.2 マイグレーション作成時のルール

1. **1つのマイグレーション = 1つの変更**
   - 複数の変更を1つにまとめない
   - ロールバックしやすくする

2. **意味のある名前をつける**
   - ✅ `add_users_phone_number`
   - ❌ `update_schema`

3. **データ移行は別マイグレーション**
   - スキーマ変更とデータ移行を分離
   - 失敗時の切り分けが容易

4. **本番適用前に必ずレビュー**
   - 生成されたSQLを確認
   - 実行計画（EXPLAIN）を確認

### 10.3 開発環境のリセット

```bash
# 開発環境を完全リセット（マイグレーション履歴も削除）
npx prisma migrate reset

# 警告: 本番では絶対に使用禁止
# - 全テーブルを削除
# - マイグレーションを再適用
# - シードを実行
```

---

## 11. トラブルシューティング

### 11.1 マイグレーションドリフト

**症状**: `prisma migrate status` で "drift detected" エラー

```
The current database is not managed by Prisma Migrate.
If you want to keep the current database...
```

**解決策**:
```bash
# 現在のDBをベースラインとして設定
npx prisma migrate resolve --applied 20260106123456_add_user_profile

# または、DBを現在のスキーマと同期
npx prisma db push --accept-data-loss  # 開発環境のみ
```

### 11.2 マイグレーション競合

**症状**: チームメンバーのマイグレーションと競合

**解決策**:
```bash
# 1. 最新を pull
git pull origin main

# 2. ローカルのマイグレーションを削除
rm -rf prisma/migrations/20260106123456_my_migration

# 3. マイグレーションを再作成
npx prisma migrate dev --name my_migration
```

### 11.3 失敗したマイグレーション

**症状**: マイグレーションが途中で失敗

```bash
# 失敗したマイグレーションをスキップ
npx prisma migrate resolve --rolled-back 20260106123456_failed_migration

# 問題を修正して再作成
npx prisma migrate dev --name fixed_migration
```

### 11.4 接続エラー

**症状**: `P1001: Can't reach database server`

**解決策**:
1. DATABASE_URL の形式を確認
2. パスワードの特殊文字をURLエンコード
3. Supabase の Connection Pooling 設定を確認
4. ファイアウォール / IP許可リストを確認

---

## 12. チェックリスト

### 12.1 マイグレーション作成時

```
□ schema.prisma を更新
□ npx prisma migrate dev --name xxx で作成
□ 生成された migration.sql を確認
□ 破壊的変更がないことを確認
□ 必要に応じて migration.sql を編集
□ npx prisma migrate dev で適用
□ 動作確認
□ Git コミット（schema.prisma + migrations/）
```

### 12.2 本番デプロイ時

```
□ PR レビュー完了
□ ステージングで検証完了
□ 本番バックアップ取得
□ ロールバック手順を確認
□ npx prisma migrate deploy 実行
□ 動作確認
□ Slack 通知（完了報告）
```

---

## 更新履歴

| 日付 | バージョン | 変更内容 |
|---|---|---|
| 2026-01-06 | v1.0 | 初版作成 |
| 2026-01-06 | v1.1 | RLS/関数/ビューのCI自動適用、migrate diff引数修正、DIRECT_URL対応追加 |
| 2026-01-06 | v1.2 | deploy-db.sh→apply-db-objects.shにリネーム、migrate責務分離（migrate は CI 個別ステップで実行） |
