from estudo import app, db
from flask import render_template, url_for, request, redirect
from estudo.models import Contato
from estudo.forms import ContatoForm #importando o formulário de contato no segundo codigo

@app.route('/')
def homepage():
    usuario = "Théo"
    return render_template("index.html", usuario=usuario)

@app.route('/contato/', methods=['GET', 'POST'])
def about():
    form = ContatoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect( url_for('homepage') )
    

    return render_template("contato.html", context=context, form=form )

@app.route('/contato/lista/')
def contatoLista():
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    dados = Contato.query.order_by("nome")
    if pesquisa != '':
        dados = dados.filter_by(nome=pesquisa)
    context = {"dados": dados.all()}
    return render_template("contato_lista.html", context=context)




@app.route('/contato/<int:id>/')
def contatoDetail(id):
    obj = Contato.query.get_or_404(id)
    return render_template("contato_detail.html",obj=obj)








# Formato não recomendado, apenas para estudo, trbalhos internos.
@app.route('/contato_old/', methods=['GET', 'POST'])
def about_old():
    context = {}
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa')
        context.update({'pesquisa': pesquisa})
        print("GET recebido:", pesquisa)
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        contato = Contato(
            nome=nome,
            email=email,
            assunto=assunto,
            mensagem=mensagem
        )

        db.session.add(contato)
        db.session.commit()

    return render_template("contato.html", context=context)