# Operations — 배포와 운영 가이드

## 1. 운영 원칙

- 상시 서버를 기본 전제로 두지 않는다.
- 자동 발행은 **GitHub Actions + Discord Webhook**을 기본값으로 삼는다.
- concept 브리핑은 저장소 markdown 원본을 진실 소스로 본다.
- trend 브리핑은 source 없이 자동 게시하지 않는다.
- 실패 추적은 GitHub Actions logs와 Discord 게시 결과를 우선 사용한다.
- 시크릿은 GitHub Secrets 또는 환경변수로만 관리한다.

## 2. 환경변수 권장 목록

로컬 개발이나 수동 smoke test를 할 때만 루트의 `.env.example`를 복사해서 `.env`를 만든다.

```bash
cp .env.example .env
```

```bash
DISCORD_BOT_TOKEN=
DISCORD_GUILD_ID=
DISCORD_BRIEF_CHANNEL_ID=
DISCORD_WEBHOOK_URL=
DATABASE_URL=sqlite:///./data/app.db
APP_ENV=development
LOG_LEVEL=INFO

# Optional
DISCORD_ADMIN_CHANNEL_ID=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

설명:
- `DISCORD_BOT_TOKEN`: 로컬 Gateway bot 실험용
- `DISCORD_GUILD_ID`: 로컬 slash command sync 실험용
- `DISCORD_BRIEF_CHANNEL_ID`: 로컬 게시/로그 확인용
- `DISCORD_WEBHOOK_URL`: GitHub Actions와 로컬 게시 스크립트의 핵심 게시 경로
- `DATABASE_URL`: 로컬 개발용 SQLite
- `APP_ENV`, `LOG_LEVEL`: 실행 환경 및 로그 레벨

실제 운영에서는 사용하는 provider 키만 둔다.

## 3. GitHub Actions 운영 형태

### 초기 권장안
- GitHub Actions `schedule`
- GitHub Actions `workflow_dispatch`
- Discord Webhook
- 필요 시 local dry-run 스크립트

### 기본 workflow
- `post-concept.yml`
- `post-trend.yml`

## 4. GitHub Secrets / Variables

### 필수 Secrets
- `DISCORD_WEBHOOK_URL`
- `DISCORD_WEBHOOK_MAP_JSON`
- `OPENAI_API_KEY`

### 선택 Variables
- `DEFAULT_TRACK`
- `TREND_MAX_RESULTS`
- `LOG_LEVEL`

### 권장 설정
- concept workflow는 `workflow_dispatch`와 `schedule` 둘 다 둔다.
- trend workflow는 채널별 관심분야 설정을 읽어 실행 시점 최신 source를 수집한다.
- 실패 시 Actions logs에서 prompt/source/validation 단계가 구분되어야 한다.

## 5. 로그 전략

### 애플리케이션 로그
남겨야 할 핵심 이벤트:
- concept markdown 검증 성공/실패
- trend 생성 성공/실패
- Discord webhook 게시 성공/실패
- source 검증 실패
- GPT 응답 파싱 실패

### 저장 위치
- GitHub Actions run log
- 필요 시 workflow summary
- 필요 시 artifact 업로드

### 최소 로그 필드
- timestamp
- level
- action
- content_id
- quiz_id
- user_id (가능하면 내부 id)
- discord_message_id
- error_code / exception

## 6. 재시도 정책

### webhook 게시 실패
- workflow 재실행 가능하게 유지
- 영구 실패면 Actions logs에 원인을 남김
- 필요 시 같은 입력으로 `workflow_dispatch` 수동 재실행

### GPT 생성 실패
- track과 prompt를 로그에서 식별 가능하게 남김
- validation 실패와 API 실패를 구분한다

### 중복 게시 방지
- `content/trends/history/published_trends.json`에 최근 게시 source를 기록한다.
- 같은 source URL은 다시 게시하지 않는다.
- arXiv URL은 버전 suffix를 제거한 canonical URL 기준으로 비교한다.

## 7. 백업

### 최소 백업 대상
- concept markdown 원본
- `content/concepts/manifest.json`
- `content/concepts/history/concept_progress.json`
- `config/channel_interest_map.json`
- `.env.example` (실제 `.env` 제외)
- prompt 템플릿
- 운영 문서
- workflow yaml
- `content/trends/history/published_trends.json`

### 주기
- DB 일일 백업
- 운영 변경 전 수동 스냅샷 권장

## 8. 장애 대응 플레이북

### 8.1 concept 브리핑이 안 올라옴
1. GitHub Actions run 확인
2. markdown parser/validator 단계 실패 여부 확인
3. `DISCORD_WEBHOOK_URL` secret 확인
4. `concept_progress.json` 갱신 여부 확인
5. workflow_dispatch로 같은 파일 재실행
6. concept 각 섹션이 Discord embed field 제한(1024자)을 넘지 않는지 확인
7. concept field 수가 25개를 넘지 않는지 확인
8. concept embed 전체 길이가 6000자를 넘지 않는지 확인

### 8.2 trend 브리핑이 안 올라옴
1. source fetch step 실패 여부 확인
2. GPT API step 실패 여부 확인
3. validation step 실패 여부 확인
4. 수집 source가 비어 있는지 확인
5. arXiv rate limit(429) 발생 시 잠시 후 재실행 또는 `max_results` 축소

### 8.3 게시는 됐는데 내용이 이상함
1. concept markdown 원본 확인
2. trend prompt 템플릿 확인
3. trend source 수집 결과 확인
4. Actions logs에서 생성 결과 확인
5. Discord 메시지에 GPT 요약 주의 문구가 포함되어 있는지 확인

## 9. 보안 운영

- 토큰을 Git에 커밋하지 않는다.
- GitHub Secrets에만 운영 키를 둔다.
- 웹훅 URL은 회전 가능하도록 관리한다.
- 로그에 정답키와 민감 토큰을 남기지 않는다.

## 10. 배포 체크리스트

- [ ] GitHub Secrets 설정 완료
- [ ] concept markdown 포맷 검증 완료
- [ ] trend source fetch 규칙 검증 완료
- [ ] workflow_dispatch 실행 성공
- [ ] schedule 설정 확인
- [ ] 첫 자동 게시 성공
- [ ] Actions logs 확인
- [ ] webhook 재생성 절차 확인
- [ ] concept embed field 제한(1024/25/6000) 준수 확인

## 11. End-to-End Smoke Path

현재 기본 운영 경로 기준으로, 운영자가 실제 Discord 서버에서 검증할 수 있는 최소 경로는 아래 순서다.

### 11.1 사전 조건

- GitHub 저장소 admin 권한
- Discord webhook 생성 완료
- concept markdown 준비 완료
- trend track 정의 완료
- GitHub Secrets 등록 완료

### 11.2 필요한 환경변수

GitHub Actions 운영 기준 필수 secret/variable을 먼저 채운다.

```bash
DISCORD_WEBHOOK_URL
OPENAI_API_KEY
```

로컬 smoke test를 할 때만 `.env.example`를 복사해서 `.env`를 사용한다.

```bash
cp .env.example .env
DISCORD_BOT_TOKEN=
DISCORD_GUILD_ID=
DISCORD_BRIEF_CHANNEL_ID=
DISCORD_WEBHOOK_URL=
DATABASE_URL=sqlite:///./data/app.db
APP_ENV=development
LOG_LEVEL=INFO
```

주의:
- GitHub Actions 자동 발행의 핵심은 `DISCORD_WEBHOOK_URL`이다.
- trend workflow에는 `OPENAI_API_KEY`가 필요하다.

설정 누락 시 확인 포인트:
- `DISCORD_WEBHOOK_URL` 누락 -> 게시 step 즉시 실패
- `OPENAI_API_KEY` 누락 -> trend workflow 생성 step 실패
- source fetch 실패 -> trend workflow 수집 step 실패

### 11.3 테스트용 데이터 준비

현재 저장소에는 로컬 smoke test용 seed 스크립트가 있다.

```bash
python3 scripts/bootstrap_sqlite.py
python3 scripts/seed_smoke_data.py
```

예상 로컬 출력:

```text
Smoke data ready
briefing_id=1
briefing_key=dl-basics-sample-001
quiz_id=1
track=dl-basics
```

이 단계로 아래 데이터가 준비된다.
- 브리핑 1건
- 퀴즈 1건
- 선택지 4개

### 11.4 GitHub Actions 수동 실행

권장 1차 검증은 `workflow_dispatch`다.

#### concept 게시

```text
Actions -> post-concept -> Run workflow
```

#### trend 게시

```text
Actions -> post-trend -> Run workflow
```

### 11.5 로컬 보조 검증

```bash
source .venv/bin/activate
python3 scripts/publish_daily.py --dry-run
```

Gateway bot 실험은 필요할 때만 선택적으로 사용한다.

### 11.6 실제 Smoke Path

아래 순서로 검증한다.

#### Step 1) 브리핑 준비 확인

concept 또는 trend 입력이 준비되었는지 확인한다.

```bash
ls content/concepts
```

확인 포인트:
- concept markdown 파일
- trend track 입력값

#### Step 2) concept workflow 실행

GitHub Actions에서 실행:

```text
post-concept -> Run workflow
```

기대 결과:
- Discord 채널에 concept 브리핑 게시
- Actions run success

#### Step 3) trend workflow 실행

GitHub Actions에서 실행:

```text
post-trend -> Run workflow
```

기대 결과:
- Discord 채널에 trend 브리핑 게시
- source 없는 경우 게시 차단

#### Step 4) Actions logs 확인

확인 포인트:
- parser 성공 여부
- validation 성공 여부
- GPT generation 성공 여부
- webhook 게시 성공 여부

#### Step 5) Discord 결과 확인

```text
concept/trend 브리핑이 실제 목표 채널에 올라왔는지 확인
```

### 11.7 실패 시 확인할 로그 포인트

#### concept workflow 실패
- GitHub Actions run log
- 검색 키워드:
  - `validation`
  - `post_concept_brief`
  - `Discord webhook`
- 추가 확인:
  - `DISCORD_WEBHOOK_URL` 설정 여부
  - markdown 필수 필드 누락 여부

#### trend workflow 실패
- GitHub Actions run log
- 추가 확인:
  - `DISCORD_WEBHOOK_MAP_JSON` 설정 여부
  - `OPENAI_API_KEY` 설정 여부
  - source fetch 단계 실패 여부
  - source 없는 trend 생성 여부
  - history 파일이 예상대로 갱신되었는지 확인

#### trend workflow가 성공인데 게시가 생략됨
- 로그에 `publish_status=skipped reason=No fresh trend sources available ...` 가 보이면 정상 동작이다.
- 같은 source가 이미 최근 게시 history에 있어서 중복 방지로 건너뛴 것이다.
- 다른 track으로 실행하거나, 나중에 다시 실행해 fresh source를 기다린다.

#### 채널별 게시가 안 됨
- `config/channel_interest_map.json`의 `enabled`, `channel_id`, `webhook_key`를 확인한다.
- `DISCORD_WEBHOOK_MAP_JSON`에 같은 `webhook_key`가 있는지 확인한다.

#### Discord에 아무것도 안 올라옴
- webhook URL이 올바른 채널인지 확인
- Actions run success 여부 확인
- repo secret이 최신 값인지 확인

### 11.8 권장 로컬 확인 경로

로컬 개발에서는 아래를 사용한다.

```bash
python3 scripts/bootstrap_sqlite.py
python3 scripts/seed_smoke_data.py
python3 scripts/publish_daily.py --dry-run
```

### 11.9 운영 시작 전 최종 체크리스트

아래 항목이 모두 맞으면 자동 스케줄 운영으로 전환해도 된다.

- [ ] `DISCORD_WEBHOOK_URL`, `DISCORD_WEBHOOK_MAP_JSON`, `OPENAI_API_KEY`가 GitHub Secrets에 최신 값으로 저장되어 있다
- [ ] `config/channel_interest_map.json`에서 실제로 운영할 채널만 `enabled: true`로 설정되어 있다
- [ ] `DISCORD_WEBHOOK_MAP_JSON`의 key와 `config/channel_interest_map.json`의 `webhook_key`가 정확히 일치한다
- [ ] `content/concepts/manifest.json`에 게시할 concept markdown 순서가 올바르게 들어 있다
- [ ] `Post Concept Brief`를 수동 실행했을 때 Discord full embed 게시와 `content/concepts/history/concept_progress.json` 갱신이 모두 성공한다
- [ ] `Post Trend Brief`를 채널별로 수동 실행했을 때 Discord 게시 또는 `skipped` 결과가 의도대로 나온다
- [ ] `content/trends/history/published_trends.json`가 게시 후 정상적으로 갱신된다
- [ ] concept 스케줄은 평일 오전 9시 KST, trend 스케줄은 월요일 오전 9시 KST로 설정되어 있다
- [ ] trend 브리핑에 GPT 요약 주의 문구가 표시된다
- [ ] webhook/모델 key는 필요 시 재발급 가능한 상태로 관리되고 있다

## 12. 롤백 전략

- 새 workflow는 먼저 `workflow_dispatch`로 검증한다.
- 게시 실패 시 이전 안정 버전 workflow로 되돌린다.
- concept markdown 원본은 Git history로 복구 가능해야 한다.
- prompt와 source file 변경 전에는 diff를 검토한다.
