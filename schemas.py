from typing import List

from pydantic import BaseModel, Field

class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superflous: str = Field(description="Critique of what is superfluous.")

class AnswerQuestion(BaseModel):
    """answer the question."""

    answer: str = Field(description="~250 word detailed answer to the question.")
    reflection: Reflection = Field(description="your reflection on the initial answer.")
    search_queries: List[str] = Field(
        description="1-3 search queries for researching imporvements to address the critique fo your current answer."
    )

class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question"""

    references: List[str] = Field(
        description="citations motivation your updated answer."
    )