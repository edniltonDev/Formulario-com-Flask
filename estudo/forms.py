from flask_wtf import FlaskForm #importando a classe FlaskForm
from wtforms import StringField, SubmitField, PasswordField #tipos de campos que iremos usar
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError #validador para garantir que o campo não esteja vazio

from estudo.models import Contato, User
from estudo import db, bcrypt


class userForm(FlaskForm): # formulário de cadastro de usuário, herda de FlaskForm, importar PasswordField
    nome = StringField("Nome", validators=[DataRequired()])
    sobrenome = StringField("Sobrenome", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()]) # validador de email válido, importar Email
    senha = PasswordField("Senha", validators=[DataRequired()])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo('senha')]) # EqualTo para garantir que a senha e a confirmação sejam iguais, importar EqualTo
    btnSubmit = SubmitField("Cadastrar")

    def Validate_email(self, email): # verifica se o email já está cadastrado importar ValidationError
        if User.query.filter_by(email=email.data).first(): # verifica se já existe um usuário com esse email imortar User
            return ValidationError("E-mail já cadastrado. Utilize outro e-mail.")
        

    #criar método save para salvar o usuário no banco de dados
    def save(self): # importar o bcrypt
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8')) #criptografa a senha, qualquer caractere especial deve ser codificado em utf-8
        user = User(  # criando o objeto usuário
            nome=self.nome.data,
            sobrenome=self.sobrenome.data,
            email=self.email.data,
            senha=senha
        )
        db.session.add(user) # adicionando o usuário na sessão do banco de dados
        db.session.commit() # confirmando a transação no banco de dados
        return user # retornando o objeto usuário criado no banco de dados


class LoginForm(FlaskForm): # formulário de login com email, senha e botão de submit  
    email = StringField("E-mail", validators=[DataRequired(), Email()])   
    senha = PasswordField("Senha", validators=[DataRequired()])
    btnSubmit = SubmitField("Login")

    def login(self):# função de login do usuário
        #retornar o usuário do email informado
        user = User.query.filter_by(email=self.email.data).first()
        #verificar se a senha informada corresponde à senha do usuário no banco de dados
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):# verifica se a senha está correta
                return user #retorna o objeto usuário se a senha estiver correta
            else:
                raise Exception("Senha incorreta.")
        else:
            raise Exception("Usuário não encontrado.")
       

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