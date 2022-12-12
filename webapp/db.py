# functions for interfacing with the database

import sqlite3
import json

from flask import current_app, g


##### database connection management #####
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE_URL'])
        g.db.row_factory=sqlite3.Row

    return g.db

def close_db(_=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def database_setup(app):
    app.teardown_appcontext(close_db)



##### database utilites #####
def packageRows(*args, **kwargs):
    """Package database rows to json. Accepts either one argument or a series of kwargs"""

    def toDictHelper(rows):
        # row casting logic
        if type(rows) is list:
            return list( map( dict, rows) )
        else: # assume it is one row
            return dict(rows)

    if len(args) > 0:
        if len(kwargs) > 0 or len(args) > 1:
            raise Exception('Not sure how to package')
        return json.dumps( toDictHelper(args[0]) )

    else:
        outputs = {}
        for k,v in kwargs.items():
            outputs[k] = toDictHelper(v)

        return json.dumps( outputs )



##### functions for adding data #####
def addPageTopic(conn, pageURL, topicName):
    """page-topic relations by url and name"""
    conn.execute("""
        INSERT INTO PageTopic (pageid, topicid)
        SELECT Page.id, Topic.id FROM Page JOIN Topic WHERE (Page.url, Topic.name)=(?,?);
        """,
         (pageURL, topicName))
    conn.commit()


def addTopicTopicRelation(conn, leftTopic, rightTopic, relationshipName):
    """relationships between topics"""
    conn.execute("""
        INSERT INTO TopicTopicRelationship (relationshipid, lefttopicid, righttopicid)
        SELECT Relationship.id, LeftTopic.id, RightTopic.id FROM 
        Relationship JOIN Topic as LeftTopic JOIN Topic as RightTopic
        WHERE (Relationship.name, LeftTopic.name, RightTopic.name)=(?,?,?);
        """, (relationshipName, leftTopic, rightTopic))
    conn.commit()


##### functions for fetching data #####







