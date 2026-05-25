from fastapi import Depends, Header, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.core.exceptions import Unauthorized, Forbidden


def _get_token(request: Request, authorization: str | None = Header(None)) -> str | None:
    if authorization and authorization.startswith("Bearer "):
        return authorization.split(" ")[1]
    cookie = request.cookies.get("access_token")
    if cookie and cookie.startswith("Bearer "):
        return cookie.split(" ")[1]
    return None


def get_current_user(
    request: Request,
    authorization: str | None = Header(None),
    db: Session = Depends(get_db),
) -> User:
    token = _get_token(request, authorization)
    if not token:
        raise Unauthorized("يرجى تسجيل الدخول")
    payload = decode_token(token)
    if payload is None:
        raise Unauthorized("رمز الدخول غير صالح أو منتهي الصلاحية")
    user = db.execute(select(User).where(User.id == int(payload.get("sub")))).scalar_one_or_none()
    if not user or not user.is_active:
        raise Unauthorized("المستخدم غير موجود أو غير نشط")
    return user


def require_role(*roles: str):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise Forbidden("ليس لديك صلاحية للوصول إلى هذه الميزة")
        return current_user
    return role_checker
