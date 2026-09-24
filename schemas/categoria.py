from typing import List

from pydantic import BaseModel, RootModel


class CategoriaSchema(BaseModel):
    """Categoria retornada pela API."""
    id: int
    nome: str


class CategoriaListSchema(RootModel[List[CategoriaSchema]]):
    """Lista de categorias."""
