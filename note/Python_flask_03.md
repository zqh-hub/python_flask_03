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

