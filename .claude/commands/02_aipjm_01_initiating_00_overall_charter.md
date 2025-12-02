---
description: "Cursor Command: 全体プロジェクト憲章（全社横断プロジェクト用）"
---

# Cursor Command: 全体プロジェクト憲章（全社横断プロジェクト用）

## 説明
このコマンドは **PMBOK第7版** に準拠し、**全社横断プロジェクト**（プログラムレベル）の憲章を自動生成します。
複数のサブプロジェクト、ベンダー管理、横断依存関係を含む統合プロジェクト憲章をMarkdown形式で作成します。

---

## プロンプトテンプレート

あなたはPMBOK第7版準拠の全社横断AIプロジェクトマネージャー（AI-PgM）です。
以下の入力情報をもとに、**全社横断プロジェクト憲章**をMarkdown形式で作成してください。

### 入力変数
- `project_name`: 全体プロジェクト名
- `sponsor`: プロジェクトスポンサー（役職含む）
- `project_manager`: プロジェクトマネージャー（役職含む）
- `department`: 主管部門
- `project_period`: プロジェクト期間（開始～終了）
- `budget_cap`: 予算上限
- `background`: 背景・目的（価値仮説）
- `business_value`: 期待価値・KPI
- `subprojects`: サブプロジェクト構成（名称、目的、責任者、期間、主要成果物）
- `quantitative_goals`: 定量目標（全サブPJの統合KPI）
- `qualitative_goals`: 定性目標
- `cross_dependencies`: 横断依存関係（データ連携、API統合、共有リソース）
- `vendors`: ベンダー構成（名称、担当サブPJ、契約種別、主要納品物）
- `assumptions`: 前提条件
- `constraints`: 制約条件（リソース制約、技術制約、組織制約）
- `external_dependencies`: 外部依存
- `high_level_risks`: 高レベルリスク（統合リスク）
- `approval_authority`: 承認権限者

---

## 出力テンプレート

```markdown
# 全社横断プロジェクト憲章
- 版/日付: v1.0 / {YYYY-MM-DD}
- 作成者: AI-PgM

## 基本情報
- プロジェクト名: {{project_name}}
- スポンサー: {{sponsor}} / PM: {{project_manager}} / 部門: {{department}}
- プロジェクト種別: 全社横断プログラム
- 期間: {{project_period}}
- 予算上限: {{budget_cap}}

## 背景・目的（価値仮説）
{{background}}

**期待価値**: {{business_value}}

## サブプロジェクト構成
| サブPJ名 | 目的 | 責任者 | 期間 | 主要成果物 |
|---|---|---|---|---|
{{subprojects}}

## 全体目標（SMART）
- 定量: {{quantitative_goals}}（全サブPJの統合KPI）
- 定性: {{qualitative_goals}}

## 横断依存関係
{{cross_dependencies}}

## ベンダー構成
| ベンダー名 | 担当サブPJ | 契約種別 | 主要納品物 |
|---|---|---|---|
{{vendors}}

## 前提・制約・依存
- 前提: {{assumptions}}
- 制約: {{constraints}}
- 依存: {{external_dependencies}}

## 高レベルリスク（統合リスク）
| リスク | 影響 | 確率 | 優先 | 初期対応 |
|---|---|---|---|---|
{{high_level_risks}}

## 承認
- スポンサー: {{approval_authority}} / 承認日: {YYYY-MM-DD}
```

---

## NotebookLM連携（推奨）

プロジェクト憲章作成前に、NotebookLMから既存情報を取得することを推奨します：

```bash
# ステップ1: EB ALLから全体プロジェクト情報を取得
python scripts/run.py ask_question.py \
  --question "プロジェクト名、目的、サブプロジェクト構成、ベンダー構成、主要マイルストーンを教えてください" \
  --notebook-id "eb-all"

# ステップ2: 取得した情報を基にエージェントを実行
/全体プロジェクト憲章を作成
```

---

## 使用例

**Claude Code/Cursor上での実行例：**

```
/全体プロジェクト憲章を作成

project_name: "Ebara Brain 全社AI変革プログラム"
sponsor: "CTO 山田太郎"
project_manager: "王 健 / PMOサポート: 伊藤 花子"
department: "イノベーション本部"
project_period: "2025-01-15 ～ 2025-12-31"
budget_cap: "5億円"
background: "全社のAI活用を推進し、業務効率化と新規事業創出を実現する"
business_value: "業務効率30%向上、新規事業売上3億円/年"
subprojects: |
  | 流体解析AIエージェント | 流体解析の自動化・高速化 | 影山氏 | 2025-02～2025-06 | AIエージェント |
  | LLM構築（楊氏） | 自社LLMの構築とFT | 楊氏 | 2025-01～2025-04 | LLMモデル |
  | 暗黙知形式知化エージェント | 暗黙知のデータ化 | 柳橋氏 | 2025-03～2025-08 | PAIエージェント |
quantitative_goals: "LLM検証完了（3月）、流体解析効率50%向上（6月）"
qualitative_goals: "AI活用文化の定着、社内データ基盤整備"
cross_dependencies: |
  - データ連携: LLM → 各エージェント（学習データ提供）
  - 共有リソース: H100 GPU 8枚、データサイエンティスト3名
vendors: |
  | Sparticle社 | LLM構築 | 準委任 | LLMモデル、RAG/FT実装 |
  | Uniadex社 | インフラ | 請負 | GPUサーバー、環境構築 |
assumptions: "GPUリソース確保済み、TerraData環境利用可能"
constraints: "予算5億円、GPU 8枚上限、データサイエンティスト3名"
external_dependencies: "Sparticle社契約承認（法務）、GPU調達"
high_level_risks: |
  | サブPJ間統合不整合 | 高 | 中 | 高 | 統合テスト計画早期策定 |
  | GPUリソース競合 | 中 | 高 | 高 | リソース配分計画作成 |
  | ベンダー契約遅延 | 中 | 中 | 中 | 早期契約手続き開始 |
approval_authority: "CTO 山田太郎"
```

---

## 備考
- 本テンプレートは **PMBOK第7版** のプログラム管理・横断管理に準拠
- サブプロジェクト、ベンダー、横断依存を統合的に管理
- **原則**: システム思考、複雑さ
- **ドメイン**: 測定、不確実性
