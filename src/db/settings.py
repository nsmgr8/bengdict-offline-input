import os

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.dirname(__file__).replace(os.sep, '/') \
    + '/database.sqlite3'
INSTALLED_APPS = ('bangladict',)

