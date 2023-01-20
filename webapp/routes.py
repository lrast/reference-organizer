import requests
import sqlite3
import json

from flask import request, g
from flask import render_template, send_file, redirect, flash
from flask import url_for

from webapp import app
from webapp.db import get_db, addPageTopic
from webapp.utilities import isURLWebOrLocal


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
        if request.args['topic'] == 'all':
            #show all topics
            topicsData = sortbyname(
                requests.get( url_for('api.topic.all_topics', _external=True)).json())
            for entry in topicsData:
                entry['link'] = url_for('viewEntry', topic=entry['id'])
            return render_template('topiclist.html',
                tableTitle='Topics',
                tableEntries=topicsData)
        else:
            topicid = int(request.args['topic'])
            topicData = requests.get( url_for('api.topic.info', topicid=topicid, _external=True) 
                ).json()

            if pageState['selectRelated']:
                # hard coding with a single relationship type for now
                pageData = requests.get( url_for('api.topic.related_pages', topicid=topicid, 
                    selectThrough=1, onThe='left', _external=True) ).json()
                topicData['pages'] = pageData

            commentEndpoint=url_for('api.comment.topic', topicid=topicid, _external=True)
            topicComments=requests.get( commentEndpoint ).json()

            return render_template('viewtopic.html', pagedata=topicData, pageState=pageState,
                comments=topicComments, commentEndpoint=commentEndpoint)


    elif 'page' in request.args:
        if request.args['page'] == 'all':
            #show all pages
            pagesData = sortbyname( 
                requests.get(url_for('api.page.all_pages', _external=True)).json() )
            for entry in pagesData:
                entry['link'] = url_for('viewEntry', page=entry['id'])
            return render_template('pagelist.html',
                tableTitle='Pages',
                tableEntries=pagesData)

        else:
            pageid = int(request.args['page'])
            pageData = requests.get( url_for('api.page.info', pageid=pageid, _external=True) ).json()

            commentEndpoint=url_for('api.comment.page', pageid=pageid, _external=True)
            pageComments=requests.get( commentEndpoint ).json()

            return render_template('viewpage.html', 
                page=pageData['page'],
                topics=pageData['topics'],
                pageState=pageState,
                comments=pageComments,
                commentEndpoint=commentEndpoint)
    else:
        return render_template('home.html')



@app.route('/table', methods=['GET'])
def viewTable():
    """show a table of publications based on the paperMetadata topic"""

    return render_template('metadatatable.html')




# utilities
def sortbyname(inlist):
    inlist.sort(key=lambda x: x['name'].lower())
    return inlist



