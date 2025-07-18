from fastapi import FastAPI, Request, Depends, Form, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session

from . import models, crud, deps, auth, schemas
from .database import engine
from .utils import slugify

app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

# --- Exception Handling ---

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_303_SEE_OTHER:
        return RedirectResponse(url="/login")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# --- Utility Redirect ---

def redirect_login():
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

# --- Home Page ---

@app.get("/", response_class=deps.templates.TemplateResponse)
def read_index(
    request: Request,
    db: Session = Depends(deps.get_db),
    user=Depends(deps.get_current_user),
):
    if not user:
        return redirect_login()
    flash = deps.get_flash(request)
    posts = crud.get_posts(db)
    return deps.templates.TemplateResponse("index.html", {
        "request": request,
        "posts": posts,
        "user": user,
        "flash": flash
    })

# --- Create Post ---

@app.get("/post/create", response_class=deps.templates.TemplateResponse)
def create_form(request: Request, user=Depends(deps.require_user)):
    flash = deps.get_flash(request)
    return deps.templates.TemplateResponse("post_form.html", {
        "request": request,
        "user": user,
        "action": "Create",
        "flash": flash
    })

@app.post("/post/create")
def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(deps.get_db),
    user=Depends(deps.require_user),
):
    post = crud.create_post(db, schemas.PostCreate(title=title, content=content), user.id)
    response = RedirectResponse(f"/post/{post.slug}", status_code=status.HTTP_303_SEE_OTHER)
    deps.set_flash(response, "Post created successfully!")
    return response

# --- Read Post (by slug) ---

@app.get("/post/{slug}", response_class=deps.templates.TemplateResponse)
def read_post(
    slug: str,
    request: Request,
    db: Session = Depends(deps.get_db),
    user=Depends(deps.require_user),
):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    flash = deps.get_flash(request)
    return deps.templates.TemplateResponse("post_detail.html", {
        "request": request,
        "post": post,
        "user": user,
        "flash": flash
    })

# --- Edit Post ---

# Edit form route (GET) with slug
@app.get("/post/{slug}/edit", response_class=deps.templates.TemplateResponse)
def edit_form(
    slug: str,
    request: Request,
    db: Session = Depends(deps.get_db),
    user=Depends(deps.require_user),
):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post or post.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    flash = deps.get_flash(request)
    return deps.templates.TemplateResponse("post_form.html", {
        "request": request,
        "user": user,
        "post": post,
        "action": "Edit",
        "flash": flash
    })


# Edit post (POST) with slug
@app.post("/post/{slug}/edit")
def edit_post(
    slug: str,  # use slug here, matching the path param
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(deps.get_db),
    user=Depends(deps.require_user),
):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post or post.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")

    # Update slug based on new title
    post.slug = slugify(title)

    # Update other fields using your crud.update_post
    crud.update_post(db, post, schemas.PostCreate(title=title, content=content))

    response = RedirectResponse(f"/post/{post.slug}", status_code=status.HTTP_303_SEE_OTHER)
    deps.set_flash(response, "Post updated successfully!")
    return response


# --- Delete Post ---

# Delete post (POST) with slug
@app.post("/post/{slug}/delete")
def delete_post(
    slug: str,
    db: Session = Depends(deps.get_db),
    user=Depends(deps.require_user),
):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post or post.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    crud.delete_post(db, post)
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    deps.set_flash(response, "Post deleted successfully!")
    return response

# --- Authentication ---

@app.get("/login", response_class=deps.templates.TemplateResponse)
def login_form(request: Request):
    flash = deps.get_flash(request)
    return deps.templates.TemplateResponse("login.html", {"request": request, "flash": flash})

@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(deps.get_db),
):
    user = crud.authenticate_user(db, username, password)
    if not user:
        response = RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
        deps.set_flash(response, "Invalid username or password")
        return response

    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user_id", value=str(user.id), httponly=True)
    deps.set_flash(response, "Logged in successfully!")
    return response

@app.get("/register", response_class=deps.templates.TemplateResponse)
def register_form(request: Request):
    flash = deps.get_flash(request)
    return deps.templates.TemplateResponse("register.html", {"request": request, "flash": flash})

@app.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(deps.get_db),
):
    user_exists = crud.get_user_by_username(db, username)
    if user_exists:
        response = RedirectResponse("/register", status_code=status.HTTP_303_SEE_OTHER)
        deps.set_flash(response, "Username already taken")
        return response

    crud.create_user(db, schemas.UserCreate(username=username, password=password))
    response = RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    deps.set_flash(response, "Registration successful. Please log in.")
    return response

@app.post("/logout")
def logout(request: Request, user=Depends(deps.require_user)):
    response = RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("user_id")
    deps.set_flash(response, "Logged out successfully.")
    return response
