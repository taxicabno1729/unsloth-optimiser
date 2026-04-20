from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    username: str
    email: str
    full_name: str | None = None
    disabled: bool | None = None
