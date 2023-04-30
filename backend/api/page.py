# Page api
import json
import sqlite3

from datetime import datetime

from flask import Blueprint, request, Response

from database.oldInterface import get_db, packageRows
from backend.api.utilities import checkNodeType, getPOSTData
from backend.api.graphQL import execute_gql_query

page = Blueprint('page', __name__)


@page.route('/', methods=['GET', 'POST'])
def all_pages():
    """Page API: data on all pages"""
    db = get_db()
    if request.method == 'GET':
        subquery = request.args.get('query', '{id, name, url, dateadded}')
        gql_query = '{pages'  + subquery + '}'
        return execute_gql_query(gql_query, lambda x:x['pages'])

    if request.method == 'POST':
        # add a new page
        receivedData = getPOSTData(request)
        name = receivedData['name']
        url = receivedData['url']
        date = receivedData.get('date', datetime.today().strftime('%Y-%m-%d'))

        try:
            inserted = db.execute("""INSERT INTO Page (name, url, dateadded) 
                VALUES (?,?, ?) RETURNING id;""", (name, url, date))
            response = packageRows(inserted.fetchone())
            db.commit()
            return response

        except sqlite3.IntegrityError:
            existing = db.execute("""SELECT id FROM Page WHERE url=(?)""", (url,))
            response = packageRows(existing.fetchone())
            return response, 303



@page.route('/<int:pageid>', methods=['GET', 'PUT', 'DELETE'])
def info(pageid):
    """Page API: info on a specific page, including topics and topics related to them"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific page
        default_subquery = """{ 
                    id, name, url, dateadded
                    topics {id, name}, 
                    leftPages {id, name}, 
                    rightPages { id, name }
                    }"""

        subquery = request.args.get('query', default_subquery)
        gql_query = '{pages (id: %s)'%pageid + subquery + '}'
        return execute_gql_query(gql_query, lambda x:x['pages'][0])

    if request.method == 'PUT':
        # over write the contents of the entry
        receivedData = getPOSTData(request)

        if 'name' in receivedData.keys():
            db.execute("UPDATE Page SET name=(?) WHERE id=(?);", (receivedData['name'], pageid) )
        if 'url' in receivedData.keys():
            db.execute("UPDATE Page SET url=(?) WHERE id=(?);", (receivedData['url'], pageid) )

        db.commit()
        return Response(status=200)

    if request.method == 'DELETE':
        db.execute("DELETE FROM Page WHERE id=(?);", (pageid,))
        db.execute("DELETE FROM PageTopic WHERE pageid=(?);", (pageid,))
        db.execute("DELETE FROM PagePageRelationship WHERE leftpageid=(?) OR rightpageid=(?);", 
            (pageid, pageid))
        db.commit()
        return Response(status=200)



@page.route('/<int:pageid>/topic', methods=['GET', 'POST'])
def related_topics(pageid):
    """More involved selections of topis that relate to the page"""
    db = get_db()
    if request.method == 'GET':
        subquery = request.args.get('query', '{ id, name }')
        gql_query = '{ pages (id: %s) { topics'%pageid + subquery + '} }'
        return execute_gql_query(gql_query, lambda x:x['pages'][0]['topics'])

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



@page.route('/<int:pageid>/page', methods=['GET', 'POST'])
def related_pages(pageid):
    """More involved selections of pages that relate to the page"""
    db = get_db()
    if request.method == 'GET':

        subquery = request.args.get('query', '{id, name}')
        gql_query = ('{ pages (id: %s) { leftPages '%pageid + 
            subquery + 
            ', rightPages' + 
            subquery +
            '} }' )
        return execute_gql_query(gql_query, lambda x:x['pages'][0])

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



