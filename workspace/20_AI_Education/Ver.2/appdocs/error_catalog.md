# エラーハンドリングカタログ

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 作成日: 2026-01-06
- 版: v1.0
- 関連文書: api_spec.md, gemini_integration_spec.md, runbook.md

---

## 1. エラーコード体系

### 1.1 コード形式

```
E{category}{number}

category:
  1 = AUTH（認証・認可）
  2 = API（APIリクエスト）
  3 = DB（データベース）
  4 = GEMINI（Gemini API）
  5 = FILE（ファイル操作）
  9 = SYSTEM（システム）

number: 001-999
```

### 1.2 カテゴリ一覧

| カテゴリ | コード範囲 | 説明 |
|---|---|---|
| AUTH | E1001-E1099 | 認証・認可関連 |
| API | E2001-E2099 | APIリクエスト関連 |
| DB | E3001-E3099 | データベース関連 |
| GEMINI | E4001-E4099 | Gemini API関連 |
| FILE | E5001-E5099 | ファイル操作関連 |
| SYSTEM | E9001-E9099 | システム全般 |

---

## 2. 認証エラー（AUTH: E1xxx）

| コード | HTTP | エラー名 | 原因 | 対処法（ユーザー向け） |
|---|:---:|---|---|---|
| E1001 | 401 | INVALID_CREDENTIALS | メールアドレスまたはパスワードが正しくない | 入力内容を確認してください |
| E1002 | 401 | SESSION_EXPIRED | セッションが期限切れ | 再度ログインしてください |
| E1003 | 401 | TOKEN_INVALID | JWTトークンが無効 | 再度ログインしてください |
| E1004 | 403 | ACCOUNT_LOCKED | アカウントがロックされている | 30分後に再試行するか、管理者に連絡してください |
| E1005 | 403 | PERMISSION_DENIED | 権限が不足している | この操作を行う権限がありません |
| E1006 | 403 | TERMS_NOT_AGREED | 利用規約に同意していない | 利用規約に同意してください |
| E1007 | 400 | INVALID_INVITE_TOKEN | 招待トークンが無効または期限切れ | 管理者に新しい招待を依頼してください |
| E1008 | 400 | EMAIL_ALREADY_REGISTERED | メールアドレスが既に登録済み | 別のメールアドレスを使用するか、ログインしてください |
| E1009 | 400 | PASSWORD_TOO_WEAK | パスワードが要件を満たしていない | 8文字以上で英数字を含むパスワードを設定してください |
| E1010 | 429 | TOO_MANY_LOGIN_ATTEMPTS | ログイン試行回数超過 | しばらく待ってから再試行してください |

### 2.1 TypeScript型定義

```typescript
type AuthErrorCode =
  | 'E1001'
  | 'E1002'
  | 'E1003'
  | 'E1004'
  | 'E1005'
  | 'E1006'
  | 'E1007'
  | 'E1008'
  | 'E1009'
  | 'E1010';

interface AuthError {
  code: AuthErrorCode;
  message: string;
  details?: {
    remainingAttempts?: number;
    lockoutUntil?: string;
  };
}
```

---

## 3. APIエラー（API: E2xxx）

| コード | HTTP | エラー名 | 原因 | 対処法（ユーザー向け） |
|---|:---:|---|---|---|
| E2001 | 400 | VALIDATION_ERROR | リクエストパラメータが不正 | 入力内容を確認してください |
| E2002 | 400 | MISSING_REQUIRED_FIELD | 必須フィールドが欠落 | 必須項目を入力してください |
| E2003 | 404 | RESOURCE_NOT_FOUND | リソースが存在しない | 指定されたリソースが見つかりません |
| E2004 | 409 | RESOURCE_CONFLICT | リソースの競合（重複など） | 既に存在するデータと競合しています |
| E2005 | 429 | RATE_LIMIT_EXCEEDED | レート制限超過 | しばらく待ってから再試行してください |
| E2006 | 413 | PAYLOAD_TOO_LARGE | リクエストサイズ超過 | データサイズを小さくしてください |
| E2007 | 415 | UNSUPPORTED_MEDIA_TYPE | サポートされていないメディアタイプ | 対応する形式でアップロードしてください |
| E2008 | 422 | UNPROCESSABLE_ENTITY | 処理できないエンティティ | 入力内容を確認してください |
| E2009 | 500 | INTERNAL_SERVER_ERROR | サーバー内部エラー | 時間をおいて再試行してください |
| E2010 | 503 | SERVICE_UNAVAILABLE | サービス一時停止中 | メンテナンス中です。しばらくお待ちください |

### 3.1 バリデーションエラー詳細

```typescript
interface ValidationError {
  code: 'E2001';
  message: string;
  details: {
    field: string;
    constraint: string;
    value?: unknown;
  }[];
}

// 例
{
  "code": "E2001",
  "message": "入力内容にエラーがあります",
  "details": [
    {
      "field": "email",
      "constraint": "email",
      "value": "invalid-email"
    },
    {
      "field": "password",
      "constraint": "minLength",
      "value": "abc"
    }
  ]
}
```

---

## 4. データベースエラー（DB: E3xxx）

| コード | HTTP | エラー名 | 原因 | 対処法（ユーザー向け） |
|---|:---:|---|---|---|
| E3001 | 500 | DB_CONNECTION_ERROR | データベース接続エラー | 時間をおいて再試行してください |
| E3002 | 403 | RLS_VIOLATION | 行レベルセキュリティ違反 | このデータへのアクセス権がありません |
| E3003 | 409 | UNIQUE_CONSTRAINT_VIOLATION | 一意制約違反 | 既に存在するデータです |
| E3004 | 409 | FOREIGN_KEY_VIOLATION | 外部キー制約違反 | 関連するデータが存在しません |
| E3005 | 500 | QUERY_TIMEOUT | クエリタイムアウト | 時間をおいて再試行してください |
| E3006 | 500 | TRANSACTION_ERROR | トランザクションエラー | 処理に失敗しました。再試行してください |
| E3007 | 400 | INVALID_DATA_FORMAT | データ形式エラー | データ形式を確認してください |
| E3008 | 500 | MIGRATION_ERROR | マイグレーションエラー | 管理者に連絡してください |

### 4.1 RLS違反の詳細

```typescript
interface RLSViolationError {
  code: 'E3002';
  message: string;
  details: {
    table: string;
    operation: 'SELECT' | 'INSERT' | 'UPDATE' | 'DELETE';
    policyName?: string;
  };
}
```

---

## 5. Gemini APIエラー（GEMINI: E4xxx）

| コード | HTTP | エラー名 | 原因 | 対処法（ユーザー向け） |
|---|:---:|---|---|---|
| E4001 | 500 | GEMINI_CONNECTION_ERROR | Gemini APIへの接続エラー | 評価処理に失敗しました。再試行してください |
| E4002 | 429 | GEMINI_RATE_LIMIT | Gemini APIのレート制限 | 評価が混雑しています。しばらくお待ちください |
| E4003 | 400 | GEMINI_CONTENT_FILTER | コンテンツフィルターによるブロック | 提出内容を確認してください |
| E4004 | 500 | GEMINI_SCHEMA_ERROR | レスポンススキーマ検証失敗 | 評価処理に失敗しました。再試行してください |
| E4005 | 504 | GEMINI_TIMEOUT | Gemini APIタイムアウト | 評価に時間がかかっています。後ほど確認してください |
| E4006 | 500 | GEMINI_PARSE_ERROR | レスポンス解析エラー | 評価処理に失敗しました。再試行してください |
| E4007 | 500 | GEMINI_UNKNOWN_ERROR | 不明なGemini APIエラー | 評価処理に失敗しました。管理者に連絡してください |
| E4008 | 202 | EVALUATION_QUEUED | 評価がキューに追加された | 評価完了までお待ちください |

### 5.1 評価エラー時のフォールバック

```typescript
interface EvaluationFallback {
  code: 'E4001' | 'E4002' | 'E4005' | 'E4006' | 'E4007';
  action: 'RETRY' | 'QUEUE_MANUAL' | 'NOTIFY_ADMIN';
  retryAfter?: number; // 秒
  manualEvaluationQueued?: boolean;
}

// フォールバックロジック
const FALLBACK_RULES = {
  E4001: { action: 'RETRY', maxRetries: 3, backoff: 'exponential' },
  E4002: { action: 'RETRY', retryAfter: 60 },
  E4005: { action: 'QUEUE_MANUAL', notifyUser: true },
  E4006: { action: 'RETRY', maxRetries: 2 },
  E4007: { action: 'NOTIFY_ADMIN', queueManual: true },
};
```

---

## 6. ファイルエラー（FILE: E5xxx）

| コード | HTTP | エラー名 | 原因 | 対処法（ユーザー向け） |
|---|:---:|---|---|---|
| E5001 | 413 | FILE_TOO_LARGE | ファイルサイズ超過（10MB超） | ファイルサイズを10MB以下にしてください |
| E5002 | 415 | INVALID_FILE_TYPE | サポートされていないファイル形式 | 対応形式: MD, JSON, TXT, PDF, PNG, JPG |
| E5003 | 500 | FILE_UPLOAD_ERROR | ファイルアップロード失敗 | 再度アップロードしてください |
| E5004 | 404 | FILE_NOT_FOUND | ファイルが見つからない | ファイルが削除された可能性があります |
| E5005 | 500 | STORAGE_ERROR | ストレージエラー | 時間をおいて再試行してください |
| E5006 | 400 | TOO_MANY_FILES | ファイル数超過（5件超） | ファイル数を5件以下にしてください |
| E5007 | 400 | EMPTY_FILE | ファイルが空 | 内容のあるファイルをアップロードしてください |
| E5008 | 400 | MALFORMED_FILE | ファイルが破損 | 正常なファイルをアップロードしてください |

### 6.1 許可されるファイル形式

```typescript
const ALLOWED_FILE_TYPES = {
  'text/markdown': ['.md'],
  'application/json': ['.json'],
  'text/plain': ['.txt'],
  'application/pdf': ['.pdf'],
  'image/png': ['.png'],
  'image/jpeg': ['.jpg', '.jpeg'],
  'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
  'video/mp4': ['.mp4'],
} as const;

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const MAX_FILES_PER_SUBMISSION = 5;
```

---

## 7. システムエラー（SYSTEM: E9xxx）

| コード | HTTP | エラー名 | 原因 | 対処法（ユーザー向け） |
|---|:---:|---|---|---|
| E9001 | 500 | UNEXPECTED_ERROR | 予期せぬエラー | 問題が発生しました。管理者に連絡してください |
| E9002 | 503 | MAINTENANCE_MODE | メンテナンス中 | メンテナンス中です。{end_time}に再開予定です |
| E9003 | 500 | CONFIGURATION_ERROR | 設定エラー | 管理者に連絡してください |
| E9004 | 500 | EXTERNAL_SERVICE_ERROR | 外部サービスエラー | 時間をおいて再試行してください |
| E9005 | 500 | MEMORY_ERROR | メモリ不足 | 管理者に連絡してください |
| E9006 | 500 | TIMEOUT_ERROR | 処理タイムアウト | 時間をおいて再試行してください |

---

## 8. エラーレスポンス形式

### 8.1 RFC 7807 準拠形式

```json
{
  "type": "https://ai-politeracy.example.com/errors/E2001",
  "title": "Validation Error",
  "status": 400,
  "detail": "入力内容にエラーがあります",
  "instance": "/api/v1/submissions",
  "code": "E2001",
  "timestamp": "2026-01-06T10:30:00Z",
  "traceId": "abc123def456",
  "errors": [
    {
      "field": "content",
      "message": "内容は100文字以上必要です"
    }
  ]
}
```

### 8.2 TypeScript型定義

```typescript
interface ApiError {
  type: string;
  title: string;
  status: number;
  detail: string;
  instance: string;
  code: string;
  timestamp: string;
  traceId: string;
  errors?: FieldError[];
}

interface FieldError {
  field: string;
  message: string;
  value?: unknown;
}
```

### 8.3 エラーレスポンス生成関数

```typescript
function createErrorResponse(
  code: string,
  detail: string,
  status: number,
  instance: string,
  errors?: FieldError[]
): ApiError {
  return {
    type: `https://ai-politeracy.example.com/errors/${code}`,
    title: ERROR_TITLES[code],
    status,
    detail,
    instance,
    code,
    timestamp: new Date().toISOString(),
    traceId: generateTraceId(),
    errors,
  };
}
```

---

## 9. フロントエンドでの表示

### 9.1 エラーメッセージコンポーネント

```tsx
interface ErrorMessageProps {
  error: ApiError;
}

function ErrorMessage({ error }: ErrorMessageProps) {
  const message = getLocalizedMessage(error.code, error.detail);

  return (
    <Alert variant="destructive">
      <AlertTitle>{message.title}</AlertTitle>
      <AlertDescription>
        {message.description}
        {error.errors && (
          <ul>
            {error.errors.map((e, i) => (
              <li key={i}>{e.message}</li>
            ))}
          </ul>
        )}
      </AlertDescription>
    </Alert>
  );
}
```

### 9.2 ローカライズメッセージ

```typescript
const ERROR_MESSAGES_JA: Record<string, { title: string; description: string }> = {
  E1001: {
    title: 'ログインに失敗しました',
    description: 'メールアドレスまたはパスワードが正しくありません。',
  },
  E1004: {
    title: 'アカウントがロックされています',
    description: 'セキュリティのため、アカウントが一時的にロックされています。30分後に再試行してください。',
  },
  E2001: {
    title: '入力エラー',
    description: '入力内容を確認してください。',
  },
  E4002: {
    title: '評価処理が混雑しています',
    description: 'しばらくお待ちいただくか、後ほど再試行してください。',
  },
  E5001: {
    title: 'ファイルサイズが大きすぎます',
    description: 'ファイルサイズは10MB以下にしてください。',
  },
  // ... 他のエラーコード
};
```

---

## 10. ロギング規則

### 10.1 ログレベル

| レベル | 用途 | エラーカテゴリ |
|---|---|---|
| ERROR | 即座に対応が必要 | E9xxx, E3001, E4007 |
| WARN | 注意が必要だが緊急ではない | E4002, E4005, E2005 |
| INFO | 通常の操作記録 | E1001, E2003 |
| DEBUG | 開発時のデバッグ | すべて（詳細） |

### 10.2 構造化ログ形式

```json
{
  "level": "error",
  "timestamp": "2026-01-06T10:30:00.000Z",
  "traceId": "abc123def456",
  "userId": "user-uuid",
  "error": {
    "code": "E4001",
    "message": "Gemini API connection error",
    "stack": "Error: ...",
    "context": {
      "exerciseId": "ex-uuid",
      "submissionId": "sub-uuid"
    }
  }
}
```

---

## 11. 監視・アラート

### 11.1 アラートルール

| エラーコード | 閾値 | アラート先 |
|---|---|---|
| E9001, E9003 | 1件/5分 | Slack #alerts-critical |
| E4001, E4007 | 5件/5分 | Slack #alerts-gemini |
| E3001 | 1件/5分 | Slack #alerts-database |
| E2005 | 100件/1分 | Slack #alerts-ratelimit |
| E1004 | 10件/5分 | Slack #alerts-security |

### 11.2 Sentry設定

```typescript
Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  beforeSend(event, hint) {
    const error = hint.originalException as ApiError;
    if (error?.code) {
      event.tags = {
        ...event.tags,
        errorCode: error.code,
        errorCategory: error.code[1], // 1=AUTH, 2=API, etc.
      };
    }
    return event;
  },
});
```

---

## 更新履歴

| 日付 | バージョン | 変更内容 |
|---|---|---|
| 2026-01-06 | v1.0 | 初版作成 |
