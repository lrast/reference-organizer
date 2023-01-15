# topic api

from flask import Blueprint, request, Response
from webapp.db import get_db, packageRows, getTopicGraph, getPagesInTopic


topic = Blueprint('topic', __name__)


@topic.route('/', methods=['GET', 'POST'])
def all_topics():
    """fetching lists of topics"""
    db = get_db()
    if request.method == 'GET':
        # PROCESS query arguments here
        # 
        #
        topicsData = db.execute("SELECT * FROM Topic;").fetchall()
        return packageRows(topicsData)

    if request.method == 'POST':
        name = request.form['name']

        db.execute("INSERT INTO Topic (name) VALUES (?)", (name,))
        db.commit()
        return Response( status=200 )



@topic.route('/<int:topicid>', methods=['GET', 'PUT', 'DELETE'])
def info(topicid):
    """Topic API: info on a specific topic, including pages and pages affiliated with related topics"""
    db = get_db()
    if request.method == 'GET':
        # to do: update to new interface


        #getpages = request.args.get('getpages', True)
        #getlefttopics = request.args.get('getlefttopics', True)
        #getrighttopics = request.args.get('getrighttopics', True)

        topicInfo = db.execute("SELECT * FROM Topic WHERE id=(?)", (topicid,) ).fetchone()

        topicPages = getPagesInTopic(db, topicid,
            request.args.get('fetchThrough', None), request.args.get('onThe', 'left')
            )
        return packageRows(topic=topicInfo, pages=topicPages)


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



@topic.route('/<int:topicid>/page?QUERYPARAMS', methods=['GET', 'POST'])
def related_pages():
    """-> 'affiliated Pages'"""
    db = get_db()
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        pass


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





@topic.route('/<int:topicid>/topic?QUERYPARAMS', methods=['GET', 'POST'])
def related_topics():
    """ -> 'affiliated Topics"""
    pass




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

    nodeType = db.execute("""SELECT nodetype FROM Relationship WHERE id=(?);""",
        (relationshipid,)).fetchone()[0]
    if nodeType != 'topic':
        return Response('Relationship is not betweeen Topics', status=422)

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







