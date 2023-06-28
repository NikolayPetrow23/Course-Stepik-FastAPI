from pydantic import BaseModel, EmailStr


class SUserRegisterOrAuth(BaseModel):
    email: EmailStr
    password: str
