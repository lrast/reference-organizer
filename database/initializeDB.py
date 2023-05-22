# database initialization script
import sqlite3
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

# add some default enries
conn = db.connect(dbURL)
cur = conn.cursor()
cur.execute("""INSERT INTO Topic VALUES ('documentation'), ('organizer');""")
cur.execute("""INSERT INTO Page VALUES (?,?);""", 
    ( (os.path.abspath('../readme.md'), 'readme', date.today().strftime('%Y-%m-%d')),
      ('https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/', 'As We May Think', date.today().strftime('%Y-%m-%d'))
    ))

conn.commit()
conn.close()


