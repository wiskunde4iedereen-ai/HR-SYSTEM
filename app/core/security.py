from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import bcrypt
from app.core.config import get_settings

ROLES = ["admin", "employee", "exporter", "importer"]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=get_settings().access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_settings().secret_key, algorithm=get_settings().algorithm)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, get_settings().secret_key, algorithms=[get_settings().algorithm])
    except JWTError:
        return None
