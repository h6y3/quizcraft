"""
Service layer for question extraction and storage
"""

import os
import logging
from typing import Dict, List, Any, Optional, Tuple

from ..ai.service import AIService

from .extractor import QuestionExtractor
from .validator import QuestionValidator
from .models import Question, QuestionSet
from .storage import QuestionStorage

logger = logging.getLogger(__name__)


class QuestionService:
    """Service layer for question extraction, validation, and storage"""

    def __init__(
        self,
        db_path: Optional[str] = None,
        use_ai_fallback: bool = True,
    ):
        """
        Initialize the question service

        Args:
            db_path: Path to the SQLite database file
            use_ai_fallback: Whether to use AI fallback for extraction
        """
        # Use default database path if not provided
        if db_path is None:
            home_dir = os.path.expanduser("~")
            db_path = os.path.join(home_dir, ".quizcraft", "questions.db")

        self.extractor = QuestionExtractor()
        self.validator = QuestionValidator()
        self.storage = QuestionStorage(db_path)
        self.use_ai_fallback = use_ai_fallback

        if use_ai_fallback:
            self.ai_service = AIService()
        else:
            self.ai_service = None

    def extract_questions_from_segments(
        self, segments: List[Dict[str, Any]], source_file: Optional[str] = None
    ) -> Tuple[List[Question], Dict[str, Any]]:
        """
        Extract questions from text segments

        Args:
            segments: List of text segments from PDF extraction
            source_file: Original source file path

        Returns:
            Tuple of (extracted questions, extraction stats)
        """
        stats = {
            "total_segments": len(segments),
            "potential_question_segments": 0,
            "pattern_extracted": 0,
            "ai_extracted": 0,
            "invalid_questions": 0,
            "stored_questions": 0,
        }

        # Count potential question segments
        for segment in segments:
            if segment["type"] == "potential_question":
                stats["potential_question_segments"] += 1

        # Extract questions using pattern matching
        pattern_questions = self.extractor.extract_questions(segments)
        stats["pattern_extracted"] = len(pattern_questions)

        # Validate extracted questions
        valid_questions, invalid_questions = (
            self.validator.validate_question_set(pattern_questions)
        )
        stats["invalid_questions"] = len(invalid_questions)

        # Try to fix invalid questions
        fixed_questions = []
        for question, errors in invalid_questions:
            fixed_question, fixes = self.validator.fix_common_issues(question)
            if fixes:
                # Re-validate the fixed question
                is_valid, new_errors = self.validator.validate_question(
                    fixed_question
                )
                if is_valid:
                    fixed_questions.append(fixed_question)
                    logger.info(f"Fixed question: {', '.join(fixes)}")

        # Combine valid and fixed questions
        all_questions = valid_questions + fixed_questions

        # Use AI fallback for extraction if enabled and we have few questions
        ai_questions = []
        if self.use_ai_fallback and stats["pattern_extracted"] < 5:
            ai_questions = self._extract_with_ai_fallback(
                segments, source_file
            )
            stats["ai_extracted"] = len(ai_questions)

            # Validate AI-generated questions
            valid_ai, invalid_ai = self.validator.validate_question_set(
                ai_questions
            )
            all_questions.extend(valid_ai)
            stats["invalid_questions"] += len(invalid_ai)

        # Store valid questions
        if source_file and all_questions:
            question_ids = self.storage.store_questions(
                all_questions, source_file
            )
            stats["stored_questions"] = len(question_ids)

        return all_questions, stats

    def _extract_with_ai_fallback(
        self, segments: List[Dict[str, Any]], source_file: Optional[str] = None
    ) -> List[Question]:
        """
        Extract questions using AI as fallback

        Args:
            segments: List of text segments from PDF extraction
            source_file: Original source file path

        Returns:
            List of questions extracted by AI
        """
        if not self.ai_service:
            return []

        # Prepare context from segments
        combined_text = "\n\n".join([segment["text"] for segment in segments])

        # Note: cache_key_prefix generation logic kept for future use
        # if needed for caching extraction results
        if source_file:
            # This would be used for caching if implemented
            pass

        # Create a custom prompt for extraction
        extraction_prompt = """
        Analyze the following educational content and extract existing
        multiple-choice questions. DO NOT create new questions - only extract
        questions that are already in the text.

        For each question you identify:
        1. Extract the question text exactly as written
        2. Identify all options (A, B, C, D, etc.)
        3. Determine the correct answer if indicated
        4. Extract any explanation if provided

        Format your response as valid JSON with this structure:
        ```json
        {
          "questions": [
            {
              "question": "Extracted question text?",
              "options": {
                "A": "First option",
                "B": "Second option",
                "C": "Third option",
                "D": "Fourth option"
              },
              "correct_answer": "A",
              "explanation": "Extracted explanation if available"
            }
          ]
        }
        ```

        If you cannot identify any questions in the text, return
        an empty array for "questions".
        """

        try:
            # Use AI service to extract questions
            result = self.ai_service.client.generate_response(
                prompt=combined_text,
                system_prompt=extraction_prompt,
                max_tokens=4000,
                temperature=0.0,  # Use lower temperature for extraction
            )

            # Parse and validate the response
            questions_json = (
                self.ai_service.client.validate_and_fix_json_response(
                    result["content"]
                )
            )

            # Convert to Question objects
            questions = []
            if "questions" in questions_json:
                for q_data in questions_json["questions"]:
                    question = Question.from_dict(q_data)
                    questions.append(question)

            return questions

        except Exception as e:
            logger.error(f"AI extraction error: {str(e)}")
            return []

    def get_questions(
        self,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        source_file: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Question]:
        """
        Get questions from storage with filtering

        Args:
            category: Filter by category
            difficulty: Filter by difficulty
            source_file: Filter by source file
            limit: Maximum number of questions to retrieve

        Returns:
            List of Question objects
        """
        return self.storage.get_questions(
            category=category,
            difficulty=difficulty,
            source_file=source_file,
            limit=limit,
        )

    def get_question_stats(
        self, source_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get statistics about stored questions

        Args:
            source_file: Optional source file to filter by

        Returns:
            Dictionary of question statistics
        """
        total = self.storage.count_questions(source_file=source_file)

        # Get counts by difficulty
        difficulty_counts = {}
        for difficulty in ["easy", "medium", "hard"]:
            count = self.storage.count_questions(
                difficulty=difficulty, source_file=source_file
            )
            if count > 0:
                difficulty_counts[difficulty] = count

        # Get counts by category if categories exist
        category_counts = {}
        questions = self.storage.get_questions(source_file=source_file)
        for question in questions:
            if question.category:
                category_counts[question.category] = (
                    category_counts.get(question.category, 0) + 1
                )

        return {
            "total_questions": total,
            "by_difficulty": difficulty_counts,
            "by_category": category_counts,
        }

    def create_question_set(
        self,
        categories: Optional[List[str]] = None,
        difficulties: Optional[List[str]] = None,
        source_file: Optional[str] = None,
        count: int = 10,
    ) -> QuestionSet:
        """
        Create a curated set of questions for quizzing

        Args:
            categories: List of categories to include
            difficulties: List of difficulties to include
            source_file: Source file to filter by
            count: Number of questions to include

        Returns:
            QuestionSet object with selected questions
        """
        selected_questions = []

        # If categories provided, get questions from each category
        if categories:
            questions_per_category = max(1, count // len(categories))
            for category in categories:
                category_questions = self.storage.get_questions(
                    category=category,
                    source_file=source_file,
                    limit=questions_per_category,
                )
                selected_questions.extend(category_questions)

        # If difficulties provided, ensure distribution across difficulties
        elif difficulties:
            questions_per_difficulty = max(1, count // len(difficulties))
            for difficulty in difficulties:
                difficulty_questions = self.storage.get_questions(
                    difficulty=difficulty,
                    source_file=source_file,
                    limit=questions_per_difficulty,
                )
                selected_questions.extend(difficulty_questions)

        # Otherwise, just get the requested number of questions
        else:
            selected_questions = self.storage.get_questions(
                source_file=source_file, limit=count
            )

        # Ensure we don't exceed the requested count
        if len(selected_questions) > count:
            selected_questions = selected_questions[:count]

        # Create metadata for the question set
        metadata = {
            "source_file": source_file,
            "categories": categories,
            "difficulties": difficulties,
            "total_questions": len(selected_questions),
        }

        return QuestionSet(questions=selected_questions, metadata=metadata)
