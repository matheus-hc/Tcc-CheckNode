from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from email_sender import check_and_send_email
import os
from datetime import timedelta, datetime
from config import Config
from models import db, Repositorio, Usuario


app = Flask(__name__)
app.config.from_object(Config)  


db.init_app(app)
with app.app_context():
    db.create_all()



def login_required(f):
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            flash("Faça login para acessar esta página.", "info")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap


@app.route('/')
@login_required
def home():
    repositorios = Repositorio.query.all() 
    return render_template('home.html', repositorios=repositorios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session['user_id'] = usuario.id
            session.permanent = True  
            app.permanent_session_lifetime = app.config['PERMANENT_SESSION_LIFETIME']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        flash('E-mail ou senha inválidos', 'danger')
    return render_template('login.html', disable_sidebar=True, disable_navbar=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('name')
        email = request.form.get('email')
        senha = request.form.get('senha')
        senha_hash = generate_password_hash(senha, method='pbkdf2:sha256')
        
        
        if Usuario.query.filter_by(email=email).first():
            flash('Este e-mail já está em uso. Tente outro.', 'danger')
            return redirect(url_for('register'))
        
       
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Conta criada com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', disable_sidebar=True, disable_navbar=True)


@app.route('/register_repo', methods=['GET', 'POST'])
@login_required
def register_repo():
    if request.method == 'POST':
        nome_repo = request.form['nome_repo']
        url_repo = request.form['url_repo']
        periodicidade = int(request.form['periodicidade'])
        usuario_id = session['user_id']
        
        novo_repositorio = Repositorio(
            nome=nome_repo, 
            url=url_repo, 
            periodicidade=periodicidade, 
            usuario_id=usuario_id
        )
        db.session.add(novo_repositorio)
        db.session.commit()
        
      
        user = Usuario.query.get(usuario_id)
        current_version = "v16.17.0"  
        check_and_send_email(nome_repo, url_repo, user.email, current_version)
        
        flash('Repositório cadastrado com sucesso!', 'success')
        return redirect(url_for('home'))
    return render_template('register_repo.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))


@app.route('/delete_repo/<int:id>', methods=['POST'])
@login_required
def delete_repo(id):
    repo = Repositorio.query.get_or_404(id)
    db.session.delete(repo)
    db.session.commit()
    flash(f'Repositório {repo.nome} excluído com sucesso!', 'success')
    return redirect(url_for('home'))

@app.route('/send_email/<int:id>', methods=['POST'])
@login_required
def send_email(id):
    repo = Repositorio.query.get_or_404(id)
    user = Usuario.query.get(repo.usuario_id)
    check_and_send_email(repo.nome, repo.url, user.email, "v16.17.0") 
    flash(f'E-mail enviado para {repo.nome}!', 'success')
    return redirect(url_for('home'))

@app.route('/history')
@login_required
def history():
    user = Usuario.query.get(session['user_id'])
    repositorios = Repositorio.query.filter_by(usuario_id=user.id).all()
    return render_template('history.html', repositorios=repositorios)

if __name__ == "__main__":
    app.run(debug=True)
