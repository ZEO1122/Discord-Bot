from __future__ import annotations

from services.grading_service import GradeResult
from services.private_feedback_renderer import PrivateFeedbackRenderer


def test_render_correct_with_explanation() -> None:
    renderer = PrivateFeedbackRenderer()
    grade_result = GradeResult(
        normalized_answer="1",
        is_correct=True,
        score=10,
        explanation="중요 포인트입니다.",
    )

    message = renderer.render(grade_result=grade_result, attempt_no=1)

    assert message == "정답입니다\n시도 횟수: 1\n점수: 10\n해설: 중요 포인트입니다."


def test_render_incorrect_without_explanation_uses_default() -> None:
    renderer = PrivateFeedbackRenderer()
    grade_result = GradeResult(
        normalized_answer="3",
        is_correct=False,
        score=1,
        explanation=None,
    )

    message = renderer.render(grade_result=grade_result, attempt_no=2)

    assert message == "오답입니다\n시도 횟수: 2\n점수: 1\n해설: 해설은 아직 준비되지 않았습니다."
