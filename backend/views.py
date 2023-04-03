import requests
import json

from flask import request, g
from flask import render_template, send_file, redirect, flash
from flask import url_for

from backend import app
from backend.utilities import isURLWebOrLocal, sortbyname

from database.oldInterface import get_db, addPageTopic

######################################## Webpages ########################################


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/newpage', methods=['GET', 'POST'])
def newPage():
    if request.method == 'GET':
        topicList = sortbyname( json.loads(
            requests.get(url_for('api.topic.all_topics', _external=True)).content
            ) )
        return render_template("entryform.html", topicList=topicList)

    elif request.method == 'POST':
        pageAdded = False
        if request.form['url'] != '':
            requests.post( url_for('api.page.all_pages', _external=True), 
                {'url': request.form['url'], 'name': request.form['name']})
            pageAdded = True

        if request.form['topics'] != '':
            for topic in request.form['topics'].split(','):
                requests.post( url_for('api.topic.all_topics', _external=True), {'name': topic})

                if pageAdded:
                    db = get_db()
                    addPageTopic(db, request.form['url'], topic)

        flash("ok")
        return redirect( url_for('home'))


@app.route('/openpage/<int:pageid>', methods=['GET'])
def servePage(pageid):
    """Redirect to the URL of the requested page""" 
    db = get_db()
    url = db.execute("SELECT url FROM Page WHERE id=(?)", (pageid,)).fetchone()['url']

    URLsource, formattedURL = isURLWebOrLocal(url)
    if URLsource == 'web':
        return redirect(formattedURL)
    elif URLsource == 'local':
        return send_file(formattedURL)



@app.route('/view', methods=['GET'])
def viewEntry():
    """Display an entry from the database"""

    # refactor this into a individual pages with react to handle page states.

    # Handling page state
    pageState = {}
    pageState['editPanel'] = request.args.get('editPanel', '')
    pageState['showRelationships'] = request.args.get('showRelationships', '')
    pageState['selectRelated'] = request.args.get('selectRelated', None)

    if 'toggle' in request.args and request.args['toggle'] in pageState.keys():
        if bool(pageState[ request.args['toggle'] ]):
            pageState[ request.args['toggle'] ] = ''
        else:
            pageState[ request.args['toggle'] ] = '1'

        if 'topic' in request.args:
            return redirect( url_for('viewEntry', topic=request.args['topic'], **pageState) )
        elif 'page' in request.args:
            return redirect( url_for('viewEntry', page=request.args['page'], **pageState) )


    if 'topic' in request.args:
        topicid = int(request.args['topic'])
        topicData = requests.get( url_for('api.topic.info', topicid=topicid, _external=True) 
            ).json()

        if pageState['selectRelated']:
            # hard coding with a single relationship type for now
            pageData = requests.get( url_for('api.topic.related_pages', topicid=topicid, 
                selectThrough=1, onThe='left', _external=True) ).json()
            topicData['pages'] = pageData
        sortbyname(topicData['pages'])

        commentEndpoint=url_for('api.comment.topic', topicid=topicid, _external=True)
        topicComments=requests.get( commentEndpoint ).json()
        commentdata = {'comments': topicComments, 'endpoint':commentEndpoint}

        allTopics = sortbyname( requests.get(url_for('api.topic.all_topics', _external=True)).json() )
        allPages = sortbyname( requests.get(url_for('api.page.all_pages', _external=True)).json() )


        return render_template('viewtopic.html', pageState=pageState, pagedata=topicData,
            commentdata=commentdata, allTopics=allTopics, allPages=allPages)


    elif 'page' in request.args:
        pageid = int(request.args['page'])
        pageData = requests.get( url_for('api.page.info', pageid=pageid, _external=True) ).json()
        sortbyname(pageData['topics'])

        commentEndpoint=url_for('api.comment.page', pageid=pageid, _external=True)
        pageComments=requests.get( commentEndpoint ).json()
        commentdata = {'comments': pageComments, 'endpoint':commentEndpoint}

        allTopics = sortbyname( requests.get(url_for('api.topic.all_topics', _external=True)).json() )
        allPages = sortbyname( requests.get(url_for('api.page.all_pages', _external=True)).json() )


        return render_template('viewpage.html', pagedata=pageData, pageState=pageState,
                commentdata=commentdata, allTopics=allTopics, allPages=allPages)
    else:
        return render_template('home.html')





@app.route('/page', methods=['GET'])
def viewPages():
    """Table view for pages"""
    pagesData = sortbyname( 
        requests.get(url_for('api.page.all_pages', _external=True)).json() )
    for entry in pagesData:
        entry['link'] = url_for('viewEntry', page=entry['id'])
    return render_template('listpages.html', tableTitle='Pages', tableEntries=pagesData)


@app.route('/page/<int:pageid>', methods=['GET'])
def viewPage(pageid):
    """Detail view for a single page"""
    return



@app.route('/topic', methods=['GET'])
def viewTopics():
    """Table view for topics"""
    topicsData = sortbyname(
        requests.get( url_for('api.topic.all_topics', _external=True)).json())
    for entry in topicsData:
        entry['link'] = url_for('viewEntry', topic=entry['id'])
    return render_template('listtopics.html', tableTitle='Topics', tableEntries=topicsData)


@app.route('/topic/<int:topicid>', methods=['GET'])
def viewTopic(topicid):
    """Detail view for a single topic"""
    return 



@app.route('/relationship', methods=['GET'])
def viewRelationships():
    """Table view for relationships"""
    allRelationships = requests.get(url_for('api.relationship.all_relationships', _external=True)).json()
    for entry in allRelationships:
        entry['link'] = url_for('viewRelationship', relationshipid=entry['id'])

    return render_template('listrelationships.html', relationships=allRelationships)


@app.route('/relationship/<int:relationshipid>', methods=['GET'])
def viewRelationship(relationshipid):
    """Detail view for a single relationship"""
    return render_template('viewrelationship.html')






# work in progress / testing

# graph ql fiddle
from backend.api.graphQL import schema
from flask_graphql import GraphQLView
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)




@app.route('/table', methods=['GET'])
def viewTable():
    """show a table of publications based on the paperMetadata topic"""
    from backend import sqlaDB as db
    from database.model import Page
    print( Page.query)

    return render_template('metadatatable.html')

