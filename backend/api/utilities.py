# utilities for api
import json
from flask import Response


def checkNodeType(db, relationshipid, target):
    """Double check that the relationship is between pages"""
    nodeType = db.execute("""SELECT nodetype FROM Relationship WHERE id=(?)""",
                          (relationshipid,)).fetchone()[0]
    if nodeType != target:
        return False, \
                Response('Relationship is not betweeen' + target, status=422)

    return True, '_'


def getPOSTData(request):
    """Get data sent in POST requests, either form or body"""
    if len(request.form) != 0:
        return request.form
    else:
        return json.loads(request.data)
