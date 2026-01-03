from estudo import db, login_manager
from datetime import datetime
from flask_login import UserMixin # informar que a classe User é compatível com o Flask-Login

@login_manager.user_loader #recuperar usuário para fazer a sessao de login, não precisa decorar, deixe salvo aqui, receita de bolo
def load_user(user_id):
    return User.query.get(int(user_id)) # função necessária para o Flask-Login carregar o usuário a partir do ID armazenado na sessão

class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        nome = db.Column(db.String(150), nullable=False)
        sobrenome = db.Column(db.String(150), nullable=False)
        email = db.Column(db.String(150), nullable=False)
        senha = db.Column(db.String(8), nullable=False)


class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    assunto = db.Column(db.String(150), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    respondido = db.Column(db.Integer, default=0)# 0 para não respondido, 1 para respondido

 