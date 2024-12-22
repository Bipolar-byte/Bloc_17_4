from pydantic import BaseModel, Field
from typing import Optional

class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int = Field(..., ge=0, description="Age must be non-negative")

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "firstname": "John",
                "lastname": "Doe",
                "age": 30
            }
        }

class UpdateUser(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, description="Age must be non-negative")

    class Config:
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe",
                "age": 31
            }
        }

class CreateTask(BaseModel):
    title: str
    content: str
    priority: int = Field(..., ge=1, le=5, description="Priority must be between 1 and 5")

    class Config:
        schema_extra = {
            "example": {
                "title": "Complete project",
                "content": "Finish the FastAPI project by the deadline.",
                "priority": 3
            }
        }

class UpdateTask(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5, description="Priority must be between 1 and 5")

    class Config:
        schema_extra = {
            "example": {
                "title": "Update project",
                "content": "Refactor the FastAPI project for better performance.",
                "priority": 4
            }
        }
