# topic api
import json
import sqlite3

from flask import Blueprint, request, Response
from database.oldInterface import get_db, packageRows

from backend.api.utilities import checkNodeType, getPOSTData
from backend.api.graphQL import execute_gql_query


topic = Blueprint('topic', __name__)



@topic.route('/', methods=['GET', 'POST'])
def all_topics():
    """fetching lists of topics"""
    db = get_db()

    if request.method == 'GET':
        subquery = request.args.get( 'query', '{ id, name }' )
        return execute_gql_query('{ topics' + subquery + '}', lambda x: x['topics'])

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
        default_subquery = """{ 
                    id, name,
                    pages {id, name}, 
                    leftTopics {id, name}, 
                    rightTopics { id, name }
                    }"""

        subquery = request.args.get('query', default_subquery)
        gql_query = '{ topics (id: %s)'%topicid + subquery + '}'
        return execute_gql_query(gql_query, lambda x:x['topics'][0])

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
        subquery = request.args.get('query', '{id, name}')
        gql_query = '{ topics (id: %s) { pages '%topicid + subquery + '} }'

        return execute_gql_query(gql_query, lambda x:x['topics'][0]['pages'])

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
        subquery = request.args.get( 'query', '{ id, name }' )

        gql_query = ('{topics (id: %s) { rightTopics'%topicid + 
            subquery + 
            ', leftTopics' +
            subquery + 
            '} }')

        return execute_gql_query(gql_query, lambda x: x['topics'][0] )

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

