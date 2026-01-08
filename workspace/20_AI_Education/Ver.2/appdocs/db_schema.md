# データベーススキーマ設計書

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 更新日: 2026-01-05
- 版: v1.4（コホート管理・利用規約同意対応）
- 関連文書: ../docs/requirements.md (v2.0), app_spec.md (v1.1), api_spec.md (v1.1)

---

## 1. 概要

### 1.1 データベース選定

| 項目 | 選定 | 理由 |
|---|---|---|
| RDBMS | PostgreSQL 15+ | RLS対応、JSON型、高い信頼性 |
| ホスティング | Supabase | 認証統合、RLS組み込み、無料枠 |
| バックアップ | 日次自動 | Supabase標準機能 |

### 1.2 設計方針

- **RLS（Row Level Security）**: 受講者は自分のデータのみアクセス可能
- **ソフトデリート**: 物理削除せず `deleted_at` で論理削除
- **監査ログ**: 重要操作は `audit_logs` に記録
- **タイムスタンプ**: 全テーブルに `created_at`, `updated_at`

### 1.3 命名規則

| 種別 | 規則 | 例 |
|---|---|---|
| テーブル名 | スネークケース、複数形 | `users`, `submissions` |
| カラム名 | スネークケース | `user_id`, `created_at` |
| 主キー | `id` (UUID) | `id UUID PRIMARY KEY` |
| 外部キー | `{テーブル単数}_id` | `user_id`, `session_id` |
| 論理削除 | `deleted_at` | `deleted_at TIMESTAMPTZ` |
| タイムスタンプ | `created_at`, `updated_at` | `TIMESTAMPTZ` |

---

## 2. ER図

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   cohorts   │       │  sessions   │       │  exercises  │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │       │ id (PK)     │       │ id (PK)     │
│ name        │       │ number      │       │ session_id  │───┐
│ organization│       │ title       │       │ number      │   │
│ start_date  │       │ phase       │       │ title       │   │
│ status      │       │ ...         │       │ is_required │   │
└──────┬──────┘       └──────┬──────┘       └─────────────┘   │
       │                     │                                 │
       │                     │                                 │
       ▼                     │  ┌──────────────────────────────┘
┌─────────────┐              │  │
│   users     │              │  │
├─────────────┤              │  │
│ id (PK)     │              │  │
│ cohort_id   │◄─────────────┘  │
│ email       │                 │
│ name        │                 │
│ role        │                 │
│ terms_...   │                 │
│ ...         │                 │
└──────┬──────┘                 │
       │                        │
       │  ┌─────────────────────┘
       │  │
       ▼  ▼
┌─────────────────┐       ┌─────────────────┐
│   submissions   │       │   evaluations   │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ user_id (FK)    │◄──────│ submission_id   │
│ exercise_id (FK)│       │ score           │
│ content         │       │ breakdown       │
│ status          │       │ evaluator_type  │
│ ...             │       │ ...             │
└────────┬────────┘       └─────────────────┘
         │
         ▼
┌─────────────────┐
│  viewing_logs   │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ session_id (FK) │
│ checked_in_at   │
│ ...             │
└─────────────────┘
```

---

## 3. テーブル定義

### 3.1 cohorts（コホート）

期別・企業別の受講者グループを管理。

```sql
CREATE TABLE cohorts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    organization VARCHAR(200) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    description TEXT,
    max_participants INT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,

    CONSTRAINT cohorts_status_check CHECK (status IN ('active', 'completed', 'cancelled')),
    CONSTRAINT cohorts_date_check CHECK (end_date >= start_date)
);

CREATE INDEX idx_cohorts_organization ON cohorts(organization) WHERE deleted_at IS NULL;
CREATE INDEX idx_cohorts_status ON cohorts(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_cohorts_start_date ON cohorts(start_date);
```

| カラム | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | UUID | NO | 自動生成 | 主キー |
| name | VARCHAR(200) | NO | - | コホート名（例: 第1期（2026年4月開講）） |
| organization | VARCHAR(200) | NO | - | 企業名 |
| start_date | DATE | NO | - | 開講日 |
| end_date | DATE | NO | - | 修了予定日 |
| status | VARCHAR(20) | NO | 'active' | 状態（active/completed/cancelled） |
| description | TEXT | YES | - | コホート説明 |
| max_participants | INT | YES | - | 最大参加者数 |
| created_at | TIMESTAMPTZ | NO | NOW() | 作成日時 |
| updated_at | TIMESTAMPTZ | NO | NOW() | 更新日時 |
| deleted_at | TIMESTAMPTZ | YES | - | 論理削除日時 |

---

### 3.2 users（ユーザー）

受講者・講師・管理者のアカウント情報を管理。

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    encrypted_password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'learner',
    organization VARCHAR(200),
    cohort_id UUID REFERENCES cohorts(id),           -- コホートID（FK）
    status VARCHAR(20) NOT NULL DEFAULT 'invited',
    invite_token VARCHAR(100) UNIQUE,
    invite_expires_at TIMESTAMPTZ,
    last_login_at TIMESTAMPTZ,
    login_failed_count INT NOT NULL DEFAULT 0,
    locked_until TIMESTAMPTZ,
    terms_agreed_at TIMESTAMPTZ,                     -- 利用規約同意日時
    terms_version VARCHAR(20),                       -- 同意した規約バージョン
    terms_ip_address INET,                           -- 同意時のIPアドレス
    final_presentation_attended_at TIMESTAMPTZ,      -- 最終発表参加日時（Week 13）
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,

    CONSTRAINT users_role_check CHECK (role IN ('learner', 'instructor', 'admin')),
    CONSTRAINT users_status_check CHECK (status IN ('invited', 'active', 'suspended', 'completed'))
);

CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_role ON users(role) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_status ON users(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_invite_token ON users(invite_token) WHERE invite_token IS NOT NULL;
CREATE INDEX idx_users_cohort_id ON users(cohort_id) WHERE deleted_at IS NULL;
```

| カラム | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | UUID | NO | 自動生成 | 主キー |
| email | VARCHAR(255) | NO | - | メールアドレス（ログインID） |
| encrypted_password | VARCHAR(255) | NO | - | ハッシュ化パスワード |
| name | VARCHAR(100) | NO | - | 氏名 |
| role | VARCHAR(20) | NO | 'learner' | ロール（learner/instructor/admin） |
| organization | VARCHAR(200) | YES | - | 所属組織 |
| cohort_id | UUID | YES | - | コホートID（FK） |
| status | VARCHAR(20) | NO | 'invited' | 状態（invited/active/suspended/completed） |
| invite_token | VARCHAR(100) | YES | - | 招待トークン |
| invite_expires_at | TIMESTAMPTZ | YES | - | 招待有効期限 |
| last_login_at | TIMESTAMPTZ | YES | - | 最終ログイン日時 |
| login_failed_count | INT | NO | 0 | ログイン失敗回数 |
| locked_until | TIMESTAMPTZ | YES | - | アカウントロック解除日時 |
| terms_agreed_at | TIMESTAMPTZ | YES | - | 利用規約同意日時 |
| terms_version | VARCHAR(20) | YES | - | 同意した規約バージョン |
| terms_ip_address | INET | YES | - | 同意時のIPアドレス |
| final_presentation_attended_at | TIMESTAMPTZ | YES | - | 最終発表参加日時（Week 13） |
| created_at | TIMESTAMPTZ | NO | NOW() | 作成日時 |
| updated_at | TIMESTAMPTZ | NO | NOW() | 更新日時 |
| deleted_at | TIMESTAMPTZ | YES | - | 論理削除日時 |

---

### 3.2 sessions（セッション）

12セッションのマスターデータ（Session 12-13は1セッション扱い）。

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    number INT NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    phase INT NOT NULL,
    phase_name VARCHAR(100) NOT NULL,
    description TEXT,
    duration_minutes INT NOT NULL DEFAULT 20,  -- 2パート×約10分
    video_part1_url VARCHAR(500),              -- Part X-1: 理論編
    video_part2_url VARCHAR(500),              -- Part X-2: 実践編
    materials_url VARCHAR(500),
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT sessions_number_check CHECK (number BETWEEN 1 AND 12),  -- 12セッション（Session 12-13は1セッション扱い）
    CONSTRAINT sessions_phase_check CHECK (phase BETWEEN 1 AND 4)
);

CREATE INDEX idx_sessions_number ON sessions(number);
CREATE INDEX idx_sessions_phase ON sessions(phase);
CREATE INDEX idx_sessions_published ON sessions(is_published);
```

| カラム | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | UUID | NO | 自動生成 | 主キー |
| number | INT | NO | - | セッション番号（1-12） |
| title | VARCHAR(200) | NO | - | セッションタイトル |
| phase | INT | NO | - | フェーズ番号（1-4） |
| phase_name | VARCHAR(100) | NO | - | フェーズ名 |
| description | TEXT | YES | - | セッション説明 |
| duration_minutes | INT | NO | 20 | 所要時間（分）2パート×約10分 |
| video_part1_url | VARCHAR(500) | YES | - | Part X-1（理論編）動画URL |
| video_part2_url | VARCHAR(500) | YES | - | Part X-2（実践編）動画URL |
| materials_url | VARCHAR(500) | YES | - | 補足資料URL |
| is_published | BOOLEAN | NO | FALSE | 公開フラグ |
| published_at | TIMESTAMPTZ | YES | - | 公開日時 |
| created_at | TIMESTAMPTZ | NO | NOW() | 作成日時 |
| updated_at | TIMESTAMPTZ | NO | NOW() | 更新日時 |

---

### 3.3 exercises（課題）

各セッションに紐づく課題のマスターデータ。

```sql
CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(id),
    number INT NOT NULL,
    exercise_code VARCHAR(10) NOT NULL,              -- 課題コード（EX-01〜EX-26）
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    is_required BOOLEAN NOT NULL DEFAULT TRUE,
    rubric_elements TEXT,
    rubric_practicality TEXT,
    rubric_creativity TEXT,
    rubric_completeness TEXT,
    max_length INT NOT NULL DEFAULT 2000,
    allow_file_upload BOOLEAN NOT NULL DEFAULT TRUE,
    evaluation_prompt TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT exercises_session_number_unique UNIQUE (session_id, number),
    CONSTRAINT exercises_code_unique UNIQUE (exercise_code)
);

CREATE INDEX idx_exercises_session_id ON exercises(session_id);
CREATE INDEX idx_exercises_required ON exercises(is_required);
CREATE INDEX idx_exercises_code ON exercises(exercise_code);
```

| カラム | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | UUID | NO | 自動生成 | 主キー |
| session_id | UUID | NO | - | セッションID（FK） |
| number | INT | NO | - | 課題番号（セッション内） |
| exercise_code | VARCHAR(10) | NO | - | 課題コード（EX-01〜EX-26） |
| title | VARCHAR(200) | NO | - | 課題タイトル |
| description | TEXT | NO | - | 課題説明・指示 |
| is_required | BOOLEAN | NO | TRUE | 必須課題フラグ |
| rubric_elements | TEXT | YES | - | 評価観点: 基本要素 |
| rubric_practicality | TEXT | YES | - | 評価観点: 実用性 |
| rubric_creativity | TEXT | YES | - | 評価観点: 創意工夫 |
| rubric_completeness | TEXT | YES | - | 評価観点: 完成度 |
| max_length | INT | NO | 2000 | 最大文字数 |
| allow_file_upload | BOOLEAN | NO | TRUE | ファイル添付可否 |
| evaluation_prompt | TEXT | YES | - | LLM評価用プロンプト |
| created_at | TIMESTAMPTZ | NO | NOW() | 作成日時 |
| updated_at | TIMESTAMPTZ | NO | NOW() | 更新日時 |

---

### 3.4 submissions（提出物）

受講者の課題提出を管理。

> **最終課題（EX-23〜26）の提出ルール**:
> - 4成果物それぞれを**個別レコード**として提出（submissions テーブルに4行）
> - 修了判定時は「EX-23〜26全て提出済み」で「最終課題完了」として**1課題**カウント
> - 各成果物は個別に評価され、4つの平均スコアが最終課題の評価となる

```sql
CREATE TABLE submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    exercise_id UUID NOT NULL REFERENCES exercises(id),
    content TEXT NOT NULL,
    file_url VARCHAR(500),
    file_name VARCHAR(255),
    file_size_bytes INT,
    status VARCHAR(20) NOT NULL DEFAULT 'submitted',
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT submissions_status_check CHECK (
        status IN ('draft', 'submitted', 'evaluating', 'evaluated', 'manual_queue')
    ),
    CONSTRAINT submissions_user_exercise_unique UNIQUE (user_id, exercise_id)
);

CREATE INDEX idx_submissions_user_id ON submissions(user_id);
CREATE INDEX idx_submissions_exercise_id ON submissions(exercise_id);
CREATE INDEX idx_submissions_status ON submissions(status);
CREATE INDEX idx_submissions_submitted_at ON submissions(submitted_at);
```

| カラム | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | UUID | NO | 自動生成 | 主キー |
| user_id | UUID | NO | - | 提出者ID（FK） |
| exercise_id | UUID | NO | - | 課題ID（FK） |
| content | TEXT | NO | - | 提出テキスト |
| file_url | VARCHAR(500) | YES | - | 添付ファイルURL |
| file_name | VARCHAR(255) | YES | - | 添付ファイル名 |
| file_size_bytes | INT | YES | - | ファイルサイズ |
| status | VARCHAR(20) | NO | 'submitted' | 状態 |
| submitted_at | TIMESTAMPTZ | NO | NOW() | 提出日時 |
| created_at | TIMESTAMPTZ | NO | NOW() | 作成日時 |
| updated_at | TIMESTAMPTZ | NO | NOW() | 更新日時 |

**ステータス定義**:
| status | 説明 |
|---|---|
| draft | 下書き保存 |
| submitted | 提出済み（評価待ち） |
| evaluating | LLM評価中 |
| evaluated | 評価完了 |
| manual_queue | 手動評価待ち |

---

### 3.5 evaluations（評価結果）

LLMまたは講師による評価結果を管理。

```sql
CREATE TABLE evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID NOT NULL REFERENCES submissions(id),
    evaluator_type VARCHAR(20) NOT NULL,
    evaluator_user_id UUID REFERENCES users(id),
    score INT NOT NULL,
    breakdown JSONB NOT NULL,
    good_points JSONB NOT NULL DEFAULT '[]',
    improvements JSONB NOT NULL DEFAULT '[]',
    next_step TEXT,
    raw_response JSONB,
    model_version VARCHAR(50),
    processing_time_ms INT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT evaluations_evaluator_type_check CHECK (
        evaluator_type IN ('gemini', 'manual')
    ),
    CONSTRAINT evaluations_score_check CHECK (score BETWEEN 0 AND 100)
);

CREATE INDEX idx_evaluations_submission_id ON evaluations(submission_id);
CREATE INDEX idx_evaluations_evaluator_type ON evaluations(evaluator_type);
CREATE INDEX idx_evaluations_is_active ON evaluations(is_active);
CREATE INDEX idx_evaluations_created_at ON evaluations(created_at);
```

| カラム | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | UUID | NO | 自動生成 | 主キー |
| submission_id | UUID | NO | - | 提出物ID（FK） |
| evaluator_type | VARCHAR(20) | NO | - | 評価者タイプ |
| evaluator_user_id | UUID | YES | - | 手動評価者ID（FK） |
| score | INT | NO | - | 総合スコア（0-100） |
| breakdown | JSONB | NO | - | 内訳スコア |
| good_points | JSONB | NO | '[]' | 良い点リスト |
| improvements | JSONB | NO | '[]' | 改善点リスト |
| next_step | TEXT | YES | - | 次のステップ |
| raw_response | JSONB | YES | - | LLM生レスポンス |
| model_version | VARCHAR(50) | YES | - | 使用モデル |
| processing_time_ms | INT | YES | - | 処理時間（ミリ秒） |
| is_active | BOOLEAN | NO | TRUE | 有効フラグ |
| created_at | TIMESTAMPTZ | NO | NOW() | 作成日時 |

**breakdown JSONスキーマ**:
```json
{
    "elements": 25,
    "practicality": 22,
    "creativity": 20,
    "completeness": 18
}
```

**evaluator_type定義**:
| type | 説明 |
|---|---|
| gemini | Gemini APIによる自動評価 |
| manual | 講師による手動評価 |

---

### 3.6 viewing_logs（視聴ログ）

動画視聴完了チェックインを管理。

```sql
CREATE TABLE viewing_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    session_id UUID NOT NULL REFERENCES sessions(id),
    checked_in_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT viewing_logs_user_session_unique UNIQUE (user_id, session_id)
);

CREATE INDEX idx_viewing_logs_user_id ON viewing_logs(user_id);
CREATE INDEX idx_viewing_logs_session_id ON viewing_logs(session_id);
CREATE INDEX idx_viewing_logs_checked_in_at ON viewing_logs(checked_in_at);
```

| カラム | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | UUID | NO | 自動生成 | 主キー |
| user_id | UUID | NO | - | 受講者ID（FK） |
| session_id | UUID | NO | - | セッションID（FK） |
| checked_in_at | TIMESTAMPTZ | NO | NOW() | チェックイン日時 |
| ip_address | INET | YES | - | IPアドレス |
| user_agent | TEXT | YES | - | ユーザーエージェント |
| created_at | TIMESTAMPTZ | NO | NOW() | 作成日時 |

---

### 3.7 notifications（通知）

メール通知の送信履歴を管理。

```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    type VARCHAR(50) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    related_id UUID,
    related_type VARCHAR(50),
    sent_at TIMESTAMPTZ,
    opened_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT notifications_type_check CHECK (
        type IN ('welcome', 'submission_evaluated',
                 'reminder', 'session_published', 'system')
    )
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_type ON notifications(type);
CREATE INDEX idx_notifications_sent_at ON notifications(sent_at);
```

| カラム | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | UUID | NO | 自動生成 | 主キー |
| user_id | UUID | NO | - | 受信者ID（FK） |
| type | VARCHAR(50) | NO | - | 通知タイプ |
| subject | VARCHAR(255) | NO | - | 件名 |
| body | TEXT | NO | - | 本文 |
| related_id | UUID | YES | - | 関連オブジェクトID |
| related_type | VARCHAR(50) | YES | - | 関連オブジェクト種別 |
| sent_at | TIMESTAMPTZ | YES | - | 送信日時 |
| opened_at | TIMESTAMPTZ | YES | - | 開封日時 |
| created_at | TIMESTAMPTZ | NO | NOW() | 作成日時 |

---

### 3.8 audit_logs（監査ログ）

重要操作の監査証跡を保存。

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

| カラム | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | UUID | NO | 自動生成 | 主キー |
| user_id | UUID | YES | - | 操作者ID（FK） |
| action | VARCHAR(100) | NO | - | 操作種別 |
| resource_type | VARCHAR(50) | NO | - | 対象リソース種別 |
| resource_id | UUID | YES | - | 対象リソースID |
| old_values | JSONB | YES | - | 変更前の値 |
| new_values | JSONB | YES | - | 変更後の値 |
| ip_address | INET | YES | - | IPアドレス |
| user_agent | TEXT | YES | - | ユーザーエージェント |
| created_at | TIMESTAMPTZ | NO | NOW() | 作成日時 |

**記録対象アクション**:
- `user.login` / `user.logout`
- `user.password_changed`
- `submission.created` / `submission.submitted`
- `evaluation.created` (manual)
- `session.published`
- `user.role_changed`

---

## 4. RLS（Row Level Security）ポリシー

### 4.1 users テーブル

```sql
-- RLSを有効化
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- 受講者: 自分のレコードのみ
CREATE POLICY users_learner_select ON users
    FOR SELECT
    USING (
        id = auth.uid()
        OR (auth.jwt() ->> 'role')::text IN ('instructor', 'admin')
    );

-- 管理者: 全レコード更新可能
CREATE POLICY users_admin_all ON users
    FOR ALL
    USING ((auth.jwt() ->> 'role')::text = 'admin');
```

### 4.2 submissions テーブル

```sql
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;

-- 受講者: 自分の提出物のみ
CREATE POLICY submissions_learner_select ON submissions
    FOR SELECT
    USING (
        user_id = auth.uid()
        OR (auth.jwt() ->> 'role')::text IN ('instructor', 'admin')
    );

-- 受講者: 自分の提出物のみ作成・更新
CREATE POLICY submissions_learner_insert ON submissions
    FOR INSERT
    WITH CHECK (user_id = auth.uid());

CREATE POLICY submissions_learner_update ON submissions
    FOR UPDATE
    USING (user_id = auth.uid() AND status = 'draft');
```

### 4.3 evaluations テーブル

```sql
ALTER TABLE evaluations ENABLE ROW LEVEL SECURITY;

-- 受講者: 自分の提出物に対する評価のみ閲覧
CREATE POLICY evaluations_learner_select ON evaluations
    FOR SELECT
    USING (
        submission_id IN (
            SELECT id FROM submissions WHERE user_id = auth.uid()
        )
        OR (auth.jwt() ->> 'role')::text IN ('instructor', 'admin')
    );

-- 講師・管理者: 評価作成可能
CREATE POLICY evaluations_instructor_insert ON evaluations
    FOR INSERT
    WITH CHECK ((auth.jwt() ->> 'role')::text IN ('instructor', 'admin'));
```

### 4.4 viewing_logs テーブル

```sql
ALTER TABLE viewing_logs ENABLE ROW LEVEL SECURITY;

-- 受講者: 自分のログのみ
CREATE POLICY viewing_logs_learner ON viewing_logs
    FOR ALL
    USING (
        user_id = auth.uid()
        OR (auth.jwt() ->> 'role')::text IN ('instructor', 'admin')
    );
```

---

## 5. ビュー

### 5.1 learner_progress（受講者進捗ビュー）

```sql
CREATE VIEW learner_progress AS
SELECT
    u.id AS user_id,
    u.name,
    u.email,
    u.organization,
    u.status,
    COUNT(DISTINCT vl.session_id) AS sessions_viewed,
    12 AS total_sessions,
    ROUND(COUNT(DISTINCT vl.session_id)::numeric / 12 * 100, 1) AS viewing_progress_pct,
    COUNT(DISTINCT s.id) FILTER (WHERE s.status = 'evaluated') AS exercises_completed,
    (SELECT COUNT(*) FROM exercises WHERE is_required = TRUE) AS total_required_exercises,
    ROUND(
        COUNT(DISTINCT s.id) FILTER (WHERE s.status = 'evaluated')::numeric /
        NULLIF((SELECT COUNT(*) FROM exercises WHERE is_required = TRUE), 0) * 100,
        1
    ) AS submission_progress_pct,
    AVG(e.score) FILTER (WHERE e.is_active = TRUE) AS avg_score,
    MAX(s.submitted_at) AS last_submission_at,
    MAX(vl.checked_in_at) AS last_viewing_at
FROM users u
LEFT JOIN viewing_logs vl ON u.id = vl.user_id
LEFT JOIN submissions s ON u.id = s.user_id
LEFT JOIN evaluations e ON s.id = e.submission_id
WHERE u.role = 'learner' AND u.deleted_at IS NULL
GROUP BY u.id, u.name, u.email, u.organization, u.status;
```

### 5.2 session_completion_stats（セッション完了統計ビュー）

```sql
CREATE VIEW session_completion_stats AS
SELECT
    s.id AS session_id,
    s.number AS session_number,
    s.title,
    COUNT(DISTINCT vl.user_id) AS viewers_count,
    (SELECT COUNT(*) FROM users WHERE role = 'learner' AND deleted_at IS NULL) AS total_learners,
    ROUND(
        COUNT(DISTINCT vl.user_id)::numeric /
        NULLIF((SELECT COUNT(*) FROM users WHERE role = 'learner' AND deleted_at IS NULL), 0) * 100,
        1
    ) AS viewing_completion_pct
FROM sessions s
LEFT JOIN viewing_logs vl ON s.id = vl.session_id
GROUP BY s.id, s.number, s.title
ORDER BY s.number;
```

---

## 6. 関数・トリガー

### 6.1 updated_at 自動更新

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 各テーブルに適用
CREATE TRIGGER trigger_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trigger_submissions_updated_at
    BEFORE UPDATE ON submissions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### 6.2 監査ログ自動記録

```sql
CREATE OR REPLACE FUNCTION log_audit()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (
        user_id,
        action,
        resource_type,
        resource_id,
        old_values,
        new_values
    ) VALUES (
        auth.uid(),
        TG_OP,
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id),
        CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN to_jsonb(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN to_jsonb(NEW) ELSE NULL END
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

## 7. 初期データ

### 7.1 セッションマスター

```sql
-- 12セッション構成（Session 12-13は「最終課題」として1セッション扱い）
INSERT INTO sessions (number, title, phase, phase_name, description) VALUES
-- Phase 1: 手書きプロンプト基礎 (Week 1-3)
(1, 'プロンプトの基本構造', 1, '手書きプロンプト基礎', 'プロンプトの4要素（指示・文脈・制約・出力形式）を学ぶ'),
(2, '文脈・制約・出力形式', 1, '手書きプロンプト基礎', 'ペルソナ設定、業務プロンプト'),
(3, '対話型プロンプト', 1, '手書きプロンプト基礎', '改善ループ、要件定義→実行'),
-- Phase 2: メタプロンプト設計 (Week 4-5)
(4, '複合プロンプト', 2, 'メタプロンプト設計', '改善ループ＋要件定義→実行の組み合わせ'),
(5, 'メタプロンプト', 2, 'メタプロンプト設計', 'プロンプトを生成するプロンプト'),
-- Phase 3: GPTs構築 (Week 6-10)
(6, 'GPTsの概念と企画', 3, 'GPTs構築', 'メタプロンプトでGPTs企画書生成'),
(7, 'Instructions設計', 3, 'GPTs構築', 'メタプロンプトでInstructions生成'),
(8, '知識ベース構築', 3, 'GPTs構築', 'メタプロンプトで知識ファイル設計'),
(9, 'テストと改善', 3, 'GPTs構築', 'メタプロンプトでテストケース生成'),
(10, '仕様書完成', 3, 'GPTs構築', 'メタプロンプトで仕様書統合'),
-- Phase 4: 業務GPTs実運用 (Week 11-13)
(11, '業務プロセス分析', 4, '業務GPTs実運用', 'メタプロンプトでフロー図・ボトルネック分析'),
(12, '最終課題', 4, '業務GPTs実運用', '設計→実装→運用→20分発表（Week 12-13）');
```

> **注**: Session 12は従来のSession 12-13を統合。最終課題（EX-23〜26）を含む2週間分。

---

## 8. データ保持・削除ポリシー

| データ種別 | 保持期間 | 削除方式 | 備考 |
|---|---|---|---|
| 受講者データ | 5年 | ソフトデリート | 助成金監査対応 |
| 提出物・評価 | 5年 | ソフトデリート | 助成金エビデンス |
| 視聴ログ | 7年 | 保持 | 助成金証跡 |
| 監査ログ | 7年 | 保持 | コンプライアンス |
| 通知履歴 | 1年 | 物理削除 | 運用データ |

---

## 9. マイグレーション戦略

### 9.1 バージョン管理

- マイグレーションツール: Supabase Migrations / Prisma Migrate
- 命名規則: `YYYYMMDDHHMMSS_description.sql`

### 9.2 ロールバック方針

- 各マイグレーションに `down.sql` を作成
- 本番適用前にステージングで検証
- データ移行を伴う場合はバックアップ必須

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|---|---|---|
| v1.0 | 2026-01-03 | 初版作成 |
| v1.1 | 2026-01-05 | 2パート制対応（20分→10分×2）、12セッション構成、修了要件明確化 |
| v1.2 | 2026-01-05 | usersテーブルにfinal_presentation_attended_atカラム追加 |
| v1.3 | 2026-01-05 | 最終課題（EX-23〜26）の提出ルール明確化 |
| v1.4 | 2026-01-05 | cohortsテーブル追加、usersにcohort_id・利用規約同意カラム追加 |

---

## 承認

| 役割 | 氏名 | 承認日 |
|---|---|---|
| プログラムマネージャー | AI-PgM | 2026-01-05 |
| データベースエンジニア | - | - |
