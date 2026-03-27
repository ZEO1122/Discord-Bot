# Club Server Transition Checklist

이 문서는 개인 테스트 서버에서 동아리 운영 서버로 전환할 때 무엇을 **유지**하고 무엇을 **초기화(reset)** 해야 하는지 정리한다.

## 1. 전환 원칙

- 코드와 workflow는 그대로 유지한다.
- Discord webhook, 채널 ID, 운영 history는 동아리 서버 기준으로 교체하거나 초기화한다.
- GitHub Actions는 새 서버 기준 secret과 설정이 준비된 뒤에만 schedule을 켠다.

## 2. 그대로 유지해도 되는 파일

아래 파일은 서버가 바뀌어도 그대로 유지해도 된다.

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/OPERATIONS.md`
- `docs/SERVER_SETUP_GUIDE.md`
- `docs/MAINTENANCE_GUIDE.md`
- `docs/ONE_PAGE_OPERATIONS.md`
- `.github/workflows/post-concept.yml`
- `.github/workflows/post-trend.yml`
- `scripts/*.py`
- `content/concepts/**/*.md`
- `content/concepts/manifest.json`

## 3. 동아리 서버 기준으로 교체해야 하는 항목

### 3.1 GitHub Secrets

반드시 교체 또는 재확인:

- `DISCORD_WEBHOOK_URL`
- `DISCORD_WEBHOOK_MAP_JSON`
- `OPENAI_API_KEY`

설명:
- `DISCORD_WEBHOOK_URL`: concept 브리핑용 동아리 서버 webhook
- `DISCORD_WEBHOOK_MAP_JSON`: trend 채널별 동아리 서버 webhook 맵
- `OPENAI_API_KEY`: 필요 시 그대로 유지 가능하지만, 보안상 재발급을 권장할 수 있음

### 3.2 채널 매핑 파일

파일:

- `config/channel_interest_map.json`

반드시 수정:
- `channel_id`
- `webhook_key`
- `enabled`
- `interests`

개인 서버용 채널 ID를 그대로 두면 안 된다.

## 4. reset을 권장하는 파일

### 4.1 concept 진행 상태

파일:

- `content/concepts/history/concept_progress.json`

언제 reset?
- 동아리 서버에서 concept 브리핑을 **처음부터 다시 보내고 싶을 때**

권장 초기값:

```json
{
  "version": 1,
  "last_index": -1,
  "last_path": null,
  "last_briefing_key": null,
  "last_posted_at": null
}
```

reset하지 않아도 되는 경우:
- 개인 서버에서 테스트하던 순서를 그대로 이어가고 싶을 때

### 4.2 trend 게시 history

파일:

- `content/trends/history/published_trends.json`

언제 reset?
- 동아리 서버에서 fresh source 기준을 **새로 시작**하고 싶을 때
- 개인 서버 채널 ID 흔적을 없애고 싶을 때

권장 초기값:

```json
{}
```

reset하지 않아도 되는 경우:
- 이전 테스트 이력까지 포함해 같은 source 재게시를 계속 막고 싶을 때

## 5. 전환 절차

1. `config/channel_interest_map.json`을 동아리 서버 기준으로 수정
2. GitHub Secrets를 동아리 서버 기준으로 교체
3. 아래 중 필요한 파일 reset
   - `content/concepts/history/concept_progress.json`
   - `content/trends/history/published_trends.json`
4. push
5. `workflow_dispatch`로 concept 1회 수동 실행
6. `workflow_dispatch`로 trend를 채널별로 수동 실행
7. 결과가 맞으면 schedule 운영 시작

## 6. 전환 전 최종 점검

- [ ] `config/channel_interest_map.json`이 동아리 서버 채널 ID로 바뀌었다
- [ ] `DISCORD_WEBHOOK_URL`이 동아리 concept 채널 webhook로 교체됐다
- [ ] `DISCORD_WEBHOOK_MAP_JSON`이 동아리 trend 채널 webhook 맵으로 교체됐다
- [ ] concept를 처음부터 보낼지 결정했고, 필요하면 `concept_progress.json`을 reset했다
- [ ] trend history를 새로 시작할지 결정했고, 필요하면 `published_trends.json`을 reset했다
- [ ] concept 수동 실행 성공
- [ ] trend 채널별 수동 실행 성공 또는 정상 `skipped` 확인

## 7. 추천 기본값

동아리 서버로 처음 옮길 때는 아래를 권장한다.

- `config/channel_interest_map.json`: 동아리 채널 정보로 교체
- `DISCORD_WEBHOOK_URL`: 새 concept 채널 webhook로 교체
- `DISCORD_WEBHOOK_MAP_JSON`: 새 trend 채널 webhook 맵으로 교체
- `content/concepts/history/concept_progress.json`: reset
- `content/trends/history/published_trends.json`: reset

이렇게 하면 개인 서버 테스트 흔적 없이 깔끔하게 시작할 수 있다.
