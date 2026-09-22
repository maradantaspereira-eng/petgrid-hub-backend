from database.database import db


class Produto(db.Model):
    __tablename__ = 'produto'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), nullable=False)
    codigo_barras = db.Column(db.String(50))
    marca = db.Column(db.String(100))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    tipo_pet = db.Column(db.String(50))
    unidade_venda = db.Column(db.String(10))
    lote = db.Column(db.String(50))
    estoque_atual = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=0)
    custo_aquisicao = db.Column(db.Float, default=0.0)
    preco_venda = db.Column(db.Float, default=0.0)
    data_entrada = db.Column(db.String(10))
    data_validade = db.Column(db.String(10))
