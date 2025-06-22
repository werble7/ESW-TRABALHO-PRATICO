# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login' # Define para onde redirecionar se não estiver logado

# Importar e registrar blueprints (serão criados na próxima etapa)
from routes.auth import auth_bp
from routes.feiras import feiras_bp
# ... outros blueprints

app.register_blueprint(auth_bp)
app.register_blueprint(feiras_bp)
# ... registrar outros blueprints

if __name__ == '__main__':
    with app.app_context(): # Usar app_context para criar o BD
        db.create_all() # Cria as tabelas no BD com base nos modelos
    app.run(debug=True)