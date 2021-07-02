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

###### 数据库的存储

```python
@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User()			-- -- -- -- -- -- -- -- --  User的实例对象
        user.username = username
        user.password = password
        db.session.add(user)
        db.session.commit()
        return "注册成功了！"
    return render_template("user/register.html")
```

###### 数据库查询

```python
查询所有：
	1、模型类.query.all()			select * from user
过滤条件：	
	2、模型类.query.filter_by(字段=值)		  select * from 表名 where 字段=值
	3、模型类.query.filter_by(字段=值).first()		  select * from 表名 where 字段=值 limit 1
	4、模型类.query.get(xx)     select * from 表名 where id = xx
  5、模型类.query.filter(模型类.字段名 ==\>\< 值).all()
  6、模型类.query.filter(模型类.字段名 == 值).first()
  7、模型类.query.filter(模型类.字段名.startswith("1")).all()
  		select * from 表名 where 字段 like 'l%'
  8、模型类.query.filter(模型类.字段名.contains("d")).all()
  		select * from 表名 where 字段 like '%d%'
  9、模型类.query.filter(模型类.字段名.like("d")).all()
  		select * from 表名 where 字段 like '%d%'
  10、from sqlalchemy import or_
  User.query.filter(or_(User.username.startswith("v"),User.username.contains("d"))).all()
      select * from 表名 where username like 'v%' or username like '%d%'
  11、from sqlalchemy import and_
  User.query.filter(and_(User.username.contains("v"), User.ctime.__eq__("2021-07-01 20:28:55"))).all()
    select * from User where username like '%v%' and ctime = '2021-07-01 20:28:55'
  12、User.query.filter(not_(User.ctime == "2021-07-01 20:28:55"))
      select * from User where ctime != "2021-07-01 20:28:55"
  13、User.query.filter(User.phone.in_(['211212', '1234']))
    	select * from User where phone in ('211212', '1234')
  14、User.query.filter(User.age.between(12,34)).all()
    	select * from User where age between 12 and 34
  15、User.query.filter(User.age.between(12,34)).order_by("id").all()  升序
  		User.query.order_by(-User.id).all()  逆序
  16、User.query.filter(User.xxx).limit(2).all()
  	  User.query.filter(User.xxx).offset(2).limit(2).all()  跳过1、2，获取3、4
```

数据库删除

```python
# app.py

@user_bp.route("/delete", endpoint="delete")
def delete_user():
    user_id = request.args.get("id")
    target = User.query.get(user_id)
    ''' 逻辑删除
    target.is_delete = True
    '''
    # 物理删除
    db.session.delete(target)
    db.session.commit()
    return redirect(url_for("user.center"))
    
# center.html
<td><a href="{{ url_for("user.delete")}}?id={{ user.id }}">删除</a></td>
```

