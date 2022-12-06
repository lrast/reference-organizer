# functions for interfacing with the database

import sqlite3 as db

from webapp import app



##### functions for adding data #####
def insertElement(name, elementType):
    """Handles insertion of new elements to tables"""
    conn = db.Connection( app.config['DATABASE_URL'] )
    cur = conn.cursor()

    # injection protection
    if elementType == 'page' or elementType == 'Page':
        tableName = "Page"
    elif elementType == 'topic' or elementType == 'Topic':
        tableName = "Topic"
    elif elementType == 'relationship' or elementType == 'Relationship':
        tableName = "Relationship"

    query = "INSERT INTO " + tableName + " VALUES(?,?)"
    cur.execute(query, (None, name))
    conn.commit()
    conn.close()


def addPageTopic(pageURL, topicName):
    """page-topic relations"""
    conn = db.Connection( app.config['DATABASE_URL'] )
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO PageTopic (pageid, topicid)
        SELECT Page.id, Topic.id FROM Page JOIN Topic WHERE (Page.url, Topic.name)=(?,?);
        """,
         (pageURL, topicName))
    conn.commit()
    conn.close()


def addTopicTopicRelation(leftTopic, rightTopic, relationshipName):
    conn = db.Connection( app.config['DATABASE_URL'] )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO TopicTopicRelationship (relationshipid, lefttopicid, righttopicid)
        SELECT Relationship.id, Left.id, Right.id FROM 
        Relationship JOIN Topic as Left JOIN Topic as Right
        WHERE (Relationship.name, Left.name, Right.name)=(?,?,?);
        """, (relationshipName, leftTopic, rightTopic))
    conn.commit()
    conn.close()



##### functions for fetching data #####







