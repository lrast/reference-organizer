# functions for interfacing with the database

import sqlite3

from flask import current_app, g, jsonify


# database connection management

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE_URL'])
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(_=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def database_setup(app):
    app.teardown_appcontext(close_db)


# database utilites

def packageRows(*args, **kwargs):
    """Package database rows to json.
    Accepts either one argument or a series of kwargs
    """

    def toDictHelper(rows):
        # row casting logic
        if type(rows) is list:
            return list(map(dict, rows))
        else:  # assume it is one row
            return dict(rows)

    if len(args) > 0:
        if len(kwargs) > 0 or len(args) > 1:
            raise Exception('Not sure how to package')
        return jsonify(toDictHelper(args[0]))

    else:
        outputs = {}
        for k, v in kwargs.items():
            outputs[k] = toDictHelper(v)

        return jsonify(outputs)
