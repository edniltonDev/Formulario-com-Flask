from flask_wtf import FlaskForm #importando a classe FlaskForm
from wtforms import StringField, SubmitField #tipos de campos que iremos usar
from wtforms.validators import DataRequired, Email #validador para garantir que o campo não esteja vazio

from estudo.models import Contato
from estudo import db



class ContatoForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()]) # dentro dos parenteses, o rótulo (label) do campo
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    assunto = StringField("Assunto", validators=[DataRequired()])
    mensagem =StringField("Mensagem", validators=[DataRequired()])
    btnSubmit = SubmitField("Enviar")

    def save(self):
        contato = Contato(
            nome=self.nome.data,
            email=self.email.data,
            assunto=self.assunto.data,
            mensagem=self.mensagem.data
        )
        
        db.session.add(contato)
        db.session.commit()