from itsdangerous import URLSafeSerializer
from fastapi import Request, Response
import re
import unicodedata


SECRET_KEY = "your-secret-key"  # keep this secret and secure

serializer = URLSafeSerializer(SECRET_KEY, salt="flash")

def set_flash(response: Response, message: str):
    cookie_val = serializer.dumps(message)
    response.set_cookie(key="flash", value=cookie_val, max_age=10, httponly=True)

def get_flash(request: Request):
    cookie_val = request.cookies.get("flash")
    if not cookie_val:
        return None
    try:
        message = serializer.loads(cookie_val)
        return message
    except Exception:
        return None

def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)




