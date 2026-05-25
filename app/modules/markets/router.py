from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.responses import RedirectResponse

from app.core.database import get_db
from app.models.market import Market
from app.modules.auth.deps import require_role
from app.templates import render
from app.core.exceptions import NotFound

router = APIRouter(prefix="/markets", tags=["markets"], dependencies=[Depends(require_role("admin", "employee"))])


@router.get("")
async def list_markets(request: Request, q: str = "", db: Session = Depends(get_db)):
    query = select(Market)
    if q:
        query = query.where(Market.country.ilike(f"%{q}%"))
    markets = db.execute(query.order_by(Market.id.desc())).scalars().all()
    return render("markets/list.html", request=request, markets=markets, q=q, show_nav=True)


@router.get("/create")
async def create_form(request: Request):
    return render("markets/form.html", request=request, market=None, show_nav=True)


@router.post("/create")
async def create(
    country: str = Form(...),
    city: str = Form(""),
    requirements: str = Form(""),
    db: Session = Depends(get_db),
):
    market = Market(country=country, city=city, requirements=requirements)
    db.add(market)
    db.commit()
    return RedirectResponse(url="/markets", status_code=302)


@router.get("/{market_id}/edit")
async def edit_form(market_id: int, request: Request, db: Session = Depends(get_db)):
    market = db.execute(select(Market).where(Market.id == market_id)).scalar_one_or_none()
    if not market:
        raise NotFound("السوق غير موجود")
    return render("markets/form.html", request=request, market=market, show_nav=True)


@router.post("/{market_id}/edit")
async def edit(
    market_id: int,
    country: str = Form(...),
    city: str = Form(""),
    requirements: str = Form(""),
    db: Session = Depends(get_db),
):
    market = db.execute(select(Market).where(Market.id == market_id)).scalar_one_or_none()
    if not market:
        raise NotFound("السوق غير موجود")
    market.country = country
    market.city = city
    market.requirements = requirements
    db.commit()
    return RedirectResponse(url="/markets", status_code=302)


@router.post("/{market_id}/delete")
async def delete(market_id: int, db: Session = Depends(get_db)):
    market = db.execute(select(Market).where(Market.id == market_id)).scalar_one_or_none()
    if not market:
        raise NotFound("السوق غير موجود")
    db.delete(market)
    db.commit()
    return RedirectResponse(url="/markets", status_code=302)
