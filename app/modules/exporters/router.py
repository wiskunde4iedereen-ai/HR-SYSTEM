from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.responses import RedirectResponse

from app.core.database import get_db
from app.models.exporter import Exporter
from app.modules.auth.deps import get_current_user, require_role
from app.models.user import User
from app.templates import render
from app.core.exceptions import NotFound, Conflict

router = APIRouter(prefix="/exporters", tags=["exporters"], dependencies=[Depends(require_role("admin", "employee"))])


@router.get("")
async def list_exporters(request: Request, q: str = "", db: Session = Depends(get_db)):
    query = select(Exporter)
    if q:
        query = query.where(Exporter.company_name.ilike(f"%{q}%"))
    exporters = db.execute(query.order_by(Exporter.id.desc())).scalars().all()
    return render("exporters/list.html", request=request, exporters=exporters, q=q, show_nav=True)


@router.get("/create")
async def create_form(request: Request):
    return render("exporters/form.html", request=request, exporter=None, show_nav=True)


@router.post("/create")
async def create(
    request: Request,
    company_name: str = Form(...),
    owner_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    commercial_registry: str = Form(""),
    address: str = Form(""),
    db: Session = Depends(get_db),
):
    existing = db.execute(select(Exporter).where(Exporter.email == email)).scalar_one_or_none()
    if existing:
        raise Conflict("البريد الإلكتروني مستخدم بالفعل")
    exporter = Exporter(company_name=company_name, owner_name=owner_name, email=email, phone=phone, commercial_registry=commercial_registry, address=address)
    db.add(exporter)
    db.commit()
    return RedirectResponse(url="/exporters", status_code=302)


@router.get("/{exporter_id}/edit")
async def edit_form(exporter_id: int, request: Request, db: Session = Depends(get_db)):
    exporter = db.execute(select(Exporter).where(Exporter.id == exporter_id)).scalar_one_or_none()
    if not exporter:
        raise NotFound("المصدر غير موجود")
    return render("exporters/form.html", request=request, exporter=exporter, show_nav=True)


@router.post("/{exporter_id}/edit")
async def edit(
    exporter_id: int,
    company_name: str = Form(...),
    owner_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    commercial_registry: str = Form(""),
    address: str = Form(""),
    db: Session = Depends(get_db),
):
    exporter = db.execute(select(Exporter).where(Exporter.id == exporter_id)).scalar_one_or_none()
    if not exporter:
        raise NotFound("المصدر غير موجود")
    dup = db.execute(select(Exporter).where(Exporter.email == email, Exporter.id != exporter_id)).scalar_one_or_none()
    if dup:
        raise Conflict("البريد الإلكتروني مستخدم بالفعل")
    exporter.company_name = company_name
    exporter.owner_name = owner_name
    exporter.email = email
    exporter.phone = phone
    exporter.commercial_registry = commercial_registry
    exporter.address = address
    db.commit()
    return RedirectResponse(url="/exporters", status_code=302)


@router.post("/{exporter_id}/delete")
async def delete(exporter_id: int, db: Session = Depends(get_db)):
    exporter = db.execute(select(Exporter).where(Exporter.id == exporter_id)).scalar_one_or_none()
    if not exporter:
        raise NotFound("المصدر غير موجود")
    db.delete(exporter)
    db.commit()
    return RedirectResponse(url="/exporters", status_code=302)
