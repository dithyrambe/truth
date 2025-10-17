from pydantic import BaseModel


class Status(BaseModel):
    id: str
    created_at: str
    uri: str
    content: str
