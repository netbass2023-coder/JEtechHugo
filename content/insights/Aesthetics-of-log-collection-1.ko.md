---
title: "로그 수집의 미학 (1): 소리 없는 아우성, Syslog를 길들이는 법"
date: 2026-02-27
description: "현대 IT 보안의 근간인 Log Ingestion의 원리와 Syslog 수집의 전략적 설계 방법론"
categories: ["Security", "Infrastructure"]
tags: ["Syslog", "SIEM", "Log-Ingestion", "SecOps", "Engineering"]
toc: true
draft: false
---
![Aesthetics of Log Collection](/insights/img/Aesthetics-of-Log-Collection.png)
보안 부서의 존재 여부나 컴플라이언스 준수라는 외부적 요인을 차치하더라도, 현대 IT 환경에서 로그 수집의 당위성을 논하는 것은 이제 무의미합니다. 로그 수집은 이미 보안 시스템을 구축함에 있어 거부할 수 없는 **디팩토(De facto) 표준**이자, 인프라의 근간으로 자리 잡았기 때문입니다.

하지만 수많은 현장에서 SecOps 분석가들과 협업하며 느낀 점이 하나 있습니다. 의외로 '로그가 어떤 경로로 우리에게 도달하는가'라는 근본적인 메커니즘, 즉 **Log Ingestion(로그 인제스션)**의 심층적인 이면을 명확히 이해하는 엔지니어가 드물다는 사실입니다.

벤더 가이드에 따라 몇 번의 클릭만으로 수집이 자동화되는 시대이지만, 진정한 전문가의 역량은 수집 과정부터 필드 매핑, 정규화(Normalization)에 이르는 전 과정을 마치 정교한 악기를 조율하듯 다루는 데서 나타납니다. 데이터 흐름의 원리를 꿰뚫고 있어야만 장애 발생 시 트러블슈팅의 지점을 본능적으로 포착할 수 있기 때문입니다.

SIEM 엔지니어로서 현장을 누볐던 경험을 바탕으로, 로그 타입별 최적의 수집 방법론을 시리즈로 연재하고자 합니다. 그 첫 번째 여정은 가장 기본적이면서도 그 깊이가 심오한 **Syslog**입니다.

---

## 우리가 주목해야 할 데이터의 본질

기술적인 디테일에 앞서 '무엇을' 수집할 것인지 정의해야 합니다. 보안 목적의 로그 수집은 기본적으로 **Access Log(접근 기록)**와 **Audit Log(감사 기록)**를 그 근간으로 합니다.

| 구분 | 주요 내용 | 보안상 가치 |
| :--- | :--- | :--- |
| **Access Log** | 사용자 로그인, 인증 시도, 리소스 접근 등 | 비인가 접근 탐지 및 계정 탈취 추적 |
| **Audit Log** | 정책 변경, 권한 부여, 주요 설정 수정 등 | 내부자 위협 및 시스템 변조 추적 |

물론 시스템 에러나 프로세스 로그도 유의미하지만, 비전문가와의 협업이나 보고 체계에서는 이 두 가지 핵심 포인트를 설정하는 것이 전략적인 시작점입니다.

---

## Syslog: 용어 뒤에 숨겨진 세 가지 정체성

현장에서 'Syslog'라는 용어는 흔히 세 가지 의미로 혼용됩니다. 이 개념들을 명확히 분리하여 인지하는 것이 엔지니어링의 시작입니다.

* **원천 데이터 (Source Data)**: 시스템 내부의 프로세스나 데몬이 생성하는 로우(Raw) 데이터입니다. 주로 `/var/log/` 경로에 위치하며 애플리케이션 로그와 구별됩니다.
* **로그 전송자 (Forwarder)**: 설정 파일(`.conf`)의 **Severity(심각도)**와 **Destination(목적지)** 정의에 따라 특정 로그를 외부로 송출하는 역할입니다.
* **로그 수집기 (Collector)**: 전송된 데이터를 수신하여 처리하는 서버입니다. 바로 이 지점에서 엔지니어의 설계 역량이 극명하게 갈립니다.

---

## 실무자를 위한 전략적 조언: Severity와 Protocol

### 1. Severity는 반드시 'Informational(Level 6)'까지 확보하십시오
저장 비용과 DB 부하를 이유로 *Critical*이나 *Error* 레벨까지만 수집하자는 의견이 종종 제기됩니다. 하지만 보안 사고 조사 시 결정적 단서가 되는 접근 및 감사 기록은 대부분 **Informational** 레벨에 포진해 있습니다. 로그 볼륨 최적화는 수집 단계를 차단하는 것이 아니라, 불필요한 노이즈(Warning 등)를 제거하는 정교한 튜닝을 통해 달성해야 합니다.

### 2. UDP와 TCP의 선택은 '데이터 온전성'의 문제입니다
흔히 UDP는 '빠르지만 불안정하다'고만 알려져 있습니다. 하지만 로그 수집에서 더 치명적인 문제는 **Truncation(잘림 현상)**입니다.

> **Truncation이란?**
> UDP는 MTU(Maximum Transmission Unit) 제한으로 인해, 차세대 방화벽(NGFW)의 상세 URL이나 위협 탐지 데이터처럼 길이가 긴 로그를 전송할 때 데이터가 유실될 위험이 큽니다.

반면, DNS 로그처럼 짧고 반복적인 데이터는 UDP가 효율적일 수 있습니다. 또한 보안 요구사항이 높은 환경이라면 표준 514 포트 대신 **TLS 기반의 6514 포트**를 활용하는 유연함이 필요합니다.

---

## 엔지니어링, 그 이상의 가치

숙련된 엔지니어는 Syslog를 단순히 '적재'하는 데 그치지 않습니다. 실시간으로 쏟아지는 데이터 스트림 속에서 Hostname이나 키워드 기반의 필터링을 수행하고, 파싱(Parsing) 단계에서 불필요한 필드를 과감히 제거하여 파이프라인의 효율을 극대화합니다.

특히 중소규모 환경(EPS 250 이하)에서는 **포트 기반의 세그멘테이션 전략**이 유효합니다.

1.  **독립성 확보**: 고객사/시스템별로 전용 포트(예: 11514, 12514) 할당
2.  **경로 명확성**: 수집 단계부터 물리적 포트 번호로 소스를 구분하여 로그 혼선 차단
3.  **유연한 제어**: 특정 수집 라인 장애 시 전체 영향 없이 해당 인스턴스만 개별 제어

결과적으로 고사양 서버를 개별 구축하기 어려운 환경에서 단일 리소스를 공유하면서도 논리적인 격리 수준을 극대화하는 영리한 설계 방식이 됩니다.

나아가 표준 Syslog를 **CEF(Common Event Format)**로 즉석 변환하거나, 특정 이벤트 탐지 시 보안 제품의 대시보드로 리다이렉션되는 동적 URL을 삽입하는 등의 고급 기술을 구현하기도 합니다.

## 마무리하며

로그 수집의 세계에는 자신만의 정교한 로직으로 시스템의 가시성을 확보하는 수많은 고수들이 존재합니다. 다음 글에서는 이들이 **에이전트(Agent)**와 **API**라는 도구를 어떻게 전략적으로 활용하는지, 그 심화된 방법론을 다뤄보겠습니다.

### Trademarks & Disclaimer

> **Trademarks:**
> * Microsoft, Azure, Sentinel, Windows, and Azure Function Apps are registered trademarks of Microsoft Corporation.
> * Palo Alto Networks, Prisma Cloud, and CCF (Cloud Connector Framework) are registered trademarks of Palo Alto Networks, Inc.
> * ArcSight and CEF (Common Event Format) are trademarks or registered trademarks of OpenText (formerly Hewlett Packard Enterprise).
> * All other product names, logos, and brands mentioned in this post are the property of their respective owners.
>
> **Disclaimer:** The views and opinions expressed in this post are those of the author and do not necessarily reflect the official policy or position of any featured companies. This content is provided for informational purposes based on hands-on technical experience and does not replace official product documentation.