from fastapi import Depends, Request, Response, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from itsdangerous import URLSafeSerializer

from .database import SessionLocal
from .models import User

templates = Jinja2Templates(directory="app/templates")

SECRET_KEY = "your-secret-key"
serializer = URLSafeSerializer(SECRET_KEY, salt="flash")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    user_id = request.cookies.get("user_id")
    if not user_id:
        return None
    return db.query(User).get(int(user_id))

def require_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    user = get_current_user(request, db)
    if user is None:
        # Redirect to login if no user found
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail="Not authenticated")
    return user

def set_flash(response: Response, message: str) -> None:
    cookie_val = serializer.dumps(message)
    response.set_cookie(key="flash", value=cookie_val, max_age=10, httponly=True)

def get_flash(request: Request) -> str | None:
    cookie_val = request.cookies.get("flash")
    if not cookie_val:
        return None
    try:
        return serializer.loads(cookie_val)
    except Exception:
        return None
