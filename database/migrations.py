# database migrations. Handwritten for now.

## keywords:
## 1) topics - these are user defined tages
## 2) pages - these are user entered resources



import os
import sqlite3 as db


dbURL = os.environ['FLASK_DATABASE_URL']


def makeAuthorTable():
    """
    Make a table of authors and an Author Page join table
    """
    conn = db.connect(dbURL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Author (
            id INTEGER PRIMARY KEY,
            first TEXT,
            last TEXT,
            middle TEXT);
        """ )
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PageAuthor (
            id INTEGER PRIMARY KEY,
            pageid INTEGER,
            authorid INTEGER,
            FOREIGN KEY( pageid ) REFERENCES Page(id),
            FOREIGN KEY( authorid ) REFERENCES Author(id)
            );
        """ )
    conn.commit()
    conn.close()


def remakePageTable():
    """Remove the requirements for the url in the Page table,
        add journal and date fields 
    """
    conn = db.connect(dbURL)
    cur = conn.cursor()
    cur.execute("""ALTER TABLE Page RENAME TO Page_temp;""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Page(
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE,
            name TEXT,
            date TEXT,
            publishedin TEXT,
            dateadded TEXT
        );
        """)
    cur.execute("""
        INSERT INTO Page(id, url, name, dateadded) SELECT id, url, name, dateadded FROM Page_temp;
        """)
    cur.execute("""DROP TABLE Page_temp;""")
    conn.commit()
    conn.close()


def addRelationshipReversename():
    """recreates the Page Topic table to have unique (rel, left, right) triples"""
    conn = db.connect(dbURL)
    cur = conn.cursor()
    cur.execute("""
        ALTER TABLE Relationship ADD reversename TEXT;
        """)
    conn.commit()
    conn.close()


def addPageDateAddedField():
    """I think its really required to have a date added field for the pages"""
    conn = db.connect(dbURL)
    cur = conn.cursor()
    conn.execute("""ALTER TABLE Page ADD 'dateadded' TEXT;""")
    conn.execute("""
        UPDATE Page SET dateadded=(SELECT DATE())
        WHERE dateadded IS NULL;""")
    conn.commit()
    conn.close()


def makeRelationshipComments():
    conn = db.connect(dbURL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS RelationshipComments(
            id INTEGER PRIMARY KEY,
            relationshipid INTEGER,
            dateadded TEXT,
            commentdata BLOB,
            FOREIGN KEY( relationshipid ) REFERENCES Relationship(id)
        );
        """)
    conn.commit()
    conn.close()


def makeTopicComments():
    conn = db.connect(dbURL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS TopicComments(
            id INTEGER PRIMARY KEY,
            topicid INTEGER,
            dateadded TEXT,
            commentdata BLOB,
            FOREIGN KEY( topicid ) REFERENCES Topic(id)
        );
        """)
    conn.commit()
    conn.close()


def makePageComments():
    conn = db.connect(dbURL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PageComments(
            id INTEGER PRIMARY KEY,
            pageid INTEGER,
            dateadded TEXT,m
            commentdata BLOB,
            FOREIGN KEY( pageid ) REFERENCES Page(id)
        );
        """)
    conn.commit()
    conn.close()


def makePagePageRelationshipTable():
    conn = db.connect(dbURL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PagePageRelationship(
            id INTEGER PRIMARY KEY,
            relationshipid INTEGER,
            leftpageid INTEGER,
            rightpageid INTEGER,
            FOREIGN KEY( leftpageid ) REFERENCES Page(id),
            FOREIGN KEY( rightpageid ) REFERENCES Page(id),
            FOREIGN KEY( relationshipid ) REFERENCES Relationship(id),
            UNIQUE(relationshipid, leftpageid, rightpageid )
        );
        """)
    conn.commit()
    conn.close()


def addRelationshipNodeType():
    """recreates the Page Topic table to have unique (rel, left, right) triples"""
    conn = db.connect(dbURL)
    cur = conn.cursor()
    cur.execute("""
        ALTER TABLE Relationship ADD nodetype TEXT;
        """)
    conn.commit()
    conn.close()


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
            FOREIGN KEY( relationshipid ) REFERENCES Relationship(id),
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











