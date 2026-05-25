from pydantic import BaseModel


class DocumentCreate(BaseModel):
    license_id: int
    filename: str
    doc_type: str = ""
