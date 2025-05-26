from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr


class CreateUser(BaseUser):
    password: str


class LoginUser(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        from_attributes = True


class UserWithToken(User):
    token: str
