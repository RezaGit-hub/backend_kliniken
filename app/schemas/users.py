from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class UserResponse(BaseModel):
    email: EmailStr
    password: str
    role: str

    class Config:
        from_attributes = True