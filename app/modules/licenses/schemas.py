from pydantic import BaseModel


class LicenseCreate(BaseModel):
    product_id: int
    exporter_id: int
    market_id: int
    notes: str = ""
