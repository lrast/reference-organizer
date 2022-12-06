# database migrations. Handwritten for now.

## keywords:
## 1) topics - these are user defined tages
## 2) pages - these are user entered resources



import os
import sqlite3 as db


dbURL = os.environ['FLASK_DATABASE_URL']


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











