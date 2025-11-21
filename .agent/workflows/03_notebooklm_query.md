---
description: NotebookLMへのクエリ実行ワークフロー
---

# NotebookLM クエリワークフロー

このワークフローは、Google NotebookLMに対して質問を投げ、ソースに基づいた回答を取得するための手順です。

## 前提条件
-   Python環境がセットアップされていること。
-   `tools/notebooklm/scripts/run.py` および `ask_question.py` が存在すること。
-   NotebookLMの認証情報が設定されていること。

## 手順

1.  **クエリの作成**
    -   具体的で明確な質問文を作成します。
    -   必要に応じて、対象とするノートブックIDを指定します。

2.  **コマンド実行**
    -   以下のコマンド形式で実行します。
    ```bash
    python3 tools/notebooklm/scripts/run.py ask_question.py --question "{質問内容}" --notebook-id "{NotebookID}"
    ```

3.  **結果の確認**
    -   出力された回答を確認し、必要に応じて追加の質問を行います。
    -   回答はMarkdown形式で出力されるため、そのままドキュメントに転記可能です。

## 使用例
```bash
# プロジェクトの課題抽出（例）
python3 tools/notebooklm/scripts/run.py ask_question.py \
  --question "現在のプロジェクトにおける主要な課題を3つ挙げ、優先順位を付けてください" \
  --notebook-id "{TargetNotebookID}"
```
