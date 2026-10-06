from pydantic import BaseModel

class LogInSchema(BaseModel):
    message: str
    authorization : str

class NegativeLogIn(BaseModel):
    message: str

