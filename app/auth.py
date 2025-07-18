# auth.py
from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import crud, schemas, deps
from passlib.hash import bcrypt

router = APIRouter(tags=["auth"])
SESSION_COOKIE = "user_id"

@router.get("/login")
def login_form(request: Request):
    return deps.templates.TemplateResponse("login.html", {"request": request, "msg": None})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(deps.get_db)):
    user = crud.get_user_by_username(db, username)
    if not user or not bcrypt.verify(password, user.hashed_password):
        return deps.templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid credentials"})
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(SESSION_COOKIE, str(user.id), httponly=True)
    return response

@router.get("/register")
def register_form(request: Request):
    return deps.templates.TemplateResponse("register.html", {"request": request, "msg": None})

@router.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(deps.get_db)):
    if crud.get_user_by_username(db, username):
        return deps.templates.TemplateResponse("register.html", {"request": request, "msg": "Username taken"})
    crud.create_user(db, schemas.UserCreate(username=username, password=password))
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie(SESSION_COOKIE)
    return response
