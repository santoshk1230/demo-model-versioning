from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class Input(BaseModel):
    email: Optional[EmailStr] = None
    phone: constr(min_length=10, max_length=10)
    name: Optional[str] = None


class DsScoreCalculator(BaseModel):
    response: dict
    m_version: str
    client_name: str
    input: Input