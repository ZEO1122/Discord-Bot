# Leaderboard Strategy

이 문서는 현재 프로젝트에서 **어디까지 구현이 끝났는지**와, 앞으로 **리더보드/상금 운영을 어떤 방향으로 설계할지**를 정리한 의사결정 문서다.

## 1. 문서 목적

- 현재 완료된 범위를 명확히 정리한다.
- 리더보드 도입 시 고려해야 할 쟁점을 구조적으로 정리한다.
- 퀴즈 형식, 순위 기준, 런타임 요구사항을 비교한다.
- 동아리 운영 관점에서 가장 현실적인 다음 단계를 제안한다.

## 2. 현재 완료된 부분

현재 저장소는 **브리핑 자동 발행 시스템**으로서의 MVP를 거의 갖춘 상태다.

### 2.1 concept 브리핑 자동화

- `content/concepts/**/*.md` 기반 콘텐츠 구조 확립
- `manifest + progress` 기반 순차 게시 구현
- 평일 오전 9시 KST 자동 발행 workflow 구현
- Discord full embed 형식으로 concept 게시되도록 조정 완료

관련 파일:
- `content/concepts/manifest.json`
- `content/concepts/history/concept_progress.json`
- `scripts/post_concept_brief.py`
- `scripts/post_concept_queue.py`
- `.github/workflows/post-concept.yml`

### 2.2 trend 브리핑 자동화

- GitHub Actions + Discord Webhook 기반 주간 발행 구조 구현
- 채널별 관심분야 설정(`channel_interest_map.json`) 구현
- 최신 source runtime fetch 구현
- GPT 기반 요약 생성 구현
- 중복 게시 방지(history) 구현
- Discord 출력 형식 정리 및 caution 문구 추가

관련 파일:
- `config/channel_interest_map.json`
- `content/trends/history/published_trends.json`
- `scripts/fetch_trend_sources.py`
- `scripts/post_trend_brief.py`
- `scripts/post_weekly_trends.py`
- `.github/workflows/post-trend.yml`

### 2.3 운영 문서

운영자가 바로 따라할 수 있는 수준의 문서가 정리되어 있다.

관련 문서:
- `docs/SERVER_SETUP_GUIDE.md`
- `docs/MAINTENANCE_GUIDE.md`
- `docs/ONE_PAGE_OPERATIONS.md`
- `docs/CLUB_SERVER_TRANSITION.md`
- `docs/OPERATIONS.md`

## 3. 현재 고민 중인 부분

다음 단계는 **참여 유도형 학습 운영**이다.

핵심 목표:
- 주니어 부원의 참여율을 높인다.
- 브리핑을 읽고 실제로 학습했는지 확인한다.
- 퀴즈 결과를 기반으로 리더보드를 만들고, 이후 상금 등 인센티브 구조로 연결한다.

하지만 이를 위해서는 아래 결정이 필요하다.

### 3.1 퀴즈 형식

선택지:
- 단답형
- 서술형

### 3.2 리더보드 기준

선택지:
- 정답 기준
- 제출 횟수 기준

### 3.3 런타임 구조

선택지:
- 현재처럼 GitHub Actions + Webhook만 유지
- 실제 Discord bot 런타임 도입
- Cloudflare Workers 같은 서버리스 interaction 처리 구조 도입

## 4. 퀴즈 형식 비교

### 4.1 단답형

정의:
- 1~2문장 또는 핵심 키워드 위주의 짧은 답변

장점:
- 자동 채점이 상대적으로 쉽다
- accepted keyword 기반으로 공정한 판정이 가능하다
- 리더보드와 연결하기 좋다
- 운영 비용과 분쟁이 적다

단점:
- 너무 짧게 설계하면 암기형 문제로 흐를 수 있다
- 사고 과정을 충분히 확인하기 어렵다

### 4.2 서술형

정의:
- 사용자가 개념을 자기 문장으로 설명하는 자유도 높은 답변

장점:
- 실제 이해도를 더 잘 드러낸다
- 학습 효과가 높다
- 부원의 설명 능력까지 확인할 수 있다

단점:
- 자동 채점이 어렵다
- 판정 기준을 설명하기 어렵다
- 상금과 연결하면 공정성 논란이 커질 수 있다
- 운영자가 수동 검토해야 할 가능성이 커진다

## 5. 리더보드 기준 비교

### 5.1 정답 기준 리더보드

추천 해석:
- 사용자가 **몇 개의 문제를 맞혔는지**를 중심으로 순위를 계산한다.
- 같은 문제를 여러 번 맞혀도 1개 문제로만 집계하는 방식이 가장 공정하다.

예시 지표:
- `unique_correct_quiz_count`
- `first_try_correct_count`
- `total_correct_attempts`

장점:
- 학습성과 중심이다
- 상금 기준으로 설명하기 쉽다
- 리더보드의 설득력이 높다

단점:
- 초보자는 초기에 불리할 수 있다

### 5.2 제출 횟수 기준 리더보드

예시 지표:
- `total_attempts`

장점:
- 참여 유도에는 강하다
- 초보자도 쉽게 순위 경쟁에 들어올 수 있다

단점:
- 많이 제출만 해도 순위가 올라갈 수 있다
- 품질보다 양으로 흐를 수 있다
- 상금 기준으로는 공정성 논란이 생길 수 있다

## 6. 추천 방향

현재 동아리 운영 목적과 상금 구조를 고려하면 아래 조합이 가장 현실적이다.

### 추천 퀴즈 형식
- **짧은 단답형 서술**

이유:
- 단순 객관식보다 이해도를 더 볼 수 있다
- 완전 자유서술보다 채점이 쉽다
- 키워드 기반 자동 채점이 가능하다

### 추천 리더보드 기준
- **정답 기준 리더보드**

구체적으로는:
1. 맞힌 문제 수(`unique_correct_quiz_count`) 우선
2. 첫 시도 정답 수(`first_try_correct_count`) 보조
3. 총 제출 수(`total_attempts`) 보조

### 참여 유도 보조안
- 메인 리더보드: 정답 기준
- 별도 참여상: 제출 횟수 기준

이렇게 하면
- 학습성과와
- 참여율
둘 다 챙길 수 있다.

## 7. 런타임 현실성

### 현재 구조의 한계

현재 기본 운영은:
- `GitHub Actions + Discord Webhook`

이 구조로는 가능:
- 브리핑 자동 게시
- 주간 trend 브리핑 자동 게시

이 구조로는 어려움:
- 사용자가 Discord 안에서 즉시 답변 제출
- 사용자별 제출 기록 저장
- 실시간 정답 판정
- 리더보드 갱신

즉, **리더보드 기능을 진짜로 운영하려면 interaction 처리를 할 런타임이 필요하다.**

### 필요한 것

- slash command 또는 modal을 처리할 백엔드
- 사용자별 답변을 저장할 데이터 저장소
- 정답 판정 로직
- 관리자 조회 및 리더보드 조회 경로

## 8. Cloudflare Workers 가능성

현재 제약:
- 로컬 서버 상시 운영은 어렵다
- 비용은 최소화해야 한다

이 조건에서는 `Cloudflare Workers`가 유력한 대안이다.

장점:
- 무료 플랜으로 소규모 트래픽 처리 가능성이 높다
- 상시 서버를 두지 않아도 Discord interaction endpoint를 운영할 수 있다
- slash command, 버튼, modal 같은 Discord interaction 구조와 잘 맞는다

주의점:
- webhook 기반 배치 발행과는 별도 아키텍처가 필요하다
- Discord 서명 검증, endpoint 설계, 저장소 연동을 새로 잡아야 한다

즉, **브리핑 발행은 계속 GitHub Actions로 유지하고, 퀴즈/리더보드는 Workers로 분리하는 하이브리드 구조**가 가장 현실적이다.

## 9. 추천 아키텍처 초안

### 브리핑 발행
- GitHub Actions + Discord Webhook 유지

### 퀴즈/리더보드
- Cloudflare Workers
- Discord interaction endpoint
- 사용자 제출 저장소
- 관리자 통계 및 리더보드 응답

```text
GitHub Actions -> Brief Post

Discord User -> Slash Command / Modal -> Cloudflare Workers
                                   ↓
                              Answer Store
                                   ↓
                        Stats / Leaderboard / Admin View
```

## 10. 다음 의사결정

현재 기준으로 다음 3가지를 확정하면 된다.

1. 퀴즈 형식은 **짧은 단답형 서술**로 갈지
2. 리더보드는 **정답 문제 수 기준**으로 갈지
3. interaction 런타임을 **Cloudflare Workers**로 도입할지

## 11. 현재 권장 결론

가장 현실적인 조합:

- 퀴즈 형식: **짧은 단답형 서술**
- 리더보드 기준: **맞힌 문제 수 기준**
- 제출 횟수는 별도 참여상 지표로 사용
- 런타임: **Cloudflare Workers 도입 검토**

이 조합이
- 참여 유도
- 공정성
- 비용 최소화
- 운영 가능성
을 가장 균형 있게 만족한다.
