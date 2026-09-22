from pydantic import BaseModel, Field
from typing import Optional


class ProdutoSchema(BaseModel):
    nome: str
    codigo_barras: Optional[str] = None
    marca: Optional[str] = None
    categoria_id: int
    tipo_pet: Optional[str] = None
    unidade_venda: Optional[str] = None
    lote: Optional[str] = None
    estoque_atual: Optional[int] = 0
    estoque_minimo: Optional[int] = 0
    custo_aquisicao: Optional[float] = 0.0
    preco_venda: Optional[float] = 0.0
    data_entrada: Optional[str] = None
    data_validade: Optional[str] = None


class ProdutoViewSchema(BaseModel):
    id: int
    nome: str
    codigo_barras: Optional[str] = None
    marca: Optional[str] = None
    categoria_id: int
    categoria_nome: Optional[str] = None
    tipo_pet: Optional[str] = None
    unidade_venda: Optional[str] = None
    lote: Optional[str] = None
    estoque_atual: Optional[int] = 0
    estoque_minimo: Optional[int] = 0
    custo_aquisicao: Optional[float] = 0.0
    preco_venda: Optional[float] = 0.0
    data_entrada: Optional[str] = None
    data_validade: Optional[str] = None


class ProdutoUpdateSchema(BaseModel):
    nome: Optional[str] = None
    codigo_barras: Optional[str] = None
    marca: Optional[str] = None
    categoria_id: Optional[int] = None
    tipo_pet: Optional[str] = None
    unidade_venda: Optional[str] = None
    lote: Optional[str] = None
    estoque_atual: Optional[int] = None
    estoque_minimo: Optional[int] = None
    custo_aquisicao: Optional[float] = None
    preco_venda: Optional[float] = None
    data_entrada: Optional[str] = None
    data_validade: Optional[str] = None
