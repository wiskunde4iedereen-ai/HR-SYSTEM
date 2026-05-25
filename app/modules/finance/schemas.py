from pydantic import BaseModel


class FinanceCreate(BaseModel):
    license_id: int
    exporter_id: int
    amount: float
    fee_type: str = ""
