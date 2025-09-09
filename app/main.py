import os
from typing import Optional, List
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from .schemas import LoginRequest, LoginResponse, AssignmentList
from .mock_data import ASSIGNMENTS
from .auth import create_token, auth_required

app = FastAPI(title="AMT Mock API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    role = "COORDINATOR" if payload.email.endswith("@deakin.edu.au") else "MARKER"
    token = create_token(sub=payload.email, role=role)
    return LoginResponse(access_token=token, role=role)

@app.get("/assignments", response_model=AssignmentList)
def list_assignments(
    status: Optional[str] = Query(None, description="OPEN|IN_PROGRESS|DONE"),
    page: int = 1,
    page_size: int = 10,
):
    items = [a for a in ASSIGNMENTS if (status is None or a.status == status)]
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return AssignmentList(page=page, page_size=page_size, total=total, items=items[start:end])

@app.get("/secure/ping")
def secure_ping(user=Depends(auth_required)):
    return {"ok": True, "user": {"email": user["sub"], "role": user["role"]}}
