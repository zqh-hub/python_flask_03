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
    # app.run()
    manager.run()
