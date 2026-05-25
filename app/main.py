import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.core.database import engine, SessionLocal, Base, get_db
from sqlalchemy.orm import Session
from app.core.logging_config import setup_logging, get_logger
from app.core.config import get_settings
from app.core.security import hash_password
from app.modules.auth.deps import get_current_user
from app.modules.auth.router import router as auth_router
from app.models.user import User
from app.templates import render
from app.core.database import init_db
from app.modules.exporters.router import router as exporters_router
from app.modules.products.router import router as products_router
from app.modules.markets.router import router as markets_router
from app.modules.licenses.router import router as licenses_router
from app.modules.finance.router import router as finance_router
from app.modules.documents.router import router as documents_router
from app.modules.reports.router import router as reports_router
from app.models.exporter import Exporter
from app.models.product import Product
from app.models.market import Market
from app.models.license import License
from app.models.finance import Finance
from app.models.document import Document
from sqlalchemy import func

# Initialize database tables (must be after all model imports)
init_db()

# Seed admin user
seed_db = SessionLocal()
if not seed_db.execute(select(User).where(User.email == "admin@heya.gov.sy")).scalar_one_or_none():
    seed_db.add(User(name="مدير النظام", email="admin@heya.gov.sy", hashed_password=hash_password("admin123"), role="admin"))
    seed_db.commit()
seed_db.close()

setup_logging()
logger = get_logger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting_up", database_url=get_settings().database_url)
    yield
    logger.info("shutting_down")


app = FastAPI(title="نظام الهيئة", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

app.include_router(auth_router)
app.include_router(exporters_router)
app.include_router(products_router)
app.include_router(markets_router)
app.include_router(licenses_router)
app.include_router(finance_router)
app.include_router(documents_router)
app.include_router(reports_router)


@app.get("/")
async def root():
    return RedirectResponse(url="/auth/login")


@app.get("/dashboard")
async def dashboard(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stats = {
        "exporters_count": db.query(func.count(Exporter.id)).scalar(),
        "products_count": db.query(func.count(Product.id)).scalar(),
        "markets_count": db.query(func.count(Market.id)).scalar(),
        "licenses_count": db.query(func.count(License.id)).scalar(),
        "finance_count": db.query(func.count(Finance.id)).scalar(),
        "documents_count": db.query(func.count(Document.id)).scalar(),
    }
    if current_user.role == "employee":
        return render("dashboard/employee.html", request=request, user=current_user, show_nav=True, stats=stats)
    return render("dashboard/index.html", request=request, user=current_user, show_nav=True, stats=stats)
