Python flask

###### flask-script与flask搭配

```python
# 注意：flask：1.1.2版本的
# app.py
from flask_script import Manager

from apps import create_app

app = create_app()
manager = Manager(app=app)

if __name__ == '__main__':
    manager.run()
    
命令行：
python3 app.py runserver -h 0.0.0.0 -p 9090

# 自定义命令
@manager.commond
def fun_name():
  xxxx
```

框架搭建

```python
1、下载第三方库
pip3 install pymysql
pip3 install flask-sqlalchemy
pip3 install flask-migrate==2.5.3

2、配置数据库连接
# 数据库+驱动://用户名:密码@主机IP:端口/数据库名
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:zqh139499@127.0.0.1:3306/flask"

3、创建SQLAlchemy对象，并加载app
-- -- -- -- -- -- -- 完整配置-- -- -- -- -- -- -- -- -- -- -- -- 
|--- settings
|--- app.py
|--- ext
	|--- __init__
|--- apps
	|--- __init__
	|--- user
		|--- __init__
# settings 连接数据库
class Config:
    # 数据库+驱动://用户名:密码@主机IP:端口/数据库名
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:zqh139499@127.0.0.1:3306/flask"
   	# 这里是为了解决“warnings.warn(FSADeprecationWarning”警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):   # 开发环境
    ENV = "development"
    DEBUG = True

class ProductionConfig(Config):   # 生产环境
    ENV = "production"
    
# ext/__init__ 创建SQLAlchemy对象
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# apps/__init__ 创建app,并加载db
from flask import Flask
import settings
from apps.user.view import user_bp
from ext import db

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    # app.config.from_object(settings)
    app.config.from_object(settings.DevelopmentConfig)  # 加载配置
    db.init_app(app)    # 加载db
    app.register_blueprint(user_bp)
    return app
# app.py  关联flask-script
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps import create_app

app = create_app()
manager = Manager(app=app)   # 关联

Migrate(app=app, db=db)  # 实现flask-script、app、SQLAlchemy的联系
manager.add_command('db', MigrateCommand)   # 将命令绑定在manager上

if __name__ == '__main__':
    # app.run()
    manager.run()
```

![001](/Users/eric/Documents/python/python_code/python_flask_03/note/img/001.png)

###### 创建模型

```python
4、创建model.py. /apps/user/model.py
from datetime import datetime

from ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(12), nullable=False)
    pwd = db.Column(db.String(12), unique=True)
    ctime = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.name
        
5、在app.py引入model

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps import create_app
from apps.user.model import User   # 导入model
from ext import db

app = create_app()
manager = Manager(app=app)

Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    
6、命令行执行命令
python3 app.py db init
python3 app.py db migrate
python3 app.py db upgrade
```

