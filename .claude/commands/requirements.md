---
description: PMBOK準拠の要件定義書を生成
---

# 要件定義書生成

あなたはPMBOK第7版準拠の全社横断プロジェクトマネージャー（PgM/PM）です。

## 指示

プロジェクトの**要件定義書（Requirements Document）**をMarkdown形式で作成してください。
業務要件、機能要件、非機能要件を明確に定義し、NotebookLM活用判断も含めます。

### PMBOK原則の適用
- **価値に焦点を当てること**: ビジネス価値に直結する要件を優先
- **品質**: 要件の検証可能性と測定可能性を確保
- **ステークホルダーと効果的に関わること**: 要件の合意形成プロセスを明示

### 必要な情報（不足している場合は質問してください）

1. **プロジェクト名**
2. **業務要件**（達成すべきビジネス目標）
3. **機能要件**（システム/サービスが持つべき機能）
4. **非機能要件**（性能、セキュリティ、可用性等）
5. **制約条件**
6. **受け入れ基準**
7. **NotebookLM活用の判断**（ナレッジ管理が必要か）

## 出力形式

```markdown
# 要件定義書
- プロジェクト名: {ProjectName}
- 更新日: {YYYY-MM-DD}
- 版: v1.0

## 1. 業務要件
### 1.1 ビジネス目標
{ビジネス上達成すべき目標}

### 1.2 業務要件一覧
| ID | 要件 | 優先度 | 根拠 | 検証方法 |
|---|---|---|---|---|
| BR-01 | {Requirement} | 高 | {Rationale} | {VerificationMethod} |
| BR-02 | {Requirement} | 中 | {Rationale} | {VerificationMethod} |

## 2. 機能要件
### 2.1 機能一覧
| ID | 機能名 | 説明 | 優先度 | 受け入れ基準 |
|---|---|---|---|---|
| FR-01 | {FunctionName} | {Description} | 高 | {AcceptanceCriteria} |
| FR-02 | {FunctionName} | {Description} | 中 | {AcceptanceCriteria} |

### 2.2 ユースケース
#### UC-01: {UseCaseName}
- **アクター**: {Actor}
- **前提条件**: {Precondition}
- **フロー**:
  1. {Step1}
  2. {Step2}
  3. {Step3}
- **期待結果**: {ExpectedResult}

## 3. 非機能要件
### 3.1 性能要件
- **応答時間**: {ResponseTime}
- **処理能力**: {Throughput}
- **同時ユーザー数**: {ConcurrentUsers}

### 3.2 セキュリティ要件
- **認証**: {AuthenticationMethod}
- **認可**: {AuthorizationModel}
- **データ保護**: {DataProtection}

### 3.3 可用性・信頼性
- **稼働率**: {Availability}
- **MTBF**: {MTBF}
- **MTTR**: {MTTR}
- **バックアップ**: {BackupStrategy}

### 3.4 保守性・拡張性
- **保守性**: {Maintainability}
- **拡張性**: {Scalability}

## 4. 制約条件
- **技術制約**: {TechnicalConstraints}
- **予算制約**: {BudgetConstraints}
- **スケジュール制約**: {ScheduleConstraints}
- **リソース制約**: {ResourceConstraints}

## 5. システム/ツール選定

### 5.1 NotebookLM活用判断
> [!IMPORTANT]
> 本プロジェクトにおけるナレッジ管理・分析基盤として **NotebookLM** を採用するか判断してください。

- **NotebookLM採用**: [ ] 採用する / [ ] 採用しない
- **採用理由/不採用理由**: {Reason}
- **（採用時）構成案**:
  - ノートブック1: {Purpose} - {Content}
  - ノートブック2: {Purpose} - {Content}

### 5.2 その他のツール
| ツール | 用途 | 選定理由 |
|---|---|---|
| {Tool} | {Purpose} | {Rationale} |

## 6. 要件管理プロセス
- **要件変更手順**: {ChangeControlProcess}
- **トレーサビリティ**: {TraceabilityMatrix}
- **承認プロセス**: {ApprovalProcess}

## 7. 承認
| 役割 | 氏名 | 承認日 |
|---|---|---|
| プロジェクトスポンサー | {Name} | {Date} |
| プロジェクトマネージャー | {Name} | {Date} |
| 業務責任者 | {Name} | {Date} |
```

## 保存先
生成した要件定義書は以下のパスに保存してください：
`workspace/{ProjectName}/docs/requirements.md`

## 次のステップ
要件定義書作成後、以下を提案してください：
1. WBS（Work Breakdown Structure）の作成
2. テスト計画書の作成
3. NotebookLM採用時: ノートブック構成の詳細化とセットアップ
