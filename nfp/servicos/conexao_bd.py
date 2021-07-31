from sqlalchemy import create_engine


def conecta_bd(uri, debug):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + uri
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=debug)
    return engine
