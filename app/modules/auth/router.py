from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.responses import RedirectResponse

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import Conflict, Unauthorized, BadRequest
from app.models.user import User
from app.modules.auth.deps import get_current_user
from app.templates import render

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise Unauthorized("البريد الإلكتروني أو كلمة المرور غير صحيحة")
    if not user.is_active:
        raise Unauthorized("الحساب غير نشط")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True, max_age=28800)
    return response


@router.get("/login")
async def login_page(request: Request):
    return render("auth/login.html", request=request, show_nav=False)


@router.get("/register")
async def register_page(request: Request):
    return render("auth/register.html", request=request, show_nav=False)


@router.post("/register")
async def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    if len(password) < 6:
        raise BadRequest("كلمة المرور يجب أن تكون 6 أحرف على الأقل")
    existing = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if existing:
        raise Conflict("البريد الإلكتروني مستخدم بالفعل")
    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role="exporter",
    )
    db.add(user)
    db.commit()
    token = create_access_token({"sub": str(user.id), "role": user.role})
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True, max_age=28800)
    return response


@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie("access_token")
    return response


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
    }
