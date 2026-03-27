# Architecture — GitHub Actions 중심 발행 구조

## 1. 문서 목적

이 문서는 서버 없는 운영 제약을 전제로, AI 학술동아리 Discord 브리핑 시스템의 현재 아키텍처를 설명한다.

현재 기본 운영 경로는 아래와 같다.

1. 개념 브리핑은 저장소의 markdown 파일에서 읽는다.
2. 최신 동향 브리핑은 실행 시점에 최신 source를 수집하고 GPT API로 생성한다.
3. 자동 발행은 GitHub Actions가 실행한다.
4. Discord 전송은 webhook으로 처리한다.

## 2. 핵심 설계 원칙

- 상시 서버를 기본 전제로 두지 않는다.
- 자동화의 중심은 `GitHub Actions + Discord Webhook`이다.
- `discord.py` Gateway bot 코드는 보조 개발 경로로 유지한다.
- trend 브리핑은 출처 없는 자동 게시를 허용하지 않는다.
- 개념 브리핑은 저장소의 markdown 파일을 진실 소스로 본다.
- 게시 실패는 Discord 응답, Actions logs, publish log로 추적 가능해야 한다.

## 3. 현재 구현 우선 구조

```text
[Markdown Brief Source]        [Live Trend Source Fetch]
           ↓                           ↓
 [Build / Validate Script]   [GPT Generation + Validation]
           ↓                           ↓
             [GitHub Actions Publisher]
                        ↓
                [Discord Webhook]
                        ↓
            [Publish Logs / Action Logs]
```

이 구조가 현재 운영의 기본값이다.

## 4. Week 1 — Concept 브리핑 자동 게시

### 목표
- 미리 작성한 딥러닝 개념 markdown을 Discord에 안정적으로 게시한다.
- 게시 결과를 추적 가능하게 만든다.

### 핵심 컴포넌트

#### Markdown Brief Source
- `content/concepts/**/*.md`
- 브리핑 원문, 요약, 토론 질문, 출처를 저장한다.

#### Build / Validate Script
- markdown frontmatter와 본문 섹션을 파싱한다.
- 필수 필드 누락 여부를 검사한다.
- Discord embed payload를 만든다.

#### GitHub Actions Publisher
- `schedule` 또는 `workflow_dispatch`로 실행된다.
- concept 파일을 선택해 게시 스크립트를 호출한다.

#### Discord Webhook
- 실제 Discord 채널 게시를 담당한다.

#### Publish Logs
- GitHub Actions logs
- webhook 결과 로그
- 선택적 로컬/외부 DB 기록

### 데이터 흐름

```text
1. concept markdown 선택
2. frontmatter / 본문 파싱
3. 필수 필드 검증
4. Discord payload 생성
5. webhook 게시
6. publish 결과 기록
```

## 5. Week 2 — Trend 브리핑 자동 게시

### 목표
- 세부 분야 최신 source를 실행 시점에 수집하고 GPT API로 브리핑을 생성한다.
- 검증을 통과한 결과만 Discord에 게시한다.

### 핵심 컴포넌트

#### Live Trend Source Fetch
- track에 따라 외부 최신 source를 수집한다.
- 현재 기본 source는 arXiv 최근 논문이다.
- title, url, published_at, source_type을 구조화해 GPT 입력으로 넘긴다.

#### GPT Generation
- 수집된 최신 source 목록을 입력으로 받아 브리핑 초안을 만든다.
- source 없는 trend 생성은 허용하지 않는다.

#### Validation
- 필수 필드 존재 여부 검사
- source 존재 여부 검사
- 금지 규칙 검사

#### GitHub Actions Publisher
- validated output만 webhook으로 게시한다.

### 데이터 흐름

```text
1. track 선택
2. 최신 source 수집
3. GPT API 호출
4. 필수 필드 / source 검증
5. Discord payload 생성
6. webhook 게시
7. publish 결과 기록
```

## 6. Week 3 — 퀴즈와 기록 전략 재설계

### 목표
- 브리핑과 함께 퀴즈를 게시하는 형식을 정리한다.
- 상시 서버 없이 유지 가능한 기록 전략을 결정한다.

### 현재 판단
- `discord.py` 기반 slash command 제출/통계는 상시 런타임이 필요하다.
- 서버를 둘 수 없다면, 아래 둘 중 하나를 선택해야 한다.

1. 퀴즈는 게시만 하고 제출/채점은 후순위로 둔다.
2. 외부 폼/시트/별도 수집 도구를 사용한다.

### 후속 확장 후보
- `discord.py` Gateway bot 기반 `/quiz_solve`
- `/stats me`
- `/admin stats`
- 외부 DB 또는 캐시 기반 통계

## 7. 컴포넌트 책임 구분

### GitHub Actions 계층
- 스케줄 실행
- 수동 실행(`workflow_dispatch`)
- secret 주입
- 로그/실패 상태 제공

### Script 계층
- markdown 파싱
- source 수집
- GPT 생성 호출
- payload 생성
- 게시 호출

### Publish Service 계층
- Discord embed payload 생성
- webhook 전송
- publish 결과 모델화

### 저장 계층
- markdown 원본
- 선택적 로컬 SQLite
- GitHub Actions logs

## 8. 개발/보조 구조

현재 저장소에는 `src/bot/*` 기반 Gateway bot 코드도 있다.

이 코드는 아래 용도로 유지한다.
- 로컬 실험
- slash command UX 검증
- 향후 상시 런타임 확보 시 재사용

하지만 현재 운영 기본 구조는 아니다.

## 9. 운영 기본값

### 기본 운영
- GitHub Actions scheduled workflow
- Discord webhook 게시
- Actions logs 기반 추적

### 보조 운영
- 로컬 `python -m bot.app`
- 수동 `/admin publish`
- slash command 실험

## 10. 장애 포인트와 대응

### 10.1 concept 게시 실패
- markdown 필드 누락 확인
- webhook secret 확인
- GitHub Actions logs 확인

### 10.2 trend 게시 실패
- source fetch 성공 여부 확인
- GPT API 응답 구조 확인
- source 없는 출력인지 확인

### 10.3 Discord 게시 성공 여부 불명확
- webhook 응답 확인
- Actions run log 확인
- 필요 시 publish log 아티팩트 저장

## 11. 설계 결론

현재 이 프로젝트의 핵심은 "상시 Discord 봇"이 아니라, **GitHub Actions가 markdown 또는 GPT 생성 결과를 Discord webhook으로 자동 발행하는 시스템**이다.

Gateway bot 기반 interaction 기능은 후속 확장으로 유지하되, 현재 MVP 아키텍처의 중심은 아니다.
