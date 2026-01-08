# 認証・認可詳細設計書

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 作成日: 2026-01-05
- 版: v1.0
- 関連文書: api_spec.md (v1.1), db_schema.md (v1.1), app_spec.md (v1.1)

---

## 1. 概要

### 1.1 認証方式

| 項目 | 選定 | 理由 |
|---|---|---|
| 認証基盤 | Supabase Auth | Next.js統合容易、RLS連携、無料枠 |
| 認証方式 | メール + パスワード | シンプル、企業利用に適合 |
| トークン形式 | JWT (JSON Web Token) | ステートレス、RLS連携 |
| セッション管理 | Supabase Session | 自動リフレッシュ対応 |

### 1.2 認可方式

| 項目 | 選定 | 理由 |
|---|---|---|
| アクセス制御 | RBAC (Role-Based Access Control) | シンプルで管理容易 |
| データ分離 | RLS (Row Level Security) | DB層での強制、漏洩防止 |
| ロール | learner / instructor / admin | 3役割で必要十分 |

---

## 2. ロール定義

### 2.1 ロール一覧

| ロール | 説明 | 主な権限 |
|---|---|---|
| **learner** | 受講者 | 自分のデータ閲覧・編集、課題提出 |
| **instructor** | 講師 | 全受講者データ閲覧、手動評価入力 |
| **admin** | 管理者 | 全機能、ユーザー管理、システム設定 |

### 2.2 権限マトリックス

| 機能 | learner | instructor | admin |
|---|:---:|:---:|:---:|
| **自分のダッシュボード** | ✓ | ✓ | ✓ |
| **自分の進捗確認** | ✓ | ✓ | ✓ |
| **課題提出** | ✓ | - | - |
| **自分の評価結果閲覧** | ✓ | ✓ | ✓ |
| **全受講者一覧** | - | ✓ | ✓ |
| **全受講者進捗閲覧** | - | ✓ | ✓ |
| **手動評価入力** | - | ✓ | ✓ |
| **レポート出力** | - | ✓ | ✓ |
| **受講者招待** | - | - | ✓ |
| **ユーザー管理** | - | - | ✓ |
| **システム設定** | - | - | ✓ |

---

## 3. JWT設計

### 3.1 JWT Payload構造

```json
{
  "aud": "authenticated",
  "exp": 1704326400,
  "iat": 1703721600,
  "iss": "https://xxxx.supabase.co/auth/v1",
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "phone": "",
  "app_metadata": {
    "provider": "email",
    "providers": ["email"]
  },
  "user_metadata": {
    "name": "山田太郎",
    "role": "learner"
  },
  "role": "authenticated",
  "aal": "aal1",
  "amr": [{ "method": "password", "timestamp": 1703721600 }],
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### 3.2 カスタムクレーム

| クレーム | 場所 | 用途 |
|---|---|---|
| `user_metadata.name` | user_metadata | 表示名 |
| `user_metadata.role` | user_metadata | アプリケーションロール |

### 3.3 トークンライフサイクル

```
┌─────────────────────────────────────────────────────────────┐
│                      トークンライフサイクル                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [ログイン]                                                  │
│      │                                                       │
│      ▼                                                       │
│  Access Token発行 ──────────────────────────────────────────│
│  (有効期限: 1時間)                                           │
│      │                                                       │
│      │ ←──────── 自動リフレッシュ (残り10分で実行)            │
│      │                                                       │
│      ▼                                                       │
│  Refresh Token ─────────────────────────────────────────────│
│  (有効期限: 7日)                                             │
│      │                                                       │
│      │ 期限切れ                                              │
│      ▼                                                       │
│  [再ログイン要求]                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.4 トークン設定

| 項目 | 値 | 設定場所 |
|---|---|---|
| Access Token有効期限 | 3600秒（1時間） | Supabase Dashboard |
| Refresh Token有効期限 | 604800秒（7日） | Supabase Dashboard |
| 自動リフレッシュ | 有効 | Supabase Client |

---

## 4. 認証フロー

### 4.1 招待・登録フロー

```
┌─────────┐    ┌─────────────┐    ┌────────────┐    ┌─────────┐
│  Admin  │    │   System    │    │   Email    │    │  User   │
└────┬────┘    └──────┬──────┘    └─────┬──────┘    └────┬────┘
     │                │                  │               │
     │ 招待作成       │                  │               │
     │───────────────▶│                  │               │
     │                │                  │               │
     │                │ users作成        │               │
     │                │ (status=invited) │               │
     │                │                  │               │
     │                │ 招待メール送信   │               │
     │                │─────────────────▶│               │
     │                │                  │               │
     │                │                  │ 招待メール    │
     │                │                  │──────────────▶│
     │                │                  │               │
     │                │                  │               │ 招待リンクclick
     │                │                  │               │───────────────┐
     │                │                  │               │               │
     │                │◀─────────────────│───────────────│◀──────────────┘
     │                │  パスワード設定  │               │
     │                │                  │               │
     │                │ users更新        │               │
     │                │ (status=active)  │               │
     │                │                  │               │
     │                │ Session発行      │               │
     │                │─────────────────▶│───────────────│▶
     │                │                  │               │
```

### 4.2 ログインフロー

```
┌─────────┐    ┌─────────────┐    ┌────────────┐
│  User   │    │   Next.js   │    │  Supabase  │
└────┬────┘    └──────┬──────┘    └─────┬──────┘
     │                │                  │
     │ email/password │                  │
     │───────────────▶│                  │
     │                │                  │
     │                │ signInWithPassword
     │                │─────────────────▶│
     │                │                  │
     │                │                  │ 認証検証
     │                │                  │────────────┐
     │                │                  │            │
     │                │◀─────────────────│◀───────────┘
     │                │  Session返却     │
     │                │                  │
     │                │ Cookie設定       │
     │                │────────────────┐ │
     │                │                │ │
     │◀───────────────│◀───────────────┘ │
     │  ダッシュボードへ                 │
     │                │                  │
```

### 4.3 パスワードリセットフロー

```
1. ユーザーがリセット申請
2. Supabase Authがリセットメール送信
3. ユーザーがリセットリンクをクリック
4. 新パスワード設定画面表示
5. 新パスワード設定完了
6. 自動ログイン
```

---

## 5. セッション管理

### 5.1 セッション永続化

```typescript
// Supabase Clientの設定
import { createBrowserSupabaseClient } from "@supabase/auth-helpers-nextjs";

const supabase = createBrowserSupabaseClient({
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  supabaseKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  options: {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      detectSessionInUrl: true,
    },
  },
});
```

### 5.2 サーバーサイドセッション検証

```typescript
// middleware.ts
import { createMiddlewareClient } from "@supabase/auth-helpers-nextjs";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(req: NextRequest) {
  const res = NextResponse.next();
  const supabase = createMiddlewareClient({ req, res });

  // セッション検証 & 自動リフレッシュ
  const {
    data: { session },
  } = await supabase.auth.getSession();

  // 未認証の場合、ログインページへリダイレクト
  if (!session && req.nextUrl.pathname.startsWith("/app")) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  // ロール検証（管理者ページ）
  if (req.nextUrl.pathname.startsWith("/admin")) {
    const role = session?.user?.user_metadata?.role;
    if (role !== "admin" && role !== "instructor") {
      return NextResponse.redirect(new URL("/app/dashboard", req.url));
    }
  }

  return res;
}

export const config = {
  matcher: ["/app/:path*", "/admin/:path*"],
};
```

---

## 6. RLS（Row Level Security）実装

### 6.1 users テーブル

```sql
-- RLS有効化
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- 受講者: 自分のレコードのみ閲覧可能
CREATE POLICY "users_select_own" ON users
  FOR SELECT
  USING (
    id = auth.uid()
    OR (auth.jwt() ->> 'user_metadata')::jsonb ->> 'role' IN ('instructor', 'admin')
  );

-- 受講者: 自分のプロフィールのみ更新可能
CREATE POLICY "users_update_own" ON users
  FOR UPDATE
  USING (id = auth.uid())
  WITH CHECK (id = auth.uid());

-- 管理者: 全レコード操作可能
CREATE POLICY "users_admin_all" ON users
  FOR ALL
  USING ((auth.jwt() ->> 'user_metadata')::jsonb ->> 'role' = 'admin');
```

### 6.2 submissions テーブル

```sql
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;

-- 受講者: 自分の提出物のみ閲覧
CREATE POLICY "submissions_select_own" ON submissions
  FOR SELECT
  USING (
    user_id = auth.uid()
    OR (auth.jwt() ->> 'user_metadata')::jsonb ->> 'role' IN ('instructor', 'admin')
  );

-- 受講者: 自分の提出物のみ作成
CREATE POLICY "submissions_insert_own" ON submissions
  FOR INSERT
  WITH CHECK (user_id = auth.uid());

-- 受講者: 下書き状態の自分の提出物のみ更新
CREATE POLICY "submissions_update_own_draft" ON submissions
  FOR UPDATE
  USING (user_id = auth.uid() AND status = 'draft')
  WITH CHECK (user_id = auth.uid());
```

### 6.3 evaluations テーブル

```sql
ALTER TABLE evaluations ENABLE ROW LEVEL SECURITY;

-- 受講者: 自分の提出物に対する評価のみ閲覧
CREATE POLICY "evaluations_select_own" ON evaluations
  FOR SELECT
  USING (
    submission_id IN (SELECT id FROM submissions WHERE user_id = auth.uid())
    OR (auth.jwt() ->> 'user_metadata')::jsonb ->> 'role' IN ('instructor', 'admin')
  );

-- 講師/管理者: 評価作成可能
CREATE POLICY "evaluations_insert_instructor" ON evaluations
  FOR INSERT
  WITH CHECK (
    (auth.jwt() ->> 'user_metadata')::jsonb ->> 'role' IN ('instructor', 'admin')
  );
```

### 6.4 viewing_logs テーブル

```sql
ALTER TABLE viewing_logs ENABLE ROW LEVEL SECURITY;

-- 受講者: 自分のログのみ操作可能
CREATE POLICY "viewing_logs_own" ON viewing_logs
  FOR ALL
  USING (
    user_id = auth.uid()
    OR (auth.jwt() ->> 'user_metadata')::jsonb ->> 'role' IN ('instructor', 'admin')
  )
  WITH CHECK (user_id = auth.uid());
```

---

## 7. アカウントロック

### 7.1 ロックポリシー

| 項目 | 設定値 |
|---|---|
| ロックまでの失敗回数 | 5回 |
| ロック期間 | 30分 |
| 失敗カウントリセット | ログイン成功時 |

### 7.2 実装

```typescript
// ログイン時のロックチェック
async function checkAccountLock(userId: string): Promise<boolean> {
  const { data: user } = await supabase
    .from("users")
    .select("login_failed_count, locked_until")
    .eq("id", userId)
    .single();

  if (!user) return false;

  // ロック中かチェック
  if (user.locked_until && new Date(user.locked_until) > new Date()) {
    return true; // ロック中
  }

  return false;
}

// ログイン失敗時
async function handleLoginFailure(userId: string): Promise<void> {
  const { data: user } = await supabase
    .from("users")
    .select("login_failed_count")
    .eq("id", userId)
    .single();

  const newCount = (user?.login_failed_count || 0) + 1;

  if (newCount >= 5) {
    // アカウントロック
    await supabase
      .from("users")
      .update({
        login_failed_count: newCount,
        locked_until: new Date(Date.now() + 30 * 60 * 1000).toISOString(),
      })
      .eq("id", userId);
  } else {
    await supabase
      .from("users")
      .update({ login_failed_count: newCount })
      .eq("id", userId);
  }
}

// ログイン成功時
async function handleLoginSuccess(userId: string): Promise<void> {
  await supabase
    .from("users")
    .update({
      login_failed_count: 0,
      locked_until: null,
      last_login_at: new Date().toISOString(),
    })
    .eq("id", userId);
}
```

---

## 8. セキュリティ考慮事項

### 8.1 パスワードポリシー

| 項目 | 要件 |
|---|---|
| 最小文字数 | 8文字 |
| 複雑さ | 英大文字・小文字・数字を含む |
| 履歴 | 直近3回と同じパスワード禁止（将来実装） |

### 8.2 セッションセキュリティ

| 項目 | 対策 |
|---|---|
| XSS | HttpOnly Cookie使用 |
| CSRF | SameSite=Lax設定 |
| セッションハイジャック | Secure Cookie（HTTPS必須） |
| セッション固定 | ログイン時にセッションID再生成 |

### 8.3 監査ログ

認証関連イベントは全てaudit_logsに記録：

- `user.login` - ログイン成功
- `user.login_failed` - ログイン失敗
- `user.logout` - ログアウト
- `user.password_changed` - パスワード変更
- `user.password_reset_requested` - リセット申請
- `user.account_locked` - アカウントロック
- `user.role_changed` - ロール変更

---

## 9. 初回ログイン・規約同意フロー

### 9.1 フロー

```
招待メールからアクセス
        │
        ▼
┌───────────────────┐
│  パスワード設定    │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  利用規約表示      │
│  ☐ 同意する       │
└─────────┬─────────┘
          │ 同意
          ▼
┌───────────────────┐
│  ダッシュボード    │
└───────────────────┘
```

### 9.2 規約同意の記録

```sql
-- usersテーブルに規約同意カラム追加
ALTER TABLE users ADD COLUMN terms_accepted_at TIMESTAMPTZ;

-- 規約同意時に更新
UPDATE users
SET terms_accepted_at = NOW()
WHERE id = auth.uid();
```

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
| セキュリティ担当 | - | - |
