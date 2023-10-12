"""
database controller
"""

from flask_sqlalchemy import SQLAlchemy


class Database(SQLAlchemy):
    def __init__(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/test.db'
        super(Database, self).__init__(app)

    def create_database(self):
        self.create_all()
