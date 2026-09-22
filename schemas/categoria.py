from pydantic import BaseModel, Field
from typing import Optional


class CategoriaSchema(BaseModel):
    id: Optional[int] = None
    nome: str
