import requests
import sqlite3
import json

from flask import request, g
from flask import render_template, send_file, redirect, flash
from flask import url_for

from webapp import app
from webapp.db import get_db, addPageTopic
from webapp.apis import allTopics, topicInfo, allPages, pageInfo



######################################## Webpages ########################################

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/newpage', methods=['GET', 'POST'])
def newPage():
    if request.method == 'GET':
        return render_template("entryform.html")

    elif request.method == 'POST':
        pageAdded = False
        if request.form['url'] != '':
            requests.post( url_for('allPages', _external=True), 
                {'url': request.form['url'], 'name': request.form['name']})
            pageAdded = True

        if request.form['topics'] != '':
            for topic in request.form['topics'].split(','):
                requests.post( url_for('allTopics', _external=True), {'name': topic})

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

    # check for local file vs webpage
    if url[:7] == 'http://' or url[:8]=='https://':
        # well formatted webpage
        return redirect(url)
    elif url[0] == '/' or url[0] == '~':
        # definitely a local file
        return send_file(url)
    else:
        # try it like a webpage
        return redirect('http://'+url)


@app.route('/view', methods=['GET'])
def viewEntry():
    """Display an entry from the database"""

    # Handling page state
    pageState = {}
    pageState['editPanel'] = request.args.get('editPanel', '')
    pageState['showRelationships'] = request.args.get('showRelationships', '')
    pageState['selectRelated'] = request.args.get('selectRelated', '')

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
            topicsData = json.loads( allTopics() )
            for entry in topicsData:
                entry['link'] = url_for('viewEntry', topic=entry['id'])
            return render_template('topiclist.html',
                tableTitle='Topics',
                tableEntries=topicsData)
        else:
            topicid = int(request.args['topic'])
            if bool( pageState['selectRelated'] ):
                topicData = json.loads( requests.get( 
                    url_for('topicInfo', topicid=topicid, fetchThrough=1, _external=True) 
                    ).content )
            else:
                topicData = json.loads( topicInfo( topicid ) )

            if bool(pageState['showRelationships']):
                # hard coding with a single relationship type for now
                relatedTopics = json.loads( requests.get(
                    url_for('relationshipInfo', relationshipid=1, topic=topicid, fetchThrough=1, _external=True)
                    ).content )['topics']
                print(relatedTopics)
            else:
                relatedTopics=[]

            return render_template('viewtopic.html',
                topic=topicData["topic"],
                pages=topicData["pages"],
                pageState=pageState,
                relatedTopics=relatedTopics)

    elif 'page' in request.args:
        if request.args['page'] == 'all':
            #show all pages
            pagesData = json.loads( allPages() )
            for entry in pagesData:
                entry['link'] = url_for('viewEntry', page=entry['id'])
            return render_template('pagelist.html',
                tableTitle='Pages',
                tableEntries=pagesData)

        else:
            pageid = int(request.args['page'])
            pageData = json.loads( pageInfo(pageid) )

            return render_template('viewpage.html', 
                page=pageData['page'],
                topics=pageData['topics'],
                pageState=pageState)
    else:
        return render_template('home.html')

