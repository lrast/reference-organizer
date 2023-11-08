# database initialization script
import sqlite3 as db
import os
from datetime import date

from migrations import *

# run the migrations in order
makeInitialTables()
addPageName()
remakePageTopic()
remakeTopicTopic()
addRelationshipNodeType()
makePagePageRelationshipTable()
makePageComments()
makeTopicComments()
makeRelationshipComments()
addPageDateAddedField()
addRelationshipReversename()
remakePageTable()
makeAuthorTable()

# add some default enries
conn = db.connect(dbURL)
cur = conn.cursor()
cur.execute("""INSERT INTO Topic(name)
              VALUES ('documentation'), ('organizer');""")
cur.executemany("""INSERT INTO Page(url, name, dateadded)
                   VALUES (?,?,?);""", [
    (os.path.abspath('../readme.md'), 'readme',
     date.today().strftime('%Y-%m-%d')),
    ('https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/',
     'As We May Think', date.today().strftime('%Y-%m-%d'))
    ])
cur.executemany("""INSERT INTO PageTopic(pageid, topicid) VALUES (?,?)""", 
                [(1, 1), (1, 2), (2, 2)])
conn.commit()
conn.close()
