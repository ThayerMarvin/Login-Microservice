from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auth import handle_login, handle_registration

app = FastAPI(title= "Login")

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

class AuthorizationResponse(BaseModel):
    status: str
    user_id: str | None = None
    session_token: str | None = None
    profile_data: dict | None = None
    error_message: str | None = None

@app.post("/login", response_model=AuthorizationResponse)
def login(request: LoginRequest):
    result = handle_login(request.username, request.password)
    if result["status"] == "failure":
        raise HTTPException(status_code=401, detail=result["error_message"])
    return result

@app.post("/register", response_model=AuthorizationResponse)
def login(request: RegisterRequest):
    result = handle_registration(request.username, request.password)
    if result["status"] == "failure":
        raise HTTPException(status_code=400, detail=result["error_message"])
    return result