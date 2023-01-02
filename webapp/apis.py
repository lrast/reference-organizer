from flask import request, Response,url_for

from webapp import app
from webapp.db import get_db, getPagesInTopic, getTopicGraph, packageRows



########################################### APIs ###########################################

@app.route('/page', methods=['GET', 'POST'])
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


@app.route('/page/<int:pageid>', methods=['GET', 'PUT', 'DELETE'])
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



@app.route('/topic', methods=['GET', 'POST'])
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


@app.route('/topic/<int:topicid>', methods=['GET', 'PUT', 'DELETE'])
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



@app.route('/relationship', methods=['GET', 'POST'])
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


@app.route('/relationship/<int:relationshipid>', methods=['GET', 'PUT', 'DELETE'])
def relationshipInfo(relationshipid):
    """Relationship API: info on specific relationships, including topic pairs and trees"""
    db = get_db()
    print(url_for('relationshipInfo', relationshipid=1, topic=1, _external=True))
    print(request.args.keys())
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



@app.route('/info', methods=['GET', 'POST', 'PUT'])
def informationOnPages():
    pass







######################################### Association Tables #########################################

@app.route('/assoc_page_topic', methods=['POST', 'DELETE'])
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


@app.route('/assoc_topic_topic', methods=['POST', 'DELETE'])
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


@app.route('/assoc_page_page', methods=['POST', 'DELETE'])
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



