# database migrations. Handwritten for now.

## keywords:
## 1) topics - these are user defined tages
## 2) pages - these are user entered resources



import os
import sqlite3 as db


dbURL = os.environ['FLASK_DATABASE_URL']


def remakeTopicTopic():
    """recreates the Page Topic table to have unique (rel, left, right) triples"""
    conn = db.connect(dbURL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS TopicTopicRelationship(
            id INTEGER PRIMARY KEY,
            relationshipid INTEGER,
            lefttopicid INTEGER,
            righttopicid INTEGER,
            FOREIGN KEY( lefttopicid ) REFERENCES Topic(id),
            FOREIGN KEY( righttopicid ) REFERENCES Topic(id),
            FOREIGN KEY( relationshipid ) REFERENCES reRelationship(id),
            UNIQUE(relationshipid, lefttopicid, righttopicid )
        );
        """)
    conn.commit()
    conn.close()


def remakePageTopic():
    """recreates the Page Topic table to have unique (pageid, topicid) pairs"""
    conn = db.connect(dbURL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PageTopic(
            id INTEGER PRIMARY KEY,
            pageid INTEGER,
            topicid INTEGER,
            FOREIGN KEY( pageid ) REFERENCES Page(id),
            FOREIGN KEY( topicid ) REFERENCES Topic(id),
            UNIQUE(pageid, topicid)
        );
        """)
    conn.commit()
    conn.close()



def addPageName():
    """Adds a page name field to the Pages Table"""
    conn = db.connect(dbURL)
    conn.execute("""ALTER TABLE Page ADD
        name TEXT;
        """)
    conn.commit()
    conn.close()


def makeInitialTables():
    """Initial database design"""
    conn = db.Connection(dbURL)

    cur = conn.cursor()

    # pages table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Page(
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE NOT NULL 
        );
        """)

    # topics tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Topic(
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        );
        """)

    # table of possible relationships
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Relationship(
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        );
        """)


    # page to topics relationships
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PageTopic(
            id INTEGER PRIMARY KEY,
            pageid INTEGER,
            topicid INTEGER,
            FOREIGN KEY( pageid ) REFERENCES Page(id),
            FOREIGN KEY( topicid ) REFERENCES Topic(id)
        );
        """)

    # topic to topic relationships
    cur.execute("""
        CREATE TABLE IF NOT EXISTS TopicTopicRelationship(
            id INTEGER PRIMARY KEY,
            relationshipid INTEGER,
            lefttopicid INTEGER,
            righttopicid INTEGER,
            FOREIGN KEY( lefttopicid ) REFERENCES Topic(id),
            FOREIGN KEY( righttopicid ) REFERENCES Topic(id)
        );
        """)

    conn.commit()
    conn.close()











