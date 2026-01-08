# セキュリティレビュー結果

- プロジェクト名: AIポリテラシー育成プログラム Ver.2
- 作成日: 2026-01-05
- 版: v1.0
- レビュー実施日: 2026-01-05
- 関連文書: auth_design.md, infrastructure_spec.md, api_spec.md

---

## 1. エグゼクティブサマリー

### 1.1 総合評価

| 項目 | 評価 | コメント |
|---|---|---|
| **全体リスクレベル** | 中 | 一般的なWebアプリとして適切な対策済み |
| **重大な脆弱性** | 0件 | 検出なし |
| **高リスク項目** | 2件 | 対策計画あり |
| **中リスク項目** | 5件 | 開発中に対応予定 |
| **低リスク項目** | 3件 | ベストプラクティス推奨 |

### 1.2 主要な推奨事項

1. **APIレート制限の実装**（高）: Gemini API呼び出しの濫用防止
2. **セッション管理の強化**（高）: 同時ログイン制限の検討
3. **入力検証の徹底**（中）: サーバーサイドでの再検証
4. **監査ログの拡充**（中）: セキュリティイベントの詳細ログ

---

## 2. OWASP Top 10 対策状況

### 2.1 A01: 認可の不備

| 対策項目 | 状態 | 実装詳細 |
|---|---|---|
| RBACの実装 | ✅ 対策済み | learner/instructor/admin の3ロール |
| RLSの実装 | ✅ 対策済み | Supabase RLSで行レベル制御 |
| 垂直権限昇格防止 | ✅ 対策済み | ロールはDB管理、JWTに埋め込み |
| 水平権限昇格防止 | ✅ 対策済み | user_id = auth.uid() でフィルタ |

**RLSポリシー例**:
```sql
-- submissions テーブル
CREATE POLICY "Users can view own submissions"
ON submissions FOR SELECT
USING (user_id = auth.uid());

CREATE POLICY "Instructors can view all submissions"
ON submissions FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM users
    WHERE id = auth.uid()
    AND role IN ('instructor', 'admin')
  )
);
```

### 2.2 A02: 暗号化の不備

| 対策項目 | 状態 | 実装詳細 |
|---|---|---|
| HTTPS強制 | ✅ 対策済み | Vercel自動HTTPS |
| パスワードハッシュ | ✅ 対策済み | Supabase Auth (bcrypt) |
| JWT署名 | ✅ 対策済み | HS256 (Supabase管理) |
| 機密情報の保管 | ✅ 対策済み | 環境変数（Vercel暗号化） |

### 2.3 A03: インジェクション

| 対策項目 | 状態 | 実装詳細 |
|---|---|---|
| SQLインジェクション | ✅ 対策済み | Supabase Client (パラメータ化) |
| XSS | ✅ 対策済み | React自動エスケープ |
| コマンドインジェクション | ✅ 対策済み | 該当機能なし |
| NoSQLインジェクション | N/A | PostgreSQL使用 |

**Supabase Clientの使用例**:
```typescript
// 安全: パラメータ化クエリ
const { data } = await supabase
  .from('submissions')
  .select('*')
  .eq('user_id', userId);

// 危険: 使用禁止
// .rpc('custom_function', { raw_sql: userInput })
```

### 2.4 A04: 安全でない設計

| 対策項目 | 状態 | 実装詳細 |
|---|---|---|
| 脅威モデリング | ⚠️ 部分対応 | 主要フローのみ実施 |
| セキュリティ要件定義 | ✅ 対策済み | auth_design.md で定義 |
| 最小権限原則 | ✅ 対策済み | ロール別権限マトリックス |

### 2.5 A05: セキュリティ設定ミス

| 対策項目 | 状態 | 実装詳細 |
|---|---|---|
| デフォルト認証情報 | ✅ 対策済み | 招待リンクで本人がパスワード設定（Supabase Auth） |
| 不要な機能の無効化 | ✅ 対策済み | 必要最小限のAPI公開 |
| エラーメッセージ | ✅ 対策済み | 詳細エラーは本番非表示 |
| セキュリティヘッダー | ✅ 対策済み | Next.js + Vercel設定 |

**セキュリティヘッダー設定**:
```typescript
// next.config.js
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Content-Security-Policy', value: "default-src 'self'; ..." },
];
```

### 2.6 A06: 脆弱なコンポーネント

| 対策項目 | 状態 | 実装詳細 |
|---|---|---|
| 依存関係の監査 | ⚠️ 計画中 | npm audit / Dependabot設定予定 |
| 定期アップデート | ⚠️ 計画中 | 月次アップデート計画 |
| EOLライブラリ | ✅ 対策済み | 最新LTS版使用 |

**推奨設定**:
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

### 2.7 A07: 認証の不備

| 対策項目 | 状態 | 実装詳細 |
|---|---|---|
| パスワードポリシー | ✅ 対策済み | 8文字以上必須 |
| ブルートフォース対策 | ✅ 対策済み | 5回失敗で15分ロック |
| セッション管理 | ⚠️ 要強化 | 同時ログイン制限未実装 |
| MFA | ⚠️ 将来対応 | 現時点では未実装 |

**アカウントロック実装**:
```sql
-- 5回連続失敗で15分ロック
UPDATE users
SET
  failed_login_attempts = failed_login_attempts + 1,
  locked_until = CASE
    WHEN failed_login_attempts >= 4
    THEN NOW() + INTERVAL '15 minutes'
    ELSE locked_until
  END
WHERE email = $1;
```

### 2.8 A08: ソフトウェアとデータの整合性

| 対策項目 | 状態 | 実装詳細 |
|---|---|---|
| CI/CDパイプライン保護 | ✅ 対策済み | GitHub protected branch |
| 依存関係の検証 | ⚠️ 計画中 | npm lockfile使用 |
| デプロイ署名 | ✅ 対策済み | Vercel自動検証 |

### 2.9 A09: ログとモニタリングの不備

| 対策項目 | 状態 | 実装詳細 |
|---|---|---|
| 認証イベントログ | ✅ 対策済み | Supabase Auth Logs |
| アクセスログ | ✅ 対策済み | Vercel Logs |
| エラーログ | ✅ 対策済み | Sentry |
| 監査ログ | ⚠️ 部分対応 | 重要操作のみ記録 |
| アラート | ✅ 対策済み | Sentry + Slack連携 |

### 2.10 A10: SSRF（サーバーサイドリクエストフォージェリ）

| 対策項目 | 状態 | 実装詳細 |
|---|---|---|
| URL検証 | ✅ 対策済み | 外部URLフェッチ機能なし |
| 内部ネットワーク保護 | ✅ 対策済み | Vercel分離環境 |

---

## 3. 認証・認可レビュー

### 3.1 認証フロー分析

| フロー | リスク評価 | 対策状況 |
|---|---|---|
| ログイン | 低 | Supabase Auth使用、ロック機構あり |
| パスワードリセット | 低 | 24時間有効トークン、1回使用 |
| 招待登録 | 低 | 管理者のみ招待可能 |
| セッション管理 | 中 | 同時ログイン制限なし |

### 3.2 JWT検証

| チェック項目 | 状態 |
|---|---|
| 署名検証 | ✅ Supabase自動検証 |
| 有効期限検証 | ✅ 1時間で期限切れ |
| 発行者検証 | ✅ iss クレーム検証 |
| オーディエンス検証 | ✅ aud クレーム検証 |

### 3.3 RLS検証結果

| テーブル | RLSポリシー | テスト結果 |
|---|---|---|
| users | 自分のデータのみ閲覧可 | ✅ Pass |
| submissions | 自分 or 講師/管理者が閲覧可 | ✅ Pass |
| evaluations | 自分 or 講師/管理者が閲覧可 | ✅ Pass |
| viewing_logs | 自分 or 講師/管理者が閲覧可 | ✅ Pass |
| sessions | 全員閲覧可 | ✅ Pass |
| exercises | 全員閲覧可 | ✅ Pass |

---

## 4. データ保護レビュー

### 4.1 個人情報の取り扱い

| データ種別 | 保護措置 | 保持期間 |
|---|---|---|
| メールアドレス | 暗号化通信、RLS保護 | 5年 |
| パスワード | bcryptハッシュ | 無期限 |
| 氏名 | RLS保護 | 5年 |
| 提出物 | RLS保護 | 5年 |
| 視聴ログ | RLS保護 | 5年 |

### 4.2 データ最小化

| 確認項目 | 状態 |
|---|---|
| 必要最小限の収集 | ✅ 学習に必要な情報のみ |
| 利用目的の明確化 | ✅ 利用規約に記載 |
| 第三者提供 | ✅ 本人同意なしに提供しない |

### 4.3 データ削除

| 確認項目 | 状態 |
|---|---|
| 削除要求対応 | ✅ 手順確立済み |
| 法定保持期間 | ✅ 助成金要件で5年 |
| 物理削除 | ✅ 保持期間後に実行 |

---

## 5. API セキュリティ

### 5.1 認証・認可

| エンドポイント | 認証 | 認可 | 状態 |
|---|---|---|---|
| /api/auth/* | Supabase Auth | N/A | ✅ |
| /api/sessions/* | JWT必須 | 全ロール | ✅ |
| /api/exercises/* | JWT必須 | 全ロール | ✅ |
| /api/submissions/* | JWT必須 | 自分 or 講師 | ✅ |
| /api/admin/* | JWT必須 | adminのみ | ✅ |

### 5.2 レート制限

| エンドポイント | 現状 | 推奨 |
|---|---|---|
| 認証エンドポイント | ⚠️ 未設定 | 10回/分/IP |
| 課題提出 | ⚠️ 未設定 | 5回/分/ユーザー |
| 評価API（Gemini呼び出し） | ⚠️ 未設定 | 10回/分/ユーザー |
| 一般API | ⚠️ 未設定 | 100回/分/ユーザー |

**推奨実装**:
```typescript
// middleware.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(100, '1 m'),
});

export async function middleware(request: NextRequest) {
  const ip = request.ip ?? '127.0.0.1';
  const { success } = await ratelimit.limit(ip);

  if (!success) {
    return NextResponse.json(
      { error: 'Too many requests' },
      { status: 429 }
    );
  }
}
```

### 5.3 入力検証

| 検証項目 | 状態 | 実装 |
|---|---|---|
| クライアント側検証 | ✅ 実装済み | Zod + React Hook Form |
| サーバー側検証 | ⚠️ 要確認 | API Route で再検証必要 |
| ファイルアップロード | ⚠️ 要確認 | サイズ・種別制限 |

**推奨実装**:
```typescript
// zodスキーマによるサーバー側検証
const submissionSchema = z.object({
  exercise_id: z.number().int().positive(),
  content: z.string().max(50000), // 50KB制限
  attachments: z.array(z.string().url()).max(5).optional(),
});

export async function POST(request: Request) {
  const body = await request.json();
  const validated = submissionSchema.parse(body); // 失敗時は400
  // ...
}
```

---

## 6. インフラセキュリティ

### 6.1 ネットワーク

| 項目 | 状態 | 詳細 |
|---|---|---|
| HTTPS強制 | ✅ | Vercel自動設定 |
| WAF | ⚠️ 要検討 | Vercel Edge Functions |
| DDoS保護 | ✅ | Vercel Edge Network |

### 6.2 環境分離

| 項目 | 状態 | 詳細 |
|---|---|---|
| 開発/本番分離 | ✅ | 別Supabaseプロジェクト |
| シークレット管理 | ✅ | Vercel環境変数 |
| アクセス制限 | ✅ | 本番はIP制限なし（公開サービス） |

### 6.3 バックアップ

| 項目 | 状態 | 詳細 |
|---|---|---|
| 自動バックアップ | ✅ | Supabase日次バックアップ |
| ポイントインタイムリカバリ | ✅ | Supabase Pro以上 |
| 復元テスト | ⚠️ 要実施 | 年1回実施予定 |

---

## 7. 発見された脆弱性と対策

### 7.1 高リスク項目

| # | 脆弱性 | リスク | 対策 | 期限 |
|---|---|---|---|---|
| H-1 | APIレート制限なし | APIの濫用、コスト増大 | Upstash Rate Limit実装 | Sprint 2 |
| H-2 | 同時ログイン制限なし | セッションハイジャック後の検知困難 | セッション管理強化 | Sprint 3 |

### 7.2 中リスク項目

| # | 脆弱性 | リスク | 対策 | 期限 |
|---|---|---|---|---|
| M-1 | サーバー側入力検証不足 | 不正データ登録 | Zodスキーマ追加 | Sprint 2 |
| M-2 | 依存関係の脆弱性スキャン未設定 | 既知脆弱性の見逃し | Dependabot設定 | Sprint 1 |
| M-3 | 監査ログの不足 | インシデント調査困難 | ログ項目追加 | Sprint 3 |
| M-4 | ファイルアップロード検証不足 | 悪意あるファイル | サイズ・種別検証 | Sprint 2 |
| M-5 | CSP設定の最適化 | XSSリスク軽減余地 | CSP強化 | Sprint 3 |

### 7.3 低リスク項目

| # | 脆弱性 | リスク | 対策 | 期限 |
|---|---|---|---|---|
| L-1 | MFA未対応 | 認証の堅牢性 | 将来的に検討 | 未定 |
| L-2 | パスワード複雑性要件 | 弱いパスワード | ポリシー強化 | Sprint 3 |
| L-3 | セッションタイムアウト延長 | セッション固定 | 適切な設定確認 | Sprint 2 |

---

## 8. ペネトレーションテスト計画

### 8.1 テスト範囲

| カテゴリ | 対象 | 優先度 |
|---|---|---|
| 認証テスト | ログイン、パスワードリセット、セッション | 高 |
| 認可テスト | RBAC、RLS、API権限 | 高 |
| 入力検証 | XSS、SQLi、パラメータ改ざん | 高 |
| ビジネスロジック | 課題提出、評価フロー | 中 |
| 設定 | ヘッダー、CORS、エラー情報 | 中 |

### 8.2 実施計画

| フェーズ | 時期 | 内容 |
|---|---|---|
| 内部テスト | MVP完成後 | 開発チームによる手動テスト |
| 外部テスト | 本番リリース前 | 外部セキュリティ会社による診断 |
| 定期テスト | 年1回 | 外部診断 |

### 8.3 テストチェックリスト

**認証テスト**:
- [ ] ブルートフォース耐性
- [ ] セッション固定攻撃
- [ ] パスワードリセットフロー
- [ ] JWT改ざん

**認可テスト**:
- [ ] 垂直権限昇格（learner → admin）
- [ ] 水平権限昇格（他ユーザーデータアクセス）
- [ ] IDOR（直接オブジェクト参照）

**入力検証**:
- [ ] SQLインジェクション
- [ ] XSS（Stored、Reflected）
- [ ] ファイルアップロード

---

## 9. コンプライアンス

### 9.1 個人情報保護法

| 要件 | 対応状況 |
|---|---|
| 利用目的の明示 | ✅ 利用規約に記載 |
| 安全管理措置 | ✅ 暗号化、アクセス制御 |
| 第三者提供制限 | ✅ 同意なく提供しない |
| 開示・訂正・削除対応 | ✅ 手順確立済み |

### 9.2 助成金関連

| 要件 | 対応状況 |
|---|---|
| データ保持（5年） | ✅ 設計済み |
| 証跡の改ざん防止 | ✅ 監査ログで記録 |
| アクセス制限 | ✅ RBACで制御 |

---

## 10. 推奨アクション（優先順）

### 10.1 即時対応（Sprint 1）

1. **Dependabot設定**: 依存関係の脆弱性自動検出
2. **npm audit実行**: 現在の脆弱性確認

### 10.2 短期対応（Sprint 2-3）

1. **APIレート制限実装**: Upstash Rate Limit
2. **サーバー側入力検証強化**: Zodスキーマ
3. **ファイルアップロード検証**: サイズ・種別

### 10.3 中期対応（Sprint 4-6）

1. **同時ログイン制限**: セッション管理強化
2. **監査ログ拡充**: セキュリティイベント詳細
3. **ペネトレーションテスト実施**

---

## 11. 変更履歴

| 日付 | バージョン | 変更内容 |
|---|---|---|
| 2026-01-05 | v1.0 | 初版作成 |
