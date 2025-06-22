from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Usuario
from app import login_manager # Importe o login_manager do app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('feiras_bp.listar_feiras')) # Redireciona se já estiver logado

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validação básica
        if not username or not password:
            flash('Por favor, preencha todos os campos.')
            return render_template('register.html')

        user = Usuario.query.filter_by(username=username).first()
        if user:
            flash('Nome de usuário já existe.')
            return render_template('register.html')

        new_user = Usuario(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Conta criada com sucesso! Faça login para continuar.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feiras_bp.listar_feiras'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Usuario.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('feiras_bp.minhas_feiras')) # Redireciona para área logada
        else:
            flash('Login ou senha inválidos.')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required # Só pode deslogar se estiver logado
def logout():
    logout_user()
    flash('Você foi desconectado.')
    return redirect(url_for('feiras_bp.listar_feiras')) # Redireciona para página pública