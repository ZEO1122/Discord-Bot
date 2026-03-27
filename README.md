# AI 학술동아리 Discord 브리핑 자동화 저장소

이 저장소는 **딥러닝 개념 브리핑 + 세부 분야 동향 브리핑 + 퀴즈 포함 게시물**을 Discord로 자동 발행하기 위한 프로젝트다.

현재 운영 전제는 다음과 같다.

1. **상시 서버를 두지 않는다.**
2. 자동 발행은 **GitHub Actions + Discord Webhook**로 처리한다.
3. `discord.py` 기반 Gateway bot 코드는 남겨두되, 당장은 **개발/실험용 보조 경로**로 취급한다.

## 핵심 목표

1. 학술동아리 멤버가 매일 짧고 신뢰 가능한 AI 브리핑을 받는다.
2. 안정적인 딥러닝 개념은 미리 작성한 `.md` 파일에서 게시한다.
3. 최신 동향 브리핑은 실행 시점에 최신 논문 소스를 수집하고 GPT API로 생성해 게시한다.
4. 게시 이력은 GitHub Actions 로그와 Discord 메시지 결과로 추적한다.
5. trend 브리핑은 최근 게시 source를 history 파일에 기록해 중복 게시를 피한다.

## 현재 프로젝트 해석

이 저장소는 더 이상 "상시 Discord 봇 서비스"가 아니라, 아래 경로를 기본으로 하는 **콘텐츠 발행 자동화 저장소**로 본다.

```text
Markdown Brief Source                    Live Trend Fetch
        ↓                                      ↓
Build / Validate Script              GPT Summarize / Validate
        ↓                                      ↓
                  GitHub Actions
                        ↓
                 Discord Webhook
                        ↓
             Publish Logs / Action Logs
```

## 이 저장소에 들어 있는 것

- `AGENTS.md`
  에이전트 작업 규칙
- `docs/PRD.md`
  제품 목표와 범위
- `docs/ARCHITECTURE.md`
  GitHub Actions 중심 구조와 후속 확장 구조
- `docs/CONTENT_PIPELINE.md`
  개념/동향 브리핑 생성 규칙
- `docs/DATABASE_SCHEMA.md`
  로컬 개발용 데이터 모델과 후속 확장 스키마
- `docs/ROADMAP.md`
  Week 1~3 구현 로드맵
- `docs/OPERATIONS.md`
  GitHub Actions 운영과 smoke path

## 권장 기술 스택

- 언어: Python 3.11+
- 자동화: GitHub Actions
- Discord 게시: Discord Webhook
- 동향 생성: GPT API
- 로컬 개발 DB: SQLite
- 선택적 로컬 실험: `discord.py` Gateway bot

## 추천 저장소 구조

```text
.
├─ AGENTS.md
├─ README.md
├─ requirements.txt
├─ requirements-dev.txt
├─ content/
│  ├─ concepts/
│  └─ trends/
├─ scripts/
│  ├─ bootstrap_sqlite.py
│  ├─ publish_daily.py
│  ├─ seed_smoke_data.py
│  ├─ post_concept_brief.py
│  └─ post_trend_brief.py
├─ .github/
│  └─ workflows/
├─ src/
│  ├─ bot/
│  ├─ services/
│  ├─ repositories/
│  ├─ models/
│  └─ core/
├─ docs/
└─ data/
```

## 가장 먼저 할 일

1. `.env.example`를 참고해 로컬 `.env` 구성
2. `content/concepts/`용 markdown 포맷 확정
3. GitHub Secrets 등록
4. concept posting workflow부터 구현
5. trend posting workflow에 최신 source 수집과 GPT 생성 연결

## 콘텐츠 운영 원칙 요약

- `discussion_prompt`와 `graded_quiz`를 분리한다.
- 정답 정보(`answer_key`)는 공개 Discord 메시지에 포함하지 않는다.
- 출처는 문자열이 아니라 구조화 객체로 저장한다.
- trend 브리핑은 **실행 시점 최신 source를 수집한 뒤** 게시한다.
- trend 브리핑은 **출처 없이 자동 게시하지 않는다.**
- concept 브리핑은 저장소의 `.md` 원본을 진실 소스로 본다.

## concept markdown 포맷

추천 형식은 `frontmatter + 본문 섹션`이다.

```md
---
briefing_key: dl-basics-attention-001
track: dl-basics
mode: concept
title: 어텐션은 왜 중요한가
one_line: 어텐션은 입력 전체 중 중요한 부분에 더 집중하도록 돕는 메커니즘이다.
discussion_prompt: Transformer가 RNN보다 유리한 상황은 언제일까?
sources:
  - title: Attention Is All You Need
    url: https://arxiv.org/abs/1706.03762
    source_type: paper
---

## 무슨 내용인가
...

## 왜 중요한가
...

## 쉬운 용어
- Attention: ...
```

필수 필드:
- `briefing_key`
- `track`
- `mode`
- `title`
- `one_line`
- `sources`
- 본문 `무슨 내용인가`
- 본문 `왜 중요한가`

## GitHub Actions 워크플로우

추가된 워크플로우 초안:

- `.github/workflows/post-concept.yml`
  - markdown concept 브리핑 게시
- `.github/workflows/post-trend.yml`
  - 최신 source 수집 + GPT API 기반 trend 브리핑 게시

trend 브리핑에는 아래 주의 문구를 항상 포함한다.

```text
주의: 이 브리핑은 최신 source를 바탕으로 GPT가 요약한 내용입니다. 해석 오류나 누락 가능성이 있으니 원문 출처를 함께 확인하세요.
```

필수 GitHub Secrets:
- `DISCORD_WEBHOOK_URL`
- `OPENAI_API_KEY`

선택 GitHub Variables/Secrets:
- `DEFAULT_TRACK`
- `TREND_MAX_RESULTS`

## 로컬 smoke path

로컬에서 concept 게시 경로를 확인하려면:

```bash
python3 scripts/bootstrap_sqlite.py
python3 scripts/seed_smoke_data.py
python3 scripts/publish_daily.py --dry-run
```

Gateway bot 실험이 필요할 때만 아래를 사용한다.

```bash
PYTHONPATH=src python -m bot.app
```

## GPT 프롬프트 위치

개념 브리핑 markdown 50개 생성을 위한 프롬프트 템플릿은 아래 파일에 둔다.

- `content/concepts/CONCEPT_BATCH_PROMPT.md`

## 현재 구현 상태 해석

- `src/bot/*` 는 실험용 slash command 경로다.
- `src/services/publish_service.py` 의 webhook 게시 경로는 GitHub Actions 자동화에서도 재사용 가능하다.
- `SQLite`는 로컬 개발/검증용이다.
- trend source는 저장소 파일이 아니라 런타임에 수집한다.
- trend 중복 방지는 `content/trends/history/published_trends.json` 으로 관리한다.
- GitHub Actions 런너는 기본적으로 휘발성이므로, 자동 발행 운영에서는 DB보다 **Actions logs + Discord 결과**를 1차 추적 수단으로 본다.
