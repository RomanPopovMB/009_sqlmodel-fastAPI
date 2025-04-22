from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from pydantic import field_validator

class CategoryBase(SQLModel):
    name: str = Field(index=True, unique=True)  # Make name unique and indexed
    description: str
    
    @field_validator("name", mode="before")
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("The name can't be empty.")
        return value

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entry: Optional["Entry"] = Relationship(back_populates="categories") 

class CategoryCreate(CategoryBase):
    category_name: str 
    
    @field_validator("category_name", mode="before")
    def validate_author_name(cls, value):
        if not value.strip():
            raise ValueError("The category name can't be empty.")
        return value

class CategoryRead(CategoryBase):
    id: int
