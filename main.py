from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auth import authenticate_user

app = FastAPI(title= "Login")

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    status: str
    user_id: str | None = None
    session_token: str | None = None
    profile_data: dict | None = None
    error_message: str | None = None

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    result = authenticate_user(request.username, request.password)
    
    if result["status"] == "failure":
        raise HTTPException(status_code=401, detail=result["error_message"])
    
    return result  