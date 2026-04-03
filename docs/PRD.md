# PRD — AI 학술동아리 Discord 브리핑 발행기

## 1. 배경

학술동아리 운영에서 가장 먼저 필요한 것은 꾸준히 읽을 수 있는 짧고 신뢰 가능한 브리핑이다.

이 저장소는 학습봇이나 상호작용 서비스가 아니라, concept와 trend 브리핑을 정해진 시간에 Discord로 자동 발행하는 운영 도구에 집중한다.

## 2. 목표

### 제품 목표
- 동아리 구성원이 정기적으로 AI 브리핑을 읽을 수 있게 한다.
- concept 브리핑은 사람이 작성한 원본을 기준으로 게시한다.
- trend 브리핑은 최신 논문 기반으로 생성하되 출처와 주의 문구를 포함한다.

### 운영 목표
- 서버 없이도 브리핑 운영이 가능해야 한다.
- 운영자가 content/config를 수정하고 바로 반영할 수 있어야 한다.
- 게시 이력과 상태를 추적 가능하게 유지한다.

## 3. 핵심 사용자

### 3.1 일반 동아리원
- 브리핑을 읽고 빠르게 핵심을 파악하고 싶다.
- 출처를 같이 확인하고 싶다.

### 3.2 운영진
- concept와 trend 브리핑을 정기적으로 게시하고 싶다.
- 게시 실패 원인을 추적하고 설정을 쉽게 수정하고 싶다.

## 4. 핵심 시나리오

### 시나리오 A — concept 게시
1. 운영자가 `content/concepts/**/*.md`를 수정한다.
2. `manifest.json`에 순서를 반영한다.
3. GAS가 다음 concept를 읽어 Discord에 게시한다.

### 시나리오 B — trend 게시
1. 운영자가 `config/trend_brief_config.json`을 관리한다.
2. GAS가 최근 논문을 수집하고 상위 후보를 선택한다.
3. OpenAI로 브리핑을 생성한 뒤 Discord에 게시한다.
4. Google Sheets에 게시 이력을 남긴다.

## 5. 범위

## In scope
- concept 브리핑 자동 게시
- trend 브리핑 자동 게시
- 출처 표시
- Script Properties와 Google Sheets 기반 운영 상태 관리
- GAS 운영 문서화

## Out of scope
- Discord 실시간 상호작용 기능
- 퀴즈 제출/채점
- 리더보드
- 사용자 통계
- 실시간 상호작용 기능

## 6. MVP 정의

MVP는 아래를 만족하면 된다.

- concept 브리핑을 평일 자동 게시할 수 있다.
- trend 브리핑을 주간 자동 게시할 수 있다.
- 게시에 필요한 Script Properties와 history 저장소가 정리돼 있다.
- 운영자가 수동 실행과 재검증을 할 수 있다.

## 7. 기능 요구사항

### 7.1 concept 브리핑
- markdown 원본 관리
- manifest 기반 순차 게시
- Discord embed 길이 제한 검증

### 7.2 trend 브리핑
- 최근 논문 수집
- 후보 점수화와 선택
- OpenAI 기반 생성
- Discord embed 게시
- history 기록

## 8. 성공 지표

- concept 게시 성공률
- trend 게시 성공률
- 운영자가 실패 원인을 Apps Script 로그에서 추적할 수 있는지 여부

## 9. 비기능 요구사항

- 브리핑 본문은 초보자도 읽을 수 있어야 한다.
- trend는 source 없이 자동 게시하지 않는다.
- 시크릿은 Script Properties로만 관리한다.
- 장애 시 어떤 단계에서 실패했는지 확인 가능해야 한다.
