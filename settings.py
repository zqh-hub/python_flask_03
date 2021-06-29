class Config:
    # 数据库+驱动://用户名:密码@主机IP:端口/数据库名
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:zqh139499@127.0.0.1:3306/flask"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True


class ProductionConfig(Config):
    ENV = "production"
