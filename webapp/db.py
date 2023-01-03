# functions for interfacing with the database

import sqlite3
import json

from flask import current_app, g, jsonify


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
        return jsonify( toDictHelper(args[0]) )

    else:
        outputs = {}
        for k,v in kwargs.items():
            outputs[k] = toDictHelper(v)

        return jsonify( outputs )



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
def getPagesInTopic(db, topicid, selectThrough=None, onThe='left' ):
    """Fetch pages corresponding to a particular topic"""
    if selectThrough is None: # only topic pages
        return db.execute("""
            SELECT Page.id, Page.name, Topic.id AS topicid, Topic.name as topicname
            FROM Page INNER JOIN PageTopic ON Page.id=PageTopic.pageid
            INNER JOIN Topic on PageTopic.topicid=Topic.id
            WHERE PageTopic.topicid =(?)
            """, (topicid,) ).fetchall()

    relationshipid = selectThrough
    if onThe == 'left':
        childCol = 'lefttopicid'
        parentCol = 'righttopicid'
    if onThe == 'right':
        childCol = 'righttopicid'
        parentCol = 'lefttopicid'

    return db.execute("""
        WITH RECURSIVE AllRelated(topicid) AS (
            SELECT (?)
            UNION
            SELECT DISTINCT TopicTopicRelationship.{childCol} FROM
            TopicTopicRelationship INNER JOIN AllRelated ON
            TopicTopicRelationship.{parentCol} = AllRelated.topicid
            WHERE TopicTopicRelationship.relationshipid=(?)
            LIMIT 10000
        )
        SELECT Page.id, Page.name, PageTopic.topicid, Topic.name AS topicname FROM Page INNER JOIN 
        PageTopic ON Page.id=PageTopic.pageid INNER JOIN
        AllRelated ON PageTopic.topicid=AllRelated.topicid INNER JOIN
        Topic ON PageTopic.topicid=Topic.id;
        """.format(childCol=childCol, parentCol=parentCol), (topicid, relationshipid)).fetchall()



def getTopicGraph(db, relationshipid, rootedAt=None, onThe='right', depth=float('inf')):
    """fetch a topic graph"""

    if rootedAt is None: # return the whole graph
        return db.execute(
            """SELECT TopicTopicRelationship.lefttopicid, TopicTopicRelationship.righttopicid,
            LeftTopic.name AS leftname, RightTopic.name AS rightname FROM TopicTopicRelationship
            JOIN Topic AS LeftTopic ON TopicTopicRelationship.lefttopicid = LeftTopic.id
            JOIN Topic AS RightTopic ON TopicTopicRelationship.righttopicid = RightTopic.id
            WHERE TopicTopicRelationship.relationshipid =(?) 
            """, (relationshipid,)).fetchall()

    topicid = rootedAt
    if onThe == 'left':
        childCol = 'lefttopicid'
        parentCol = 'righttopicid'
    if onThe == 'right':
        childCol = 'righttopicid'
        parentCol = 'lefttopicid'

    if depth == 1:
        return db.execute("""
            SELECT Current.id AS parentid, Topic.id AS childid, 
            Current.name AS parentname, Topic.name AS childname 
            FROM Topic JOIN 
            TopicTopicRelationship ON Topic.id=TopicTopicRelationship.{childCol} 
            JOIN Topic AS Current
            WHERE TopicTopicRelationship.{parentCol}=(?) AND TopicTopicRelationship.relationshipid=(?)
            AND Current.id=(?);
            """.format(childCol=childCol, parentCol=parentCol),
            (topicid, relationshipid, topicid) ).fetchall()

    if depth == float('inf'):
        return db.execute("""
            WITH RECURSIVE AllRelated(parentid, childid) AS (
                SELECT {parentCol}, {childCol} FROM TopicTopicRelationship 
                WHERE {parentCol}=(?) AND relationshipid=(?)
                UNION
                SELECT DISTINCT TopicTopicRelationship.{parentCol}, TopicTopicRelationship.{childCol}
                FROM TopicTopicRelationship INNER JOIN AllRelated ON
                TopicTopicRelationship.{parentCol} = AllRelated.childid
                WHERE TopicTopicRelationship.relationshipid=(?)
                LIMIT 10000
            )
            SELECT AllRelated.parentid, AllRelated.childid, Parent.name AS parentname, 
            Child.name AS childname
            FROM AllRelated JOIN Topic AS Parent on AllRelated.parentid=Parent.id
            JOIN Topic AS Child on AllRelated.childid=Child.id
            """.format(childCol=childCol, parentCol=parentCol),
            (topicid, relationshipid,relationshipid) ).fetchall()









