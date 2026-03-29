from __future__ import annotations

import json

from models.quiz import Quiz
from services.grading_service import GradingService


def build_quiz(answer_key: list[int], explanation: str | None = "해설") -> Quiz:
    return Quiz(
        briefing_id=1,
        quiz_type="mcq",
        question="문제",
        answer_key_json=json.dumps(answer_key),
        explanation=explanation,
        status="open",
    )


def test_grade_multiple_choice_first_try_correct_scores_ten() -> None:
    grading_service = GradingService()
    quiz = build_quiz(answer_key=[2])

    result = grading_service.grade_multiple_choice(quiz=quiz, selected_choice=2, attempt_no=1)

    assert result.normalized_answer == "2"
    assert result.is_correct is True
    assert result.score == 10
    assert result.explanation == "해설"


def test_grade_multiple_choice_second_try_correct_scores_four() -> None:
    grading_service = GradingService()
    quiz = build_quiz(answer_key=[1, 3], explanation=None)

    result = grading_service.grade_multiple_choice(quiz=quiz, selected_choice=3, attempt_no=2)

    assert result.normalized_answer == "3"
    assert result.is_correct is True
    assert result.score == 4
    assert result.explanation is None


def test_grade_multiple_choice_incorrect_scores_one() -> None:
    grading_service = GradingService()
    quiz = build_quiz(answer_key=[4])

    result = grading_service.grade_multiple_choice(quiz=quiz, selected_choice=2, attempt_no=1)

    assert result.normalized_answer == "2"
    assert result.is_correct is False
    assert result.score == 1
