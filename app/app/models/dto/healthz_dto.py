from pydantic import BaseModel


class HealtcheckOutDTO(BaseModel):
    status: int
    message: str
