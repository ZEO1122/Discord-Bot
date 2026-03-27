# One-Page Operations

이 문서는 이 저장소를 처음 맡는 운영자가 **바로 따라할 수 있도록** 핵심 절차만 1페이지로 요약한 문서다.

## 1. 이 프로젝트가 하는 일

- 평일 오전 9시 KST: concept 브리핑 1개 자동 게시
- 월요일 오전 9시 KST: 채널별 관심분야에 맞는 trend 브리핑 자동 게시
- 실행 방식: **GitHub Actions + Discord Webhook**

## 2. 먼저 확인할 파일

- 서버 연결: `docs/SERVER_SETUP_GUIDE.md`
- 유지보수: `docs/MAINTENANCE_GUIDE.md`
- 장애 대응: `docs/OPERATIONS.md`
- concept 순서: `content/concepts/manifest.json`
- concept 진행 상태: `content/concepts/history/concept_progress.json`
- 채널별 관심분야: `config/channel_interest_map.json`
- trend 중복 방지 이력: `content/trends/history/published_trends.json`

## 3. GitHub Secrets

반드시 있어야 하는 값:

- `DISCORD_WEBHOOK_URL`
- `DISCORD_WEBHOOK_MAP_JSON`
- `OPENAI_API_KEY`

의미:
- `DISCORD_WEBHOOK_URL`: concept 게시용 기본 webhook
- `DISCORD_WEBHOOK_MAP_JSON`: trend 채널별 webhook 맵
- `OPENAI_API_KEY`: trend GPT 생성용 key

## 4. concept 운영 방법

### concept 추가
1. `content/concepts/dl-basics/`에 새 `.md` 파일 추가
2. `content/concepts/manifest.json` 마지막에 경로 추가
3. push

### concept 수동 테스트
GitHub Actions에서:

- `Post Concept Brief`
- `brief_path`: 비워두기
- `dry_run`: `false`

정상 결과:
- Discord에 concept full embed 게시
- `content/concepts/history/concept_progress.json` 갱신

## 5. trend 운영 방법

### 채널 설정 변경
1. `config/channel_interest_map.json` 수정
2. 운영할 채널은 `enabled: true`
3. `interests`와 `max_topics` 조정
4. push

### trend 수동 테스트
GitHub Actions에서:

- `Post Trend Brief`
- `channel_key`: 예) `vision-study`
- `max_results`: `3`
- `dry_run`: `false`

정상 결과:
- 해당 채널에만 weekly trend 브리핑 게시
- `content/trends/history/published_trends.json` 갱신

주의:
- `publish_status=skipped`는 실패가 아니라 **fresh source 없음**일 수 있다

## 6. 자주 보는 에러

### concept가 안 올라옴
- `Post Concept Brief` run 확인
- markdown 포맷 확인
- `concept_progress.json` 갱신 확인
- embed 제한 초과 확인
  - field value 1024 이하
  - field 25개 이하
  - embed 총 6000자 이하

### trend가 안 올라옴
- `OPENAI_API_KEY` 확인
- `DISCORD_WEBHOOK_MAP_JSON` 확인
- `channel_interest_map.json`의 `webhook_key`와 secret key 일치 확인
- fresh source 부족이면 `skipped` 가능

## 7. 운영 시작 전 마지막 확인

- [ ] concept 수동 실행 성공
- [ ] trend 채널별 수동 실행 성공 또는 의도된 `skipped` 확인
- [ ] schedule이 concept=평일 9시, trend=월요일 9시 KST로 맞음
- [ ] 새 concept를 추가하면 `manifest.json`도 같이 수정함
- [ ] 채널/관심분야 변경 시 `channel_interest_map.json`도 같이 수정함

## 8. 운영자용 한 줄 요약

- concept는 `manifest.json`만 보면 된다
- trend는 `channel_interest_map.json`만 보면 된다
- 문제 생기면 먼저 GitHub Actions 로그부터 본다
