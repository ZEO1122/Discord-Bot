# Roadmap — GitHub Actions 중심 MVP

## MVP 범위

서버를 별도로 두지 않는 현재 제약에서, 초기 MVP는 아래 순서를 따른다.

1. 개념 브리핑 markdown 게시 자동화
2. 최신 동향 브리핑 GPT 생성/게시 자동화
3. 게시 로그와 검증 규칙 정리
4. 퀴즈 포함 게시 포맷 정리
5. 제출/통계 기능은 후순위 재설계

핵심 원칙:
- concept 브리핑은 저장소의 `.md` 파일을 진실 소스로 본다.
- trend 브리핑은 source 없이 자동 게시하지 않는다.
- 자동 발행은 `GitHub Actions + Discord Webhook`으로 처리한다.
- 상시 `discord.py` Gateway bot은 개발/실험용 보조 경로로 둔다.

## Week 1 — concept 브리핑 자동 게시

### 목표
- `content/concepts/**/*.md` 브리핑을 Discord에 자동 게시한다.
- concept 브리핑 포맷과 검증 규칙을 고정한다.

### 체크리스트
- [ ] concept markdown 디렉터리 구조 정의
- [ ] markdown frontmatter 규격 확정
- [ ] 본문 필수 섹션 규격 확정
- [ ] markdown parser 스크립트 추가
- [ ] 필수 필드 validator 추가
- [ ] Discord payload builder 연결
- [ ] concept posting workflow 추가
- [ ] `workflow_dispatch` 수동 실행 경로 추가
- [ ] 게시 성공/실패 로그 확인 경로 정리

### 산출물
- `content/concepts/` 포맷
- concept parser / validator
- `.github/workflows/post-concept.yml`
- concept 게시 실행 가이드

### 완료 조건
- [ ] concept markdown 1건을 Actions에서 Discord로 게시할 수 있다
- [ ] 필수 필드 누락 시 게시가 차단된다
- [ ] 운영자가 workflow_dispatch로 수동 실행할 수 있다

### 제외 범위
- [ ] 사용자 제출 기록
- [ ] 관리자 slash command 기반 게시 운영
- [ ] 실시간 Discord interaction 채점

## Week 2 — trend 브리핑 GPT 생성/게시

### 목표
- 실행 시점에 최신 source를 수집하고 GPT로 trend 브리핑을 생성해 Discord에 게시한다.

### 체크리스트
- [ ] trend source 수집 전략 정의
- [ ] track별 source fetch 규칙 정의
- [ ] `cv`, `multimodal` query 정교화
- [ ] GPT prompt 템플릿 확정
- [ ] trend generator 스크립트 추가
- [ ] source 수집 실패 처리 규칙 추가
- [ ] source 필수 검증 규칙 추가
- [ ] 최근 게시 source 중복 방지 규칙 추가
- [ ] GPT 출력 validator 추가
- [ ] trend posting workflow 추가
- [ ] `OPENAI_API_KEY` secret 기준 실행 경로 정리
- [ ] 실패 시 Actions logs에서 원인을 확인할 수 있게 정리

### 산출물
- trend source fetch 스크립트
- GPT prompt 템플릿
- `.github/workflows/post-trend.yml`
- trend 생성/게시 실행 가이드

### 완료 조건
- [ ] 실행 시점 최신 source를 수집해 trend 브리핑 1건을 자동 생성/게시할 수 있다
- [ ] source 없는 trend 생성은 차단된다
- [ ] GPT 출력 필수 필드 누락 시 게시가 차단된다

### 제외 범위
- [ ] 자동 웹 검색
- [ ] source 없는 완전 자동 생성
- [ ] 실시간 Discord 답변 수집

## Week 3 — 퀴즈/기록 방식 재설계

### 목표
- 서버 없는 운영 제약 안에서 퀴즈를 어떤 방식으로 게시/수집할지 결정한다.

### 체크리스트
- [ ] 브리핑 게시물에 포함할 퀴즈 포맷 확정
- [ ] 공개 메시지에 노출 가능한 퀴즈 정보 범위 확정
- [ ] 답변 수집 방식 옵션 비교
  - [ ] Discord interaction 기반
  - [ ] 외부 폼 기반
  - [ ] 게시만 하고 제출은 미루기
- [ ] 서버 없는 운영에 맞는 기록 전략 문서화
- [ ] 후속 상시 런타임 필요 여부 판단

### 산출물
- 퀴즈 포함 게시 포맷
- 기록 방식 비교안
- 후속 확장 방향 문서

### 완료 조건
- [ ] 현재 운영 제약 안에서 가능한 퀴즈 UX가 정의된다
- [ ] 제출/통계 기능을 언제 어떤 전제로 다시 열지 정리된다

### 제외 범위
- [ ] slash command 기반 실시간 채점 MVP 강행
- [ ] 상시 서버 전제 통계 기능 확장

## MVP 최종 완료 조건

- [ ] concept markdown을 Discord로 자동 게시할 수 있다
- [ ] trend source 목록을 기반으로 GPT 생성 브리핑을 Discord로 자동 게시할 수 있다
- [ ] 게시 실패 원인을 Actions logs 또는 publish log로 추적할 수 있다
- [ ] 퀴즈 포함 게시 포맷이 정리되어 있다
- [ ] 상시 서버가 없을 때 제출/통계 기능을 어떻게 다룰지 결정되어 있다

## 후순위 확장 항목

- [ ] `discord.py` Gateway bot 상시 운영
- [ ] `/quiz_solve`
- [ ] `/stats me`
- [ ] `/admin stats`
- [ ] 외부 DB 기반 사용자 통계
- [ ] 고급 리더보드
- [ ] 개인화 추천
