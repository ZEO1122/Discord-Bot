# Linux OpenCode Setup

## 1. 목표

이 문서는 Linux 환경에서 OpenCode로 이 저장소를 다룰 때 필요한 최소 흐름을 정리한다.

현재 프로젝트는 Google Apps Script 기반 브리핑 발행기이므로, 로컬 Discord bot 런타임이나 Python 서버를 전제로 하지 않는다.

## 2. 기본 준비

### 필수 도구
- `git`
- `node`
- `npm`
- `clasp`

### 설치 예시
```bash
node --version
npm --version
npm install
```

## 3. 기본 작업 명령

```bash
npx clasp login
npx clasp status
npx clasp push
npx clasp pull
npx clasp open
```

## 4. OpenCode로 주로 건드릴 대상

- `apps-script/*.gs`
- `config/trend_brief_config.json`
- `content/concepts/**/*.md`
- `docs/*.md`

## 5. 권장 작업 예시

- concept embed 형식 조정
- trend 선정 로직 수정
- OpenAI 프롬프트 보정
- 운영 문서 업데이트

## 6. 점검 포인트

- 변경 후 `npx clasp push`가 가능한지 확인
- GAS `runConceptDaily()`와 `runTrendWeekly()` 로그로 동작 확인
- Script Properties 키가 최신인지 확인

## 7. 로그 확인

문제가 생기면 아래부터 확인한다.

```bash
ls ~/.local/share/opencode/log/
tail -f ~/.local/share/opencode/log/<latest-log-file>
```
