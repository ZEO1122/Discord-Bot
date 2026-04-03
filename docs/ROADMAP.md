# Roadmap — GAS 중심 브리핑 발행기

## 현재 방향

이 레포는 concept와 trend 브리핑 발행에만 집중한다.

우선순위는 아래 순서를 따른다.

1. concept 게시 안정화
2. trend 선정과 생성 품질 개선
3. 운영 로그와 유지보수성 강화

## Phase 1 — concept 경로 안정화

### 목표
- manifest 기반 concept 순차 게시가 안정적으로 동작한다.
- Discord embed 길이 제한 오류를 줄인다.

### 체크리스트
- [ ] `manifest.json` 순서 검증
- [ ] concept markdown 필수 필드 점검
- [ ] Script Properties progress 갱신 검증

## Phase 2 — trend 경로 개선

### 목표
- 지난 7일 논문 안에서 citation_count 기준 선정 품질을 안정화한다.
- 생성 결과를 더 안정적으로 게시한다.

### 체크리스트
- [ ] trend config 정교화
- [ ] 지난 7일 논문 범위 유지 여부 검증
- [ ] citation_count 기준 선정 로직 점검
- [ ] OpenAI 프롬프트 품질 개선
- [ ] Google Sheets history 기반 중복 방지 검증

## Phase 3 — 운영 편의 개선

### 목표
- 운영자가 실패 원인을 빠르게 파악할 수 있다.
- 문서와 실제 구조가 계속 일치한다.

### 체크리스트
- [ ] Apps Script 로그 포인트 정리
- [ ] 운영 체크리스트 최신화
- [ ] 유지보수 가이드 보강
