import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.login_schema import LoginCredentials, LoginResponse

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=LoginResponse, status_code=200)
def login(login_cred: LoginCredentials):
    if login_cred.username != "admin" or login_cred.password != "password123":
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    return LoginResponse(token=str(uuid.uuid4()))
