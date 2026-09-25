from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from pydantic import BaseModel

from database.database import db, init_db
from logger import logger
from model.categoria import Categoria
from model.produto import Produto
from schemas.categoria import CategoriaListSchema
from schemas.produto import (
    ProdutoSchema, ProdutoUpdateSchema, ProdutoViewSchema, ProdutoListSchema,
    ProdutoCriadoSchema, ResumoSchema, MensagemSchema, ErroSchema,
    datas_coerentes, MENSAGEM_DATAS,
)

info = Info(
    title="PetGrid Hub API",
    version="1.0.0",
    description="API REST para gestão de produtos e controle de estoque de pet shops.",
)
app = OpenAPI(__name__, info=info)
CORS(app)

init_db(app)

produto_tag = Tag(name="Produto", description="Cadastro e consulta de produtos do estoque")
categoria_tag = Tag(name="Categoria", description="Categorias usadas para classificar os produtos")
resumo_tag = Tag(name="Resumo", description="Indicadores consolidados do estoque")


class ProdutoPath(BaseModel):
    id: int


def buscar_produto(produto_id):
    return db.session.get(Produto, produto_id)


# --- Categorias ---

@app.get('/categorias', tags=[categoria_tag],
         summary="Listar categorias",
         responses={"200": CategoriaListSchema})
def get_categorias():
    """Retorna todas as categorias cadastradas."""
    categorias = Categoria.query.order_by(Categoria.id).all()
    return [{"id": c.id, "nome": c.nome} for c in categorias], 200


# --- Resumo ---

@app.get('/resumo', tags=[resumo_tag],
         summary="Obter indicadores do estoque",
         responses={"200": ResumoSchema})
def get_resumo():
    """Calcula no servidor os totais do estoque: produtos, categorias, itens com
    estoque crítico, produtos vencidos ou a vencer em 30 dias e valor total em estoque."""
    produtos = Produto.query.all()
    return {
        "total_produtos": len(produtos),
        "total_categorias": Categoria.query.count(),
        "estoque_critico": sum(1 for p in produtos if p.estoque_critico()),
        "vencidos": sum(1 for p in produtos if p.status_validade() == "vencido"),
        "a_vencer": sum(1 for p in produtos if p.status_validade() == "a_vencer"),
        "valor_estoque": round(sum((p.estoque_atual or 0) * (p.preco_venda or 0) for p in produtos), 2),
    }, 200


# --- Produtos ---

@app.get('/produtos', tags=[produto_tag],
         summary="Listar produtos",
         responses={"200": ProdutoListSchema})
def get_produtos():
    """Retorna todos os produtos, já com o nome da categoria relacionada e o
    status de validade (vencido, a_vencer, ok ou sem_validade)."""
    return [p.to_dict() for p in Produto.query.order_by(Produto.id).all()], 200


@app.get('/produtos/<int:id>', tags=[produto_tag],
         summary="Buscar produto por ID",
         responses={"200": ProdutoViewSchema, "404": ErroSchema})
def get_produto(path: ProdutoPath):
    """Retorna os dados de um produto. Responde 404 se o ID não existir."""
    produto = buscar_produto(path.id)
    if not produto:
        return {"erro": "Produto não encontrado"}, 404
    return produto.to_dict(), 200


@app.post('/produtos', tags=[produto_tag],
          summary="Cadastrar produto",
          responses={"201": ProdutoCriadoSchema, "404": ErroSchema})
def add_produto(body: ProdutoSchema):
    """Cadastra um novo produto. `nome` e `categoria_id` são obrigatórios.
    Responde 404 se a categoria não existir e 422 se algum campo for inválido
    (datas fora do formato AAAA-MM-DD, validade anterior à entrada, valores negativos)."""
    if not db.session.get(Categoria, body.categoria_id):
        return {"erro": "Categoria não encontrada"}, 404

    produto = Produto(**body.model_dump())
    db.session.add(produto)
    db.session.commit()
    logger.info("Produto criado: id=%s nome=%s", produto.id, produto.nome)

    return {"id": produto.id, "mensagem": "Produto adicionado com sucesso"}, 201


@app.put('/produtos/<int:id>', tags=[produto_tag],
         summary="Atualizar produto",
         responses={"200": MensagemSchema, "400": ErroSchema, "404": ErroSchema})
def update_produto(path: ProdutoPath, body: ProdutoUpdateSchema):
    """Atualiza parcialmente um produto: apenas os campos enviados são alterados.
    Responde 404 se o produto ou a categoria informada não existirem e 400 se a
    validade resultante ficar anterior à data de entrada."""
    produto = buscar_produto(path.id)
    if not produto:
        return {"erro": "Produto não encontrado"}, 404

    # Campos enviados vazios limpam o valor; nome e categoria nunca podem ficar nulos
    alteracoes = body.model_dump(exclude_unset=True)
    for obrigatorio in ("nome", "categoria_id"):
        if alteracoes.get(obrigatorio) is None:
            alteracoes.pop(obrigatorio, None)

    if "categoria_id" in alteracoes and not db.session.get(Categoria, alteracoes["categoria_id"]):
        return {"erro": "Categoria não encontrada"}, 404

    entrada = alteracoes.get("data_entrada", produto.data_entrada)
    validade = alteracoes.get("data_validade", produto.data_validade)
    if not datas_coerentes(entrada, validade):
        return {"erro": MENSAGEM_DATAS}, 400

    for campo, valor in alteracoes.items():
        setattr(produto, campo, valor)

    db.session.commit()
    logger.info("Produto atualizado: id=%s campos=%s", produto.id, list(alteracoes))
    return {"mensagem": "Produto atualizado com sucesso"}, 200


@app.delete('/produtos/<int:id>', tags=[produto_tag],
            summary="Remover produto",
            responses={"200": MensagemSchema, "404": ErroSchema})
def delete_produto(path: ProdutoPath):
    """Remove um produto. Responde 404 se o ID não existir."""
    produto = buscar_produto(path.id)
    if not produto:
        return {"erro": "Produto não encontrado"}, 404
    db.session.delete(produto)
    db.session.commit()
    logger.info("Produto removido: id=%s", path.id)
    return {"mensagem": "Produto removido com sucesso"}, 200


# --- Seed de categorias ---
with app.app_context():
    if Categoria.query.count() == 0:
        db.session.add_all([Categoria(nome=nome) for nome in
                            ("Rações", "Petiscos", "Higiene", "Brinquedos", "Medicamentos", "Acessórios")])
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
