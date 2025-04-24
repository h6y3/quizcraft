"""Prompt engineering and construction for AI models."""

import logging

from .tokens import estimate_token_count, optimize_context

from typing import Dict

logger = logging.getLogger(__name__)


class PromptTemplate:
    """Base class for prompt templates with token optimization."""

    def __init__(self, system_prompt: str, user_prompt_template: str):
        """
        Initialize the prompt template.

        Args:
            system_prompt: System prompt text
            user_prompt_template: User prompt template with placeholders
        """
        self.system_prompt = system_prompt
        self.user_prompt_template = user_prompt_template

    def construct(self, context: str, **kwargs) -> Dict[str, str]:
        """
        Construct a prompt with token optimization.

        Args:
            context: The document or text context
            **kwargs: Variables to substitute in the template

        Returns:
            Dictionary with system and user prompts
        """
        # Optimize context to fit within token limits
        optimized_context = optimize_context(context)

        # Format the user prompt template with provided variables
        user_prompt = self.user_prompt_template.format(
            context=optimized_context, **kwargs
        )

        # Log token usage
        system_tokens = estimate_token_count(self.system_prompt)
        user_tokens = estimate_token_count(user_prompt)
        logger.info(
            f"Prompt token estimate: {system_tokens + user_tokens} tokens "
            f"(System: {system_tokens}, User: {user_tokens})"
        )

        return {
            "system_prompt": self.system_prompt,
            "user_prompt": user_prompt,
        }


class QuestionGenerationPrompt(PromptTemplate):
    """Prompt template for question generation."""

    def __init__(self):
        """Initialize the question generation prompt template."""
        system_prompt = (
            "You are an expert educational content creator who specializes "
            "in creating high-quality multiple-choice questions. Create "
            "questions that test both factual recall and deeper "
            "understanding. Each question should be challenging but fair."
        )

        user_prompt_template = """
Create {num_questions} multiple-choice questions based on the following 
educational content. The questions should be at {difficulty} difficulty level.

For each question:
1. Write a clear question that tests understanding
2. Provide 4 possible answers (A, B, C, D)
3. Indicate the correct answer
4. Include a brief explanation of why the answer is correct

Please format your response as valid JSON with this structure:
```json
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": {{
        "A": "First option",
        "B": "Second option",
        "C": "Third option",
        "D": "Fourth option"
      }},
      "correct_answer": "A",
      "explanation": "Explanation of why A is correct"
    }}
  ]
}}
```

Here is the content to base the questions on:

{context}
"""

        super().__init__(system_prompt, user_prompt_template)


# Export specific prompt templates
question_generation_prompt = QuestionGenerationPrompt()
