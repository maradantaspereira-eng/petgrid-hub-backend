from datetime import date, timedelta

from database.database import db

DIAS_ALERTA_VALIDADE = 30


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

    def estoque_critico(self):
        return (self.estoque_atual or 0) <= (self.estoque_minimo or 0)

    def status_validade(self, hoje=None):
        """Classifica a validade: sem_validade, vencido, a_vencer ou ok."""
        if not self.data_validade:
            return "sem_validade"
        hoje = hoje or date.today()
        try:
            validade = date.fromisoformat(self.data_validade)
        except ValueError:
            return "sem_validade"
        if validade < hoje:
            return "vencido"
        if validade <= hoje + timedelta(days=DIAS_ALERTA_VALIDADE):
            return "a_vencer"
        return "ok"

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "codigo_barras": self.codigo_barras,
            "marca": self.marca,
            "categoria_id": self.categoria_id,
            "categoria_nome": self.categoria.nome if self.categoria else None,
            "tipo_pet": self.tipo_pet,
            "unidade_venda": self.unidade_venda,
            "lote": self.lote,
            "estoque_atual": self.estoque_atual,
            "estoque_minimo": self.estoque_minimo,
            "custo_aquisicao": self.custo_aquisicao,
            "preco_venda": self.preco_venda,
            "data_entrada": self.data_entrada,
            "data_validade": self.data_validade,
            "status_validade": self.status_validade(),
        }
