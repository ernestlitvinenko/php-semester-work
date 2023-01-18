from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr | None
    password: str


class UserSchemaWithoutPWD(BaseModel):
    username: str
    email: EmailStr | None


class AccessToken(BaseModel):
    user_id: str
    access_token: str
