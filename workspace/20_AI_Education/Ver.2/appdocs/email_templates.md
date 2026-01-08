# メール通知テンプレート仕様書

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 作成日: 2026-01-05
- 版: v1.0
- 関連文書: auth_design.md (v1.0), operation_sop.md (v2.0), api_spec.md (v1.3)

---

## 1. 概要

### 1.1 メール配信方式

| 項目 | 選定 | 理由 |
|---|---|---|
| 配信基盤 | Supabase Auth + Edge Functions | 認証メール統合、コスト効率 |
| トランザクションメール | Resend | 高配信率、Next.js統合、無料枠 |
| テンプレートエンジン | React Email | TypeScript対応、プレビュー可能 |

### 1.2 メール種別一覧

| # | 種別 | トリガー | 送信先 | 優先度 |
|---|---|---|---|---|
| 1 | 招待メール | 管理者が受講者を登録 | learner | 必須 |
| 2 | パスワードリセット | 本人がリセット要求 | all | 必須 |
| 3 | 評価完了通知 | Gemini API評価完了 | learner | 必須 |
| 4 | リマインダー（視聴） | 週次バッチ（未視聴検知） | learner | 必須 |
| 5 | リマインダー（課題） | 週次バッチ（未提出検知） | learner | 必須 |
| 6 | 修了証発行通知 | 修了要件達成 | learner | 必須 |
| 7 | 週次進捗サマリー | 週次バッチ（毎週月曜） | instructor, admin | 任意 |

---

## 2. 共通設計

### 2.1 送信元情報

```
From: AIポリテラシー育成プログラム <noreply@{domain}>
Reply-To: support@{domain}
```

### 2.2 共通ヘッダー/フッター

**ヘッダー**:
```html
<div style="background: #4F46E5; padding: 20px; text-align: center;">
  <img src="{logo_url}" alt="AIポリテラシー育成プログラム" height="40">
</div>
```

**フッター**:
```html
<div style="background: #F3F4F6; padding: 20px; text-align: center; font-size: 12px; color: #6B7280;">
  <p>本メールは自動送信です。返信はサポート窓口へお願いします。</p>
  <p>サポート: support@{domain}</p>
  <p>© 2026 AIポリテラシー育成プログラム</p>
  <p><a href="{unsubscribe_url}">配信設定の変更</a></p>
</div>
```

### 2.3 変数プレースホルダー

| 変数 | 説明 | 例 |
|---|---|---|
| `{user_name}` | 受講者名 | 山田太郎 |
| `{user_email}` | メールアドレス | yamada@example.com |
| `{app_url}` | アプリケーションURL | https://ai-literacy.example.com |
| `{domain}` | ドメイン | ai-literacy.example.com |
| `{support_email}` | サポートメール | support@example.com |
| `{current_date}` | 送信日 | 2026年1月5日 |
| `{invite_link}` | 招待リンク（48時間有効） | https://ai-literacy.example.com/auth/invite?token=xxx |
| `{reset_url}` | パスワードリセットリンク | https://ai-literacy.example.com/auth/reset?token=xxx |
| `{logo_url}` | ロゴ画像URL | https://ai-literacy.example.com/logo.png |
| `{unsubscribe_url}` | 配信停止設定URL | https://ai-literacy.example.com/settings/notifications |

---

## 3. テンプレート詳細

### 3.1 招待メール（Invitation）

**トリガー**: 管理者が `/admin/invite` APIで受講者を登録

**件名**:
```
【AIポリテラシー育成プログラム】受講のご案内
```

**本文**:
```html
<p>{user_name} 様</p>

<p>AIポリテラシー育成プログラム Ver.2へのご登録ありがとうございます。</p>

<p>以下の招待リンクをクリックして、アカウントを有効化してください。</p>

<div style="background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center;">
  <a href="{invite_link}" style="display: inline-block; background: #4F46E5; color: white; padding: 12px 32px; border-radius: 6px; text-decoration: none; font-weight: bold;">
    アカウントを有効化する
  </a>
  <p style="margin-top: 12px; font-size: 12px; color: #6B7280;">
    このリンクは48時間有効です
  </p>
</div>

<p style="color: #6B7280; font-size: 14px;">
  ボタンがクリックできない場合は、以下のURLをブラウザに貼り付けてください：<br>
  <code style="word-break: break-all;">{invite_link}</code>
</p>

<h3>受講の流れ</h3>
<ol>
  <li>上記リンクをクリックしてパスワードを設定</li>
  <li>利用規約に同意</li>
  <li>Session 0（オリエンテーション）を視聴</li>
  <li>Week 1の動画視聴・課題提出を開始</li>
</ol>

<h3>プログラム概要</h3>
<ul>
  <li><strong>期間:</strong> 13週間</li>
  <li><strong>動画:</strong> 各セッション約20分（10分×2パート）</li>
  <li><strong>課題:</strong> 必須12課題 + 任意12課題</li>
  <li><strong>ミーティング:</strong> 隔週Zoom（全8回）</li>
</ul>

<h3>修了要件</h3>
<ul>
  <li>動画視聴率: 100%</li>
  <li>必須課題提出率: 100%</li>
  <li>最終発表への参加</li>
</ul>

<p>ご不明点は <a href="mailto:{support_email}">{support_email}</a> までお問い合わせください。</p>
```

**プレーンテキスト版**:
```
{user_name} 様

AIポリテラシー育成プログラム Ver.2へのご登録ありがとうございます。

以下の招待リンクをクリックして、アカウントを有効化してください。

━━━━━━━━━━━━━━━━━━━━━━━━━━
招待リンク: {invite_link}
（このリンクは48時間有効です）
━━━━━━━━━━━━━━━━━━━━━━━━━━

【受講の流れ】
1. 上記リンクをクリックしてパスワードを設定
2. 利用規約に同意
3. Session 0（オリエンテーション）を視聴
4. Week 1の動画視聴・課題提出を開始

【プログラム概要】
- 期間: 13週間
- 動画: 各セッション約20分（10分×2パート）
- 課題: 必須12課題 + 任意12課題
- ミーティング: 隔週Zoom（全8回）

【修了要件】
- 動画視聴率: 100%
- 必須課題提出率: 100%
- 最終発表への参加

ご不明点は {support_email} までお問い合わせください。
```

---

### 3.2 パスワードリセット（Password Reset）

**トリガー**: ユーザーがログイン画面から「パスワードを忘れた」をクリック

**件名**:
```
【AIポリテラシー育成プログラム】パスワードリセットのご案内
```

**本文**:
```html
<p>{user_name} 様</p>

<p>パスワードリセットのリクエストを受け付けました。</p>

<p>以下のボタンをクリックして、新しいパスワードを設定してください。</p>

<div style="text-align: center; margin: 30px 0;">
  <a href="{reset_url}" style="background: #4F46E5; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold;">
    パスワードをリセット
  </a>
</div>

<p style="color: #6B7280; font-size: 14px;">
  このリンクは <strong>24時間</strong> 有効です。<br>
  リンクの有効期限が切れた場合は、再度リセットをリクエストしてください。
</p>

<div style="background: #FEF3C7; border: 1px solid #F59E0B; border-radius: 8px; padding: 16px; margin: 20px 0;">
  <p style="margin: 0; color: #92400E;">
    <strong>心当たりがない場合</strong><br>
    このメールに心当たりがない場合は、無視してください。<br>
    パスワードは変更されません。
  </p>
</div>

<p style="color: #6B7280; font-size: 12px;">
  リンクが機能しない場合は、以下のURLをブラウザに直接貼り付けてください:<br>
  <code>{reset_url}</code>
</p>
```

**有効期限**: 24時間

**リトライ制限**: 同一メールアドレスに対して1時間に3回まで

---

### 3.3 評価完了通知（Evaluation Complete）

**トリガー**: Gemini APIによる自動評価が完了

**件名**:
```
【AIポリテラシー育成プログラム】{exercise_title} の評価が完了しました
```

**本文**:
```html
<p>{user_name} 様</p>

<p>ご提出いただいた課題の評価が完了しました。</p>

<div style="background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 20px; margin: 20px 0;">
  <h3 style="margin-top: 0;">評価結果</h3>
  <table style="width: 100%; border-collapse: collapse;">
    <tr>
      <td style="padding: 8px 0; border-bottom: 1px solid #E5E7EB;"><strong>セッション:</strong></td>
      <td style="padding: 8px 0; border-bottom: 1px solid #E5E7EB;">{session_title}</td>
    </tr>
    <tr>
      <td style="padding: 8px 0; border-bottom: 1px solid #E5E7EB;"><strong>課題:</strong></td>
      <td style="padding: 8px 0; border-bottom: 1px solid #E5E7EB;">{exercise_title}</td>
    </tr>
    <tr>
      <td style="padding: 8px 0; border-bottom: 1px solid #E5E7EB;"><strong>スコア:</strong></td>
      <td style="padding: 8px 0; border-bottom: 1px solid #E5E7EB;">
        <span style="font-size: 24px; font-weight: bold; color: {score_color};">{score}</span> / 100点
      </td>
    </tr>
    <tr>
      <td style="padding: 8px 0;"><strong>評価日時:</strong></td>
      <td style="padding: 8px 0;">{evaluated_at}</td>
    </tr>
  </table>
</div>

<h3>フィードバック</h3>
<div style="background: #EFF6FF; border-left: 4px solid #3B82F6; padding: 16px; margin: 20px 0;">
  <p style="margin: 0;">{feedback_summary}</p>
</div>

<h3>評価詳細（ルーブリック）</h3>
<table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background: #F3F4F6;">
      <th style="padding: 12px; text-align: left; border: 1px solid #E5E7EB;">評価項目</th>
      <th style="padding: 12px; text-align: center; border: 1px solid #E5E7EB;">スコア</th>
      <th style="padding: 12px; text-align: left; border: 1px solid #E5E7EB;">コメント</th>
    </tr>
  </thead>
  <tbody>
    {rubric_rows}
  </tbody>
</table>

<div style="text-align: center; margin: 30px 0;">
  <a href="{app_url}/exercises/{exercise_id}/result" style="background: #4F46E5; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold;">
    詳細を確認する
  </a>
</div>

<p style="color: #6B7280; font-size: 14px;">
  ※ 評価に疑問がある場合は、ミーティングで講師にご質問ください。
</p>
```

**スコア色の条件分岐**:
| スコア範囲 | 色 | 変数値 |
|---|---|---|
| 80-100 | 緑 | `#059669` |
| 60-79 | 青 | `#3B82F6` |
| 40-59 | 黄 | `#D97706` |
| 0-39 | 赤 | `#DC2626` |

---

### 3.4 リマインダー（視聴）

**トリガー**: 週次バッチ（毎週月曜 9:00 JST）で未視聴検知

**条件**:
- 当該週の動画を未視聴
- 視聴進捗が50%未満

**件名**:
```
【AIポリテラシー育成プログラム】{session_title} の動画をまだご視聴いただいていません
```

**本文**:
```html
<p>{user_name} 様</p>

<p>今週視聴予定の動画がまだ完了していません。</p>

<div style="background: #FEF3C7; border: 1px solid #F59E0B; border-radius: 8px; padding: 20px; margin: 20px 0;">
  <h3 style="margin-top: 0; color: #92400E;">未視聴の動画</h3>
  <table style="width: 100%;">
    <tr>
      <td><strong>セッション:</strong></td>
      <td>{session_title}</td>
    </tr>
    <tr>
      <td><strong>パート:</strong></td>
      <td>{unwatched_parts}</td>
    </tr>
    <tr>
      <td><strong>視聴目安:</strong></td>
      <td>約{remaining_minutes}分</td>
    </tr>
  </table>
</div>

<p>修了要件として、すべての動画を視聴する必要があります。</p>

<div style="text-align: center; margin: 30px 0;">
  <a href="{app_url}/sessions/{session_id}" style="background: #4F46E5; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold;">
    動画を視聴する
  </a>
</div>

<h3>あなたの進捗状況</h3>
<table style="width: 100%; margin: 20px 0;">
  <tr>
    <td>動画視聴率:</td>
    <td><strong>{video_progress}%</strong> （{watched_count}/{total_count}本）</td>
  </tr>
  <tr>
    <td>必須課題完了率:</td>
    <td><strong>{exercise_progress}%</strong> （{completed_exercises}/{total_exercises}課題）</td>
  </tr>
</table>
```

**送信頻度制限**: 同一セッションについて週1回まで

---

### 3.5 リマインダー（課題）

**トリガー**: 週次バッチ（毎週金曜 9:00 JST）で未提出検知

**条件**:
- 当該週の必須課題が未提出
- 提出期限まで3日以内

**件名**:
```
【AIポリテラシー育成プログラム】{exercise_title} の提出期限が近づいています
```

**本文**:
```html
<p>{user_name} 様</p>

<p>必須課題の提出期限が近づいています。</p>

<div style="background: #FEE2E2; border: 1px solid #EF4444; border-radius: 8px; padding: 20px; margin: 20px 0;">
  <h3 style="margin-top: 0; color: #991B1B;">未提出の必須課題</h3>
  <table style="width: 100%;">
    <tr>
      <td><strong>課題:</strong></td>
      <td>{exercise_title}</td>
    </tr>
    <tr>
      <td><strong>セッション:</strong></td>
      <td>{session_title}</td>
    </tr>
    <tr>
      <td><strong>推奨提出期限:</strong></td>
      <td style="color: #DC2626; font-weight: bold;">{deadline}</td>
    </tr>
  </table>
</div>

<p>修了要件として、すべての必須課題を提出する必要があります。</p>

<div style="text-align: center; margin: 30px 0;">
  <a href="{app_url}/exercises/{exercise_id}" style="background: #DC2626; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold;">
    課題を提出する
  </a>
</div>

<h3>ヒント</h3>
<ul>
  <li>下書き保存機能を活用して、少しずつ作成できます</li>
  <li>完璧でなくても、まずは提出してフィードバックを受けましょう</li>
  <li>質問があれば、Slackまたはミーティングでお気軽にどうぞ</li>
</ul>
```

**送信頻度制限**: 同一課題について3日に1回まで

---

### 3.6 修了証発行通知

**トリガー**: 修了要件をすべて達成（システム自動判定）

**条件**:
- 動画視聴率: 100%
- 必須課題提出率: 100%
- 最終発表参加: 済み

**件名**:
```
【AIポリテラシー育成プログラム】修了おめでとうございます！修了証を発行しました
```

**本文**:
```html
<p>{user_name} 様</p>

<p style="font-size: 18px; color: #059669; font-weight: bold;">
  AIポリテラシー育成プログラム Ver.2 の修了、おめでとうございます！
</p>

<p>13週間のプログラムを完遂されたことを心よりお祝い申し上げます。</p>

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 30px; margin: 30px 0; text-align: center; color: white;">
  <h2 style="margin-top: 0;">修了証</h2>
  <p style="font-size: 20px; margin: 20px 0;">{user_name} 殿</p>
  <p>AIポリテラシー育成プログラム Ver.2</p>
  <p>修了日: {completion_date}</p>
  <p>修了証番号: {certificate_number}</p>
</div>

<h3>あなたの学習成果</h3>
<table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
  <tr style="background: #F3F4F6;">
    <td style="padding: 12px; border: 1px solid #E5E7EB;"><strong>総学習時間</strong></td>
    <td style="padding: 12px; border: 1px solid #E5E7EB;">{total_learning_hours}時間</td>
  </tr>
  <tr>
    <td style="padding: 12px; border: 1px solid #E5E7EB;"><strong>視聴した動画</strong></td>
    <td style="padding: 12px; border: 1px solid #E5E7EB;">{total_videos}本（{total_video_minutes}分）</td>
  </tr>
  <tr style="background: #F3F4F6;">
    <td style="padding: 12px; border: 1px solid #E5E7EB;"><strong>提出した課題</strong></td>
    <td style="padding: 12px; border: 1px solid #E5E7EB;">{total_exercises}課題</td>
  </tr>
  <tr>
    <td style="padding: 12px; border: 1px solid #E5E7EB;"><strong>平均スコア</strong></td>
    <td style="padding: 12px; border: 1px solid #E5E7EB;">{average_score}点</td>
  </tr>
  <tr style="background: #F3F4F6;">
    <td style="padding: 12px; border: 1px solid #E5E7EB;"><strong>参加ミーティング</strong></td>
    <td style="padding: 12px; border: 1px solid #E5E7EB;">{attended_meetings}回</td>
  </tr>
</table>

<div style="text-align: center; margin: 30px 0;">
  <a href="{certificate_url}" style="background: #4F46E5; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold; margin-right: 10px;">
    修了証をダウンロード (PDF)
  </a>
</div>

<h3>今後について</h3>
<ul>
  <li>修了証は職場やLinkedInでのスキル証明にご活用ください</li>
  <li>学んだスキルを実務で活用し、AIとの協働を続けてください</li>
  <li>フォローアップセミナーやアップデート情報をお送りする場合があります</li>
</ul>

<p>改めまして、プログラムへのご参加ありがとうございました。</p>
```

**添付ファイル**: 修了証PDF（自動生成）

---

### 3.7 週次進捗サマリー（講師・管理者向け）

**トリガー**: 週次バッチ（毎週月曜 8:00 JST）

**送信先**: instructor, admin ロールのユーザー

**件名**:
```
【週次レポート】AIポリテラシー育成プログラム - Week {week_number} 進捗サマリー
```

**本文**:
```html
<p>{user_name} 様</p>

<p>Week {week_number} の受講者進捗をお知らせします。</p>

<h3>概要</h3>
<table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
  <tr style="background: #F3F4F6;">
    <td style="padding: 12px; border: 1px solid #E5E7EB;"><strong>アクティブ受講者</strong></td>
    <td style="padding: 12px; border: 1px solid #E5E7EB;">{active_learners}名</td>
  </tr>
  <tr>
    <td style="padding: 12px; border: 1px solid #E5E7EB;"><strong>今週の動画視聴完了率</strong></td>
    <td style="padding: 12px; border: 1px solid #E5E7EB;">{video_completion_rate}%</td>
  </tr>
  <tr style="background: #F3F4F6;">
    <td style="padding: 12px; border: 1px solid #E5E7EB;"><strong>今週の課題提出率</strong></td>
    <td style="padding: 12px; border: 1px solid #E5E7EB;">{exercise_submission_rate}%</td>
  </tr>
  <tr>
    <td style="padding: 12px; border: 1px solid #E5E7EB;"><strong>平均スコア</strong></td>
    <td style="padding: 12px; border: 1px solid #E5E7EB;">{average_score}点</td>
  </tr>
</table>

<h3>要注意受講者（進捗遅れ）</h3>
<table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background: #FEE2E2;">
      <th style="padding: 12px; text-align: left; border: 1px solid #E5E7EB;">受講者</th>
      <th style="padding: 12px; text-align: center; border: 1px solid #E5E7EB;">動画</th>
      <th style="padding: 12px; text-align: center; border: 1px solid #E5E7EB;">課題</th>
      <th style="padding: 12px; text-align: left; border: 1px solid #E5E7EB;">状況</th>
    </tr>
  </thead>
  <tbody>
    {at_risk_learners_rows}
  </tbody>
</table>

<h3>今週提出された課題（評価待ち）</h3>
<p>評価待ち: <strong>{pending_evaluations}件</strong></p>

<div style="text-align: center; margin: 30px 0;">
  <a href="{app_url}/admin/dashboard" style="background: #4F46E5; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold;">
    管理画面で詳細を確認
  </a>
</div>
```

---

## 4. 技術実装

### 4.1 Supabase Auth メールテンプレート設定

Supabase Dashboardで設定するカスタムテンプレート:

```sql
-- Supabase Auth Settings > Email Templates

-- Confirmation (招待メール用)
Subject: 【AIポリテラシー育成プログラム】受講のご案内
Body: (Section 3.1の内容)

-- Reset Password
Subject: 【AIポリテラシー育成プログラム】パスワードリセットのご案内
Body: (Section 3.2の内容)
```

### 4.2 Resend統合（トランザクションメール）

```typescript
// lib/email/resend.ts
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function sendEmail({
  to,
  subject,
  html,
  text,
  attachments,
}: {
  to: string;
  subject: string;
  html: string;
  text?: string;
  attachments?: Array<{ filename: string; content: Buffer }>;
}) {
  return resend.emails.send({
    from: 'AIポリテラシー育成プログラム <noreply@ai-literacy.example.com>',
    to,
    subject,
    html,
    text,
    attachments,
  });
}
```

### 4.3 バッチ処理（Vercel Cron Jobs）

```typescript
// app/api/cron/send-reminders/route.ts
import { NextResponse } from 'next/server';

export const runtime = 'edge';
export const maxDuration = 60;

export async function GET(request: Request) {
  // Verify cron secret
  const authHeader = request.headers.get('authorization');
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // 1. 未視聴者を検出
  const unwatchedLearners = await getUnwatchedLearners();

  // 2. 未提出者を検出
  const unsubmittedLearners = await getUnsubmittedLearners();

  // 3. リマインダーメール送信
  await sendViewingReminders(unwatchedLearners);
  await sendSubmissionReminders(unsubmittedLearners);

  return NextResponse.json({
    sent: {
      viewing: unwatchedLearners.length,
      submission: unsubmittedLearners.length,
    }
  });
}
```

### 4.4 vercel.json Cron設定

```json
{
  "crons": [
    {
      "path": "/api/cron/send-reminders",
      "schedule": "0 0 * * 1,5"
    },
    {
      "path": "/api/cron/weekly-summary",
      "schedule": "0 23 * * 0"
    }
  ]
}
```

---

## 5. 配信ポリシー

### 5.1 オプトアウト設定

| メール種別 | オプトアウト可否 |
|---|---|
| 招待メール | 不可 |
| パスワードリセット | 不可 |
| 評価完了通知 | 可 |
| リマインダー（視聴） | 可 |
| リマインダー（課題） | 可 |
| 修了証発行通知 | 不可 |
| 週次進捗サマリー | 可 |

### 5.2 配信制限

| 制限項目 | 値 |
|---|---|
| 同一アドレスへの1日あたり送信上限 | 10通 |
| リマインダーの最小間隔 | 3日 |
| パスワードリセットの時間あたり上限 | 3回 |

### 5.3 バウンス処理

- **ハードバウンス**: 即座に配信停止、管理者に通知
- **ソフトバウンス**: 3回リトライ後、配信停止

---

## 6. テスト計画

### 6.1 単体テスト

| テストケース | 期待結果 |
|---|---|
| 招待メール送信 | 正しいテンプレートで送信される |
| パスワードリセットURL生成 | 24時間有効なURLが生成される |
| 評価完了通知のスコア色 | スコアに応じた色が適用される |
| リマインダー送信制限 | 頻度制限内でのみ送信される |

### 6.2 E2Eテスト

| シナリオ | 検証項目 |
|---|---|
| 新規受講者招待 | メール受信 → ログイン → パスワード変更 |
| パスワードリセット | リセット要求 → メール受信 → パスワード変更 |
| 課題提出 → 評価完了 | 提出 → 自動評価 → メール受信 → 結果確認 |

---

## 7. 変更履歴

| 日付 | バージョン | 変更内容 |
|---|---|---|
| 2026-01-05 | v1.0 | 初版作成 |
