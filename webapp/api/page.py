# Page api
import json

from datetime import datetime

from flask import Blueprint, request, Response

from webapp.db import get_db, packageRows, getTopicGraph
from webapp.api.utilities import checkNodeType, getPOSTData


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
        receivedData = getPOSTData(request)
        name = receivedData['name']
        url = receivedData['url']
        date = receivedData.get('date', datetime.today().strftime('%Y-%m-%d'))

        inserted = db.execute("""INSERT INTO Page (name, url, dateadded) 
            VALUES (?,?, ?) RETURNING id;""", (name, url, date))
        response = packageRows(inserted.fetchone())
        db.commit()
        return response


@page.route('/<int:pageid>', methods=['GET', 'PUT', 'DELETE'])
def info(pageid):
    """Page API: info on a specific page, including topics and topics related to them"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific page
        pageInfo = db.execute("SELECT * FROM Page WHERE id=(?)", (pageid,)).fetchone()

        if bool(request.args.get('infoOnly', '')):
            return packageRows(page=pageInfo)

        pageTopics = db.execute(
            """SELECT Topic.id, Topic.name FROM 
            Topic INNER JOIN PageTopic ON Topic.id = PageTopic.topicid
            WHERE PageTopic.pageid =(?)
            """, (pageid,)).fetchall()
        leftPages = db.execute(
            """
            SELECT Page.name, PagePageRelationship.leftpageid,
            PagePageRelationship.relationshipid
            FROM PagePageRelationship INNER JOIN Page 
            ON PagePageRelationship.leftpageid = Page.id
            WHERE PagePageRelationship.rightpageid=(?);
            """, (pageid,)).fetchall()
        rightPages = db.execute(
            """
            SELECT Page.name, PagePageRelationship.rightpageid,
            PagePageRelationship.relationshipid
            FROM PagePageRelationship INNER JOIN Page 
            ON PagePageRelationship.rightpageid = Page.id
            WHERE PagePageRelationship.leftpageid=(?);
            """, (pageid,)).fetchall()

        return packageRows(page=pageInfo, topics=pageTopics, leftPages=leftPages, rightPages=rightPages)

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




@page.route('/<int:pageid>/topic', methods=['GET', 'POST'])
def related_topics(pageid):
    """More involved selections of topis that relate to the page"""
    db = get_db()
    if request.method == 'GET':
        # PROCESS query arguments here
        pass

    if request.method == 'POST':
        topicid = getPOSTData(request)['topicid']

        inserted = db.execute("""INSERT INTO PageTopic(pageid, topicid) VALUES (?,?) RETURNING id;""", 
            (pageid, topicid))
        response = packageRows(inserted.fetchone())
        db.commit()
        return response



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
    """More involved selections of pages that relate to the page"""
    db = get_db()
    if request.method == 'GET':
        # PROCESS query arguments here
        pass

    if request.method == 'POST':
        receivedData = getPOSTData(request)

        relatedpageid = receivedData['relatedpageid']
        relationshipid = receivedData['relationshipid']
        side = receivedData['side']

        ok, resp = checkNodeType(db, relationshipid, 'page')
        if not ok:
            return resp

        if side == 'left':
            db.execute("""
                INSERT INTO PagePageRelationship(relationshipid, lefttopicid, righttopicid)
                VALUES (?,?,?);""", (relationshipid, relatedtopicid, topicid) )

        if side == 'right':
            db.execute("""
                INSERT INTO PagePageRelationship(relationshipid, righttopicid, lefttopicid)
                VALUES (?,?,?);""", (relationshipid, relatedtopicid, topicid) )





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

    ok, resp = checkNodeType(db, relationshipid, 'page')
    if not ok:
        return resp

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



