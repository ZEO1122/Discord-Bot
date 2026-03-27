# Maintenance Guide

이 문서는 운영 중인 Discord 브리핑 자동화 레포를 유지보수하는 방법을 정리한다.

## 1. 유지보수 범위

주요 유지보수 대상은 아래 4가지다.

1. concept 콘텐츠
2. trend 채널/관심분야 설정
3. GitHub Secrets 및 webhook
4. GitHub Actions 실행 결과

## 2. concept 콘텐츠 유지보수

관련 파일:

- `content/concepts/dl-basics/*.md`
- `content/concepts/manifest.json`
- `content/concepts/history/concept_progress.json`

### 새 concept 추가 절차

1. 새 `.md` 파일 작성
2. 기존 concept 포맷과 동일한 frontmatter/섹션 구조 유지
3. `manifest.json` 마지막에 새 파일 경로 추가
4. PR 또는 직접 push

### 수정 시 체크 포인트

- title / one_line이 명확한가
- 섹션 수가 과도하지 않은가
- 각 섹션이 embed field 1024자 이하인가
- 전체 field 수가 25개 이하인가
- source / 주의 섹션이 빠지지 않았는가

### 게시 순서 문제

- concept가 이미 게시된 뒤 파일을 수정하는 건 가능하지만,
- 순서를 바꾸고 싶으면 `manifest.json`을 수정해야 한다.
- 다음으로 어떤 개념이 나갈지는 `concept_progress.json` 기준이다.

## 3. trend 유지보수

관련 파일:

- `config/channel_interest_map.json`
- `content/trends/history/published_trends.json`

### 채널별 관심분야 변경

1. `channel_interest_map.json` 수정
2. `interests` 변경
3. 필요하면 `max_topics` 조정
4. push

### 채널 비활성화

- 특정 채널에서 weekly trend를 중지하려면:
  - `enabled: false`

### 중복 방지 history

- `published_trends.json`은 최근 게시 source를 저장한다.
- fresh source가 없으면 workflow는 `skipped`될 수 있다.
- 이건 정상 동작일 수 있다.

### history를 정리해야 하는 경우

- 테스트 중 잘못된 채널로 많이 보냈을 때
- 운영 채널을 바꿨을 때
- 예전 채널 ID 기록이 과하게 쌓였을 때

주의:
- history를 지우면 같은 source가 다시 게시될 수 있다.

## 4. GitHub Secrets 유지보수

필수 secret:

- `DISCORD_WEBHOOK_URL`
- `DISCORD_WEBHOOK_MAP_JSON`
- `OPENAI_API_KEY`

### 교체가 필요한 경우

- webhook URL이 외부에 노출됨
- OpenAI key가 노출됨
- 서버/채널을 새로 연결함

### 교체 절차

1. Discord 채널에서 새 webhook 생성
2. GitHub `Settings -> Secrets and variables -> Actions` 이동
3. 해당 secret 값 교체
4. `workflow_dispatch`로 수동 검증

## 5. GitHub Actions 유지보수

관련 workflow:

- `.github/workflows/post-concept.yml`
- `.github/workflows/post-trend.yml`

### concept workflow 운영 확인

확인 포인트:
- 평일 오전 9시 KST에 실행되는가
- concept 게시 성공 후 `concept_progress.json`가 커밋되는가

### trend workflow 운영 확인

확인 포인트:
- 월요일 오전 9시 KST에 실행되는가
- 채널별 관심분야를 읽는가
- `published_trends.json`가 갱신되는가

## 6. 운영자가 자주 보는 파일

- `README.md`
  - 전체 구조 요약
- `docs/OPERATIONS.md`
  - 장애 대응, 배포 체크리스트
- `config/channel_interest_map.json`
  - 채널별 관심분야
- `content/concepts/manifest.json`
  - concept 순서
- `content/concepts/history/concept_progress.json`
  - concept 게시 위치
- `content/trends/history/published_trends.json`
  - trend 중복 방지 상태

## 7. 장애 대응 요약

### concept가 안 올라옴

- `Post Concept Brief` workflow run 확인
- markdown 포맷 확인
- `concept_progress.json` 갱신 여부 확인
- embed 제한 초과 여부 확인

### trend가 안 올라옴

- `Post Trend Brief` workflow run 확인
- `OPENAI_API_KEY` 확인
- `DISCORD_WEBHOOK_MAP_JSON` 확인
- fresh source 부족인지 확인

### 특정 채널만 안 올라옴

- `channel_interest_map.json`의 `enabled` 확인
- `webhook_key`와 secret key 일치 여부 확인
- `channel_key` 수동 실행으로 재검증

## 8. 운영 변경 권장 방식

권장:
- 작은 변경은 PR로 검토 후 반영
- 큰 변경은 `workflow_dispatch`로 먼저 테스트
- 채널 매핑/manifest/history는 변경 이유를 commit message에 명확히 남기기

## 9. 최소 운영 체크리스트

- [ ] concept 신규 파일 추가 시 `manifest.json`도 수정했는가
- [ ] 채널/관심분야 변경 시 `channel_interest_map.json`을 수정했는가
- [ ] secret 변경 후 수동 실행으로 검증했는가
- [ ] failed가 아니라 `skipped`인 경우 정상 skip인지 확인했는가
- [ ] schedule이 실제 운영 시간과 맞는가
