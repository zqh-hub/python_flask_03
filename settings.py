class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:zqh139499@127.0.0.1:3306/flask"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True


class ProductionConfig(Config):
    ENC = "production"
