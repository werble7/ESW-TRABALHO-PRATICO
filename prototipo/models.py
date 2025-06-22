# models.py
from app import db, login_manager
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256 # ou bcrypt, sha256_crypt

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False) # Armazenará o hash da senha

    # Relacionamentos (um usuário pode criar várias feiras, expositores, etc.)
    feiras = db.relationship('Feira', backref='criador', lazy=True)
    expositores = db.relationship('Expositor', backref='criador', lazy=True)
    produtos = db.relationship('Produto', backref='criador', lazy=True)
    ingressos = db.relationship('Ingresso', backref='criador', lazy=True)

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def __repr__(self):
        return f"Usuario('{self.username}')"

class Feira(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    local = db.Column(db.String(100))
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(2)) # UF

    criador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    expositores = db.relationship('Expositor', backref='feira', lazy=True, cascade="all, delete-orphan")
    ingressos = db.relationship('Ingresso', backref='feira', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"Feira('{self.nome}')"

# Repita o padrão para Expositor, Produto e Ingresso
# Lembre-se dos FKs e relacionamentos.

class Expositor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    contato = db.Column(db.String(100))

    feira_id = db.Column(db.Integer, db.ForeignKey('feira.id'), nullable=False)
    criador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    produtos = db.relationship('Produto', backref='expositor', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"Expositor('{self.nome}')"

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

    expositor_id = db.Column(db.Integer, db.ForeignKey('expositor.id'), nullable=False)
    criador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f"Produto('{self.nome}')"

class Ingresso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False) # Ex: UUID
    data_emissao = db.Column(db.Date, nullable=False)

    feira_id = db.Column(db.Integer, db.ForeignKey('feira.id'), nullable=False)
    criador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f"Ingresso('{self.numero}')"