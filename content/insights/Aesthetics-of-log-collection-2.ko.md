---
title: "로그 수집의 미학 (2): 규격화된 소통, CEF와 고도화되는 Ingestion 패러다임"
date: 2026-03-06
description: "CEF 표준 포맷의 전략적 가치와 에이전트 및 API 수집 기술의 현대화 방향"
categories: ["Security", "Infrastructure"]
tags: ["CEF", "SIEM", "Log-Ingestion", "API", "Cloud-Security"]
draft: false
---
![Aesthetics of Log Collection 2](/insights/img/Aesthetics-of-Log-Collection2.png)

## CEF(Common Event Format): 로그 표준화를 위한 전략적 선택

과거 SIEM 마켓의 리더였던 ArcSight가 제안한 **CEF(Common Event Format)**는 서로 다른 벤더 간의 Log Format Inconsistency 문제를 해결하기 위한 강력한 대안이었습니다. 표준 RFC에서 정의한 Syslog 규격만으로는 복잡한 보안 이벤트의 컨텍스트를 완벽히 구조화하기 어렵기 때문입니다.

일반적인 Web Server 로그 등은 사용자가 직접 포맷을 정의할 수 있지만, 보안 엔지니어가 수많은 어플리케이션의 내부 로직을 파악해 매번 Custom Format을 설계하고 배포하는 것은 운영 오버헤드가 매우 큽니다. 하지만 CEF는 데이터의 구조 자체가 다릅니다. 과거에는 엔지니어가 Raw 데이터 내 값의 순서(Ordinal)와 오프셋을 계산해 파싱 로직을 짰다면, CEF는 'One-single Line' 내에 Key-Value Pair를 명시적으로 포함합니다.

SIEM은 이 메타데이터를 기반으로 각 컬럼(Column)에 값을 즉시 매핑합니다. 이제 CEF는 업계의 Standard Format으로 자리 잡아, 주요 보안 벤더들은 이를 기본 옵션이나 Recommended Format으로 제공합니다. 덕분에 보안팀은 네트워크팀이나 인프라팀에 'CEF 가이드'라는 명확한 근거를 바탕으로 로그 변경을 요청할 수 있으며, 이는 유관 부서 간의 기술적 신뢰를 구축하는 실질적인 토대가 됩니다.

**Technical Insight:**
CEF는 통신 프로토콜의 변화가 아니라, Syslog라는 운송 수단에 담기는 Payload의 규격화입니다. Palo Alto Firewall처럼 OS 버전 업데이트에 따라 필드가 추가되는 경우, 이에 맞춰 CEF 포맷을 동적으로 관리해줘야 합니다. 간혹 SIEM 설정에 따라 정의되지 않은 신규 필드를 'Additional Field'로 묶어 처리하는 경우도 있으니 데이터 유실 여부를 상시 모니터링해야 합니다.

---

## Appliance: 하드웨어의 진화와 로그 전송의 메커니즘

TCP/IP 확산 초기, Appliance는 라우터와 스위치 중심이었습니다. 당시 방화벽은 일반 서버 OS 커널 위에 여러개의 network interface를 장착하고 소프트웨어 형태로 구동되다, 2000년대 초반에 이르러서야 전용 Network Processor와 Switch Fabric을 탑재한 임베디드 플랫폼 기반의 보안 어플라이언스로 완성되었습니다.

이러한 장비들은 패킷/프레임 핸들링 성능은 탁월하지만, 폐쇄적인 임베디드 구조상 별도의 에이전트 설치가 원천적으로 불가능합니다. 따라서 현재도 UI나 CLI를 통해 Remote Syslog Collector 정보를 입력하는 고전적인 방식을 유지하고 있습니다.

물론 내부는 Next-gen Firewall이라는 이름 아래 IDS/IPS, AV, URL Filtering 등 수많은 모듈이 스택 형태로 쌓이며 비대해졌습니다. Threat Intel 정보는 수시로 업데이트되며, 의심스러운 파일의 IOC를 추출해 벤더 클라우드로 전송하거나 아예 관리 콘솔(Console)을 SaaS 형태로 운영하기도 합니다. 하지만 외형적인 변화와 관계없이, 로깅의 근간은 여전히 Agentless 기반의 Syslog 전송에 머물러 있습니다.

---

## Agent와 API: 기술적 난이도와 수집의 현대화

모든 로그를 Syslog로 수집할 수 없기에, 엔지니어는 더 높은 기술적 난이도를 요구하는 영역에 도전해야 합니다.

* **Agent-based Collection:** 초기 에이전트의 주 타깃은 Windows Event Log였습니다. 윈도우 로그는 Syslog 포맷과 호환되지 않을뿐더러 XML 기반의 Multi-line 구조를 가졌기에, 초기에는 특정 컬렉터가 윈도우 서버에 직접 Credential을 가지고 접속해 로그 파일을 읽어오는 방식을 취했습니다. 이후 각 벤더는 시스템 리소스 점유율까지 정교하게 제어하며 이벤트 로그를 안전하게 전달하는 전용 에이전트 모델로 발전시켰습니다.
* **API-based Ingestion의 고도화:** 과거 API를 통한 수집은 엔지니어링 역량이 최우선시되는 Advanced 기술 영역이었습니다. 단순히 URL을 호출하는 수준을 넘어, Passkey 관리, 페이징 처리를 위한 Query 설계, 수신 데이터의 후처리(Post-processing)까지 SOC 내부에서 직접 개발해야 했기 때문입니다. 이를 위해 Azure 환경에서는 Function Apps나 Logic Apps 같은 서버리스 아키텍처를 별도로 빌드해야 했습니다.

최근에는 이러한 복잡한 Ingestion 과정을 패키지화하여 배포하는 추세입니다. Prisma Cloud의 CCF(Cloud Connector Framework) 사례처럼, 과거에는 숙련된 개발자만이 가능했던 로그 통합 과정을 벤더 간의 기술 제휴를 통해 추상화하고 단순화하는 방향으로 진화하고 있습니다.


### Trademarks & Disclaimer

> **Trademarks:**
> * Microsoft, Azure, Sentinel, Windows, and Azure Function Apps are registered trademarks of Microsoft Corporation.
> * Palo Alto Networks, Prisma Cloud, and CCF (Cloud Connector Framework) are registered trademarks of Palo Alto Networks, Inc.
> * ArcSight and CEF (Common Event Format) are trademarks or registered trademarks of OpenText (formerly Hewlett Packard Enterprise).
> * All other product names, logos, and brands mentioned in this post are the property of their respective owners.
>
> **Disclaimer:** The views and opinions expressed in this post are those of the author and do not necessarily reflect the official policy or position of any featured companies. This content is provided for informational purposes based on hands-on technical experience and does not replace official product documentation.