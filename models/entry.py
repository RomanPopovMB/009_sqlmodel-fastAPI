from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from models.author import Author
from models.category import Category
from pydantic import field_validator

class EntryBase(SQLModel):
    title: str = Field(index=True, unique=True)  # Make title unique and indexed
    content: str
    
    @field_validator("title", mode="before")
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("The title can't be empty.")
        return value
    
    @field_validator("content", mode="before")
    def validate_content(cls, value):
        if not value.strip():
            raise ValueError("The content can't be empty.")
        return value

class Entry(EntryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="author.id")
    author: Optional["Author"] = Relationship(back_populates="entries")
    category_id: int = Field(foreign_key="category.id")
    categories: Optional["Category"] = Relationship(back_populates="entry")

class EntryCreate(EntryBase):
    author_name: str 
    
    @field_validator("author_name", mode="before")
    def validate_author_name(cls, value):
        if not value.strip():
            raise ValueError("The author name can't be empty.")
        return value

class EntryRead(EntryBase):
    id: int
    author: Author
