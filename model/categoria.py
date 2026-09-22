from database.database import db


class Categoria(db.Model):
    __tablename__ = 'categoria'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)

    produtos = db.relationship('Produto', backref='categoria', lazy=True)
