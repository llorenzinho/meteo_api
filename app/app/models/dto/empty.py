from typing import Optional

from pydantic import BaseModel


class EmptyOutDto(BaseModel):
    code: int
    message: Optional[str]
