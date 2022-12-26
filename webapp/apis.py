from flask import request, Response

from webapp import app
from webapp.db import get_db, packageRows



########################################### APIs ###########################################

@app.route('/page', methods=['GET', 'POST'])
def allPages():
    """Page API"""
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
    """Page API"""
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
    """Topic API"""
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
    """Topic API"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific topic
        topicInfo = db.execute("SELECT * FROM Topic WHERE id=(?)", (topicid,) ).fetchone()
        topicPages = db.execute(
            """SELECT Page.id, Page.name FROM 
            Page INNER JOIN PageTopic ON Page.id = PageTopic.pageid
            WHERE PageTopic.topicid =(?)
            """, (topicid,)).fetchall()

        if 'fetchThrough' in request.args:
            relationshipid = request.args['fetchThrough']
            onThe = request.args.get('onThe', 'left')

            if onThe == 'left':
                allPages = db.execute("""
                    WITH RECURSIVE AllRelated(topicid) AS (
                        SELECT (?)
                        UNION
                        SELECT DISTINCT TopicTopicRelationship.lefttopicid FROM
                        TopicTopicRelationship INNER JOIN AllRelated ON
                        TopicTopicRelationship.righttopicid = AllRelated.topicid
                        LIMIT 10000
                    )
                    SELECT Page.id, Page.name, PageTopic.topicid, Topic.name AS topicname FROM Page INNER JOIN 
                    PageTopic ON Page.id=PageTopic.pageid INNER JOIN
                    AllRelated ON PageTopic.topicid=AllRelated.topicid INNER JOIN
                    Topic ON PageTopic.topicid=Topic.id;
                    """, (topicid,)).fetchall()
            elif onThe == 'right':
                allPages = db.execute("""
                    WITH RECURSIVE AllRelated(topicid) AS (
                        SELECT (?)
                        UNION
                        SELECT DISTINCT TopicTopicRelationship.righttopicid FROM
                        TopicTopicRelationship INNER JOIN AllRelated ON
                        TopicTopicRelationship.lefttopicid = AllRelated.topicid
                        LIMIT 10000
                    )
                    SELECT Page.id, Page.name, PageTopic.topicid, Topic.name AS topicname FROM Page INNER JOIN 
                    PageTopic ON Page.id=PageTopic.pageid INNER JOIN
                    AllRelated ON PageTopic.topicid=AllRelated.topicid INNER JOIN
                    Topic ON PageTopic.topicid=Topic.id;
                    """, (topicid,)).fetchall()

            topicPages = allPages
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
    """Relationship API"""
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
    """Relationship API"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific relationship
        relationshipInfo = db.execute("SELECT * FROM Relationship WHERE id=(?)", (relationshipid,) ).fetchone()

        if 'topic' in request.args:
            topicid = request.args['topic']
            myside = request.args.get('myside', 'right')

            if myside == 'left':
                relatedTopics = db.execute(
                    """SELECT Topic.id, Topic.name FROM Topic JOIN TopicTopicRelationship
                    ON Topic.id=TopicTopicRelationship.righttopicid WHERE 
                    TopicTopicRelationship.lefttopicid=(?) AND TopicTopicRelationship.relationshipid=(?);
                    """, (topicid, relationshipid) ).fetchall()

            if myside == 'right':
                relatedTopics = db.execute(
                    """SELECT Topic.id, Topic.name FROM Topic JOIN TopicTopicRelationship
                    ON Topic.id=TopicTopicRelationship.lefttopicid WHERE 
                    TopicTopicRelationship.righttopicid=(?) AND TopicTopicRelationship.relationshipid=(?);
                    """, (topicid, relationshipid) ).fetchall()

            return packageRows(relationship=relationshipInfo, topics=relatedTopics)

        else:
            topicPairs = db.execute(
                """SELECT lefttopicid, righttopicid FROM 
                TopicTopicRelationship WHERE relationshipid =(?)
                """, (relationshipid,)).fetchall()
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



