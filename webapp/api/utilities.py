# utilities for api
import json

def checkNodeType(db, relationshipid, target):
    print('here')
    """Double check that the relationship is between pages"""
    nodeType = db.execute("""SELECT nodetype FROM Relationship WHERE id=(?)""",
        (relationshipid,)).fetchone()[0]
    if nodeType != target:
        return False, Response('Relationship is not betweeen' + target ,status=422)

    return True, '_'


def getPOSTData(request, names):
    """Get data sent in POST requests, either form or body"""
    toReturn = {}

    try:
        bodydata = json.loads(request.data)
    except:
        bodydata = {}

    def getItem(name):
        if name in request.form:
            toReturn[name] = request.form[name]
        else:
            toReturn[name] = bodydata[name]

    if type(names) == list:
        for name in names:
            getItem(name)
    else:
        getItem(names)

    return toReturn


