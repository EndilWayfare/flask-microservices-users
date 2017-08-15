import subprocess
import unittest

import coverage
from flask_script import Manager

from project import create_app, db
from project.api.models import User


COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=['project/tests/*']
)
COV.start()


app = create_app()
manager = Manager(app)


@manager.command
def recreate_db():
    """Recreates a database"""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_db():
    """Seeds the database with sample data."""
    db.session.add(User(username='michael', email='michael@realpython.com'))
    db.session.add(User(username='michaelherman', email='michael@mherman.org'))
    db.session.commit()


@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    return 0 if result.wasSuccessful() else 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def gunicorn(bind='0.0.0.0'):
    print(f'Starting gunicorn (binding to{bind})')
    subprocess.call(['gunicorn', '-b', bind, 'manage:app'])


if __name__ == '__main__':
    manager.run()
