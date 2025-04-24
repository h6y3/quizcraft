"""
Tests for the question extraction module
"""

import unittest
import tempfile
import os
import json
from typing import Dict, List, Any

from quizcraft.questions.extractor import QuestionExtractor
from quizcraft.questions.validator import QuestionValidator
from quizcraft.questions.storage import QuestionStorage
from quizcraft.questions.models import Question


class TestQuestionExtractor(unittest.TestCase):
    """Test the QuestionExtractor class"""

    def setUp(self):
        """Set up the test fixtures"""
        self.extractor = QuestionExtractor()
        self.validator = QuestionValidator()
        
        # Sample questions in the expected format
        self.sample_segments = [
            {
                "page": 1,
                "text": "1. What is Python?\nA) A snake\nB) A programming language\nC) A game\nD) A tool\n\nAnswer: B",
                "type": "potential_question",
                "metadata": {}
            },
            {
                "page": 1,
                "text": "2. Which of the following is not a Python data type?\nA) List\nB) Dictionary\nC) Array\nD) Tuple\n\nCorrect: C",
                "type": "potential_question",
                "metadata": {}
            },
            {
                "page": 2,
                "text": "This is not a question, just some text.",
                "type": "paragraph",
                "metadata": {}
            }
        ]

    def test_extract_questions(self):
        """Test question extraction from segments"""
        # Debug finding questions
        for segment in self.sample_segments:
            if self.extractor._is_question_segment(segment["text"]):
                print(f"Found question segment: {segment['text'][:30]}...")
        
        # Debug extracting options
        for segment in self.sample_segments:
            options = self.extractor._extract_options(segment["text"])
            if options:
                print(f"Found options: {options}")
                
                # Debug extracting correct answer
                answer = self.extractor._extract_correct_answer(segment["text"], options)
                print(f"Correct answer: {answer}")
                
                # Debug question text extraction
                question_text = self.extractor._extract_question_text(segment["text"])
                print(f"Question text: {question_text}")
            
        # Debug group formation
        groups = self.extractor._group_question_segments(self.sample_segments)
        print(f"Number of groups formed: {len(groups)}")
        for i, group in enumerate(groups):
            print(f"Group {i+1} has {len(group)} segments")
            
            # Try parsing each group
            question = self.extractor._parse_question_group(group)
            if question:
                print(f"  Successfully parsed question: {question.question_text}")
            else:
                print(f"  Failed to parse question from group {i+1}")
            
        # Perform the actual extraction
        questions = self.extractor.extract_questions(self.sample_segments)
        
        # Should extract 2 questions
        self.assertEqual(len(questions), 2, f"Expected 2 questions, got {len(questions)}")
        
        # Manual test to see if we can extract correctly
        # Create a direct question for the first segment
        segment = self.sample_segments[0]
        question_text = self.extractor._extract_question_text(segment["text"])
        options = self.extractor._extract_options(segment["text"])
        correct_answer = self.extractor._extract_correct_answer(segment["text"], options)
        
        if question_text and options and correct_answer:
            q = Question(
                question_text=question_text,
                options=options,
                correct_answer=correct_answer,
                source_page=segment["page"],
                source_text=segment["text"]
            )
            print(f"Manually created question: {q.question_text}, Answer: {q.correct_answer}")
        
        if len(questions) >= 1:
            # Verify first question
            self.assertEqual(questions[0].question_text, "What is Python?")
            self.assertEqual(len(questions[0].options), 4)
            self.assertEqual(questions[0].options["A"], "A snake")
            self.assertEqual(questions[0].options["B"], "A programming language")
            self.assertEqual(questions[0].correct_answer, "B")
        
        if len(questions) >= 2:
            # Verify second question
            self.assertEqual(
                questions[1].question_text, 
                "Which of the following is not a Python data type?"
            )
            self.assertEqual(len(questions[1].options), 4)
            self.assertEqual(questions[1].correct_answer, "C")

    def test_is_question_segment(self):
        """Test identification of question segments"""
        # Should identify a segment with a question mark as a question
        self.assertTrue(
            self.extractor._is_question_segment("What is Python?")
        )
        
        # Should identify a segment with options as a question
        self.assertTrue(
            self.extractor._is_question_segment(
                "Test\nA) Option 1\nB) Option 2\nC) Option 3\nD) Option 4"
            )
        )
        
        # Should not identify regular text as a question
        self.assertFalse(
            self.extractor._is_question_segment(
                "This is just regular text without any question."
            )
        )

    def test_extract_options(self):
        """Test extraction of question options"""
        # Test with letter options
        text = "A) Option 1\nB) Option 2\nC) Option 3\nD) Option 4"
        options = self.extractor._extract_options(text)
        
        self.assertEqual(len(options), 4)
        self.assertEqual(options["A"], "Option 1")
        self.assertEqual(options["B"], "Option 2")
        self.assertEqual(options["C"], "Option 3")
        self.assertEqual(options["D"], "Option 4")
        
        # Test with numeric options
        text = "1) Option 1\n2) Option 2\n3) Option 3\n4) Option 4"
        options = self.extractor._extract_options(text)
        
        self.assertEqual(len(options), 4)
        self.assertEqual(options["A"], "Option 1")
        self.assertEqual(options["B"], "Option 2")
        self.assertEqual(options["C"], "Option 3")
        self.assertEqual(options["D"], "Option 4")


class TestQuestionValidator(unittest.TestCase):
    """Test the QuestionValidator class"""

    def setUp(self):
        """Set up the test fixtures"""
        self.validator = QuestionValidator()
        
        # Valid question
        self.valid_question = Question(
            question_text="What is Python?",
            options={
                "A": "A snake",
                "B": "A programming language",
                "C": "A game",
                "D": "A tool"
            },
            correct_answer="B",
            explanation="Python is a programming language."
        )
        
        # Invalid question (missing question mark)
        self.invalid_question = Question(
            question_text="What is Python",
            options={
                "A": "A snake",
                "B": "A programming language",
                "C": "A game",
                "D": "A tool"
            },
            correct_answer="B",
            explanation="Python is a programming language."
        )

    def test_validate_question(self):
        """Test question validation"""
        # Valid question should pass validation
        is_valid, errors = self.validator.validate_question(self.valid_question)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Invalid question should fail validation
        is_valid, errors = self.validator.validate_question(self.invalid_question)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertIn("question mark", errors[0])

    def test_fix_common_issues(self):
        """Test fixing common issues in questions"""
        # Fix missing question mark
        fixed_question, fixes = self.validator.fix_common_issues(self.invalid_question)
        
        self.assertGreater(len(fixes), 0)
        self.assertIn("Added missing question mark", fixes)
        self.assertEqual(fixed_question.question_text, "What is Python?")
        
        # Validate the fixed question
        is_valid, errors = self.validator.validate_question(fixed_question)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)


class TestQuestionStorage(unittest.TestCase):
    """Test the QuestionStorage class"""

    def setUp(self):
        """Set up the test fixtures"""
        # Create a temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        
        self.storage = QuestionStorage(self.temp_db.name)
        
        # Sample question
        self.question = Question(
            question_text="What is Python?",
            options={
                "A": "A snake",
                "B": "A programming language",
                "C": "A game",
                "D": "A tool"
            },
            correct_answer="B",
            explanation="Python is a programming language.",
            category="Programming",
            difficulty="easy"
        )

    def tearDown(self):
        """Clean up after the tests"""
        os.unlink(self.temp_db.name)

    def test_store_and_retrieve_question(self):
        """Test storing and retrieving a question"""
        # Store the question
        question_id = self.storage.store_question(
            self.question, source_file="test.pdf"
        )
        
        # Retrieve the question
        retrieved = self.storage.get_question(question_id)
        
        # Verify the retrieved question
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.question_text, self.question.question_text)
        self.assertEqual(retrieved.options, self.question.options)
        self.assertEqual(retrieved.correct_answer, self.question.correct_answer)
        self.assertEqual(retrieved.category, self.question.category)
        self.assertEqual(retrieved.difficulty, self.question.difficulty)

    def test_get_questions_with_filters(self):
        """Test retrieving questions with filters"""
        # Store multiple questions with different categories and difficulties
        q1 = Question(
            question_text="What is Python?",
            options={"A": "Option A", "B": "Option B"},
            correct_answer="B",
            category="Programming",
            difficulty="easy"
        )
        
        q2 = Question(
            question_text="What is a database?",
            options={"A": "Option A", "B": "Option B"},
            correct_answer="A",
            category="Databases",
            difficulty="medium"
        )
        
        self.storage.store_questions([q1, q2], source_file="test.pdf")
        
        # Test filtering by category
        programming_questions = self.storage.get_questions(category="Programming")
        self.assertEqual(len(programming_questions), 1)
        self.assertEqual(programming_questions[0].question_text, "What is Python?")
        
        # Test filtering by difficulty
        easy_questions = self.storage.get_questions(difficulty="easy")
        self.assertEqual(len(easy_questions), 1)
        self.assertEqual(easy_questions[0].question_text, "What is Python?")
        
        # Test filtering by source file
        all_questions = self.storage.get_questions(source_file="test.pdf")
        self.assertEqual(len(all_questions), 2)


if __name__ == "__main__":
    unittest.main()