from pydantic import BaseModel, EmailStr
from typing import Optional


class ContactFormRequest(BaseModel):
    user_name: str
    user_email: EmailStr
    message_content: str


class ContactFormResponse(BaseModel):
    success: bool
    message: str
    classification: str
    routed_to: str
    timestamp: str
    request_id: str