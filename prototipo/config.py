class Config:
    SECRET_KEY = 'sua_super_secreta_chave' # MUITO IMPORTANTE! Mude para uma string complexa
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # Para SQLite
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@host:port/database' # Para PostgreSQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False