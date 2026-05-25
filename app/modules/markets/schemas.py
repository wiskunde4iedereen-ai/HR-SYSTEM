from pydantic import BaseModel


class MarketCreate(BaseModel):
    country: str
    city: str = ""
    requirements: str = ""
