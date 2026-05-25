import csv
import io
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from fastapi.responses import StreamingResponse

from app.core.database import get_db
from app.models.license import License
from app.models.finance import Finance
from app.models.exporter import Exporter
from app.models.product import Product
from app.models.market import Market
from app.modules.auth.deps import require_role
from app.templates import render

router = APIRouter(prefix="/reports", tags=["reports"],
                   dependencies=[Depends(require_role("admin", "employee"))])


@router.get("")
async def reports_page(request: Request, db: Session = Depends(get_db)):
    total_exporters = db.query(func.count(Exporter.id)).scalar()
    total_products = db.query(func.count(Product.id)).scalar()
    total_licenses = db.query(func.count(License.id)).scalar()
    pending_licenses = db.query(func.count(License.id)).where(License.status == "pending").scalar()
    approved_licenses = db.query(func.count(License.id)).where(License.status == "approved").scalar()
    total_fees = db.query(func.coalesce(func.sum(Finance.amount), 0)).scalar()
    paid_fees = db.query(func.coalesce(func.sum(Finance.amount), 0)).where(Finance.status == "paid").scalar()

    return render("reports/index.html", request=request, show_nav=True,
                  total_exporters=total_exporters,
                  total_products=total_products,
                  total_licenses=total_licenses,
                  pending_licenses=pending_licenses,
                  approved_licenses=approved_licenses,
                  total_fees=total_fees,
                  paid_fees=paid_fees)


@router.get("/export/csv")
async def export_csv(
    entity: str = Query("licenses"),
    db: Session = Depends(get_db),
):
    output = io.StringIO()
    writer = csv.writer(output)

    if entity == "licenses":
        writer.writerow(["ID", "المنتج", "المصدر", "السوق", "الحالة", "تاريخ الإنشاء", "تاريخ الاعتماد"])
        rows = db.execute(
            select(License).order_by(License.id.desc())
        ).scalars().all()
        for r in rows:
            writer.writerow([r.id, r.product_id, r.exporter_id, r.market_id, r.status,
                           r.created_at.strftime("%Y-%m-%d") if r.created_at else "",
                           r.approved_at.strftime("%Y-%m-%d") if r.approved_at else ""])

    elif entity == "finance":
        writer.writerow(["ID", "الترخيص", "المصدر", "المبلغ", "نوع الرسوم", "الحالة", "تاريخ الإنشاء", "تاريخ الدفع"])
        rows = db.execute(
            select(Finance).order_by(Finance.id.desc())
        ).scalars().all()
        for r in rows:
            writer.writerow([r.id, r.license_id, r.exporter_id, r.amount, r.fee_type, r.status,
                           r.created_at.strftime("%Y-%m-%d") if r.created_at else "",
                           r.paid_at.strftime("%Y-%m-%d") if r.paid_at else ""])

    elif entity == "exporters":
        writer.writerow(["ID", "الشركة", "المالك", "البريد", "الهاتف", "السجل التجاري", "العنوان"])
        rows = db.execute(select(Exporter).order_by(Exporter.id.desc())).scalars().all()
        for r in rows:
            writer.writerow([r.id, r.company_name, r.owner_name, r.email, r.phone, r.commercial_registry, r.address])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={entity}.csv"},
    )
