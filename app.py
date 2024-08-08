from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
from flask import make_response
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@127.0.0.1:3306/meubanco'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) 

class Usuario(db.Model):
	id = db.Column('usu_id', db.Integer, primary_key = True)
	nome = db.Column('usu_nome', db.String(256))
	email = db.Column('usu_email', db.String(256))
	senha = db.Column('usu_senha', db.String(256))
	end = db.Column('usu_endereco', db.String(256))

	def __init__(self, nome, email, senha, end):
		self.nome = nome
		self.email = email
		self.senha = senha
		self.end = end

class Categoria(db.Model):
    
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))

    def __init__ (self, nome):
        self.nome = nome
	

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anc_id', db.Integer, primary_key=True)
    nome = db.Column('anc_nome', db.String(256))
    desc = db.Column('anc_desc', db.String(256))
    qtd = db.Column('anc_qtd', db.Integer)
    preco = db.Column('anc_preco', db.Float)
    cat_id = db.Column('cat_id',db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, desc, qtd, preco, cat_id, usu_id):
        self.nome = nome
        self.desc = desc
        self.qtd = qtd
        self.preco = preco
        self.cat_id = cat_id
        self.usu_id = usu_id
     

@app.errorhandler(404)
def paginanaoencontrada(error):
	return render_template('paginanaoencontrada.html')

@app.route('/')
def index():
	return render_template('index.html')
#------------------------------------------------------------------------------
####Usuário####
@app.route("/cad/usuario")
def cadusuario():
	return render_template('usuario.html',usuarios = Usuario.query.all(), titulo="Usuário")

@app.route("/usuario/criar", methods=['POST'] )
def criarusuario():
	usuario = Usuario(request.form.get('user'), request.form.get('email'), request.form.get('senha'), request.form.get('end'))
	db.session.add(usuario)
	db.session.commit()
	return redirect(url_for('cadusuario'))

@app.route("/usuario/buscar/<int:id>")
def buscausuario(id):
	usuario = Usuario.query.get(id)
	return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editarusuario(id):
	usuario = Usuario.query.get(id)
	if request.method == 'POST':
		usuario.nome = request.form.get('user')
		usuario.email = request.form.get('email')
		usuario.senha = request.form.get('senha')
		usuario.end = request.form.get('end')
	
		db.session.add(usuario)
		db.session.commit()
		return redirect(url_for('cadusuario'))
	
	return render_template('ausuario.html', usuario = usuario, titulo="Usuário")

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
	usuario = Usuario.query.get(id)
	db.session.delete(usuario)
	db.session.commit()
	return redirect(url_for('cadusuario'))


#------------------------------------------------------------------------------
####Anúncios####
@app.route("/cad/anuncio")
def anuncio():
	return render_template('anuncio.html', anuncios = Anuncio.query.all(), categorias = Categoria.query.all(), usuarios = Usuario.query.all(), titulo="Anuncio")

@app.route("/anuncio/criar", methods=['POST'] )
def criaranuncio():
	anuncio = Anuncio(request.form.get('nome'), request.form.get('desc'),request.form.get('qtd'),request.form.get('preco'),request.form.get('cat'), request.form.get('uso'))
	db.session.add(anuncio)
	db.session.commit()
	return redirect(url_for('anuncio'))

@app.route("/anuncio/buscar/<int:id>")
def buscaanuncio(id):
	anuncio = Anuncio.query.get(id)
	return anuncio.nome

@app.route("/anuncio/deletar/<int:id>")
def deletaranuncio(id):
	anuncio = Anuncio.query.get(id)
	db.session.delete(anuncio)
	db.session.commit()
	return redirect(url_for('anuncio'))

@app.route("/anuncio/editar/<int:id>", methods=['GET','POST'])
def editaranuncio(id):
	anuncio = Anuncio.query.get(id)
	if request.method == 'POST':
		anuncio.nome = request.form.get('nome')
		anuncio.desc = request.form.get('desc')
		anuncio.qtd = request.form.get('qtd')
		anuncio.preco = request.form.get('preco')
		anuncio.cat_id = request.form.get('cat')
		anuncio.usu_id = request.form.get('uso')
	
		db.session.add(anuncio)
		db.session.commit()
		return redirect(url_for('anuncio'))
	
	return render_template('aanuncio.html', anuncio = anuncio, categorias = Categoria.query.all(), usuarios = Usuario.query.all(), titulo="Anúncio")
#------------------------------------------------------------------------------
####Perguntas####
@app.route("/anuncios/pergunta")
def pergunta():
	return render_template('pergunta.html', titulo="Perguntas")

#------------------------------------------------------------------------------
####Compra####
@app.route("/anuncios/compra")
def compra():
	return render_template('compra.html', titulo="Compras")

#------------------------------------------------------------------------------
####Anúncios Favoritos####
@app.route("/anuncio/favoritos")
def favoritos():
	return render_template('favoritos.html', titulo="Anúncios Favoritos")

#------------------------------------------------------------------------------
####Categoria####
@app.route("/config/categoria")
def categoria():
	return render_template('categoria.html',categorias = Categoria.query.all(), titulo="Categoria")

@app.route("/categoria/criar", methods=['POST'] )
def criarcategoria():
	categoria = Categoria(request.form.get('nome'))
	db.session.add(categoria)
	db.session.commit()
	return redirect(url_for('categoria'))

@app.route("/categoria/buscar/<int:id>")
def buscarcategoria(id):
	categoria = Categoria.query.get(id)
	return categoria.nome

@app.route("/categoria/deletar/<int:id>")
def deletarcategoria(id):
	categoria = Categoria.query.get(id)
	db.session.delete(categoria)
	db.session.commit()
	return redirect(url_for('categoria'))

@app.route("/categoria/editar/<int:id>", methods=['GET','POST'])
def editarcategoria(id):
	categoria = Categoria.query.get(id)
	if request.method == 'POST':
		categoria.nome = request.form.get('nome')
		
		db.session.add(categoria)
		db.session.commit()
		return redirect(url_for('categoria'))
	
	return render_template('acategoria.html', categoria = categoria, titulo="Categoria")
#------------------------------------------------------------------------------
####Relatório Vendas####
@app.route("/relatorios/vendas")
def relVendas():
	return render_template('relVendas.html', titulo="Relatório de Vendas")

#------------------------------------------------------------------------------
####Relatório Compras####
@app.route("/relatorios/compras")
def relCompras():
	return render_template('relCompras.html', titulo="Relatório de Compras")


#app.py
if __name__ == 'app': 
	print('teste')
	db.create_all()