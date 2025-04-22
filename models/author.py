from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from pydantic import EmailStr, field_validator

class AuthorBase(SQLModel):
    name: str
    email: EmailStr = Field(index=True, unique=True)  # Use EmailStr for email validation
    
    @field_validator("name", mode="before")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("The name can't be empty.")
        return value

    @field_validator("email", mode="before")
    def validate_email(cls, value):
        if not value.strip():
            raise ValueError("The email can't be empty.")
        return value

class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entries: List["Entry"] = Relationship(back_populates="author")  # type: ignore

class AuthorCreate(AuthorBase):
    pass  # Excluir el campo id para la creación de un nuevo autor
