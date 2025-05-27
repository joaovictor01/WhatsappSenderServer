from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "joaovictorsp@x.com",
                "fullname": "João Victor",
                "password": "somepassword",
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {"email": "joaovictorsp@x.com", "password": "somepassword"}
        }


class WhatsappLogin(BaseModel):
    phone_number: str = Field(...)
    instance_name: str = Field(...)


class WhatsappMessage(BaseModel):
    message: str = Field(...)
    is_message_base64: bool = Field(default=False)
    sender_number: Optional[str] = ""
    sender_instance: str = Field(...)
    sender_name: Optional[str] = ""
    receiver_number: str = Field(...)
    receiver_name: Optional[str] = ""
    timestamp: Optional[str] = ""
    attachment_path: Optional[str] = ""
    sent: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Mensagem de teste",
                "is_message_base64": False,
                "sender_number": "sender_number",
                "sender_instance": "sender_instance",
                "sender_name": "sender_name",
                "receiver_number": "receiver_number",
                "receiver_instance": "receiver_instance",
                "receiver_name": "receiver_name",
                "timestamp": "timestamp",
                "attachment_path": "path/to/attachment",
                "sent": False,
            }
        }
