from pydantic import BaseModel

class Chat(BaseModel):
    message: str
    to: str