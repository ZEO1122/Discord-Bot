from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models.base import Base
from models.briefing import Briefing
from repositories.briefing_repository import BriefingRepository
from repositories.publish_log_repository import PublishLogRepository
from services.publish_service import InMemoryPublisher, PublishFlowError, PublishService


def create_test_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return session_factory()


def test_publish_latest_briefing_marks_briefing_and_writes_log() -> None:
    session = create_test_session()
    briefing_repository = BriefingRepository(session)
    publish_log_repository = PublishLogRepository(session)
    briefing = briefing_repository.ensure_sample_briefing(track="dl-basics")

    service = PublishService(briefing_repository, publish_log_repository)
    result = service.publish_latest_briefing(
        track="dl-basics",
        channel_id="test-channel",
        publisher=InMemoryPublisher(),
    )
    session.commit()

    refreshed = briefing_repository.get_by_briefing_key(briefing.briefing_key)
    publish_log = publish_log_repository.get_latest_for_briefing(briefing.id)

    assert result.publish_status == "success"
    assert result.discord_message_id == f"dry-run-{briefing.briefing_key}"
    assert refreshed is not None
    assert refreshed.status == "published"
    assert publish_log is not None
    assert publish_log.publish_status == "success"
    assert publish_log.discord_message_id == f"dry-run-{briefing.briefing_key}"


def test_build_embed_payload_falls_back_when_source_is_missing() -> None:
    session = create_test_session()
    service = PublishService(BriefingRepository(session), PublishLogRepository(session))
    briefing_without_sources = Briefing(
        briefing_key="no-source-briefing",
        track="dl-basics",
        title="제목",
        one_line="한 줄 요약",
        what_happened="무슨 내용인가",
        why_it_matters="왜 중요한가",
        easy_terms_json="[]",
        discussion_prompt=None,
        status="draft",
    )

    payload = service.build_embed_payload(briefing_without_sources)

    assert payload["fields"][2]["value"] == "아직 준비되지 않았습니다."
    assert payload["fields"][3]["value"] == "- 출처 없음"


class _FailingPublisher:
    def publish(self, briefing: object, payload: object) -> str:
        raise RuntimeError("webhook timeout")


def test_publish_briefing_failure_writes_failed_log() -> None:
    session = create_test_session()
    briefing_repository = BriefingRepository(session)
    publish_log_repository = PublishLogRepository(session)
    briefing = briefing_repository.ensure_sample_briefing(track="dl-basics")
    service = PublishService(briefing_repository, publish_log_repository)

    result = service.publish_briefing(
        briefing=briefing,
        channel_id="test-channel",
        publisher=_FailingPublisher(),
    )
    session.commit()

    refreshed = briefing_repository.get_by_briefing_key(briefing.briefing_key)
    publish_log = publish_log_repository.get_latest_for_briefing(briefing.id)
    assert result.publish_status == "failed"
    assert result.discord_message_id is None
    assert result.error_message == "webhook timeout"
    assert refreshed is not None
    assert refreshed.status == "draft"
    assert publish_log is not None
    assert publish_log.publish_status == "failed"
    assert publish_log.error_message == "webhook timeout"
    assert publish_log.published_at is None


def test_get_latest_briefing_payload_requires_published_briefing() -> None:
    session = create_test_session()
    briefing_repository = BriefingRepository(session)
    publish_log_repository = PublishLogRepository(session)
    briefing_repository.ensure_sample_briefing(track="dl-basics")
    service = PublishService(briefing_repository, publish_log_repository)

    try:
        service.get_latest_briefing_payload(track="dl-basics")
    except PublishFlowError:
        pass
    else:
        raise AssertionError("Expected PublishFlowError when no published briefing exists")
