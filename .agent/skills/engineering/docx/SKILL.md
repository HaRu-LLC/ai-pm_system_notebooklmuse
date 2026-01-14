---
name: docx
description: Word文書(.docx)の読み取り、作成、編集を行うスキル。トラッキング変更、コメント、フォーマット管理に対応。
source: https://github.com/anthropics/skills/tree/main/skills/docx
---

## 目的

Word文書(.docx)の包括的な操作を行う。テキスト抽出から新規作成、既存文書の編集、トラッキング変更の適用まで対応。

---

## トリガー語

- 「Word文書を作成」
- 「docxを編集」
- 「文書の変更履歴を追跡」
- 「Wordファイルからテキスト抽出」

---

## コア機能

### 読み取り・分析

pandocまたはXML直接アクセスでテキスト抽出。コメント、フォーマット、メタデータも取得可能。

```bash
# テキスト抽出
pandoc --track-changes=all file.docx -o output.md

# 文書アンパック（XML直接アクセス）
python ooxml/scripts/unpack.py <file> <dir>
```

### 新規作成

docx-jsライブラリ（JavaScript/TypeScript）でDocument, Paragraph, TextRunコンポーネントを使用。

### 既存編集

Python DocumentライブラリでハイレベルメソッドとDOM直接アクセスの両方をサポート。

### トラッキング変更（Redlining）

1. 文書をmarkdownに変換
2. 変更を論理的なバッチ（3-10個/バッチ）で特定
3. 修正を体系的に適用してプロフェッショナルなフォーマットを維持

---

## キーワークフロー

```bash
# 文書アンパック
python ooxml/scripts/unpack.py <file> <dir>

# 文書パック
python ooxml/scripts/pack.py <dir> <file.docx>
```

---

## 重要ガイドライン

- 作成/編集前に参照ファイル（docx-js.md, ooxml.md）を完全に読み込む
- トラッキング変更はバッチ処理で保守性を確保
- 「最小編集」原則：変更テキストのみ、元の属性を維持

---

## 依存関係

- pandoc
- docx (npm)
- LibreOffice
- Poppler utilities
- defusedxml

---

## ライセンス

Anthropic Skills Repository License（LICENSE.txt参照）
