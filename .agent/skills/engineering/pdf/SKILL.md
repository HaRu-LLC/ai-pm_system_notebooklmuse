---
name: pdf
description: PDFファイルの読み取り、作成、操作を行うスキル。テキスト/テーブル抽出、マージ、注釈、メタデータ処理に対応。
source: https://github.com/anthropics/skills/tree/main/skills/pdf
---

## 目的

PDFファイルの包括的な操作を行う。テキスト・テーブル抽出、文書のマージ/分割、注釈追加、OCR処理まで対応。

---

## トリガー語

- 「PDFを作成」
- 「PDFからテキスト抽出」
- 「PDFをマージ」
- 「PDFに注釈を追加」
- 「スキャン文書をOCR」

---

## 主要ライブラリ

### pypdf

基本操作：マージ、分割、メタデータ抽出、ページ回転

```python
from pypdf import PdfReader, PdfWriter

# マージ例
writer = PdfWriter()
for pdf in pdf_files:
    reader = PdfReader(pdf)
    for page in reader.pages:
        writer.add_page(page)
writer.write("merged.pdf")
```

### pdfplumber

テキスト・テーブル抽出（レイアウト維持）

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        # DataFrameへ変換可能
```

### reportlab

新規PDF作成（Canvas + Platypusフレームワーク）

---

## コマンドラインツール

| ツール | 用途 |
|--------|------|
| pdftotext | テキスト抽出（レイアウト維持オプション） |
| qpdf | マージ、分割、回転、復号化 |
| pdftk | マージ・分割の代替 |

---

## 専門タスク

### スキャン文書のOCR

```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path("scanned.pdf")
for img in images:
    text = pytesseract.image_to_string(img)
```

### 透かし（Watermark）

透かしページを既存文書にマージ

### パスワード保護

pypdfの暗号化メソッドを使用

---

## 参照

- forms.md: PDFフォーム入力手順
- reference.md: 高度な機能

---

## ライセンス

Anthropic Skills Repository License（LICENSE.txt参照）
