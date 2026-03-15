---
title: "Azure Sentinel、Prisma Cloud ログ連携の進化：Function App から CCF へ"
date: 2026-02-20
draft: false
tags: ["Azure Sentinel", "Prisma Cloud", "Cloud Security", "CCF", "Log Integration"]
categories: ["Technical Insights"]
image: "insights/img/prisma-ccf.png"
---

Azure Sentinel に Palo Alto Prisma Cloud（以下 Prisma）ログを統合するプロセスは、技術的に大きく変化してきました。本記事では、Prismaの構造的理解と、最近導入された**Codeless Connector Framework（CCF）**を活用した実務的なログ統合の経験を共有します。

## 1. Prisma Cloud モジュールの理解（CSPM vs CWPP）

ログ連携を始める前に、Prismaの主要モジュール（Blade）と各ログの性質を理解することが重要です。

* **Cloud Security（CSPM）:** インフラ、IAM、ネットワーキング、ストレージなど、クラウド設定およびコントロールプレーンの誤構成を検出します。
* **Runtime Security（CWPP）:** VMやコンテナ、ホストなどのワークロード内部の実行段階を保護し、ポリシー適用に注力します。
* **その他:** Application Security や Data Security などのモジュールも存在します。

## 2. 過去のログ収集方式：カスタム開発の苦労

2025年初頭までは、ログ収集方式はかなり複雑で断片化していました。

* **CSPM:** Azure Function App を自前で開発・運用し、ログを取り込みにくる必要がありました。
* **CWPP:** 公式コネクタが存在せず、Logic Apps で API を呼び出して収集する手間がありました。

特に **Function App 方式**には以下のような現場のペインポイントがありました。

1. **データサイズの制限:** レコード1行あたり32KBを超えるケースで処理が困難になる。
2. **非定型スキーマ:** JSON内にメタデータやポリシー定義が多量に含まれ、フィールドマッピング・正規化に膨大なリソースを要する。

---

![Prisma CCF](insights/img/prisma-ccf.png)
---

## 3. Codeless Connector Framework（CCF）の導入とメリット

最近導入された **CCF（Codeless Connector Framework）** は、これまでの複雑さを劇的に解消しました。私が実務で感じた主な利点は以下のとおりです。

* **No-Code & Simplified Auth:** コードを書かずに、複雑な認証設定なしでコネクタをセットアップできる。
* **Vendor-Defined Normalization:** ベンダーと Microsoft が事前定義した正規化・マッピングが提供されるため、データ整合性の担保に悩む必要がない。
* **Pre-canned Content の活用:** ネイティブコネクタを利用することで、将来提供される分析ルール（Analytics Rules）や統合コンテンツをすぐに利用可能になる。

## 4. 実務適用例：DCR を活用した効率的なフィルタリング

CCF コネクタでは、**DCR（Data Collection Rule）** 内でフィルタリングやマッピングを直接行うことができます。

> **💡 実務Tip:**
> Prisma 内で QA 環境と本番環境が分かれていない場合、**DCR 内で環境識別子を使ってフィルタリング**する方法が有効です。これにより、必要なデータだけを選択的に収集し、コストと運用効率の両方を改善できます。

---

## 5. まとめ

2026年1月時点で、CSPM コネクタはプレビュー提供中であり、CCF 方式が採用されています。

アプリケーションログ収集は常に課題を伴いますが、API ベースの CCF を積極的に活用することで、Sentinel の使い勝手は大きく向上します。これは単なるログ収集にとどまらず、セキュリティ担当者がより高度な検出コンテンツ開発に専念できる環境を実現するものです。

---

### Copyright Notice
本投稿に記載された製品名、ロゴおよびブランドは、それぞれの権利者に帰属します。本内容は筆者の実務経験に基づくガイドであり、公式ドキュメントの代替ではありません。
