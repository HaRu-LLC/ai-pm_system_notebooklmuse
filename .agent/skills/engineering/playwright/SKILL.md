---
name: playwright
description: Playwrightによるブラウザ自動化スキル。Webテスト、フォーム入力、スクリーンショット、レスポンシブ検証に対応。
source: https://github.com/lackeyjb/playwright-skill
---

## 目的

Playwrightを使用した包括的なブラウザ自動化を実現。Webサイトテスト、フォーム入力、スクリーンショット、レスポンシブデザイン検証、ログインフロー、リンクチェックに対応。

---

## トリガー語

- 「ブラウザ自動化」
- 「Webテストを実行」
- 「スクリーンショットを撮る」
- 「フォームを自動入力」
- 「Playwrightでテスト」

---

## コア機能

- カスタム自動化コード生成（事前スクリプトに限定されない）
- 可視ブラウザモード（headless: false）でリアルタイム確認
- モジュール解決エラー防止
- 一時ファイルの安全な管理

---

## 重要ワークフロー

### 3ステッププロセス

1. **開発サーバー自動検出**: 検出ヘルパーを最初に使用
2. **/tmpにスクリプト記述**: スキルディレクトリには書き込まない
3. **run.jsラッパーで実行**: スキルディレクトリから実行

---

## 使用パターン

### マルチビューポートレスポンシブテスト

```javascript
const viewports = [
  { width: 375, height: 667, name: 'mobile' },
  { width: 768, height: 1024, name: 'tablet' },
  { width: 1920, height: 1080, name: 'desktop' }
];

for (const vp of viewports) {
  await page.setViewportSize({ width: vp.width, height: vp.height });
  await page.screenshot({ path: `/tmp/screenshot-${vp.name}.png` });
}
```

### ログインフロー検証

### フォーム送信自動化

### リンク切れ検出

---

## デフォルト設定

| 設定 | 値 |
|------|-----|
| headlessモード | off（可視ブラウザ） |
| スローモーション | 100ms |
| タイムアウト | 30秒 |
| スクリーンショット保存先 | /tmp/ |

---

## 設定オプション

環境変数でカスタムHTTPヘッダーを設定：
- `PW_HEADER_NAME`
- `PW_HEADER_VALUE`
- `PW_EXTRA_HEADERS`

---

## セットアップ

```bash
npm run setup  # Playwright + Chromiumインストール（初回のみ）
```

---

## 重要原則

- URLはパラメータ化して環境間で柔軟に
- テストファイルは/tmpに書き込み、プロジェクトを汚さない
- ユーザーが明示的に要求しない限りheadless: false

---

## ライセンス

MIT License
