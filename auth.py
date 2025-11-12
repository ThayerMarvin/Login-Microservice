import uuid
import hashlib
from database import load_users, save_users

def hash_password(password: str):
    """Securely hash the user's password."""
    return hashlib.sha256(password.encode()).hexdigest()

def handle_login(username: str, password: str):
    users_db = load_users()
    hashed_pwd = hash_password(password)
    user = users_db.get(username)

    if not user:
        return {"status": "failure", "error_message": "User does not exist."}

    if user["password_hash"] != hashed_pwd:
        return {"status": "failure", "error_message": "Invalid password."}

    return {
        "status": "success",
        "user_id": user["user_id"],
        "session_token": str(uuid.uuid4()),
        "profile_data": user["profile_data"]
    }

def handle_registration(username: str, password: str):
    users_db = load_users()

    if username in users_db:
        return {"status": "failure", "error_message": "Username already exists."}

    if len(password) < 8:
        return {"status": "failure", "error_message": "Password must be at least 8 characters long."}

    user_id = f"u{len(users_db)+1:03d}"
    hashed_pwd = hash_password(password)

    users_db[username] = {
        "user_id": user_id,
        "password_hash": hashed_pwd,
        "profile_data": {"theme": "default", "language": "en"}
    }

    save_users(users_db)

    return {
        "status": "success",
        "user_id": user_id,
        "session_token": str(uuid.uuid4()),
        "profile_data": users_db[username]["profile_data"]
    }