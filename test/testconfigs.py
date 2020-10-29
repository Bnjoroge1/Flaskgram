from flask import config, request
import pytest, os 
from srcode import create_current_app, db as db_test
from config import TestConfig


DATABASE_URL = '/tmp/test_app.db'
@pytest.fixture(scope='session')
def app():
     app = create_current_app(config = TestConfig)
     app_context = app.app_context()
     app_context.push()

@pytest.fixture(scope='session')
def db(app, request):
     '''session-wide db testing'''
     if os.path.exists(DATABASE_URL):
          os.unlink(DATABASE_URL)
     
     db_test.app = app
     db_test.create_all()
     
     def teardown():
          db_test.drop_all()
          os.unlink(DATABASE_URL)
     request.add_finalizer(teardown)
     return db_test

@pytest.fixture(scope='function')
def session(db, request):
     session = db.create_scoped_session()
     db.session = session
     def teardown():
          session.remove()
     request.addfinalizer(teardown)
     return session    