# database initialization script
import sqlite3

from migrations import *

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

