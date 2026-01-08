# 助成金コンプライアンス仕様書

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 作成日: 2026-01-05
- 版: v1.0
- 関連文書: operation_sop.md (v2.0), db_schema.md (v1.3), api_spec.md (v1.3)

---

## 1. 概要

### 1.1 対象助成金

| 助成金名 | 管轄 | 対象 |
|---|---|---|
| **人材開発支援助成金** | 厚生労働省 | 事業主が雇用する労働者に対する職業訓練 |
| **リスキリング支援コース** | 厚生労働省 | デジタル分野等の新たな分野での人材育成 |

### 1.2 本プログラムの助成金適格性

| 要件 | 本プログラムの対応 | 適合 |
|---|---|---|
| 訓練時間10時間以上 | 約40時間（動画4時間＋課題20時間＋ミーティング8時間） | ✅ |
| OFF-JT（座学）であること | eラーニング＋オンラインミーティング | ✅ |
| 訓練内容が業務に関連 | 生成AI活用スキルは業務直結 | ✅ |
| 受講証明が可能 | 視聴ログ・提出ログ・参加ログで証明 | ✅ |
| 修了証発行 | 修了要件達成者に発行 | ✅ |

---

## 2. 厚労省要件マッピング

### 2.1 訓練実施計画に必要な情報

| 厚労省要件 | システム対応 | 出力方法 |
|---|---|---|
| **訓練実施期間** | プログラム開始〜終了日（13週間） | 管理画面で設定・出力 |
| **訓練時間数** | 総時間数の自動集計 | 受講者別CSVエクスポート |
| **訓練内容** | 各セッションの学習目標 | カリキュラム文書PDF |
| **訓練方法** | eラーニング＋同時双方向通信 | 実施報告書 |
| **受講対象者名簿** | 登録済み受講者リスト | 管理画面CSVエクスポート |

### 2.2 訓練実施記録に必要な情報

| 厚労省要件 | システム対応 | データソース |
|---|---|---|
| **出席記録** | 動画視聴チェックイン | viewing_logs テーブル |
| **ミーティング参加記録** | Zoomログから手動集計（外部管理） | Zoom管理画面 |
| **課題提出記録** | 課題提出履歴 | submissions テーブル |
| **学習時間記録** | 自動算出（動画＋課題）+ Zoom手動集計 | 合算レポート |
| **修了判定記録** | 修了要件達成フラグ | users.status = 'completed' |

> **Note**: ミーティング参加記録はZoom管理画面から別途エクスポートし、CSVで統合します。

---

## 3. 学習時間計算ロジック

### 3.1 時間要素の定義

| 要素 | 算出方法 | 標準時間 | データソース |
|---|---|---|---|
| **動画視聴** | 視聴完了セッション数 × セッション時間 | 20分/セッション | viewing_logs |
| **課題取り組み** | 提出済み課題数 × 課題標準時間 | 課題別固定値（下表参照） | submissions + 固定マスタ |
| **ミーティング参加** | 参加回数 × 60分 | 60分/回 | Zoom参加ログ（外部） |

> **Note**: 課題標準時間はDB上のカラムではなく、下表の固定値をレポート出力時に適用します。

### 3.2 課題標準時間一覧

| Phase | 課題コード | 課題名 | 標準時間 | 必須/任意 |
|---|---|---|---|---|
| Phase 1 | EX-01 | 初めてのAI対話 | 30分 | 必須 |
| Phase 1 | EX-02 | 役割設定を試す | 45分 | 任意 |
| Phase 2 | EX-03 | 文脈設計の実践 | 60分 | 必須 |
| Phase 2 | EX-04 | 出力形式の指定 | 45分 | 任意 |
| Phase 2 | EX-05 | 制約条件の活用 | 45分 | 任意 |
| Phase 2 | EX-06 | 議事録作成の最適化 | 60分 | 必須 |
| Phase 3 | EX-07 | フィードバック活用 | 45分 | 任意 |
| Phase 3 | EX-08 | 段階的洗練 | 60分 | 必須 |
| Phase 3 | EX-09 | 改善サイクル設計 | 60分 | 任意 |
| Phase 3 | EX-10 | 要件定義の言語化 | 60分 | 必須 |
| Phase 3 | EX-11 | メタプロンプト理論 | 45分 | 任意 |
| Phase 3 | EX-12 | メタプロンプト実践 | 75分 | 必須 |
| Phase 3 | EX-13 | GPTs基礎設計 | 60分 | 任意 |
| Phase 3 | EX-14 | カスタムGPTs作成 | 90分 | 必須 |
| Phase 4 | EX-15 | 業務シナリオ分析 | 60分 | 任意 |
| Phase 4 | EX-16 | GPTs高度設計 | 75分 | 必須 |
| Phase 4 | EX-17 | 知識ベース構築 | 60分 | 任意 |
| Phase 4 | EX-18 | 運用テスト計画 | 45分 | 任意 |
| Phase 4 | EX-19 | 運用実践（5回以上） | 120分 | 必須 |
| Phase 4 | EX-20 | フィードバック分析 | 60分 | 任意 |
| Phase 4 | EX-21 | 改善ドキュメント | 60分 | 必須 |
| Phase 4 | EX-22 | 業務展開提案 | 75分 | 任意 |
| 最終 | EX-23 | GPTs設計書 | 90分 | 必須 |
| 最終 | EX-24 | GPTs実装＋運用ログ | 120分 | 必須 |
| 最終 | EX-25 | 振り返りレポート | 60分 | 必須 |
| 最終 | EX-26 | 最終発表資料 | 90分 | 必須 |

**最終課題（EX-23〜26）の扱い**: 4成果物で1課題としてカウント

### 3.3 総学習時間の算出SQL

```sql
-- 受講者別総学習時間算出（動画＋課題のみ。ミーティングは外部集計）
-- 課題標準時間はアプリ側で固定マッピングを適用

WITH video_time AS (
  SELECT
    vl.user_id,
    COUNT(DISTINCT vl.session_id) * 20 AS video_minutes
  FROM viewing_logs vl
  WHERE vl.checked_in_at IS NOT NULL
  GROUP BY vl.user_id
),
exercise_counts AS (
  SELECT
    s.user_id,
    e.exercise_code,
    COUNT(*) AS submission_count
  FROM submissions s
  JOIN exercises e ON e.id = s.exercise_id
  WHERE s.submitted_at IS NOT NULL
  GROUP BY s.user_id, e.exercise_code
)
SELECT
  u.id AS user_id,
  u.name,
  u.email,
  u.organization AS "所属",
  COALESCE(vt.video_minutes, 0) AS video_minutes,
  -- 課題時間はアプリ側で exercise_code → 標準時間マッピングを適用
  -- ここでは提出課題数のみ出力
  (SELECT COUNT(DISTINCT exercise_code) FROM exercise_counts ec WHERE ec.user_id = u.id) AS submitted_exercises
FROM users u
LEFT JOIN video_time vt ON vt.user_id = u.id
WHERE u.role = 'learner'
  AND u.deleted_at IS NULL
ORDER BY u.name;
```

> **運用手順**: 上記SQLで基礎データを出力後、3.2の標準時間表を参照して課題時間を算出。ミーティング参加時間はZoomレポートから別途集計し、最終レポートで合算。

### 3.4 目標学習時間

| 項目 | 時間 | 備考 |
|---|---|---|
| 動画視聴 | 4時間 | 20分×12セッション |
| 必須課題 | 約13時間 | 12課題（最終課題含む） |
| 任意課題 | 約10時間 | 12課題（全て取り組んだ場合） |
| ミーティング | 8時間 | 60分×8回 |
| **最小合計（必須のみ）** | **約25時間** | 助成金要件（10時間）を大幅超過 |
| **最大合計（全課題）** | **約35時間** | - |

---

## 4. 視聴ログ証跡フォーマット

### 4.1 データベーステーブル（現行スキーマ）

```sql
-- viewing_logs テーブル（db_schema.md準拠）
-- Note: 現行スキーマはチェックイン方式（視聴完了時に1レコード作成）

CREATE TABLE viewing_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  session_id UUID NOT NULL REFERENCES sessions(id),
  checked_in_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),  -- 視聴完了チェックイン日時
  ip_address INET,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  UNIQUE(user_id, session_id)
);
```

> **Note**: 現行スキーマでは詳細な視聴開始/終了時刻は記録せず、セッション単位でのチェックイン方式を採用。助成金証跡としては「視聴完了日時」と「IPアドレス」で対応。

### 4.2 エクスポート形式（CSV）

**ファイル名**: `視聴証跡_{出力日}.csv`

**カラム定義**:

| # | カラム名 | 説明 | 例 |
|---|---|---|---|
| 1 | 受講者ID | システム内部ID | USR-001 |
| 2 | 受講者名 | 氏名 | 山田太郎 |
| 3 | メールアドレス | 登録メール | yamada@example.com |
| 4 | 所属 | organization列 | 株式会社サンプル |
| 5 | セッション番号 | 1〜12 | 1 |
| 6 | セッション名 | Session 1: プロンプト基礎 | Session 1: プロンプト基礎 |
| 7 | 視聴完了日時 | ISO 8601 | 2026-01-06T10:12:34+09:00 |
| 8 | IPアドレス | IPv4/IPv6 | 192.168.1.1 |

**エクスポートSQL**:

```sql
SELECT
  'USR-' || LPAD(ROW_NUMBER() OVER (ORDER BY u.created_at)::TEXT, 3, '0') AS "受講者ID",
  u.name AS "受講者名",
  u.email AS "メールアドレス",
  u.organization AS "所属",
  s.number AS "セッション番号",
  s.title AS "セッション名",
  TO_CHAR(vl.checked_in_at AT TIME ZONE 'Asia/Tokyo', 'YYYY-MM-DD"T"HH24:MI:SS+09:00') AS "視聴完了日時",
  vl.ip_address::TEXT AS "IPアドレス"
FROM viewing_logs vl
JOIN users u ON u.id = vl.user_id
JOIN sessions s ON s.id = vl.session_id
WHERE u.deleted_at IS NULL
ORDER BY u.name, s.number;
```

---

## 5. 課題提出証跡フォーマット

### 5.1 エクスポート形式（CSV）

**ファイル名**: `課題提出証跡_{企業名}_{出力日}.csv`

**カラム定義**:

| # | カラム名 | 説明 | 例 |
|---|---|---|---|
| 1 | 受講者ID | システム内部ID | USR-001 |
| 2 | 受講者名 | 氏名 | 山田太郎 |
| 3 | 課題コード | EX-01〜EX-26 | EX-01 |
| 4 | 課題名 | 課題タイトル | 初めてのAI対話 |
| 5 | 必須/任意 | required/optional | required |
| 6 | 提出日時 | ISO 8601 | 2026-01-06T15:30:00+09:00 |
| 7 | 評価スコア | 0-100 | 85 |
| 8 | 評価日時 | ISO 8601 | 2026-01-06T15:35:12+09:00 |
| 9 | 評価者 | gemini/instructor | gemini |
| 10 | 標準時間（分） | 課題設定値 | 30 |

---

## 6. ミーティング参加証跡フォーマット

### 6.1 データ管理方法（外部管理）

> **Note**: 現行スキーマではミーティング参加記録をDB管理しません。Zoom管理画面からエクスポートしたレポートを利用します。

**Zoomレポート取得手順**:
1. Zoom管理画面 → レポート → 使用状況レポート → ミーティング
2. 対象ミーティングを選択
3. 参加者一覧をCSVでエクスポート

### 6.2 エクスポート形式（Zoom標準 + 手動統合）

**カラム定義**（Zoom標準レポートから抽出）:

| # | カラム名 | 説明 | 例 |
|---|---|---|---|
| 1 | 受講者名 | 氏名（Zoom登録名から照合） | 山田太郎 |
| 2 | ミーティング番号 | 1〜8（手動付与） | 1 |
| 3 | 開催日 | YYYY-MM-DD | 2026-01-10 |
| 4 | 参加有無 | レポートに存在すればtrue | true |
| 5 | 参加開始時刻 | HH:MM | 19:02 |
| 6 | 参加終了時刻 | HH:MM | 20:01 |
| 7 | 参加時間（分） | 整数 | 59 |

> **統合手順**: Zoomレポートを受講者名簿と照合し、助成金レポート用CSVに統合。

---

## 7. 修了判定証跡

### 7.1 修了要件

| 要件 | 条件 | 確認方法 |
|---|---|---|
| 動画視聴 | 12セッション×2パート＝24本すべて完了 | viewing_logs |
| 必須課題提出 | 12課題すべて提出済み | submissions |
| 最終発表参加 | 最終発表に参加 | final_presentation_attended_at |

### 7.2 修了判定SQL

```sql
-- 修了要件達成状況
-- Note: 現行スキーマではviewing_logsはセッション単位（パート単位ではない）
-- 24本視聴 = 12セッション × 2パート → 簡易的に12セッション完了で判定
WITH video_completion AS (
  SELECT
    user_id,
    COUNT(DISTINCT session_id) AS completed_sessions,
    COUNT(DISTINCT session_id) >= 12 AS video_complete
  FROM viewing_logs
  GROUP BY user_id
),
exercise_completion AS (
  SELECT
    s.user_id,
    COUNT(DISTINCT s.exercise_id) AS submitted_required,
    COUNT(DISTINCT s.exercise_id) >= 12 AS exercise_complete
  FROM submissions s
  JOIN exercises e ON e.id = s.exercise_id
  WHERE e.is_required = true
    AND s.submitted_at IS NOT NULL
  GROUP BY s.user_id
),
presentation_completion AS (
  SELECT
    id AS user_id,
    final_presentation_attended_at IS NOT NULL AS presentation_complete
  FROM users
)
SELECT
  u.id,
  u.name,
  u.email,
  COALESCE(vc.completed_sessions, 0) AS video_sessions_completed,
  COALESCE(vc.video_complete, false) AS video_requirement_met,
  COALESCE(ec.submitted_required, 0) AS required_exercises_submitted,
  COALESCE(ec.exercise_complete, false) AS exercise_requirement_met,
  pc.presentation_complete AS presentation_requirement_met,
  CASE
    WHEN COALESCE(vc.video_complete, false)
     AND COALESCE(ec.exercise_complete, false)
     AND pc.presentation_complete
    THEN true
    ELSE false
  END AS completion_eligible
FROM users u
LEFT JOIN video_completion vc ON vc.user_id = u.id
LEFT JOIN exercise_completion ec ON ec.user_id = u.id
LEFT JOIN presentation_completion pc ON pc.user_id = u.id
WHERE u.role = 'learner'
  AND u.deleted_at IS NULL
ORDER BY u.name;
```

### 7.3 修了証エクスポート形式

**ファイル名**: `修了者名簿_{企業名}_{出力日}.csv`

| # | カラム名 | 説明 |
|---|---|---|
| 1 | 修了証番号 | CERT-2026-001 形式 |
| 2 | 受講者名 | 氏名 |
| 3 | メールアドレス | - |
| 4 | 所属企業 | - |
| 5 | 受講開始日 | users.created_at（登録日） |
| 6 | 修了日 | 最終要件達成日 |
| 7 | 総学習時間 | 時間単位 |
| 8 | 動画視聴完了率 | 100% |
| 9 | 必須課題提出率 | 100% |
| 10 | 平均評価スコア | 0-100 |

---

## 8. データエクスポートAPI

### 8.1 エンドポイント一覧

| エンドポイント | 説明 | 権限 |
|---|---|---|
| `GET /admin/export/viewing-logs` | 視聴証跡CSV | admin |
| `GET /admin/export/submissions` | 課題提出証跡CSV | admin |
| `GET /admin/export/attendance` | ミーティング参加証跡CSV | admin |
| `GET /admin/export/completion` | 修了者名簿CSV | admin |
| `GET /admin/export/learning-hours` | 学習時間集計CSV | admin |
| `GET /admin/export/all` | 全証跡一括ZIP | admin |

### 8.2 クエリパラメータ

| パラメータ | 型 | 説明 |
|---|---|---|
| organization | string | 対象企業名（任意、フィルタ用） |
| start_date | date | 開始日（任意） |
| end_date | date | 終了日（任意） |
| format | string | csv（デフォルト）/ xlsx |

> **Note**: 現行スキーマではcohortsテーブルを使用せず、users.organizationでフィルタリングします。

### 8.3 レスポンス例

```http
GET /admin/export/learning-hours?organization=株式会社サンプル&format=csv

HTTP/1.1 200 OK
Content-Type: text/csv; charset=utf-8
Content-Disposition: attachment; filename="学習時間集計_第1期_2026-01-05.csv"

受講者ID,受講者名,メールアドレス,所属企業,動画視聴（分）,課題取組（分）,ミーティング（分）,合計（分）,合計（時間）
USR-001,山田太郎,yamada@example.com,株式会社サンプル,240,780,480,1500,25.0
...
```

---

## 9. 監査対応チェックリスト

### 9.1 事前準備チェック

| # | 確認項目 | 確認方法 | 担当 |
|---|---|---|---|
| 1 | 訓練実施計画書の作成 | テンプレート使用 | PM |
| 2 | 受講者名簿の準備 | 管理画面エクスポート | Admin |
| 3 | カリキュラム詳細の文書化 | curriculum_design.md | PM |
| 4 | 講師の資格証明 | 経歴書・実績 | 講師 |

### 9.2 実施中チェック

| # | 確認項目 | 頻度 | 担当 |
|---|---|---|---|
| 1 | 視聴ログの確認 | 週次 | Admin |
| 2 | 課題提出状況の確認 | 週次 | Admin |
| 3 | 未受講者へのフォローアップ | 週次 | Support |
| 4 | データバックアップ | 日次（自動） | System |

### 9.3 終了後チェック

| # | 確認項目 | 期限 | 担当 |
|---|---|---|---|
| 1 | 全証跡データのエクスポート | 修了後1週間 | Admin |
| 2 | 修了証の発行・記録 | 修了後2週間 | PM |
| 3 | 学習時間集計の確定 | 修了後2週間 | Admin |
| 4 | 助成金申請書類の作成 | 修了後1ヶ月 | PM |
| 5 | 証跡データの長期保管 | 5年間 | System |

### 9.4 監査時対応

| 要求 | 対応方法 | 所要時間 |
|---|---|---|
| 受講者名簿の提出 | 管理画面からCSVエクスポート | 即時 |
| 出席記録の提出 | 視聴ログ＋ミーティング参加記録エクスポート | 即時 |
| 学習時間の証明 | 学習時間集計CSVエクスポート | 即時 |
| 修了者リストの提出 | 修了者名簿CSVエクスポート | 即時 |
| 訓練内容の説明 | カリキュラム文書＋動画サンプル | 30分 |

---

## 10. データ保持・セキュリティ

### 10.1 保持期間

| データ種別 | 保持期間 | 根拠 |
|---|---|---|
| 受講者情報 | 5年 | 助成金要件 |
| 視聴ログ | 5年 | 助成金要件 |
| 課題提出データ | 5年 | 助成金要件 |
| 評価結果 | 5年 | 助成金要件 |
| 修了証記録 | 永続 | ビジネス要件 |
| 監査ログ | 7年 | 会計監査要件 |

### 10.2 アクセス制御

| 役割 | 閲覧可能データ | エクスポート権限 |
|---|---|---|
| learner | 自分のデータのみ | なし |
| instructor | 全受講者データ | なし |
| admin | 全データ | 全エクスポート可能 |

### 10.3 データ削除ポリシー

- **個人情報削除要求**: 法定保持期間（5年）経過後に対応
- **保持期間終了後**: 自動削除ジョブで物理削除
- **削除ログ**: 削除実行の監査ログを別途保持

---

## 11. 変更履歴

| 日付 | バージョン | 変更内容 |
|---|---|---|
| 2026-01-05 | v1.0 | 初版作成 |
