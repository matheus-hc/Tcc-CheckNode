from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

class Repositorio(db.Model):
    __tablename__ = 'repositorios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False) 
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    periodicidade = db.Column(db.Integer, nullable=False)
    ultima_verificacao = db.Column(db.Date)  

    usuario = db.relationship('Usuario', backref=db.backref('repositorios', lazy=True))

def __repr__(self):
        return f'<Repositorio {self.nome}>'