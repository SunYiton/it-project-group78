from typing import List
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class Assignment(BaseModel):
    id: int
    code: str
    title: str
    status: str = Field(description="OPEN|IN_PROGRESS|DONE")

class AssignmentList(BaseModel):
    page: int
    page_size: int
    total: int
    items: List[Assignment]
