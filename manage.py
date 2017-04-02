#!/usr/bin/env python

import os
from flask_script import Manager, Shell
from flask_migrate import init as db_init, migrate as db_migrate, upgrade as db_upgrade, Migrate, MigrateCommand

from app import create_app, db
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def init_app():
    """Run database initialization."""
    # initialize migtrations
    migrations_dir = os.path.join(app.config['APP_ROOT'], 'migrations')
    if not os.path.exists(migrations_dir):
        db_init()

    # perform database migrations
    db_migrate()

    # migrate database to latest revision
    db_upgrade()

    print "Migrations completed ........................................."


if __name__ == '__main__':
    manager.run()
