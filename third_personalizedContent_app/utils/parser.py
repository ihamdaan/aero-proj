from pydantic import BaseModel, Field
from typing import List, Optional
import re, json, logging

class ContentItem(BaseModel):
    title: str = Field(..., description="Title of the content")
    description: str = Field(..., description="Description or prompt")
    word_length: Optional[int] = Field(None, description="Desired word length")

class PersonalizedContent(BaseModel):
    title: str
    content: str
    word_count_doc: int = Field(..., description="Actual word count of the generated content")
