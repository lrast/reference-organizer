import json
import requests

from flask import request, Response, Blueprint, url_for

from webapp.db import get_db, getPagesInTopic, getTopicGraph, packageRows
from webapp.utilities import isURLWebOrLocal

api = Blueprint('api', __name__)


@api.route('/page', methods=['GET', 'POST'])
def allPages():
    """Page API: data on all pages"""
    db = get_db()
    if request.method == 'GET':
        # return info on all pages
        pagesData = db.execute("SELECT * FROM Page;").fetchall()
        return packageRows(pagesData)

    if request.method == 'POST':
        # add a new page
        name = request.form['name']
        url = request.form['url']

        entryData = db.execute("INSERT INTO Page (name, url) VALUES (?,?) RETURNING id", 
            (name, url)).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200 )


@api.route('/page/<int:pageid>', methods=['GET', 'PUT', 'DELETE'])
def pageInfo(pageid):
    """Page API: info on a specific page, including topics and topics related to them"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific page
        pageInfo = db.execute("SELECT * FROM Page WHERE id=(?)", (pageid,)).fetchone()

        pageTopics = db.execute(
            """SELECT Topic.id, Topic.name FROM 
            Topic INNER JOIN PageTopic ON Topic.id = PageTopic.topicid
            WHERE PageTopic.pageid =(?)
            """, (pageid,)).fetchall()
        return packageRows(page=pageInfo, topics=pageTopics)

    if request.method == 'PUT':
        # over write the contents of the entry
        if 'name' in request.form.keys():
            db.execute("UPDATE Page SET name=(?) WHERE id=(?);", (request.form['name'], pageid) )
        if 'url' in request.form.keys():
            db.execute("UPDATE Page SET url=(?) WHERE id=(?);", (request.form['url'], pageid) )
        db.commit()
        return Response(status=200)

    if request.method == 'DELETE':
        db.execute("DELETE FROM Page WHERE id=(?);", (pageid,))
        db.execute("DELETE FROM PageTopic WHERE pageid=(?);", (pageid,))
        db.commit()
        return Response(status=200)



@api.route('/topic', methods=['GET', 'POST'])
def allTopics():
    """Topic API: data on all topics"""
    db = get_db()
    if request.method == 'GET':
        # return info on all topics
        topicsData = db.execute("SELECT * FROM Topic;").fetchall()
        return packageRows(topicsData)

    if request.method == 'POST':
        # add a new topic
        name = request.form['name']

        entryData = db.execute("INSERT INTO Topic (name) VALUES (?) RETURNING id", 
            (name,)).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200 )


@api.route('/topic/<int:topicid>', methods=['GET', 'PUT', 'DELETE'])
def topicInfo(topicid):
    """Topic API: info on a specific topic, including pages and pages affiliated with related topics"""
    db = get_db()
    if request.method == 'GET':
        topicInfo = db.execute("SELECT * FROM Topic WHERE id=(?)", (topicid,) ).fetchone()

        topicPages = getPagesInTopic(db, topicid,
            request.args.get('fetchThrough', None), request.args.get('onThe', 'left')
            )
        return packageRows(topic=topicInfo, pages=topicPages)

    if request.method == 'PUT':
        # over write the contents of the entry
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



@api.route('/relationship', methods=['GET', 'POST'])
def allRelationships():
    """Relationship API: global relationship data"""
    db = get_db()
    if request.method == 'GET':
        # return info on all relationships
        topicsData = db.execute("SELECT * FROM Relationship;").fetchall()
        return packageRows(topicsData)

    if request.method == 'POST':
        # add a new relationship
        name = request.form['name']

        entryData = db.execute("INSERT INTO Relationship (name) VALUES (?) RETURNING id", 
            (name,)).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200 )


@api.route('/relationship/<int:relationshipid>', methods=['GET', 'PUT', 'DELETE'])
def relationshipInfo(relationshipid):
    """Relationship API: info on specific relationships, including topic pairs and trees"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific relationship
        relationshipInfo = db.execute("SELECT * FROM Relationship WHERE id=(?)", (relationshipid,) ).fetchone()

        if 'fetchThrough' in request.args:
            topicDepth = float('inf')
        else:
            topicDepth = 1

        topicPairs = getTopicGraph(db, relationshipid, rootedAt=request.args.get('topic', None),
            onThe=request.args.get('onThe', 'left'), depth=topicDepth)

        return packageRows(relationship=relationshipInfo, topics=topicPairs)

    if request.method == 'PUT':
        # over write the contents of the entry
        if 'name' in request.form.keys():
            db.execute("UPDATE Relationship SET name=(?) WHERE id=(?);", (request.form['name'], relationshipid) )
        db.commit()
        return Response(status=200)

    if request.method == 'DELETE':
        db.execute("DELETE FROM Relationship WHERE id=(?)", (relationshipid,))
        db.execute("DELETE FROM TopicTopicRelationship WHERE relationshipid=(?)", (relationshipid,) )
        db.commit()
        return Response(status=200)


@api.route('/comments/page/<int:pageid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def pageComments(pageid):
    db = get_db()

    if request.method == 'POST' or request.method == 'PUT':
        print('here')
        requestData = json.loads(request.data)
        print(requestData)

    if request.method == 'GET':
        comments = db.execute("SELECT * FROM PageComments WHERE pageid=(?);", (pageid,)).fetchall()
        return packageRows(comments)

    if request.method == 'POST':
        commentdata = requestData['commentdata']
        db.execute("""INSERT INTO PageComments(pageid, dateadded, commentdata) VALUES 
            (?, (SELECT DATE()), ?);""", (pageid, commentdata))

    if request.method == 'PUT':
        commentid = request.args['commentid']
        commentdata = requestData['commentdata']
        db.execute("""INSERT OR REPLACE INTO PageComments(id, pageid, dateadded, commentdata)
            VALUES (?, ?, (SELECT DATE()), ?);""", (commentid, pageid, commentdata))

    if request.method == 'DELETE':
        print('Called DELETE')
        commentid = request.args['commentid']
        db.execute("DELETE FROM PageComments WHERE id=(?);", (commentid,))

    db.commit()
    return Response(status=200)


@api.route('/comments/topic/<int:topicid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def topicComments(topicid):
    db = get_db()

    if request.method == 'POST' or request.method == 'PUT':
        requestData = json.loads(request.data)

    if request.method == 'GET':
        comments = db.execute("SELECT * FROM TopicComments WHERE topicid=(?);", (topicid,)).fetchall()
        return packageRows(comments)

    if request.method == 'POST':
        commentdata = requestData['commentdata']
        db.execute("""INSERT INTO TopicComments(topicid, dateadded, commentdata) VALUES 
            (?, (SELECT DATE()), ?);""", (topicid, commentdata))

    if request.method == 'PUT':
        commentid = request.args['commentid']
        commentdata = requestData['commentdata']
        db.execute("""INSERT OR REPLACE INTO TopicComments(id, topicid, dateadded, commentdata)
            VALUES (?, ?, (SELECT DATE()), ?);""", (commentid, topicid, commentdata))

    if request.method == 'DELETE':
        commentid = request.args['commentid']
        db.execute("DELETE FROM TopicComments WHERE id=(?);", (commentid,))

    db.commit()
    return Response(status=200)


@api.route('/comments/page/<int:pageid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def relationshipComments(relationshipid):
    db = get_db()

    if request.method == 'POST' or request.method == 'PUT':
        requestData = json.loads(request.data)

    if request.method == 'GET':
        comments = db.execute("SELECT * FROM RelationshipComments WHERE relationshipid=(?);",
            (relationshipid,))
        return packageRows(comments)

    if request.method == 'POST':
        commentdata = requestData['commentdata']
        db.execute("""INSERT INTO RelationshipComments(relationshipid, dateadded, commentdata) VALUES 
            (?, (SELECT DATE()), ?);""", (relationshipid, commentdata))

    if request.method == 'PUT':
        commentid = request.args['commentid']
        commentdata = requestData['commentdata']
        db.execute("""INSERT OR REPLACE INTO RelationshipComments(id, relationshipid, dateadded, commentdata)
            VALUES (?, ?, (SELECT DATE()), ?);""", (commentid, relationshipid, commentdata))

    if request.method == 'DELETE':

        commentid = request.args['commentid']
        db.execute("DELETE FROM RelationshipComments WHERE id=(?);", (commentid,))

    db.commit()
    return Response(status=200)





######################################### Association Tables #########################################

@api.route('/assoc_page_topic', methods=['POST', 'DELETE'])
def associatePageTopic():
    db = get_db()
    pageid = request.args['pageid']
    topicid = request.args['topicid']

    if request.method == 'POST':
        entryData = db.execute("INSERT INTO PageTopic(pageid, topicid) VALUES (?,?) RETURNING id;",
            (pageid, topicid)).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200)

    elif request.method == 'DELETE':
        db.execute("DELETE FROM PageTopic WHERE pageid=(?) AND topicid=(?);", (pageid, topicid))
        db.commit()
        return Response(status=200)


@api.route('/assoc_topic_topic', methods=['POST', 'DELETE'])
def associateTopicTopic():
    db = get_db()
    lefttopicid = request.args['lefttopicid']
    righttopicid = request.args['righttopicid']
    relationshipid = request.args['relationshipid']

    nodeType = db.execute("""SELECT nodetype FROM Relationship WHERE id=(?)""",
        (relationshipid,)).fetchone()[0]
    if nodeType != 'topic':
        return Response('Relationship is not betweeen Topics',status=422)

    if request.method == 'POST':
        entryData = db.execute("""
            INSERT INTO TopicTopicRelationship(relationshipid, lefttopicid, righttopicid)
            VALUES (?,?,  ?) RETURNING id;""",
            (relationshipid, lefttopicid, righttopicid) ).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200)

    elif request.method == 'DELETE':
        db.execute(
            """ DELETE FROM TopicTopicRelationship WHERE 
            relationshipid=(?) AND lefttopicid=(?) AND righttopicid=(?);""",
            (relationshipid, lefttopicid, righttopicid))
        db.commit()
        return Response(status=200)


@api.route('/assoc_page_page', methods=['POST', 'DELETE'])
def associatePagePage():
    db = get_db()
    leftpageid = request.args['leftpageid']
    rightpageid = request.args['rightpageid']
    relationshipid = request.args['relationshipid']

    nodeType = db.execute("""SELECT nodetype FROM Relationship WHERE id=(?)""",
        (relationshipid,)).fetchone()[0]
    if nodeType != 'page':
        return Response('Relationship is not betweeen Page',status=422)

    if request.method == 'POST':
        entryData = db.execute("""
            INSERT INTO PagePageRelationship(relationshipid, leftpageid, rightpageid)
            VALUES (?,?,?) RETURNING id;""",
            (relationshipid, leftpageid, rightpageid) ).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200)

    elif request.method == 'DELETE':
        db.execute(
            """ DELETE FROM PagePageRelationship WHERE 
            relationshipid=(?) AND leftpageid=(?) AND rightpageid=(?);""",
            (relationshipid, leftpageid, rightpageid))
        db.commit()
        return Response(status=200)


# 
@api.route('/getWebpageTitle', methods=['POST'])
def getWebpageTitle():
    """Fetches the title for webpages"""
    try:
        url = request.data.decode()

        if len(url) == 0:
            return Response('', status=200)

        URLsource, formattedURL = isURLWebOrLocal(url)
        if URLsource != "web":
            return Response('', status=200)

        resp = requests.get(formattedURL)
        if resp.status_code != 200:
            return Response('', status=200)

        workingTitle = ( resp.content.split(b'title>')[1][:-2] ).decode()

        return Response(workingTitle, status=200)

    except:
        return Response('', status=200)


