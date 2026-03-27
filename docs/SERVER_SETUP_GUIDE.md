# Server Setup Guide

이 문서는 이 저장소를 처음 보는 사람이 새 Discord 서버에 브리핑 자동화를 연결할 때 필요한 절차를 정리한다.

목표:
- concept 브리핑은 평일 오전 9시 KST에 자동 게시
- trend 브리핑은 월요일 오전 9시 KST에 채널별 관심분야 기준으로 자동 게시
- 자동화는 GitHub Actions + Discord Webhook으로만 운영

## 1. 준비물

- GitHub 저장소 관리자 권한
- Discord 서버 관리자 권한
- 게시할 Discord 채널 목록
- 채널별 webhook 생성 권한
- OpenAI API key

## 2. Discord 서버에서 해야 할 일

### 2.1 concept 브리핑 채널 정하기

- concept 브리핑을 올릴 채널 1개를 정한다.
- 이 채널은 평일 오전 9시에 하루 1개 concept를 받는다.

### 2.2 trend 브리핑 채널 정하기

- 관심분야별 채널을 정한다.
- 예:
  - `llm-brief`
  - `detection-segmentation-brief`
  - `vision-language-brief`

### 2.3 각 채널 webhook 만들기

Discord 채널 설정에서 다음 순서로 만든다.

1. 채널 우클릭 또는 채널 설정 진입
2. `연동` 또는 `Integrations`
3. `Webhook`
4. `새 웹훅 생성`
5. 이름 지정
6. `Webhook URL 복사`

필요한 webhook은 최소 아래 2종류다.

- concept 브리핑용 기본 webhook 1개
- trend 채널별 webhook 여러 개

## 3. GitHub Secrets 설정

저장소에서 다음 경로로 간다.

`Settings -> Secrets and variables -> Actions`

### 3.1 필수 Secret

#### `DISCORD_WEBHOOK_URL`

- concept 브리핑을 보낼 기본 채널 webhook URL

#### `DISCORD_WEBHOOK_MAP_JSON`

- trend 채널별 webhook 매핑
- 값은 JSON 또는 YAML 스타일 문자열이면 된다.

예시 JSON:

```json
{
  "llm-brief": "https://discord.com/api/webhooks/<CHANNEL_ID>/<WEBHOOK_TOKEN>",
  "detection-segmentation-brief": "https://discord.com/api/webhooks/<CHANNEL_ID>/<WEBHOOK_TOKEN>",
  "vision-language-brief": "https://discord.com/api/webhooks/<CHANNEL_ID>/<WEBHOOK_TOKEN>"
}
```

예시 YAML:

```yaml
llm-brief: https://discord.com/api/webhooks/<CHANNEL_ID>/<WEBHOOK_TOKEN>
detection-segmentation-brief: https://discord.com/api/webhooks/<CHANNEL_ID>/<WEBHOOK_TOKEN>
vision-language-brief: https://discord.com/api/webhooks/<CHANNEL_ID>/<WEBHOOK_TOKEN>
```

#### `OPENAI_API_KEY`

- trend 브리핑 생성용 API key

## 4. 채널 매핑 파일 수정

파일:

`config/channel_interest_map.json`

이 파일에서 실제 운영할 채널만 `enabled: true`로 두고, 각 채널의 관심분야를 입력한다.
초기 운영 기준 taxonomy는 아래 3개를 권장한다.

- `llm`
- `detection-segmentation`
- `vision-language`

예시:

```json
{
  "version": 1,
  "timezone": "Asia/Seoul",
  "channels": [
    {
      "channel_key": "llm-brief",
      "channel_id": "123456789012345678",
      "webhook_key": "llm-brief",
      "enabled": true,
      "interests": ["llm"],
      "max_topics": 1
    },
    {
      "channel_key": "detection-segmentation-brief",
      "channel_id": "234567890123456789",
      "webhook_key": "detection-segmentation-brief",
      "enabled": true,
      "interests": ["detection-segmentation"],
      "max_topics": 1
    },
    {
      "channel_key": "vision-language-brief",
      "channel_id": "345678901234567890",
      "webhook_key": "vision-language-brief",
      "enabled": true,
      "interests": ["vision-language"],
      "max_topics": 1
    }
  ]
}
```

주의:
- `webhook_key` 값은 `DISCORD_WEBHOOK_MAP_JSON`의 key와 정확히 같아야 한다.
- `channel_id`는 운영 추적용이므로 실제 Discord 채널 ID로 맞춘다.

## 5. concept 게시 순서 확인

파일:

- `content/concepts/manifest.json`
- `content/concepts/history/concept_progress.json`

### 역할

- `manifest.json`: concept 게시 순서
- `concept_progress.json`: 어디까지 게시했는지 기록

새 concept를 추가할 때는 보통 아래 순서로 한다.

1. `content/concepts/dl-basics/`에 새 `.md` 파일 추가
2. `content/concepts/manifest.json` 마지막에 경로 추가
3. push

## 6. 첫 수동 검증

자동 스케줄 전에 반드시 수동 실행으로 확인한다.

### 6.1 concept 검증

`Actions -> Post Concept Brief -> Run workflow`

입력값:

- `brief_path`: 비워두기
- `dry_run`: `false`

정상이라면:
- concept 브리핑이 Discord에 올라감
- `content/concepts/history/concept_progress.json`가 갱신됨

### 6.2 trend 검증

`Actions -> Post Trend Brief -> Run workflow`

입력값 예시:

- `channel_key`: `llm-brief`
- `max_results`: `3`
- `dry_run`: `false`

정상이라면:
- 해당 채널에만 weekly trend 브리핑이 올라감
- `content/trends/history/published_trends.json`가 갱신됨

## 7. 자동 스케줄 확인

현재 기본 스케줄은 아래와 같다.

- concept: 평일 오전 9시 KST
- trend: 월요일 오전 9시 KST

GitHub Actions cron은 UTC 기준이므로 workflow에는 아래 값이 들어 있다.

- concept: `0 0 * * 1-5`
- trend: `0 0 * * 1`

## 8. 운영 시작 전 최종 확인

- [ ] `DISCORD_WEBHOOK_URL` 설정 완료
- [ ] `DISCORD_WEBHOOK_MAP_JSON` 설정 완료
- [ ] `OPENAI_API_KEY` 설정 완료
- [ ] `channel_interest_map.json` 실제 값 반영 완료
- [ ] concept 수동 실행 성공
- [ ] trend 채널별 수동 실행 성공 또는 의도된 `skipped` 확인
- [ ] `concept_progress.json` 갱신 확인
- [ ] `published_trends.json` 갱신 확인

## 9. 흔한 실수

- `webhook_key`와 secret key 이름이 다름
- concept 채널 webhook을 `DISCORD_WEBHOOK_URL`에 안 넣음
- `enabled: false` 상태 채널을 왜 안 보내냐고 확인함
- trend fresh source가 없는데 실패로 오해함 (`skipped`는 정상일 수 있음)
- concept markdown가 embed field 제한을 넘김
