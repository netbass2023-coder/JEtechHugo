---
title: "Azure Sentinel, Prisma Cloud 로그 연동의 진화: Function App에서 CCF로"
date: 2026-02-20
draft: false
tags: ["Azure Sentinel", "Prisma Cloud", "Cloud Security", "CCF", "Log Integration"]
categories: ["Technical Insights"]
image: "/insights/img/prisma-ccf.png" 
---

Azure Sentinel에 Palo Alto Prisma Cloud(이하 Prisma) 로그를 통합하는 과정은 기술적으로 많은 변화가 있었습니다. 본 포스팅에서는 Prisma의 구조적 이해와 더불어, 최근 도입된 **Codeless Connector Framework(CCF)**를 통한 실무적인 로그 통합 경험을 공유하고자 합니다.

## 1. Prisma Cloud 모듈의 이해 (CSPM vs CWPP)

로그 연동에 앞서, Prisma의 주요 모듈(Blades)과 각 로그의 성격을 파악하는 것이 중요합니다.

* **Cloud Security (CSPM):** 인프라, IAM, 네트워킹, 스토리지 등 클라우드 설정 및 제어 평면(Control-plane)의 구성 오류를 탐지합니다.
* **Runtime Security (CWPP):** 가상 머신(VM), 컨테이너, 호스트와 같은 워크로드 내부의 실행 단계 보호와 정책 적용에 집중합니다.
* **기타:** Application Security, Data Security 모듈이 존재합니다.

## 2. 과거의 로그 수집 방식: 커스텀 개발의 고충

2025년 초까지만 해도 로그 수집 방식은 다소 복잡하고 파편화되어 있었습니다.

* **CSPM:** Azure Function App을 직접 개발 및 운영하여 로그를 인입해야 했습니다.
* **CWPP:** 표준 커넥터가 부재하여 API를 호출하는 Logic Apps를 통해 수집하는 번거로움이 있었습니다.

특히 **Function App 방식**은 실무적으로 다음과 같은 페인 포인트(Pain Points)가 존재했습니다.
1. **데이터 크기 제한:** Row당 32KB를 초과하는 레코드 처리 문제.
2. **비정형 스키마:** JSON 포맷 내에 Metadata, Policy Definition 등 과도한 정보가 포함되어 필드 매핑 및 정규화 시 많은 리소스가 소모됨.

---

## 3. Codeless Connector Framework(CCF)의 도입과 이점

최근 CSPM 로그 수집을 위해 도입된 **CCF(Codeless Connector Framework)**는 이전의 복잡성을 획기적으로 해결해 주었습니다. 제가 체감한 CCF의 주요 장점은 다음과 같습니다.

* **No-Code & Simplified Auth:** 별도의 코드 작성이나 복잡한 인증 설정 없이 커넥터 셋팅이 가능합니다.
* **Vendor-Defined Normalization:** 벤더와 Microsoft가 미리 정의한 정규화(Normalization) 및 매핑을 사용하므로, 데이터 무결성을 고민할 필요가 없습니다.
* **Pre-canned Contents 활용:** Native 커넥터를 사용함으로써 향후 제공될 분석 규칙(Analytics Rules)과 통합 통합 콘텐츠를 즉시 적용할 수 있습니다.

## 4. 실무 적용 사례: DCR을 통한 효율적 필터링

CCF 기반 커넥터를 사용하면 **DCR(Data Collection Rule)** 내에서 직접 필터링과 매핑을 수행할 수 있습니다.

> **💡 실무 Tip:**
> 만약 Prisma 내에서 QA와 운영(Prod) 테넌트가 분리되지 않은 환경이라면, **DCR 내에서 환경별 Identifier를 식별하여 필터링하는 방식**을 적용해 보시기 바랍니다. 이를 통해 필요한 데이터만 선별적으로 수집하여 비용과 운영 효율을 모두 잡을 수 있습니다.

---

## 5. 마무리하며

2026년 1월 현재, CSPM 커넥터는 Preview 모드로 제공되고 있으며 CCF 방식을 채택하고 있습니다.

애플리케이션 로그 수집은 항상 많은 고민을 동반하지만, API 기반의 CCF를 적극 활용한다면 Sentinel의 사용 편의성이 극대화될 것입니다. 이는 단순한 로그 수집을 넘어, 보안 담당자가 더 고도화된 탐지 콘텐츠 개발에 집중할 수 있는 환경을 만들어 줄 것이라 확신합니다.

---

### Copyright Notice
본 포스팅에 언급된 모든 제품명, 로고 및 브랜드는 해당 소유권자의 저작권 및 상표권에 속합니다. 본 내용은 작성자의 실무 경험을 바탕으로 작성된 가이드이며, 공식 제품 매뉴얼을 대체하지 않습니다.