from app import db
from datetime import datetime
import json


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    features = db.Column(db.JSON, nullable=False)  # Alterado para JSON
    
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    instancias = db.relationship('Instancia', backref='dataset', lazy=True)

    def __repr__(self):
        return f"Dataset(id={self.id}, nome='{self.nome}')"

class Instancia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
    
    values = db.Column(db.JSON, nullable=False)
    
    def __init__(self, values, dataset_id):
        self.values = json.dumps(values)  # Convertendo o array para JSON antes de armazenar
        self.dataset_id = dataset_id

    def __repr__(self):
        return f"Instancia(id={self.id}, dataset_id={self.dataset_id}, values={self.values})"

