import requests

from flask import request, Response, send_file, redirect, url_for

from backend import app
from backend.utilities import isURLWebOrLocal

from database.oldInterface import get_db



@app.route('/openpage/<int:pageid>', methods=['GET'])
def servePage(pageid):
    """Redirect to the URL of the requested page""" 
    db = get_db()
    url = db.execute("SELECT url FROM Page WHERE id=(?)", (pageid,)).fetchone()['url']

    # handle empty url
    if url == '':
        return Response('', status=404)

    URLsource, formattedURL = isURLWebOrLocal(url)
    if URLsource == 'web':
        return redirect(formattedURL)
    elif URLsource == 'local':
        return send_file(formattedURL)


# graph ql fiddle
from backend.api.graphQL import schema
from flask_graphql import GraphQLView
app.add_url_rule(
    '/graphiql',
    view_func=GraphQLView.as_view(
        'graphiql',
        schema=schema,
        graphiql=True
    )
)

