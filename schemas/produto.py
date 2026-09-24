from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, RootModel, field_validator, model_validator


def _normalizar_data(valor: Optional[str]) -> Optional[str]:
    """Aceita None/vazio ou uma data ISO (AAAA-MM-DD); caso contrário, rejeita."""
    if valor is None or valor == "":
        return None
    try:
        date.fromisoformat(valor)
    except ValueError:
        raise ValueError("Data inválida. Use o formato AAAA-MM-DD.")
    return valor


def datas_coerentes(data_entrada: Optional[str], data_validade: Optional[str]) -> bool:
    """A validade não pode ser anterior à data de entrada."""
    if data_entrada and data_validade:
        return date.fromisoformat(data_validade) >= date.fromisoformat(data_entrada)
    return True


MENSAGEM_DATAS = "A data de validade não pode ser anterior à data de entrada."


class ProdutoSchema(BaseModel):
    """Corpo de requisição para cadastrar um produto."""
    nome: str = Field(..., min_length=1, max_length=200, description="Nome do produto")
    codigo_barras: Optional[str] = Field(None, max_length=50, description="Código de barras")
    marca: Optional[str] = Field(None, max_length=100)
    categoria_id: int = Field(..., description="ID de uma categoria existente")
    tipo_pet: Optional[str] = Field(None, max_length=50, description="Ex.: Cães, Gatos, Aves")
    unidade_venda: Optional[str] = Field(None, max_length=10, description="Ex.: UN, KG, L, PCT")
    lote: Optional[str] = Field(None, max_length=50)
    estoque_atual: Optional[int] = Field(0, ge=0)
    estoque_minimo: Optional[int] = Field(0, ge=0)
    custo_aquisicao: Optional[float] = Field(0.0, ge=0)
    preco_venda: Optional[float] = Field(0.0, ge=0)
    data_entrada: Optional[str] = Field(None, description="AAAA-MM-DD")
    data_validade: Optional[str] = Field(None, description="AAAA-MM-DD")

    _datas = field_validator("data_entrada", "data_validade")(_normalizar_data)

    @model_validator(mode="after")
    def _validar_periodo(self):
        if not datas_coerentes(self.data_entrada, self.data_validade):
            raise ValueError(MENSAGEM_DATAS)
        return self


class ProdutoUpdateSchema(BaseModel):
    """Corpo de requisição para atualização parcial: envie apenas os campos a alterar."""
    nome: Optional[str] = Field(None, min_length=1, max_length=200)
    codigo_barras: Optional[str] = Field(None, max_length=50)
    marca: Optional[str] = Field(None, max_length=100)
    categoria_id: Optional[int] = None
    tipo_pet: Optional[str] = Field(None, max_length=50)
    unidade_venda: Optional[str] = Field(None, max_length=10)
    lote: Optional[str] = Field(None, max_length=50)
    estoque_atual: Optional[int] = Field(None, ge=0)
    estoque_minimo: Optional[int] = Field(None, ge=0)
    custo_aquisicao: Optional[float] = Field(None, ge=0)
    preco_venda: Optional[float] = Field(None, ge=0)
    data_entrada: Optional[str] = Field(None, description="AAAA-MM-DD")
    data_validade: Optional[str] = Field(None, description="AAAA-MM-DD")

    _datas = field_validator("data_entrada", "data_validade")(_normalizar_data)


class ProdutoViewSchema(BaseModel):
    """Produto retornado pela API."""
    id: int
    nome: str
    codigo_barras: Optional[str] = None
    marca: Optional[str] = None
    categoria_id: int
    categoria_nome: Optional[str] = Field(None, description="Nome da categoria relacionada")
    tipo_pet: Optional[str] = None
    unidade_venda: Optional[str] = None
    lote: Optional[str] = None
    estoque_atual: Optional[int] = 0
    estoque_minimo: Optional[int] = 0
    custo_aquisicao: Optional[float] = 0.0
    preco_venda: Optional[float] = 0.0
    data_entrada: Optional[str] = None
    data_validade: Optional[str] = None
    status_validade: str = Field(
        ..., description="vencido, a_vencer (próximos 30 dias), ok ou sem_validade"
    )


class ProdutoListSchema(RootModel[List[ProdutoViewSchema]]):
    """Lista de produtos."""


class ProdutoCriadoSchema(BaseModel):
    id: int
    mensagem: str


class ResumoSchema(BaseModel):
    """Indicadores consolidados do estoque, calculados no servidor."""
    total_produtos: int
    total_categorias: int
    estoque_critico: int = Field(..., description="Produtos com estoque atual <= estoque mínimo")
    vencidos: int = Field(..., description="Produtos com validade anterior a hoje")
    a_vencer: int = Field(..., description="Produtos que vencem nos próximos 30 dias")
    valor_estoque: float = Field(..., description="Soma de estoque atual x preço de venda")


class MensagemSchema(BaseModel):
    mensagem: str


class ErroSchema(BaseModel):
    erro: str
