---
description: Google NotebookLMライブラリの管理 (一覧表示、追加、削除)
---

# NotebookLM 管理ワークフロー

NotebookLMのノートブック一覧の取得、新規追加、削除を行うための管理手順です。

## 手順

1.  **認証状態の確認**:
    -   実行: `python3 .agent/skills/business/notebooklm/scripts/run.py auth_manager.py status`
    -   未認証の場合は、セットアップを実行してください（`03_notebooklm_query.md` 参照）。

2.  **ノートブック一覧の取得**:
    -   実行: `python3 .agent/skills/business/notebooklm/scripts/run.py notebook_manager.py list`
    -   ノートブックのIDと名前の一覧をユーザーに提示します。

3.  **ノートブックの追加**:
    -   **スマート追加（推奨）**:
        -   ユーザーがURLのみを提供した場合:
            1.  まず内容を問い合わせる: `python3 .agent/skills/business/notebooklm/scripts/run.py ask_question.py --question "このノートブックの内容は何ですか？要約とトピックを教えてください。" --notebook-url "[URL]"`
            2.  要約結果を用いて `--description` と `--topics` を埋める。
            3.  登録実行: `python3 .agent/skills/business/notebooklm/scripts/run.py notebook_manager.py add --url "[URL]" --name "[NAME]" --description "[DESC]" --topics "[TOPICS]"`
    -   **手動追加**:
        -   詳細情報が提供されている場合:
            `python3 .agent/skills/business/notebooklm/scripts/run.py notebook_manager.py add --url "[URL]" --name "[NAME]" --description "[DESC]" --topics "[TOPICS]"`

4.  **ノートブックの削除**:
    -   実行: `python3 .agent/skills/business/notebooklm/scripts/run.py notebook_manager.py remove --id [ID]`
