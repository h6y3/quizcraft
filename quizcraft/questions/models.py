"""
Models for question extraction and storage
"""

from typing import Dict, List, Optional, Any


class Question:
    """Represents a multiple-choice question"""

    def __init__(
        self,
        question_text: str,
        options: Dict[str, str],
        correct_answer: str,
        explanation: Optional[str] = None,
        source_page: Optional[int] = None,
        source_text: Optional[str] = None,
        difficulty: Optional[str] = None,
        category: Optional[str] = None,
    ):
        """
        Initialize a Question object

        Args:
            question_text: The question text
            options: Dictionary of options (e.g., {"A": "Option A", "B": "Option B"})
            correct_answer: The correct answer key (e.g., "A")
            explanation: Explanation of the correct answer
            source_page: Page number where the question was found
            source_text: Original text from which the question was extracted
            difficulty: Question difficulty level (easy, medium, hard)
            category: Question category or topic
        """
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.source_page = source_page
        self.source_text = source_text
        self.difficulty = difficulty
        self.category = category

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert question to dictionary format

        Returns:
            Dictionary representation of the question
        """
        return {
            "question": self.question_text,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "source_page": self.source_page,
            "source_text": self.source_text,
            "difficulty": self.difficulty,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Question":
        """
        Create a Question object from a dictionary

        Args:
            data: Dictionary representation of the question

        Returns:
            Question object
        """
        return cls(
            question_text=data["question"],
            options=data["options"],
            correct_answer=data["correct_answer"],
            explanation=data.get("explanation"),
            source_page=data.get("source_page"),
            source_text=data.get("source_text"),
            difficulty=data.get("difficulty"),
            category=data.get("category"),
        )


class QuestionSet:
    """Represents a collection of questions"""

    def __init__(
        self, questions: List[Question], metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a QuestionSet object

        Args:
            questions: List of Question objects
            metadata: Additional metadata about the question set
        """
        self.questions = questions
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert question set to dictionary format

        Returns:
            Dictionary representation of the question set
        """
        return {
            "questions": [q.to_dict() for q in self.questions],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuestionSet":
        """
        Create a QuestionSet object from a dictionary

        Args:
            data: Dictionary representation of the question set

        Returns:
            QuestionSet object
        """
        questions = [Question.from_dict(q) for q in data["questions"]]
        return cls(questions=questions, metadata=data.get("metadata", {}))