# Page api

from flask import Blueprint, request, Response
from webapp.db import get_db, packageRows, getTopicGraph


page = Blueprint('page', __name__)


@page.route('/', methods=['GET', 'POST'])
def all_pages():
    """Page API: data on all pages"""
    db = get_db()
    if request.method == 'GET':
        # PROCESS query arguments
        # here

        pagesData = db.execute("SELECT * FROM Page;").fetchall()
        return packageRows(pagesData)

    if request.method == 'POST':
        # add a new page
        name = request.form['name']
        url = request.form['url']

        db.execute("INSERT INTO Page (name, url) VALUES (?,?);", (name, url))
        db.commit()
        return Response(status=200 )


@page.route('/<int:pageid>', methods=['GET', 'PUT', 'DELETE'])
def info(pageid):
    """Page API: info on a specific page, including topics and topics related to them"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific page

        # PROCESS query arguments
        # here

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




@page.route('/<int:pageid>/topic?QUERYPARAMS', methods=['GET', 'POST'])
def related_topics():
    """ -> 'affiliated Topics"""
    pass



@page.route('/<int:pageid>/topic/<int:relatedtopicid>', methods=['PUT', 'DELETE'])
def related_topics_id(pageid, relatedtopicid):
    """Page Topic Association"""
    db = get_db()
    if request.method == 'PUT':
        db.execute("INSERT INTO PageTopic(pageid, topicid) VALUES (?,?);",
            (pageid, relatedtopicid))
    elif request.method == 'DELETE':
        db.execute("DELETE FROM PageTopic WHERE pageid=(?) AND topicid=(?);", (pageid, relatedtopicid))

    db.commit()
    return Response(status=200)




@page.route('/<int:pageid>/page?QUERYPARAMS', methods=['GET', 'POST'])
def related_pages():
    """-> 'affiliated Pages'"""
    pass



@page.route('/<int:pageid>/page/<int:relatedpageid>', methods=['PUT', 'DELETE'])
def related_pages_id(pageid, relatedpageid):
    """Page Page Association"""
    db = get_db()

    relationshipid = request.args.get('relationshipid', 2)
    primaryside = request.args.get('primaryside', 'left')

    if primaryside == 'left':
        leftpageid = pageid
        rightpageid = relatedpageid
    if primaryside == 'right':
        leftpageid = relatedpageid
        rightpageid = pageid

    nodeType = db.execute("""SELECT nodetype FROM Relationship WHERE id=(?)""",
        (relationshipid,)).fetchone()[0]
    if nodeType != 'page':
        return Response('Relationship is not betweeen Page',status=422)

    if request.method == 'PUT':
        entryData = db.execute("""
            INSERT INTO PagePageRelationship(relationshipid, leftpageid, rightpageid)
            VALUES (?,?,?);""",
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







