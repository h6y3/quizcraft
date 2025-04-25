"""
Question validation module for ensuring question quality and structure
"""

from typing import List, Optional, Tuple

from .models import Question


class QuestionValidator:
    """Validates the structure and quality of extracted questions"""

    def __init__(
        self,
        min_question_length: int = 10,
        min_options: int = 2,
        max_options: int = 6,
        required_fields: Optional[List[str]] = None,
    ):
        """
        Initialize the question validator

        Args:
            min_question_length: Minimum length for question text
            min_options: Minimum number of options required
            max_options: Maximum number of options allowed
            required_fields: List of required fields in the question
        """
        self.min_question_length = min_question_length
        self.min_options = min_options
        self.max_options = max_options
        self.required_fields = required_fields or [
            "question_text",
            "options",
            "correct_answer",
        ]

    def validate_question(self, question: Question) -> Tuple[bool, List[str]]:
        """
        Validate a single question

        Args:
            question: Question object to validate

        Returns:
            Tuple of (is_valid, list of validation errors)
        """
        errors = []

        # Check required fields
        for field in self.required_fields:
            if not hasattr(question, field) or not getattr(question, field):
                errors.append(f"Missing required field: {field}")

        # Validate question text
        if hasattr(question, "question_text") and question.question_text:
            if len(question.question_text) < self.min_question_length:
                errors.append(
                    f"Question text too short: {len(question.question_text)} "
                    f"characters (minimum {self.min_question_length})"
                )
            if not question.question_text.strip().endswith("?"):
                errors.append("Question text should end with a question mark")

        # Validate options
        if hasattr(question, "options") and question.options:
            num_options = len(question.options)
            if num_options < self.min_options:
                errors.append(
                    f"Too few options: {num_options} "
                    f"(minimum {self.min_options})"
                )
            if num_options > self.max_options:
                errors.append(
                    f"Too many options: {num_options} "
                    f"(maximum {self.max_options})"
                )

            # Validate option keys
            valid_keys = set("ABCDE"[: self.max_options])
            for key in question.options.keys():
                if key not in valid_keys:
                    errors.append(f"Invalid option key: {key}")

            # Check for empty options
            for key, text in question.options.items():
                if not text or not text.strip():
                    errors.append(f"Empty text for option {key}")

        # Validate correct answer
        if (
            hasattr(question, "correct_answer")
            and question.correct_answer
            and hasattr(question, "options")
            and question.options
        ):
            if question.correct_answer not in question.options:
                errors.append(
                    f"Answer '{question.correct_answer}' not in options"
                )

        return len(errors) == 0, errors

    def validate_question_set(
        self, questions: List[Question]
    ) -> Tuple[List[Question], List[Tuple[Question, List[str]]]]:
        """
        Validate a set of questions and filter invalid ones

        Args:
            questions: List of Question objects to validate

        Returns:
            Tuple of (valid questions, list of (invalid question, errors))
        """
        valid_questions = []
        invalid_questions = []

        for question in questions:
            is_valid, errors = self.validate_question(question)
            if is_valid:
                valid_questions.append(question)
            else:
                invalid_questions.append((question, errors))

        return valid_questions, invalid_questions

    def fix_common_issues(
        self, question: Question
    ) -> Tuple[Question, List[str]]:
        """
        Attempt to fix common issues in a question

        Args:
            question: Question object to fix

        Returns:
            Tuple of (fixed question, list of fixes applied)
        """
        fixes = []
        fixed_question = Question(
            question_text=question.question_text,
            options=question.options.copy(),
            correct_answer=question.correct_answer,
            explanation=question.explanation,
            source_page=question.source_page,
            source_text=question.source_text,
            difficulty=question.difficulty,
            category=question.category,
        )

        # Fix missing question mark
        if (
            hasattr(fixed_question, "question_text")
            and fixed_question.question_text
            and not fixed_question.question_text.strip().endswith("?")
        ):
            fixed_question.question_text = (
                fixed_question.question_text.strip() + "?"
            )
            fixes.append("Added missing question mark")

        # Standardize option keys to uppercase
        if hasattr(fixed_question, "options") and fixed_question.options:
            new_options = {}
            for key, value in fixed_question.options.items():
                new_key = key.upper()
                if new_key != key:
                    fixes.append(f"Standardized option key {key} to {new_key}")
                new_options[new_key] = value
            fixed_question.options = new_options

        # Fix correct answer case to match options
        if (
            hasattr(fixed_question, "correct_answer")
            and fixed_question.correct_answer
            and fixed_question.correct_answer.upper()
            != fixed_question.correct_answer
        ):
            fixed_question.correct_answer = (
                fixed_question.correct_answer.upper()
            )
            fixes.append("Standardized correct answer to uppercase")

        return fixed_question, fixes
