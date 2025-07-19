# 📝 FastAPI Blog App with Server-Side HTML Rendering

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](#)

A full-featured blog application built with **FastAPI**, **Jinja2**, and **SQLAlchemy**. Supports server-side HTML rendering, user authentication, flash messaging, and full CRUD functionality — all with clean modular code and session-based route protection.

---

## 🚀 Features

- 🔐 User registration, login, and logout
- ⚡ Session-based authentication using secure cookies
- 💬 Flash messages for user feedback
- 📝 Create, Read, Update, Delete (CRUD) blog posts
- 🔗 Slug generation for posts
- 🧰 FastAPI + Jinja2 HTML templating
- 🧱 SQLite database (easy to swap out)
- 🛡️ Protected routes (dashboard, create post, etc.)
- 🗃️ Clean, modular architecture (auth, crud, schemas, models)
- 🚀 Deployable on **Render**, **Heroku**, or **any ASGI server**

---

## 🧰 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: SQLAlchemy
- **Templates**: Jinja2
- **Schema Validation**: Pydantic
- **Database**: SQLite (can be upgraded to PostgreSQL/MySQL)
- **Web Server**: Uvicorn

---

## 📁 Project Structure

```
fastapi-html/
├── app/
│   ├── auth.py           # Auth routes (register, login, logout)
│   ├── crud.py           # Post/user CRUD logic
│   ├── database.py       # SQLAlchemy DB connection
│   ├── deps.py           # Dependency overrides and helpers
│   ├── main.py           # App entry point
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── templates/        # HTML templates
│   └── utils.py          # Flash messaging & helpers
├── blog_app.db           # SQLite DB file
├── requirements.txt      # Python dependencies
├── render.yml            # Render deployment config
└── README.md             # You're reading it!
```

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/shahidmalik4/fastapi-html.git
cd fastapi-html

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

---

## 🔐 Auth Flow

- `/register`: Register new user
- `/login`: Login page (sets session)
- `/logout`: Logout and clear session
- Routes like `/dashboard` and `/create-post` are protected and require login

---

## 🧑‍💻 CRUD Endpoints

| Route              | Method | Auth Required | Description              |
|-------------------|--------|---------------|--------------------------|
| `/register`       | GET/POST | ❌           | Register a new user      |
| `/login`          | GET/POST | ❌           | Login with credentials   |
| `/logout`         | GET     | ✅            | Logout user              |
| `/dashboard`      | GET     | ✅            | View user dashboard      |
| `/create-post`    | GET/POST | ✅           | Create a new post        |
| `/edit-post/{id}` | GET/POST | ✅           | Edit an existing post    |
| `/delete-post/{id}`| GET     | ✅           | Delete a post            |
| `/post/{slug}`    | GET     | ✅           | View a single post       |

---

## 🧾 Models & Schemas

### 🧍 User (SQLAlchemy)
- `id: int`
- `username: str`
- `hashed_password: str`

### 📝 Post (SQLAlchemy)
- `id: int`
- `title: str`
- `content: str`
- `slug: str`
- `owner_id: int`

### 📦 Pydantic Schemas

```python
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    slug: Optional[str] = None

class PostOut(PostBase):
    id: int
    slug: str
    class Config:
        orm_mode = True
```

---

## ⚙️ Environment Variables

Create a `.env` file (or configure environment manually):

```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./blog_app.db
```

---

## 💬 Flash Messages

Implemented using custom middleware and session cookies. You’ll see success or error messages after login, logout, and form actions.

---

## 🧪 Testing

Coming soon. You can use [TestClient](https://fastapi.tiangolo.com/tutorial/testing/) from FastAPI and Pytest for full test coverage.

---

## 📤 Deployment (Render Example)

`render.yml` already included for Render deployment.

> You can also deploy using Docker, Heroku, or any ASGI-compatible cloud.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/feature-name`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/feature-name`)
5. Create a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Shahid

Permission is hereby granted, free of charge, to any person obtaining a copy...
```

> Full license text is in [LICENSE](./LICENSE)

---

## 👤 Author

**Shahid Malik**  
📬 [@shahidmalik4](https://github.com/shahidmalik4)

---

## 🙋‍♂️ Questions or Suggestions?

Open an [issue](https://github.com/shahidmalik4/fastapi-html/issues) or start a discussion.

---
