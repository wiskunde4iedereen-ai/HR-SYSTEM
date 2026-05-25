from pydantic import BaseModel


class ExporterCreate(BaseModel):
    company_name: str
    owner_name: str
    email: str
    phone: str = ""
    commercial_registry: str = ""
    address: str = ""


class ExporterUpdate(BaseModel):
    company_name: str
    owner_name: str
    email: str
    phone: str = ""
    commercial_registry: str = ""
    address: str = ""
