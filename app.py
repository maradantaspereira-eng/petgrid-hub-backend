from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from database.database import db, init_db
from model.categoria import Categoria
from model.produto import Produto
from schemas.produto import ProdutoSchema, ProdutoViewSchema, ProdutoUpdateSchema
from schemas.categoria import CategoriaSchema
from pydantic import BaseModel

info = Info(title="PetGrid Hub API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

init_db(app)

produto_tag = Tag(name="Produto", description="Operações com produtos")
categoria_tag = Tag(name="Categoria", description="Operações com categorias")


# --- Categorias ---

@app.get('/categorias', tags=[categoria_tag])
def get_categorias():
    """Lista todas as categorias."""
    categorias = Categoria.query.all()
    resultado = []
    for c in categorias:
        resultado.append({"id": c.id, "nome": c.nome})
    return resultado, 200


# --- Produtos ---

@app.get('/produtos', tags=[produto_tag])
def get_produtos():
    """Lista todos os produtos."""
    produtos = Produto.query.all()
    resultado = []
    for p in produtos:
        cat = Categoria.query.get(p.categoria_id)
        resultado.append({
            "id": p.id,
            "nome": p.nome,
            "codigo_barras": p.codigo_barras,
            "marca": p.marca,
            "categoria_id": p.categoria_id,
            "categoria_nome": cat.nome if cat else None,
            "tipo_pet": p.tipo_pet,
            "unidade_venda": p.unidade_venda,
            "lote": p.lote,
            "estoque_atual": p.estoque_atual,
            "estoque_minimo": p.estoque_minimo,
            "custo_aquisicao": p.custo_aquisicao,
            "preco_venda": p.preco_venda,
            "data_entrada": p.data_entrada,
            "data_validade": p.data_validade
        })
    return resultado, 200


class ProdutoPath(BaseModel):
    id: int


@app.get('/produtos/<int:id>', tags=[produto_tag])
def get_produto(path: ProdutoPath):
    """Busca um produto pelo ID."""
    produto = Produto.query.get(path.id)
    if not produto:
        return {"erro": "Produto não encontrado"}, 404
    cat = Categoria.query.get(produto.categoria_id)
    return {
        "id": produto.id,
        "nome": produto.nome,
        "codigo_barras": produto.codigo_barras,
        "marca": produto.marca,
        "categoria_id": produto.categoria_id,
        "categoria_nome": cat.nome if cat else None,
        "tipo_pet": produto.tipo_pet,
        "unidade_venda": produto.unidade_venda,
        "lote": produto.lote,
        "estoque_atual": produto.estoque_atual,
        "estoque_minimo": produto.estoque_minimo,
        "custo_aquisicao": produto.custo_aquisicao,
        "preco_venda": produto.preco_venda,
        "data_entrada": produto.data_entrada,
        "data_validade": produto.data_validade
    }, 200


@app.post('/produtos', tags=[produto_tag])
def add_produto(body: ProdutoSchema):
    """Adiciona um novo produto."""
    categoria = Categoria.query.get(body.categoria_id)
    if not categoria:
        return {"erro": "Categoria não encontrada"}, 404

    produto = Produto(
        nome=body.nome,
        codigo_barras=body.codigo_barras,
        marca=body.marca,
        categoria_id=body.categoria_id,
        tipo_pet=body.tipo_pet,
        unidade_venda=body.unidade_venda,
        lote=body.lote,
        estoque_atual=body.estoque_atual,
        estoque_minimo=body.estoque_minimo,
        custo_aquisicao=body.custo_aquisicao,
        preco_venda=body.preco_venda,
        data_entrada=body.data_entrada,
        data_validade=body.data_validade
    )
    db.session.add(produto)
    db.session.commit()

    return {"id": produto.id, "mensagem": "Produto adicionado com sucesso"}, 201


@app.put('/produtos/<int:id>', tags=[produto_tag])
def update_produto(path: ProdutoPath, body: ProdutoUpdateSchema):
    """Atualiza um produto existente."""
    produto = Produto.query.get(path.id)
    if not produto:
        return {"erro": "Produto não encontrado"}, 404

    if body.nome is not None:
        produto.nome = body.nome
    if body.codigo_barras is not None:
        produto.codigo_barras = body.codigo_barras
    if body.marca is not None:
        produto.marca = body.marca
    if body.categoria_id is not None:
        categoria = Categoria.query.get(body.categoria_id)
        if not categoria:
            return {"erro": "Categoria não encontrada"}, 404
        produto.categoria_id = body.categoria_id
    if body.tipo_pet is not None:
        produto.tipo_pet = body.tipo_pet
    if body.unidade_venda is not None:
        produto.unidade_venda = body.unidade_venda
    if body.lote is not None:
        produto.lote = body.lote
    if body.estoque_atual is not None:
        produto.estoque_atual = body.estoque_atual
    if body.estoque_minimo is not None:
        produto.estoque_minimo = body.estoque_minimo
    if body.custo_aquisicao is not None:
        produto.custo_aquisicao = body.custo_aquisicao
    if body.preco_venda is not None:
        produto.preco_venda = body.preco_venda
    if body.data_entrada is not None:
        produto.data_entrada = body.data_entrada
    if body.data_validade is not None:
        produto.data_validade = body.data_validade

    db.session.commit()
    return {"mensagem": "Produto atualizado com sucesso"}, 200


@app.delete('/produtos/<int:id>', tags=[produto_tag])
def delete_produto(path: ProdutoPath):
    """Remove um produto."""
    produto = Produto.query.get(path.id)
    if not produto:
        return {"erro": "Produto não encontrado"}, 404
    db.session.delete(produto)
    db.session.commit()
    return {"mensagem": "Produto removido com sucesso"}, 200


# --- Seed de categorias ---
with app.app_context():
    if Categoria.query.count() == 0:
        categorias_iniciais = [
            Categoria(nome="Rações"),
            Categoria(nome="Petiscos"),
            Categoria(nome="Higiene"),
            Categoria(nome="Brinquedos"),
            Categoria(nome="Medicamentos"),
            Categoria(nome="Acessórios"),
        ]
        db.session.add_all(categorias_iniciais)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
