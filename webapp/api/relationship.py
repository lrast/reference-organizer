# relationship api
# to do: overhaul to make conformant with the new api design

from flask import Blueprint, request, Response
from webapp.db import get_db, packageRows


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


        # check if the relationship is over topics or pages


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




########################################### Utilities ###########################################

def getTopicGraph(db, relationshipid, rootedAt=None, onThe='right', depth=float('inf')):
    """Fetch a topic graph / subgraph """

    if rootedAt is None: # return the whole graph
        return db.execute(
            """SELECT TopicTopicRelationship.lefttopicid, TopicTopicRelationship.righttopicid,
            LeftTopic.name AS leftname, RightTopic.name AS rightname FROM TopicTopicRelationship
            JOIN Topic AS LeftTopic ON TopicTopicRelationship.lefttopicid = LeftTopic.id
            JOIN Topic AS RightTopic ON TopicTopicRelationship.righttopicid = RightTopic.id
            WHERE TopicTopicRelationship.relationshipid =(?) 
            """, (relationshipid,)).fetchall()

    topicid = rootedAt
    if onThe == 'left':
        childCol = 'lefttopicid'
        parentCol = 'righttopicid'
    if onThe == 'right':
        childCol = 'righttopicid'
        parentCol = 'lefttopicid'

    if depth == 1:
        return db.execute("""
            SELECT Current.id AS parentid, Topic.id AS childid, 
            Current.name AS parentname, Topic.name AS childname 
            FROM Topic JOIN 
            TopicTopicRelationship ON Topic.id=TopicTopicRelationship.{childCol} 
            JOIN Topic AS Current
            WHERE TopicTopicRelationship.{parentCol}=(?) AND TopicTopicRelationship.relationshipid=(?)
            AND Current.id=(?);
            """.format(childCol=childCol, parentCol=parentCol),
            (topicid, relationshipid, topicid) ).fetchall()

    if depth == float('inf'):
        return db.execute("""
            WITH RECURSIVE AllRelated(parentid, childid) AS (
                SELECT {parentCol}, {childCol} FROM TopicTopicRelationship 
                WHERE {parentCol}=(?) AND relationshipid=(?)
                UNION
                SELECT DISTINCT TopicTopicRelationship.{parentCol}, TopicTopicRelationship.{childCol}
                FROM TopicTopicRelationship INNER JOIN AllRelated ON
                TopicTopicRelationship.{parentCol} = AllRelated.childid
                WHERE TopicTopicRelationship.relationshipid=(?)
                LIMIT 10000
            )
            SELECT AllRelated.parentid, AllRelated.childid, Parent.name AS parentname, 
            Child.name AS childname
            FROM AllRelated JOIN Topic AS Parent on AllRelated.parentid=Parent.id
            JOIN Topic AS Child on AllRelated.childid=Child.id
            """.format(childCol=childCol, parentCol=parentCol),
            (topicid, relationshipid,relationshipid) ).fetchall()




