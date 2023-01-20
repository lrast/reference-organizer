# relationship api
# to do: overhaul to make conformant with the new api design

from flask import Blueprint, request, Response
from webapp.db import get_db, packageRows, getTopicGraph


relationship = Blueprint('relationship', __name__)


@relationship.route('/', methods=['GET', 'POST'])
def all_relationships():
    """Relationship API: global relationship data"""
    db = get_db()
    if request.method == 'GET':
        # return info on all relationships
        topicsData = db.execute("SELECT * FROM Relationship;").fetchall()
        return packageRows(topicsData)

    if request.method == 'POST':
        # add a new relationship
        name = request.form['name']
        inserted = db.execute("INSERT INTO Relationship (name) VALUES (?) RETURNING id;", (name,))
        response = packageRows(inserted.fetchone())
        db.commit()
        return response


@relationship.route('/<int:relationshipid>', methods=['GET', 'PUT', 'DELETE'])
def info(relationshipid):
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


