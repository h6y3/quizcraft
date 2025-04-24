"""
Storage module for questions using SQLite database
"""

import json
import os
import sqlite3
from typing import Dict, List, Any, Optional, Tuple

from .models import Question, QuestionSet


class QuestionStorage:
    """Stores and retrieves questions using a SQLite database"""

    def __init__(self, db_path: str):
        """
        Initialize the question storage

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database schema if it doesn't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create questions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                options TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                explanation TEXT,
                source_page INTEGER,
                source_text TEXT,
                difficulty TEXT,
                category TEXT,
                source_file TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Create index for faster searches
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_questions_category
            ON questions(category)
            """
        )

        conn.commit()
        conn.close()

    def store_question(self, question: Question, source_file: Optional[str] = None) -> int:
        """
        Store a single question in the database

        Args:
            question: Question object to store
            source_file: Source file the question was extracted from

        Returns:
            ID of the stored question
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO questions (
                question_text, options, correct_answer, explanation,
                source_page, source_text, difficulty, category, source_file
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                question.question_text,
                json.dumps(question.options),
                question.correct_answer,
                question.explanation,
                question.source_page,
                question.source_text,
                question.difficulty,
                question.category,
                source_file,
            ),
        )

        question_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return question_id

    def store_questions(
        self, questions: List[Question], source_file: Optional[str] = None
    ) -> List[int]:
        """
        Store multiple questions in the database

        Args:
            questions: List of Question objects to store
            source_file: Source file the questions were extracted from

        Returns:
            List of IDs of the stored questions
        """
        question_ids = []
        conn = sqlite3.connect(self.db_path)
        
        try:
            conn.execute("BEGIN TRANSACTION")
            cursor = conn.cursor()
            
            for question in questions:
                cursor.execute(
                    """
                    INSERT INTO questions (
                        question_text, options, correct_answer, explanation,
                        source_page, source_text, difficulty, category, source_file
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        question.question_text,
                        json.dumps(question.options),
                        question.correct_answer,
                        question.explanation,
                        question.source_page,
                        question.source_text,
                        question.difficulty,
                        question.category,
                        source_file,
                    ),
                )
                question_ids.append(cursor.lastrowid)
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
        
        return question_ids

    def get_question(self, question_id: int) -> Optional[Question]:
        """
        Retrieve a question by ID

        Args:
            question_id: ID of the question to retrieve

        Returns:
            Question object or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                question_text, options, correct_answer, explanation,
                source_page, source_text, difficulty, category
            FROM questions
            WHERE id = ?
            """,
            (question_id,),
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return Question(
            question_text=row[0],
            options=json.loads(row[1]),
            correct_answer=row[2],
            explanation=row[3],
            source_page=row[4],
            source_text=row[5],
            difficulty=row[6],
            category=row[7],
        )

    def get_questions(
        self,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        source_file: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Question]:
        """
        Retrieve questions with optional filtering

        Args:
            category: Filter by category
            difficulty: Filter by difficulty
            source_file: Filter by source file
            limit: Maximum number of questions to retrieve

        Returns:
            List of Question objects
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = """
            SELECT
                question_text, options, correct_answer, explanation,
                source_page, source_text, difficulty, category
            FROM questions
            WHERE 1=1
        """
        params = []

        if category:
            query += " AND category = ?"
            params.append(category)

        if difficulty:
            query += " AND difficulty = ?"
            params.append(difficulty)

        if source_file:
            query += " AND source_file = ?"
            params.append(source_file)

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        questions = []
        for row in rows:
            questions.append(
                Question(
                    question_text=row[0],
                    options=json.loads(row[1]),
                    correct_answer=row[2],
                    explanation=row[3],
                    source_page=row[4],
                    source_text=row[5],
                    difficulty=row[6],
                    category=row[7],
                )
            )

        return questions

    def delete_question(self, question_id: int) -> bool:
        """
        Delete a question by ID

        Args:
            question_id: ID of the question to delete

        Returns:
            True if the question was deleted, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return deleted

    def count_questions(
        self,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        source_file: Optional[str] = None,
    ) -> int:
        """
        Count questions with optional filtering

        Args:
            category: Filter by category
            difficulty: Filter by difficulty
            source_file: Filter by source file

        Returns:
            Number of matching questions
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM questions WHERE 1=1"
        params = []

        if category:
            query += " AND category = ?"
            params.append(category)

        if difficulty:
            query += " AND difficulty = ?"
            params.append(difficulty)

        if source_file:
            query += " AND source_file = ?"
            params.append(source_file)

        cursor.execute(query, params)
        count = cursor.fetchone()[0]

        conn.close()
        return count