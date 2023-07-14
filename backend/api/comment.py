# comments api
import json

from flask import Blueprint, request, Response
from database.oldInterface import get_db, packageRows


comment = Blueprint('comment', __name__)


@comment.route('/page/<int:pageid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def page(pageid):
    return processCommentRequest('PageComments', 'pageid', pageid, request)


@comment.route('/topic/<int:topicid>',
               methods=['GET', 'POST', 'PUT', 'DELETE'])
def topic(topicid):
    return processCommentRequest('TopicComments', 'topicid', topicid, request)


@comment.route('/relationship/<int:relationshipid>',
               methods=['GET', 'POST', 'PUT', 'DELETE'])
def relationship(relationshipid):
    return processCommentRequest('RelationshipComments', 'relationshipid', 
                                 relationshipid, request)


def processCommentRequest(tableName, colName, elementid, request):
    """Generic utility for processing comment requests"""
    db = get_db()
    if request.method == 'POST' or request.method == 'PUT':
        requestData = json.loads(request.data)

    if request.method == 'GET':
        comments = db.execute(
                f"SELECT * FROM {tableName} WHERE {colName}=(?);",
                (elementid,)
            ).fetchall()
        return packageRows(comments)

    if request.method == 'POST':
        commentdata = requestData['commentdata']
        db.execute(
            """INSERT INTO {tableName}({colName}, dateadded, commentdata) VALUES 
            (?, (SELECT DATE()), ?);""".format(tableName=tableName, colName=colName),
             (elementid, commentdata))

    if request.method == 'PUT':
        commentid = request.args['commentid']
        commentdata = requestData['commentdata']
        db.execute(
            """INSERT OR REPLACE INTO {tableName}(id, {colName}, dateadded, commentdata)
            VALUES (?, ?, (SELECT DATE()), ?);""".format(tableName=tableName, colName=colName),
             (commentid, elementid, commentdata))

    if request.method == 'DELETE':
        commentid = request.args['commentid']
        db.execute(
            "DELETE FROM {tableName} WHERE id=(?);".format(tableName=tableName),
            (commentid,))

    db.commit()
    return Response(status=200)
