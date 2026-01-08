# API仕様書

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 更新日: 2026-01-05
- 版: v1.4（コホート管理・利用規約同意API追加）
- 関連文書: ../docs/requirements.md (v2.0), app_spec.md (v1.1), db_schema.md (v1.1)

---

## 1. 概要

### 1.1 API設計方針

| 項目 | 方針 |
|---|---|
| アーキテクチャ | RESTful API |
| データ形式 | JSON |
| 認証 | Bearer Token (JWT) |
| バージョニング | URLパス（/api/v1/...） |
| エラーハンドリング | RFC 7807 準拠 |

### 1.2 ベースURL

| 環境 | ベースURL |
|---|---|
| 開発 | `http://localhost:3000/api/v1` |
| ステージング | `https://staging.ai-politeracy.example.com/api/v1` |
| 本番 | `https://ai-politeracy.example.com/api/v1` |

### 1.3 共通ヘッダー

**リクエスト**:
```
Content-Type: application/json
Authorization: Bearer {access_token}
```

**レスポンス**:
```
Content-Type: application/json
X-Request-Id: {uuid}
```

---

## 2. 認証API

### 2.1 ログイン

ユーザー認証を行い、アクセストークンを発行する。

**エンドポイント**: `POST /auth/login`

**認証**: 不要

**リクエスト**:
```json
{
    "email": "user@example.com",
    "password": "securePassword123"
}
```

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| email | string | ✓ | メールアドレス |
| password | string | ✓ | パスワード |

**レスポンス（成功: 200）**:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4...",
    "token_type": "Bearer",
    "expires_in": 604800,
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "name": "山田太郎",
        "role": "learner"
    }
}
```

**エラーレスポンス（401）**:
```json
{
    "type": "https://api.example.com/errors/authentication-failed",
    "title": "Authentication Failed",
    "status": 401,
    "detail": "メールアドレスまたはパスワードが正しくありません",
    "instance": "/api/v1/auth/login"
}
```

**エラーレスポンス（423 - ロック）**:
```json
{
    "type": "https://api.example.com/errors/account-locked",
    "title": "Account Locked",
    "status": 423,
    "detail": "アカウントがロックされています。30分後に再度お試しください",
    "locked_until": "2026-01-03T15:30:00Z"
}
```

---

### 2.2 トークンリフレッシュ

アクセストークンを更新する。

**エンドポイント**: `POST /auth/refresh`

**認証**: 不要

**リクエスト**:
```json
{
    "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."
}
```

**レスポンス（成功: 200）**:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "bmV3IHJlZnJlc2ggdG9rZW4...",
    "token_type": "Bearer",
    "expires_in": 604800
}
```

---

### 2.3 ログアウト

現在のセッションを終了する。

**エンドポイント**: `POST /auth/logout`

**認証**: 必須

**レスポンス（成功: 204）**: 本文なし

---

### 2.4 パスワードリセット申請

パスワードリセットメールを送信する。

**エンドポイント**: `POST /auth/forgot-password`

**認証**: 不要

**リクエスト**:
```json
{
    "email": "user@example.com"
}
```

**レスポンス（成功: 200）**:
```json
{
    "message": "パスワードリセットメールを送信しました"
}
```

> **注意**: セキュリティ上、メールアドレスが存在しない場合も同じレスポンスを返す

---

### 2.5 パスワードリセット実行

新しいパスワードを設定する。

**エンドポイント**: `POST /auth/reset-password`

**認証**: 不要

**リクエスト**:
```json
{
    "token": "reset_token_from_email",
    "password": "newSecurePassword456",
    "password_confirmation": "newSecurePassword456"
}
```

**レスポンス（成功: 200）**:
```json
{
    "message": "パスワードを変更しました"
}
```

---

### 2.6 招待登録

招待トークンを使用してアカウントを有効化する。

**エンドポイント**: `POST /auth/register`

**認証**: 不要

**リクエスト**:
```json
{
    "token": "invite_token_from_email",
    "password": "securePassword123",
    "password_confirmation": "securePassword123"
}
```

**レスポンス（成功: 201）**:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4...",
    "token_type": "Bearer",
    "expires_in": 604800,
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "name": "山田太郎",
        "role": "learner"
    }
}
```

---

### 2.7 利用規約同意

初回ログイン時または規約更新時に利用規約への同意を記録する。

**エンドポイント**: `POST /auth/agree-terms`

**認証**: 必須

**リクエスト**:
```json
{
    "terms_version": "v1.0",
    "agreed": true
}
```

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| terms_version | string | ✓ | 同意する規約バージョン |
| agreed | boolean | ✓ | 同意フラグ（trueのみ受付） |

**レスポンス（成功: 200）**:
```json
{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "terms_version": "v1.0",
    "agreed_at": "2026-01-05T10:00:00Z",
    "message": "利用規約への同意を記録しました"
}
```

**エラーレスポンス（400）**:
```json
{
    "type": "https://api.example.com/errors/validation-error",
    "title": "Validation Error",
    "status": 400,
    "detail": "同意が必要です"
}
```

> **注意**:
> - 同意情報はIPアドレスとともに記録される
> - 規約バージョンが更新された場合、再同意が必要
> - 同意履歴は監査用に保持される

---

## 3. ユーザーAPI

### 3.1 現在のユーザー情報取得

**エンドポイント**: `GET /users/me`

**認証**: 必須

**レスポンス（成功: 200）**:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "山田太郎",
    "role": "learner",
    "organization": "株式会社サンプル",
    "status": "active",
    "created_at": "2026-01-01T09:00:00Z",
    "last_login_at": "2026-01-03T10:15:00Z"
}
```

---

### 3.2 プロフィール更新

**エンドポイント**: `PATCH /users/me`

**認証**: 必須

**リクエスト**:
```json
{
    "name": "山田太郎（更新）",
    "organization": "株式会社サンプル"
}
```

**レスポンス（成功: 200）**:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "山田太郎（更新）",
    "organization": "株式会社サンプル",
    "updated_at": "2026-01-03T11:00:00Z"
}
```

---

### 3.3 パスワード変更

**エンドポイント**: `POST /users/me/change-password`

**認証**: 必須

**リクエスト**:
```json
{
    "current_password": "oldPassword123",
    "new_password": "newPassword456",
    "new_password_confirmation": "newPassword456"
}
```

**レスポンス（成功: 200）**:
```json
{
    "message": "パスワードを変更しました"
}
```

---

## 4. セッションAPI

### 4.1 セッション一覧取得

**エンドポイント**: `GET /sessions`

**認証**: 必須

**クエリパラメータ**:
| パラメータ | 型 | 必須 | デフォルト | 説明 |
|---|---|---|---|---|
| phase | integer | - | - | フェーズ番号でフィルタ |

**レスポンス（成功: 200）**:
```json
{
    "sessions": [
        {
            "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "number": 1,
            "title": "プロンプトの基本構造",
            "phase": 1,
            "phase_name": "手書きプロンプト基礎",
            "description": "プロンプトの4要素（指示・文脈・制約・出力形式）を学ぶ",
            "duration_minutes": 20,
            "is_published": true,
            "progress": {
                "is_viewed": true,
                "viewed_at": "2026-01-02T14:30:00Z",
                "required_exercises_total": 1,
                "required_exercises_completed": 1,
                "optional_exercises_total": 1,
                "optional_exercises_completed": 0
            }
        },
        {
            "id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
            "number": 2,
            "title": "文脈・制約・出力形式",
            "phase": 1,
            "phase_name": "手書きプロンプト基礎",
            "description": "ペルソナ設定と業務プロンプト設計",
            "duration_minutes": 20,
            "is_published": true,
            "progress": {
                "is_viewed": false,
                "viewed_at": null,
                "required_exercises_total": 1,
                "required_exercises_completed": 0,
                "optional_exercises_total": 1,
                "optional_exercises_completed": 0
            }
        }
    ],
    "total": 12
}
```

---

### 4.2 セッション詳細取得

**エンドポイント**: `GET /sessions/{session_id}`

**認証**: 必須

**レスポンス（成功: 200）**:
```json
{
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "number": 1,
    "title": "プロンプトの基本構造",
    "phase": 1,
    "phase_name": "プロンプトエンジニアリング基礎",
    "description": "プロンプトの4要素（指示・文脈・制約・出力形式）を学ぶ",
    "duration_minutes": 20,
    "is_published": true,
    "videos": {
        "part_1": {
            "url": "https://www.youtube.com/embed/xxxxx",
            "title": "Part X-1: 理論・概念",
            "duration_minutes": 10
        },
        "part_2": {
            "url": "https://www.youtube.com/embed/yyyyy",
            "title": "Part X-2: 実践・応用",
            "duration_minutes": 10
        }
    },
    "materials_url": "https://drive.google.com/...",
    "exercises": [
        {
            "id": "ex1-uuid",
            "exercise_code": "EX-01",
            "title": "4要素プロンプト作成",
            "is_required": true,
            "submission_status": "evaluated",
            "score": 85
        },
        {
            "id": "ex2-uuid",
            "exercise_code": "EX-02",
            "title": "4要素プロンプト改善",
            "is_required": false,
            "submission_status": null,
            "score": null
        }
    ],
    "progress": {
        "is_viewed": true,
        "viewed_at": "2026-01-02T14:30:00Z"
    }
}
```

---

## 5. 課題API

### 5.1 課題詳細取得

**エンドポイント**: `GET /exercises/{exercise_id}`

**認証**: 必須

**レスポンス（成功: 200）**:
```json
{
    "id": "ex1-uuid",
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "session_number": 1,
    "number": 1,
    "title": "基本プロンプト作成",
    "description": "以下の要件を満たすプロンプトを作成してください：\n1. 自己紹介文を生成するプロンプト\n2. 300文字以内で出力するよう指定\n3. ビジネスシーン向けのトーンを指定",
    "is_required": true,
    "rubric": {
        "elements": "指示・文脈・制約・出力形式の4要素が含まれているか",
        "practicality": "実際の業務で使用できる実用性があるか",
        "creativity": "独自の工夫や創意がみられるか",
        "completeness": "指示が明確で漏れがないか"
    },
    "max_length": 2000,
    "allow_file_upload": true,
    "my_submission": {
        "id": "sub1-uuid",
        "status": "evaluated",
        "submitted_at": "2026-01-02T15:00:00Z",
        "evaluation": {
            "score": 85,
            "breakdown": {
                "elements": 22,
                "practicality": 23,
                "creativity": 18,
                "completeness": 22
            }
        }
    }
}
```

---

## 6. 提出API

### 6.1 提出一覧取得

**エンドポイント**: `GET /submissions`

**認証**: 必須

**クエリパラメータ**:
| パラメータ | 型 | 必須 | デフォルト | 説明 |
|---|---|---|---|---|
| session_id | uuid | - | - | セッションでフィルタ |
| status | string | - | - | ステータスでフィルタ |
| page | integer | - | 1 | ページ番号 |
| per_page | integer | - | 20 | 1ページあたりの件数 |

**レスポンス（成功: 200）**:
```json
{
    "submissions": [
        {
            "id": "sub1-uuid",
            "exercise": {
                "id": "ex1-uuid",
                "title": "基本プロンプト作成",
                "session_number": 1
            },
            "status": "evaluated",
            "submitted_at": "2026-01-02T15:00:00Z",
            "evaluation": {
                "score": 85,
                "evaluator_type": "gemini"
            }
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 20,
        "total": 12,
        "total_pages": 1
    }
}
```

---

### 6.2 提出詳細取得

**エンドポイント**: `GET /submissions/{submission_id}`

**認証**: 必須

**レスポンス（成功: 200）**:
```json
{
    "id": "sub1-uuid",
    "exercise": {
        "id": "ex1-uuid",
        "title": "基本プロンプト作成",
        "session_number": 1,
        "session_title": "プロンプトの基本構造"
    },
    "content": "あなたは経験豊富なキャリアカウンセラーです。以下の情報をもとに、ビジネスシーン向けの自己紹介文を作成してください...",
    "file": {
        "url": "https://storage.example.com/files/xxx.pdf",
        "name": "supplement.pdf",
        "size_bytes": 102400
    },
    "status": "evaluated",
    "submitted_at": "2026-01-02T15:00:00Z",
    "evaluation": {
        "id": "eval1-uuid",
        "score": 85,
        "breakdown": {
            "elements": 22,
            "practicality": 23,
            "creativity": 18,
            "completeness": 22
        },
        "good_points": [
            "役割設定が明確で、キャリアカウンセラーとしての専門性を活かしています",
            "出力形式（300文字以内）の指定が具体的です"
        ],
        "improvements": [
            "ビジネスシーンの具体的な場面（面接、名刺交換等）を指定するとより効果的です"
        ],
        "next_step": "Session 2では、文脈設定についてさらに深く学びます。今回の自己紹介プロンプトに文脈を追加する練習をしてみましょう。",
        "evaluator_type": "gemini",
        "created_at": "2026-01-02T15:05:00Z"
    }
}
```

---

### 6.3 下書き保存

**エンドポイント**: `PUT /exercises/{exercise_id}/draft`

**認証**: 必須

> **注意**: 下書きは提出前の状態であり、まだ`submission_id`が存在しないため、課題IDで識別する。

**リクエスト**:
```json
{
    "content": "あなたは経験豊富な..."
}
```

**レスポンス（成功: 200）**:
```json
{
    "id": "sub1-uuid",
    "status": "draft",
    "content": "あなたは経験豊富な...",
    "updated_at": "2026-01-02T14:30:00Z"
}
```

---

### 6.4 下書き取得

**エンドポイント**: `GET /exercises/{exercise_id}/draft`

**認証**: 必須

**レスポンス（成功: 200 - 下書きあり）**:
```json
{
    "exercise_id": "ex1-uuid",
    "content": "あなたは経験豊富な...",
    "has_draft": true,
    "updated_at": "2026-01-02T14:30:00Z"
}
```

**レスポンス（成功: 200 - 下書きなし）**:
```json
{
    "exercise_id": "ex1-uuid",
    "content": null,
    "has_draft": false,
    "updated_at": null
}
```

---

### 6.5 課題提出

**エンドポイント**: `POST /submissions`

**認証**: 必須

**リクエスト（multipart/form-data）**:
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| exercise_id | uuid | ✓ | 課題ID |
| content | string | ✓ | 回答テキスト |
| file | file | - | 添付ファイル（10MB以下） |

**レスポンス（成功: 201）**:
```json
{
    "id": "sub1-uuid",
    "exercise_id": "ex1-uuid",
    "status": "submitted",
    "submitted_at": "2026-01-02T15:00:00Z",
    "message": "提出を受け付けました。評価完了までしばらくお待ちください。"
}
```

**再提出時の動作**:
- 同一課題への再提出は **上書き更新** として処理されます
- 既存のsubmissionレコードのcontent、file_url、submitted_atが更新されます
- 既存の評価（evaluations）は無効化（is_active = false）され、新規評価が実行されます
- 最新の提出・評価が常に有効として表示されます

**レスポンス（再提出成功: 200）**:
```json
{
    "id": "sub1-uuid",
    "exercise_id": "ex1-uuid",
    "status": "submitted",
    "submitted_at": "2026-01-05T10:30:00Z",
    "is_resubmission": true,
    "message": "再提出を受け付けました。評価完了までしばらくお待ちください。"
}
```

---

## 7. 評価API

### 7.1 評価詳細取得

**エンドポイント**: `GET /evaluations/{evaluation_id}`

**認証**: 必須

**レスポンス（成功: 200）**:
```json
{
    "id": "eval1-uuid",
    "submission_id": "sub1-uuid",
    "score": 85,
    "breakdown": {
        "elements": 22,
        "practicality": 23,
        "creativity": 18,
        "completeness": 22
    },
    "good_points": [
        "役割設定が明確で、キャリアカウンセラーとしての専門性を活かしています",
        "出力形式（300文字以内）の指定が具体的です"
    ],
    "improvements": [
        "ビジネスシーンの具体的な場面（面接、名刺交換等）を指定するとより効果的です"
    ],
    "next_step": "Session 2では、文脈設定についてさらに深く学びます。",
    "evaluator_type": "gemini",
    "model_version": "gemini-1.5-flash",
    "created_at": "2026-01-02T15:05:00Z"
}
```

---

## 8. 視聴ログAPI

### 8.1 視聴チェックイン

**エンドポイント**: `POST /viewing-logs`

**認証**: 必須

**リクエスト**:
```json
{
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**レスポンス（成功: 201）**:
```json
{
    "id": "vlog1-uuid",
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "checked_in_at": "2026-01-03T11:00:00Z",
    "message": "視聴完了を記録しました"
}
```

**エラーレスポンス（409 - 既にチェックイン済み）**:
```json
{
    "type": "https://api.example.com/errors/already-checked-in",
    "title": "Already Checked In",
    "status": 409,
    "detail": "このセッションは既に視聴完了記録済みです"
}
```

---

### 8.2 視聴ログ一覧取得

**エンドポイント**: `GET /viewing-logs`

**認証**: 必須

**レスポンス（成功: 200）**:
```json
{
    "viewing_logs": [
        {
            "id": "vlog1-uuid",
            "session": {
                "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "number": 1,
                "title": "プロンプトの基本構造"
            },
            "checked_in_at": "2026-01-02T14:30:00Z"
        },
        {
            "id": "vlog2-uuid",
            "session": {
                "id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
                "number": 2,
                "title": "文脈と制約の設計"
            },
            "checked_in_at": "2026-01-03T11:00:00Z"
        }
    ],
    "total": 2
}
```

---

## 9. ダッシュボードAPI

### 9.1 受講者ダッシュボード

**エンドポイント**: `GET /dashboard`

**認証**: 必須（learner）

**レスポンス（成功: 200）**:
```json
{
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "山田太郎"
    },
    "progress": {
        "overall_pct": 45,
        "sessions_viewed": 6,
        "sessions_total": 12,
        "viewing_progress_pct": 50,
        "required_exercises_completed": 6,
        "required_exercises_total": 12,
        "exercise_progress_pct": 50,
        "optional_exercises_completed": 3,
        "optional_exercises_total": 12,
        "is_completion_eligible": false,
        "completion_requirements": {
            "viewing_100pct": false,
            "required_exercises_100pct": false,
            "final_presentation_attended": false
        }
    },
    "next_actions": [
        {
            "type": "exercise",
            "priority": "high",
            "message": "Session 4の課題「対話型プロンプト設計」が未提出です",
            "link": "/sessions/session4-uuid/exercises/ex1-uuid"
        },
        {
            "type": "viewing",
            "priority": "medium",
            "message": "Session 5の動画が未視聴です",
            "link": "/sessions/session5-uuid"
        }
    ],
    "recent_evaluations": [
        {
            "exercise_title": "業務報告メール作成",
            "session_number": 3,
            "score": 85,
            "evaluated_at": "2026-01-02T15:05:00Z",
            "link": "/submissions/sub1-uuid"
        }
    ],
    "average_score": 82.5
}
```

---

### 9.2 修了状態確認

**エンドポイント**: `GET /completion-status`

**認証**: 必須（learner）

**レスポンス（成功: 200）**:
```json
{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "is_completed": false,
    "completion_date": null,
    "requirements": {
        "viewing": {
            "required": 12,
            "completed": 6,
            "progress_pct": 50,
            "is_met": false
        },
        "required_exercises": {
            "required": 12,
            "completed": 6,
            "progress_pct": 50,
            "is_met": false,
            "breakdown": {
                "session_1_11": { "required": 11, "completed": 5 },
                "final_project": {
                    "required": 1,
                    "completed": 1,
                    "note": "EX-23〜26の4成果物全て提出で1課題完了",
                    "deliverables": {
                        "EX-23": { "title": "GPTs設計書", "submitted": true },
                        "EX-24": { "title": "GPTs実装＋運用ログ", "submitted": true },
                        "EX-25": { "title": "振り返りレポート", "submitted": true },
                        "EX-26": { "title": "最終発表資料", "submitted": true }
                    }
                }
            }
        },
        "final_presentation": {
            "is_met": false,
            "attended_at": null
        }
    },
    "certificate": {
        "is_available": false,
        "download_url": null
    }
}
```

> **修了要件**:
> - 動画視聴率: **100%**（12セッション全て）
> - 必須課題提出率: **100%**（Session 1-11各1課題 + 最終課題）
> - 最終発表: **参加必須**（Week 13）

---

## 10. 管理者API

### 10.1 受講者一覧取得

**エンドポイント**: `GET /admin/learners`

**認証**: 必須（instructor, admin）

**クエリパラメータ**:
| パラメータ | 型 | 必須 | デフォルト | 説明 |
|---|---|---|---|---|
| status | string | - | - | ステータスでフィルタ |
| search | string | - | - | 名前・メールで検索 |
| sort_by | string | - | name | ソート項目 |
| sort_order | string | - | asc | ソート順 |
| page | integer | - | 1 | ページ番号 |
| per_page | integer | - | 50 | 1ページあたりの件数 |

**レスポンス（成功: 200）**:
```json
{
    "learners": [
        {
            "id": "user1-uuid",
            "name": "山田太郎",
            "email": "yamada@example.com",
            "organization": "株式会社A",
            "status": "active",
            "progress": {
                "viewing_pct": 46,
                "submission_pct": 42,
                "average_score": 82.5
            },
            "last_activity_at": "2026-01-03T10:00:00Z"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 50,
        "total": 24,
        "total_pages": 1
    }
}
```

---

### 10.2 受講者招待

**エンドポイント**: `POST /admin/invitations`

**認証**: 必須（admin）

**リクエスト**:
```json
{
    "email": "newuser@example.com",
    "name": "新規受講者",
    "organization": "株式会社B"
}
```

**レスポンス（成功: 201）**:
```json
{
    "id": "user-new-uuid",
    "email": "newuser@example.com",
    "name": "新規受講者",
    "status": "invited",
    "invite_expires_at": "2026-01-10T11:00:00Z",
    "message": "招待メールを送信しました"
}
```

---

### 10.3 手動評価キュー取得

**エンドポイント**: `GET /admin/evaluation-queue`

**認証**: 必須（instructor, admin）

**レスポンス（成功: 200）**:
```json
{
    "queue": [
        {
            "id": "sub-manual-uuid",
            "learner": {
                "id": "user1-uuid",
                "name": "山田太郎"
            },
            "exercise": {
                "id": "ex1-uuid",
                "title": "基本プロンプト作成",
                "session_number": 1
            },
            "reason": "api_timeout",
            "submitted_at": "2026-01-02T15:00:00Z",
            "waiting_since": "2026-01-02T15:10:00Z"
        }
    ],
    "total": 2
}
```

---

### 10.4 手動評価入力

**エンドポイント**: `POST /admin/submissions/{submission_id}/evaluate`

**認証**: 必須（instructor, admin）

**リクエスト**:
```json
{
    "score": 88,
    "breakdown": {
        "elements": 23,
        "practicality": 22,
        "creativity": 21,
        "completeness": 22
    },
    "good_points": [
        "役割設定が明確です",
        "制約条件が具体的です"
    ],
    "improvements": [
        "より具体的な出力例を含めると効果的です"
    ],
    "next_step": "次のセッションでは文脈設定を学びます"
}
```

**レスポンス（成功: 201）**:
```json
{
    "id": "eval-manual-uuid",
    "submission_id": "sub-manual-uuid",
    "score": 88,
    "evaluator_type": "manual",
    "created_at": "2026-01-03T14:00:00Z",
    "message": "評価を登録しました。受講者に通知を送信しました。"
}
```

---

### 10.5 レポート出力

**エンドポイント**: `GET /admin/reports/export`

**認証**: 必須（admin）

**クエリパラメータ**:
| パラメータ | 型 | 必須 | デフォルト | 説明 |
|---|---|---|---|---|
| type | string | ✓ | - | レポート種別（progress, viewing, evaluation） |
| format | string | - | csv | 出力形式（csv, xlsx） |
| from_date | date | - | - | 開始日 |
| to_date | date | - | - | 終了日 |

**レスポンス（成功: 200）**:
```
Content-Type: text/csv
Content-Disposition: attachment; filename="progress_report_20260103.csv"

受講者ID,氏名,所属,視聴進捗,提出進捗,平均スコア,最終活動日
user1-uuid,山田太郎,株式会社A,46%,42%,82.5,2026-01-03
...
```

---

### 10.6 最終発表参加記録

Week 13の最終発表への参加を記録する（修了要件の一つ）。

**エンドポイント**: `POST /admin/learners/{user_id}/final-presentation`

**認証**: 必須（instructor, admin）

**リクエスト**:
```json
{
    "attended_at": "2026-03-28T13:00:00Z",
    "notes": "発表時間20分、質疑5分完了"
}
```

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| attended_at | datetime | - | 参加日時（省略時は現在時刻） |
| notes | string | - | 備考（任意） |

**レスポンス（成功: 200）**:
```json
{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "final_presentation_attended_at": "2026-03-28T13:00:00Z",
    "is_completion_eligible": true,
    "message": "最終発表参加を記録しました"
}
```

**エラーレスポンス（400）**:
```json
{
    "type": "https://api.example.com/errors/validation-error",
    "title": "Validation Error",
    "status": 400,
    "detail": "既に最終発表参加が記録されています"
}
```

> **注意**: 受講者自身はこのAPIを呼び出せない。講師または管理者が発表参加を確認後に記録する。

---

### 10.7 コホート一覧取得

**エンドポイント**: `GET /admin/cohorts`

**認証**: 必須（admin）

**クエリパラメータ**:
| パラメータ | 型 | 必須 | デフォルト | 説明 |
|---|---|---|---|---|
| status | string | - | - | ステータスでフィルタ（active/completed/cancelled） |
| organization | string | - | - | 企業名でフィルタ |

**レスポンス（成功: 200）**:
```json
{
    "cohorts": [
        {
            "id": "cohort1-uuid",
            "name": "第1期（2026年4月開講）",
            "organization": "株式会社サンプル",
            "start_date": "2026-04-01",
            "end_date": "2026-06-30",
            "status": "active",
            "members_count": 15,
            "created_at": "2026-01-05T10:00:00Z"
        }
    ],
    "total": 3
}
```

---

### 10.8 コホート作成

**エンドポイント**: `POST /admin/cohorts`

**認証**: 必須（admin）

**リクエスト**:
```json
{
    "name": "第2期（2026年7月開講）",
    "organization": "株式会社サンプル",
    "start_date": "2026-07-01",
    "end_date": "2026-09-30",
    "description": "夏期開講コース",
    "max_participants": 20
}
```

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| name | string | ✓ | コホート名 |
| organization | string | ✓ | 企業名 |
| start_date | date | ✓ | 開講日 |
| end_date | date | ✓ | 修了予定日 |
| description | string | - | 説明 |
| max_participants | integer | - | 最大参加者数 |

**レスポンス（成功: 201）**:
```json
{
    "id": "cohort2-uuid",
    "name": "第2期（2026年7月開講）",
    "organization": "株式会社サンプル",
    "start_date": "2026-07-01",
    "end_date": "2026-09-30",
    "status": "active",
    "message": "コホートを作成しました"
}
```

---

### 10.9 コホート編集

**エンドポイント**: `PUT /admin/cohorts/{cohort_id}`

**認証**: 必須（admin）

**リクエスト**:
```json
{
    "name": "第2期（2026年7月開講）【更新】",
    "status": "completed"
}
```

**レスポンス（成功: 200）**:
```json
{
    "id": "cohort2-uuid",
    "name": "第2期（2026年7月開講）【更新】",
    "status": "completed",
    "updated_at": "2026-10-01T10:00:00Z",
    "message": "コホートを更新しました"
}
```

---

### 10.10 コホートメンバー割当

**エンドポイント**: `POST /admin/cohorts/{cohort_id}/members`

**認証**: 必須（admin）

**リクエスト**:
```json
{
    "user_ids": [
        "user1-uuid",
        "user2-uuid",
        "user3-uuid"
    ]
}
```

**レスポンス（成功: 200）**:
```json
{
    "cohort_id": "cohort1-uuid",
    "added_count": 3,
    "members_count": 18,
    "message": "3名をコホートに追加しました"
}
```

**エラーレスポンス（400）**:
```json
{
    "type": "https://api.example.com/errors/validation-error",
    "title": "Validation Error",
    "status": 400,
    "detail": "一部のユーザーは既に他のコホートに所属しています",
    "conflicts": ["user2-uuid"]
}
```

---

### 10.11 コホートメンバー削除

**エンドポイント**: `DELETE /admin/cohorts/{cohort_id}/members/{user_id}`

**認証**: 必須（admin）

**レスポンス（成功: 200）**:
```json
{
    "cohort_id": "cohort1-uuid",
    "user_id": "user1-uuid",
    "members_count": 17,
    "message": "メンバーをコホートから削除しました"
}
```

---

## 11. Webhook（内部）

### 11.1 評価完了通知

Gemini API評価完了後、内部的に呼び出される。

**エンドポイント**: `POST /internal/webhooks/evaluation-complete`

**認証**: 内部APIキー

**リクエスト**:
```json
{
    "submission_id": "sub1-uuid",
    "evaluation_id": "eval1-uuid",
    "status": "success",
    "score": 85
}
```

**処理**:
1. submissionsテーブルのstatusを`evaluated`に更新
2. 受講者へメール通知送信
3. notificationsテーブルに記録

---

## 12. エラーレスポンス共通仕様

### 12.1 エラー形式（RFC 7807）

```json
{
    "type": "https://api.example.com/errors/{error-type}",
    "title": "Human Readable Title",
    "status": 400,
    "detail": "詳細なエラーメッセージ",
    "instance": "/api/v1/endpoint",
    "errors": [
        {
            "field": "email",
            "message": "有効なメールアドレス形式で入力してください"
        }
    ]
}
```

### 12.2 共通エラーコード

| HTTPステータス | type | 説明 |
|---|---|---|
| 400 | validation-error | バリデーションエラー |
| 401 | authentication-required | 認証が必要 |
| 403 | forbidden | 権限不足 |
| 404 | not-found | リソースが見つからない |
| 409 | conflict | 競合（重複登録等） |
| 422 | unprocessable-entity | 処理不可 |
| 423 | account-locked | アカウントロック |
| 429 | rate-limit-exceeded | レート制限超過 |
| 500 | internal-error | サーバーエラー |
| 503 | service-unavailable | サービス利用不可 |

---

## 13. レート制限

| エンドポイント | 制限 | ウィンドウ |
|---|---|---|
| POST /auth/login | 5回 | 15分 |
| POST /submissions | 10回 | 1時間 |
| その他API | 100回 | 1分 |

**レート制限超過時のレスポンス（429）**:
```json
{
    "type": "https://api.example.com/errors/rate-limit-exceeded",
    "title": "Rate Limit Exceeded",
    "status": 429,
    "detail": "リクエスト回数が上限に達しました。しばらく待ってから再度お試しください。",
    "retry_after": 60
}
```

**レスポンスヘッダー**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1704268800
Retry-After: 60
```

---

## 14. API変更履歴

| バージョン | 日付 | 変更内容 |
|---|---|---|
| v1.0 | 2026-01-03 | 初版作成 |
| v1.1 | 2026-01-05 | 2パート制対応、修了要件API追加、課題分類（必須/任意）対応 |
| v1.2 | 2026-01-05 | 4要素表記統一、最終発表参加記録API追加、下書きAPI識別子統一 |
| v1.3 | 2026-01-05 | 最終課題（EX-23〜26）の提出形式詳細追加 |
| v1.4 | 2026-01-05 | 利用規約同意API（2.7）追加、コホート管理API（10.7-10.11）追加 |

---

## 承認

| 役割 | 氏名 | 承認日 |
|---|---|---|
| プログラムマネージャー | AI-PgM | 2026-01-05 |
| バックエンドエンジニア | - | - |
