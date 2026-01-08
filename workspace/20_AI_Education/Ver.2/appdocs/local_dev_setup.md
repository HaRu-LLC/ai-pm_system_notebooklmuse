# ローカル開発環境構築ガイド

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 作成日: 2026-01-06
- 版: v1.0
- 関連文書: infrastructure_spec.md, db_schema.md, auth_design.md

---

## 1. 前提条件

### 1.1 必須ソフトウェア

| ソフトウェア | バージョン | 確認コマンド |
|---|---|---|
| **Node.js** | 20.x LTS | `node -v` |
| **npm** | 10.x 以上 | `npm -v` |
| **Git** | 2.x 以上 | `git --version` |

### 1.2 推奨ツール

| ツール | 用途 |
|---|---|
| **VSCode** | エディタ（推奨） |
| **Postman / Insomnia** | API テスト |
| **TablePlus / DBeaver** | DBクライアント |

### 1.3 VSCode 推奨拡張機能

```json
// .vscode/extensions.json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "prisma.prisma",
    "formulahendry.auto-rename-tag",
    "usernamehw.errorlens",
    "ms-playwright.playwright"
  ]
}
```

---

## 2. リポジトリセットアップ

### 2.1 クローン

```bash
# リポジトリをクローン
git clone https://github.com/your-org/ai-politeracy-app.git
cd ai-politeracy-app
```

### 2.2 依存関係インストール

```bash
# 依存関係のインストール
npm install

# 期待される出力:
# added XXX packages in Xs
```

### 2.3 package.json scripts 一覧

| コマンド | 説明 |
|---|---|
| `npm run dev` | 開発サーバー起動（localhost:3000） |
| `npm run build` | 本番ビルド |
| `npm run start` | 本番サーバー起動 |
| `npm run lint` | ESLint 実行 |
| `npm run lint:fix` | ESLint 自動修正 |
| `npm run format:check` | Prettier フォーマットチェック |
| `npm run type-check` | TypeScript 型チェック |
| `npm run test` | 単体テスト実行（Vitest） |
| `npm run test:watch` | テスト監視モード |
| `npm run test:coverage` | カバレッジレポート生成 |
| `npm run test:e2e` | E2Eテスト実行（Playwright） |
| `npm run prisma:generate` | Prisma Client 生成 |
| `npm run prisma:push` | スキーマを開発DBに適用 |
| `npm run prisma:studio` | Prisma Studio 起動 |
| `npm run prisma:migrate` | マイグレーション作成・適用 |
| `npm run prisma:seed` | シードデータ投入 |
| `npm run analyze` | バンドルサイズ分析（ANALYZE=true で実行） |

---

## 3. 環境変数設定

### 3.1 環境変数ファイルの作成

```bash
# テンプレートからコピー
cp .env.example .env.local
```

### 3.2 .env.local テンプレート

```bash
# ======================
# Supabase
# ======================
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Database (Prisma用)
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres

# ======================
# Gemini API
# ======================
GEMINI_API_KEY=AIzaSy...

# ======================
# メール (Resend)
# ======================
RESEND_API_KEY=re_...
EMAIL_FROM=noreply@ai-politeracy.example.com

# ======================
# アプリケーション
# ======================
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_APP_NAME=AIポリテラシー育成プログラム

# ======================
# 監視 (オプション)
# ======================
NEXT_PUBLIC_SENTRY_DSN=https://...@sentry.io/...
```

### 3.3 Supabase プロジェクト情報の取得

1. [Supabase Dashboard](https://supabase.com/dashboard) にログイン
2. 開発用プロジェクト（ai-politeracy-dev）を選択
3. **Settings** → **API** を開く
4. 以下の値をコピー:
   - `Project URL` → `NEXT_PUBLIC_SUPABASE_URL`
   - `anon public` → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `service_role secret` → `SUPABASE_SERVICE_ROLE_KEY`
5. **Settings** → **Database** → **Connection string** → **URI** をコピー:
   - `DATABASE_URL` に設定（`[YOUR-PASSWORD]` を実際のパスワードに置換）

### 3.4 Gemini API キーの取得

1. [Google AI Studio](https://aistudio.google.com/) にアクセス
2. **Get API key** → **Create API key** をクリック
3. 生成されたキーを `GEMINI_API_KEY` に設定

### 3.5 Resend API キーの取得（メール送信用）

1. [Resend Dashboard](https://resend.com/) にログイン
2. **API Keys** → **Create API Key** をクリック
3. 生成されたキーを `RESEND_API_KEY` に設定

---

## 4. Prisma 設定

### 4.1 Prisma Client 生成

```bash
# Prisma Client を生成
npm run prisma:generate

# 期待される出力:
# ✔ Generated Prisma Client (vX.X.X) to ./node_modules/@prisma/client
```

### 4.2 スキーマを開発DBに適用

```bash
# 開発DBにスキーマを適用（既存データは保持）
npm run prisma:push

# 期待される出力:
# 🚀 Your database is now in sync with your Prisma schema.
```

### 4.3 Prisma Studio でDB確認

```bash
# Prisma Studio を起動
npm run prisma:studio

# ブラウザが開き、http://localhost:5555 でDBを確認可能
```

### 4.4 シードデータ投入（オプション）

```bash
# 開発用サンプルデータを投入
npm run prisma:seed

# 投入されるデータ:
# - テスト用ユーザー（admin@example.com, learner@example.com）
# - サンプルセッション（12セッション）
# - サンプル課題（EX-01〜EX-26）
```

---

## 5. 開発サーバー起動

### 5.1 起動

```bash
# 開発サーバーを起動
npm run dev

# 期待される出力:
# ▲ Next.js 14.x.x
# - Local:        http://localhost:3000
# - Environments: .env.local
# ✓ Ready in Xs
```

### 5.2 動作確認

1. ブラウザで http://localhost:3000 を開く
2. ランディングページが表示されることを確認
3. `/login` にアクセスしてログイン画面を確認

### 5.3 テストアカウント（シードデータ投入後）

| ロール | メールアドレス | パスワード |
|---|---|---|
| 管理者 | admin@example.com | admin123 |
| 講師 | instructor@example.com | instructor123 |
| 受講者 | learner@example.com | learner123 |

---

## 6. テスト実行

### 6.1 単体テスト

```bash
# 全テスト実行
npm run test

# 監視モード（ファイル変更時に自動実行）
npm run test:watch

# カバレッジレポート生成
npm run test:coverage
```

### 6.2 E2Eテスト（Playwright）

```bash
# Playwright ブラウザをインストール（初回のみ）
npx playwright install

# E2Eテスト実行
npm run test:e2e

# UIモードで実行（デバッグ時に便利）
npx playwright test --ui
```

### 6.3 型チェック

```bash
# TypeScript 型チェック
npm run type-check
```

### 6.4 Lint

```bash
# ESLint 実行
npm run lint

# 自動修正
npm run lint:fix
```

---

## 7. ディレクトリ構成

```
ai-politeracy-app/
├── .github/
│   └── workflows/         # GitHub Actions
├── .vscode/               # VSCode 設定
├── prisma/
│   ├── schema.prisma      # Prisma スキーマ
│   ├── migrations/        # マイグレーションファイル
│   └── seed.ts            # シードスクリプト
├── public/                # 静的ファイル
├── src/
│   ├── app/               # Next.js App Router
│   │   ├── (auth)/        # 認証関連ページ
│   │   ├── (learner)/     # 受講者ページ
│   │   ├── (admin)/       # 管理者ページ
│   │   ├── api/           # API Routes
│   │   └── layout.tsx     # ルートレイアウト
│   ├── components/        # UIコンポーネント
│   │   ├── ui/            # shadcn/ui コンポーネント
│   │   └── ...
│   ├── lib/               # ユーティリティ
│   │   ├── supabase/      # Supabase クライアント
│   │   ├── prisma.ts      # Prisma クライアント
│   │   └── gemini.ts      # Gemini API クライアント
│   ├── hooks/             # カスタムフック
│   ├── types/             # TypeScript 型定義
│   └── styles/            # グローバルスタイル
├── tests/
│   ├── unit/              # 単体テスト
│   └── e2e/               # E2Eテスト
├── .env.example           # 環境変数テンプレート
├── .env.local             # ローカル環境変数（gitignore）
├── next.config.js         # Next.js 設定
├── tailwind.config.js     # Tailwind CSS 設定
├── tsconfig.json          # TypeScript 設定
└── package.json
```

---

## 8. トラブルシューティング

### 8.1 Supabase 接続エラー

**症状**: `Error: Invalid URL` または `NEXT_PUBLIC_SUPABASE_URL is not defined`

**解決策**:
1. `.env.local` が存在するか確認
2. 環境変数名が正しいか確認（`NEXT_PUBLIC_` プレフィックス必須）
3. 開発サーバーを再起動

```bash
# 開発サーバーを再起動
npm run dev
```

### 8.2 Prisma Client 生成エラー

**症状**: `Cannot find module '@prisma/client'`

**解決策**:
```bash
# Prisma Client を再生成
npm run prisma:generate
```

### 8.3 DATABASE_URL エラー

**症状**: `Error: P1001: Can't reach database server`

**解決策**:
1. `DATABASE_URL` の形式を確認:
   ```
   postgresql://postgres:[PASSWORD]@db.xxxx.supabase.co:5432/postgres
   ```
2. パスワードに特殊文字がある場合はURLエンコード
3. Supabase Dashboard で IP 許可設定を確認

### 8.4 Gemini API エラー

**症状**: `Error: 401 Unauthorized` または `API key not valid`

**解決策**:
1. `GEMINI_API_KEY` が設定されているか確認
2. API キーが有効か [Google AI Studio](https://aistudio.google.com/) で確認
3. API の利用制限に達していないか確認

### 8.5 ポート 3000 が使用中

**症状**: `Error: Port 3000 is already in use`

**解決策**:
```bash
# 別のポートで起動
npm run dev -- -p 3001

# または、使用中のプロセスを確認・停止
lsof -i :3000
kill -9 <PID>
```

### 8.6 node_modules の問題

**症状**: 依存関係の解決エラー

**解決策**:
```bash
# node_modules を削除して再インストール
rm -rf node_modules
rm -rf .next
npm install
```

### 8.7 TypeScript エラー

**症状**: 型エラーが多発

**解決策**:
```bash
# TypeScript サーバーを再起動（VSCode）
# Cmd+Shift+P → "TypeScript: Restart TS Server"

# または、型定義を再生成
npm run prisma:generate
```

---

## 9. 開発時の注意事項

### 9.1 ブランチ運用

```bash
# 新機能開発
git checkout -b feature/機能名

# バグ修正
git checkout -b fix/バグ内容

# 作業完了後
git push origin feature/機能名
# GitHub で PR を作成
```

### 9.2 コミットメッセージ規約

```
<type>: <subject>

type:
- feat: 新機能
- fix: バグ修正
- docs: ドキュメント
- style: フォーマット
- refactor: リファクタリング
- test: テスト
- chore: ビルド・設定

例:
feat: ログイン機能を実装
fix: 視聴チェックインのバグを修正
docs: README を更新
```

### 9.3 環境変数の追加時

1. `.env.example` にテンプレートを追加
2. `README.md` または本ドキュメントに説明を追加
3. Vercel の環境変数にも追加

---

## 10. 参考リンク

| リソース | URL |
|---|---|
| Next.js ドキュメント | https://nextjs.org/docs |
| Prisma ドキュメント | https://www.prisma.io/docs |
| Supabase ドキュメント | https://supabase.com/docs |
| Tailwind CSS ドキュメント | https://tailwindcss.com/docs |
| shadcn/ui | https://ui.shadcn.com |
| Playwright ドキュメント | https://playwright.dev/docs |

---

## 更新履歴

| 日付 | バージョン | 変更内容 |
|---|---|---|
| 2026-01-06 | v1.0 | 初版作成 |
| 2026-01-06 | v1.1 | package.json scripts一覧を更新（prisma:seed, test:coverage, analyze, format:check追加） |
