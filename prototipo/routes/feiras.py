# routes/feiras.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import db, Feira, Expositor

feiras_bp = Blueprint('feiras_bp', __name__)

# -- Rotas Públicas --
@feiras_bp.route('/')
def listar_feiras():
    feiras = Feira.query.all()
    return render_template('listar_feiras.html', feiras=feiras)

@feiras_bp.route('/feira/<int:feira_id>')
def detalhes_feira(feira_id):
    feira = Feira.query.get_or_404(feira_id)
    # Expositores e produtos serão listados na mesma página ou em links
    return render_template('detalhes_feira.html', feira=feira)

# -- Rotas para Usuários Autenticados (CRUD) --
@feiras_bp.route('/minhas_feiras')
@login_required
def minhas_feiras():
    # Lista apenas as feiras criadas pelo usuário logado
    minhas_feiras = Feira.query.filter_by(criador=current_user).all()
    return render_template('minhas_feiras.html', feiras=minhas_feiras)

@feiras_bp.route('/feira/criar', methods=['GET', 'POST'])
@login_required
def criar_feira():
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        data_inicio = request.form.get('data_inicio') # Tratar formato de data
        data_fim = request.form.get('data_fim')     # Tratar formato de data
        local = request.form.get('local')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')

        try:
            # Converter datas de string para objeto date
            from datetime import datetime
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de data inválido. Use AAAA-MM-DD.')
            return render_template('criar_feira.html')

        nova_feira = Feira(
            nome=nome, descricao=descricao, data_inicio=data_inicio,
            data_fim=data_fim, local=local, cidade=cidade, estado=estado,
            criador=current_user # Associa a feira ao usuário logado
        )
        db.session.add(nova_feira)
        db.session.commit()
        flash('Feira criada com sucesso!')
        return redirect(url_for('feiras_bp.minhas_feiras'))
    return render_template('criar_feira.html')

@feiras_bp.route('/feira/<int:feira_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_feira(feira_id):
    feira = Feira.query.get_or_404(feira_id)
    # Regra de Negócio: Apenas o criador pode editar
    if feira.criador != current_user:
        flash('Você não tem permissão para editar esta feira.')
        return redirect(url_for('feiras_bp.detalhes_feira', feira_id=feira.id))

    if request.method == 'POST':
        feira.nome = request.form.get('nome')
        feira.descricao = request.form.get('descricao')
        # ... (atualizar outros campos e tratar datas)
        try:
            from datetime import datetime
            feira.data_inicio = datetime.strptime(request.form.get('data_inicio'), '%Y-%m-%d').date()
            feira.data_fim = datetime.strptime(request.form.get('data_fim'), '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de data inválido. Use AAAA-MM-DD.')
            return render_template('editar_feira.html', feira=feira)
        feira.local = request.form.get('local')
        feira.cidade = request.form.get('cidade')
        feira.estado = request.form.get('estado')

        db.session.commit()
        flash('Feira atualizada com sucesso!')
        return redirect(url_for('feiras_bp.detalhes_feira', feira_id=feira.id))
    return render_template('editar_feira.html', feira=feira)

@feiras_bp.route('/feira/<int:feira_id>/excluir', methods=['POST'])
@login_required
def excluir_feira(feira_id):
    feira = Feira.query.get_or_404(feira_id)
    # Regra de Negócio: Apenas o criador pode excluir
    if feira.criador != current_user:
        flash('Você não tem permissão para excluir esta feira.')
        return redirect(url_for('feiras_bp.detalhes_feira', feira_id=feira.id))

    # Regra de Negócio: Exclusão só se não houver expositores ou ingressos associados
    if feira.expositores or feira.ingressos:
        flash('Não é possível excluir esta feira, pois há expositores ou ingressos associados.')
        return redirect(url_for('feiras_bp.minhas_feiras'))

    db.session.delete(feira)
    db.session.commit()
    flash('Feira excluída com sucesso!')
    return redirect(url_for('feiras_bp.minhas_feiras'))