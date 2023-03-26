import json
import requests

from flask import request, Response, Blueprint, url_for

from database.oldInterface import get_db, packageRows
from backend.utilities import isURLWebOrLocal

from backend.api.comment import comment
from backend.api.relationship import relationship
from backend.api.page import page
from backend.api.topic import topic

api = Blueprint('api', __name__)

api.register_blueprint(page, url_prefix='/page')
api.register_blueprint(topic, url_prefix='/topic')
api.register_blueprint(relationship, url_prefix='/relationship')
api.register_blueprint(comment, url_prefix='/comment')



# utilities 
@api.route('/getWebpageTitle', methods=['POST'])
def getWebpageTitle():
    """Fetches the title for webpages"""
    try:
        url = request.data.decode()

        if len(url) == 0:
            return Response('', status=200)

        URLsource, formattedURL = isURLWebOrLocal(url)
        if URLsource != "web":
            return Response('', status=200)

        resp = requests.get(formattedURL)
        if resp.status_code != 200:
            return Response('', status=200)

        workingTitle = ( resp.content.split(b'title>')[1][:-2] ).decode()

        return Response(workingTitle, status=200)

    except:
        return Response('', status=200)


