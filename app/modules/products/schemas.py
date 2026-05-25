from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    category: str = ""
    hs_code: str = ""
    origin: str = ""
    unit: str = ""
    exporter_id: int
