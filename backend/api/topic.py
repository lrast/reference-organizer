# topic api
import json
import sqlite3

from flask import Blueprint, request, Response
from database.oldInterface import get_db, packageRows

from backend.api.utilities import checkNodeType, getPOSTData


topic = Blueprint('topic', __name__)



@topic.route('/', methods=['GET', 'POST'])
def all_topics():
    """fetching lists of topics"""
    db = get_db()

    if request.method == 'GET':
        # PROCESS query arguments here
        if 'rootOnly' in request.args and bool(request.args['rootOnly']):
            topicsData = db.execute("""
                SELECT * FROM Topic WHERE Topic.id NOT IN (SELECT lefttopicid FROM TopicTopicRelationship);
                """).fetchall()
            return packageRows(topicsData)

        topicsData = db.execute("SELECT * FROM Topic;").fetchall()
        return packageRows(topicsData)

    if request.method == 'POST':
        name = getPOSTData(request)['name']

        try:
            inserted = db.execute("INSERT INTO Topic(name) VALUES (?) RETURNING id", (name,))
            response = packageRows(inserted.fetchone())
            db.commit()
        except sqlite3.IntegrityError:
            existing = db.execute("SELECT id FROM Topic WHERE name=(?);", (name,))
            response = packageRows(existing.fetchone())

        return response


@topic.route('/<int:topicid>', methods=['GET', 'PUT', 'DELETE'])
def info(topicid):
    """all info on a specific topic, including affiliated pages and topics"""
    db = get_db()
    if request.method == 'GET':
        topicInfo = db.execute("SELECT * FROM Topic WHERE id=(?)", (topicid,) ).fetchone()

        if bool(request.args.get('infoOnly', '')):
            return packageRows(topic=topicInfo)

        topicPages = getPagesInTopic(db, topicid, selectThrough=None)
        leftTopics = db.execute(
            """
            SELECT Topic.name, TopicTopicRelationship.lefttopicid,
            TopicTopicRelationship.relationshipid
            FROM TopicTopicRelationship INNER JOIN Topic ON
            TopicTopicRelationship.lefttopicid = Topic.id WHERE
            TopicTopicRelationship.righttopicid=(?);
            """,
            (topicid,)).fetchall()
        rightTopics = db.execute(
            """
            SELECT Topic.name, TopicTopicRelationship.righttopicid,
            TopicTopicRelationship.relationshipid
            FROM TopicTopicRelationship INNER JOIN Topic ON
            TopicTopicRelationship.righttopicid = Topic.id WHERE 
            TopicTopicRelationship.lefttopicid=(?);
            """,
            (topicid,)).fetchall()

        return packageRows(topic=topicInfo, pages=topicPages, leftTopics=leftTopics,
            rightTopics=rightTopics)

    if request.method == 'PUT':
        if 'name' in request.form.keys():
            db.execute("UPDATE Topic SET name=(?) WHERE id=(?);", (request.form['name'], topicid) )
        db.commit()
        return Response(status=200)

    if request.method == 'DELETE':
        db.execute("DELETE FROM Topic WHERE id=(?)", (topicid,))
        db.execute("DELETE FROM PageTopic WHERE topicid=(?);", (topicid,))
        db.execute("DELETE FROM TopicTopicRelationship WHERE lefttopicid=(?) OR righttopicid=(?)", 
            (topicid, topicid))
        db.commit()
        return Response(status=200)


@topic.route('/<int:topicid>/page', methods=['GET', 'POST'])
def related_pages(topicid):
    """More involved selections of pages that relate to the topic"""
    db = get_db()
    if request.method == 'GET':
        selectThrough = request.args.get('selectThrough', None)
        onThe = request.args.get('onThe', 'left')

        pages = getPagesInTopic(db, topicid, selectThrough, onThe)

        return packageRows(pages)

    if request.method == 'POST':
        pageid = getPOSTData(request)['pageid']

        inserted = db.execute("""
            INSERT INTO PageTopic(pageid, topicid) VALUES (?,?) RETURNING id;
            """, (pageid, topicid))
        response = packageRows(inserted.fetchone())
        db.commit()
        return response


@topic.route('/<int:topicid>/page/<int:relatedpageid>', methods=['PUT', 'DELETE'])
def related_pages_id(topicid, relatedpageid):
    """Page Topic Association"""
    db = get_db()
    if request.method == 'PUT':
        db.execute("INSERT INTO PageTopic(pageid, topicid) VALUES (?,?);", (relatedpageid, topicid))
    elif request.method == 'DELETE':
        db.execute("DELETE FROM PageTopic WHERE pageid=(?) AND topicid=(?);", (relatedpageid, topicid))

    db.commit()
    return Response(status=200)


@topic.route('/<int:topicid>/topic', methods=['GET', 'POST'])
def related_topics(topicid):
    """More involved selections of topis that relate to the topic"""
    db = get_db()
    if request.method == 'GET':
        # PROCESS query arguments here
        leftTopics = db.execute(
            """
            SELECT Topic.name, TopicTopicRelationship.lefttopicid,
            TopicTopicRelationship.relationshipid
            FROM TopicTopicRelationship INNER JOIN Topic ON
            TopicTopicRelationship.lefttopicid = Topic.id WHERE
            TopicTopicRelationship.righttopicid=(?);
            """,
            (topicid,)).fetchall()
        rightTopics = db.execute(
            """
            SELECT Topic.name, TopicTopicRelationship.righttopicid,
            TopicTopicRelationship.relationshipid
            FROM TopicTopicRelationship INNER JOIN Topic ON
            TopicTopicRelationship.righttopicid = Topic.id WHERE 
            TopicTopicRelationship.lefttopicid=(?);
            """,
            (topicid,)).fetchall()

        return packageRows(leftTopics=leftTopics, rightTopics=rightTopics)

    if request.method == 'POST':
        relatedtopicid = getPOSTData(request)['relatedtopicid']

        relationshipid = request.values['relationshipid']
        side = request.values['side']

        ok, resp = checkNodeType(db, relationshipid, 'topic')
        if not ok:
            return resp

        if side == 'left':
            inserted = db.execute("""
                INSERT INTO TopicTopicRelationship(relationshipid, lefttopicid, righttopicid)
                VALUES (?,?,?) RETURNING id;""", (relationshipid, relatedtopicid, topicid) )

        if side == 'right':
            inserted = db.execute("""
                INSERT INTO TopicTopicRelationship(relationshipid, righttopicid, lefttopicid)
                VALUES (?,?,?) RETURNING id;""", (relationshipid, relatedtopicid, topicid) )

        response = packageRows(inserted.fetchone())
        db.commit()
        return response


@topic.route('/<int:topicid>/topic/<int:relatedtopicid>', methods=['PUT', 'DELETE'])
def related_topics_id(topicid, relatedtopicid):
    """Topic Topic relationships"""
    db = get_db()
    relationshipid = request.args.get('relationshipid', 1)
    primaryside = request.args.get('primaryside', 'left')

    if primaryside == 'left':
        lefttopicid = topicid
        righttopicid = relatedtopicid
    if primaryside == 'right':
        lefttopicid = relatedtopicid
        righttopicid = topicid

    ok, resp = checkNodeType(db, relationshipid, 'topic')
    if not ok:
        return resp

    if request.method == 'PUT':
        db.execute("""
            INSERT INTO TopicTopicRelationship(relationshipid, lefttopicid, righttopicid)
            VALUES (?,?,?);""", (relationshipid, lefttopicid, righttopicid) )

    elif request.method == 'DELETE':
        db.execute(
            """ DELETE FROM TopicTopicRelationship WHERE 
            relationshipid=(?) AND lefttopicid=(?) AND righttopicid=(?);""",
            (relationshipid, lefttopicid, righttopicid))

    db.commit()
    return Response(status=200)




########################################### Utilities ###########################################

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







