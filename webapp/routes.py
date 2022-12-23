# url routing logic

import requests
import sqlite3
import json

from flask import request, g
from flask import render_template, send_file, redirect, Response, flash
from flask import url_for, redirect

from webapp import app
from webapp.db import get_db, packageRows, addPageTopic



######################################## Webpages ########################################

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/newpage', methods=['GET', 'POST'])
def newPage():
    if request.method == 'GET':
        # fetch topics list
        topicsData = allTopics()
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
        return render_template("entryform.html")


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
    pageState['selectRelated'] = request.args.get('showRelationships', '')

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
            topicData = json.loads( topicInfo( topicid ) )

            if bool(pageState['showRelationships']):
                # hard coding with a single relationship type for now
                relatedTopics = json.loads( requests.get(
                    url_for('relationshipInfo', relationshipid=1, topic=topicid, _external=True)
                    ).content )['topics']
                print( relatedTopics)
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


################################### Front End Drivers ###################################

# eventually, these will moved to the front end
# currently, they are all hacks
@app.route('/button_delete')
def button_delete():
    # delete button action
    if 'topicid' in request.args.keys():
        topicid = request.args['topicid']
        requests.delete( url_for( 'topicInfo', topicid=topicid, _external=True))
        return redirect( url_for('viewEntry', topic='all') )

    elif 'pageid' in request.args.keys():
        pageid = request.args['pageid']
        requests.delete( url_for('pageInfo', pageid=pageid, _external=True) )
        return redirect( url_for('viewEntry', page='all') )


@app.route('/button_remove_pair')
def button_remove_pair():
    # delete topic button action
    topicid = request.args['topicid']
    pageid = request.args['pageid']
    base = request.args['base']

    requests.delete( url_for('associatePageTopic', topicid=topicid, pageid=pageid, _external=True) )

    if base == 'topic':
        return redirect( url_for('viewEntry', topic=topicid) )
    else:
        return redirect( url_for('viewEntry', page=pageid) )


@app.route('/button_add_PTR')
def button_add_PTR():
    if 'pageid' in request.args and 'topicid' in request.args:
        topicid = request.args['topicid']
        pageid = request.args['pageid']
        callback = request.args['callback']

        requests.post(url_for('associatePageTopic', topicid=topicid, pageid=pageid, _external=True))
        if callback == 'topic':
            return redirect( url_for('viewEntry', topic=topicid) )
        if callback == 'page':
            return redirect( url_for('viewEntry', page=pageid) )

    elif 'pageid' in request.args: # adding a topic to a specific page
        currentPage = request.args['pageid']
        topicsData = json.loads( allTopics() )
        for entry in topicsData:
            entry['link'] = url_for('button_add_PTR', topicid=entry['id'], pageid=currentPage, callback='page')

        return render_template("addpairdialog.html",
            tableEntries=topicsData, tableTitle='Topics',
            cancel=url_for('viewEntry', page=currentPage) )

    elif 'topicid' in request.args: # adding a page to a specific topic
        currentTopic = request.args['topicid']

        pagesData = json.loads( allPages() )
        for entry in pagesData:
            entry['link'] = url_for('button_add_PTR', topicid=currentTopic, pageid=entry['id'], callback='topic')

        return render_template("addpairdialog.html",
            tableEntries=pagesData, tableTitle='Pages',
            cancel=url_for('viewEntry', topic=currentTopic))


@app.route('/button_add_TTR')
def button_add_TTR():
    """Driver for topic-topic relationship addtion"""
    # hard coded for now
    relationshipid = 1

    if 'lefttopicid' in request.args and 'righttopicid' in request.args:
        lefttopicid = request.args['lefttopicid']
        righttopicid = request.args['righttopicid']

        requests.post(url_for('associateTopicTopic', 
            lefttopicid=lefttopicid, righttopicid=righttopicid, relationshipid=relationshipid,
            _external=True))

        return redirect( url_for('viewEntry', topic=righttopicid, showRelationships='1') )


    elif 'righttopicid' in request.args:
        currentTopic = request.args['righttopicid']
        topicsData = json.loads( allTopics() )
        for entry in topicsData:
            entry['link'] = url_for('button_add_TTR', lefttopicid=entry['id'], righttopicid=currentTopic)

        return render_template("addpairdialog.html", tableEntries=topicsData, tableTitle='Topics',
            cancel=url_for('viewEntry', topic=currentTopic))


@app.route('/button_remove_TTR')
def button_remove_TTR():
    # delete topic button action
    lefttopicid = request.args['lefttopicid']
    righttopicid = request.args['righttopicid']
    relationshipid = 1

    requests.delete( url_for('associateTopicTopic', 
        lefttopicid=lefttopicid, righttopicid=righttopicid, relationshipid=relationshipid,
        _external=True) )

    return redirect( url_for('viewEntry', topic=righttopicid, showRelationships=1 ) )





################################### API. ###################################

@app.route('/page', methods=['GET', 'POST'])
def allPages():
    """Page API"""
    db = get_db()
    if request.method == 'GET':
        # return info on all pages
        pagesData = db.execute("SELECT * FROM Page;").fetchall()
        return packageRows(pagesData)

    if request.method == 'POST':
        # add a new page
        name = request.form['name']
        url = request.form['url']

        entryData = db.execute("INSERT INTO Page (name, url) VALUES (?,?) RETURNING id", 
            (name, url)).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200 )


@app.route('/page/<int:pageid>', methods=['GET', 'PUT', 'DELETE'])
def pageInfo(pageid):
    """Page API"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific page
        pageInfo = db.execute("SELECT * FROM Page WHERE id=(?)", (pageid,)).fetchone()
        pageTopics = db.execute(
            """SELECT Topic.id, Topic.name FROM 
            Topic INNER JOIN PageTopic ON Topic.id = PageTopic.topicid
            WHERE PageTopic.pageid =(?)
            """, (pageid,)).fetchall()
        return packageRows(page=pageInfo, topics=pageTopics)

    if request.method == 'PUT':
        # over write the contents of the entry
        if 'name' in request.form.keys():
            db.execute("UPDATE Page SET name=(?) WHERE id=(?);", (request.form['name'], pageid) )
        if 'url' in request.form.keys():
            db.execute("UPDATE Page SET url=(?) WHERE id=(?);", (request.form['url'], pageid) )
        db.commit()
        return Response(status=200)

    if request.method == 'DELETE':
        db.execute("DELETE FROM Page WHERE id=(?);", (pageid,))
        db.execute("DELETE FROM PageTopic WHERE pageid=(?);", (pageid,))
        db.commit()
        return Response(status=200)




@app.route('/topic', methods=['GET', 'POST'])
def allTopics():
    """Topic API"""
    db = get_db()
    if request.method == 'GET':
        # return info on all topics
        topicsData = db.execute("SELECT * FROM Topic;").fetchall()
        return packageRows(topicsData)

    if request.method == 'POST':
        # add a new topic
        name = request.form['name']

        entryData = db.execute("INSERT INTO Topic (name) VALUES (?) RETURNING id", 
            (name,)).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200 )


@app.route('/topic/<int:topicid>', methods=['GET', 'PUT', 'DELETE'])
def topicInfo(topicid):
    """Topic API"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific topic
        topicInfo = db.execute("SELECT * FROM Topic WHERE id=(?)", (topicid,) ).fetchone()
        topicPages = db.execute(
            """SELECT Page.id, Page.name FROM 
            Page INNER JOIN PageTopic ON Page.id = PageTopic.pageid
            WHERE PageTopic.topicid =(?)
            """, (topicid,)).fetchall()

        if 'fetchThrough' in request.args.keys():
            relationshipid = request.args['fetchThrough']
            subsetPages = db.execute(
                """SELECT Page.id, Page.name FROM Page 
                INNER JOIN PageTopic ON Page.id=PageTopic.pageid INNER JOIN
                TopicTopicRelationship ON PageTopic.topicid =TopicTopicRelationship.lefttopicid WHERE
                TopicTopicRelationship.righttopicid=(?) AND TopicTopicRelationship.relationshipid=(?);
                """, (topicid, relationshipid)).fetchall()
            topicPages.extend(subsetPages)

        return packageRows(topic=topicInfo, pages=topicPages)

    if request.method == 'PUT':
        # over write the contents of the entry
        if 'name' in request.form.keys():
            db.execute("UPDATE Topic SET name=(?) WHERE id=(?);", (request.form['name'], topicid) )
        db.commit()
        return Response(status=200)

    if request.method == 'DELETE':
        db.execute("DELETE FROM Topic WHERE id=(?)", (topicid,))
        db.execute("DELETE FROM PageTopic WHERE topicid=(?);", (topicid,))
        db.execute("DELETE FROM TopicTopicRelationship WHERE lefttopicid=(?) OR righttopicid=(?)", 
            (topicid, topicid))

        db.commit()
        return Response(status=200)



@app.route('/relationship', methods=['GET', 'POST'])
def allRelationships():
    """Relationship API"""
    db = get_db()
    if request.method == 'GET':
        # return info on all relationships
        topicsData = db.execute("SELECT * FROM Relationship;").fetchall()
        return packageRows(topicsData)

    if request.method == 'POST':
        # add a new relationship
        name = request.form['name']

        entryData = db.execute("INSERT INTO Relationship (name) VALUES (?) RETURNING id", 
            (name,)).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200 )

@app.route('/relationship/<int:relationshipid>', methods=['GET', 'PUT', 'DELETE'])
def relationshipInfo(relationshipid):
    """Relationship API"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific topic
        relationshipInfo = db.execute("SELECT * FROM Relationship WHERE id=(?)", (relationshipid,) ).fetchone()
        topicPairs = db.execute(
            """SELECT lefttopicid, righttopicid FROM 
            TopicTopicRelationship WHERE relationshipid =(?)
            """, (relationshipid,)).fetchall()

        if 'topic' in request.args.keys():
            topicid = request.args['topic']
            myside = 'right'
            if 'myside' in request.args.keys():
                myside = request.args['myside']

            if myside == 'left':
                relatedTopics = db.execute(
                    """SELECT Topic.id, Topic.name FROM Topic JOIN TopicTopicRelationship
                    ON Topic.id=TopicTopicRelationship.righttopicid WHERE 
                    TopicTopicRelationship.lefttopicid=(?) AND TopicTopicRelationship.relationshipid=(?);
                    """, (topicid, relationshipid) ).fetchall()

            if myside == 'right':
                relatedTopics = db.execute(
                    """SELECT Topic.id, Topic.name FROM Topic JOIN TopicTopicRelationship
                    ON Topic.id=TopicTopicRelationship.lefttopicid WHERE 
                    TopicTopicRelationship.righttopicid=(?) AND TopicTopicRelationship.relationshipid=(?);
                    """, (topicid, relationshipid) ).fetchall()

        return packageRows(relationship=relationshipInfo, topics=relatedTopics)

    else:
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




@app.route('/assoc_page_topic', methods=['POST', 'DELETE'])
def associatePageTopic():
    db = get_db()
    pageid = request.args['pageid']
    topicid = request.args['topicid']

    if request.method == 'POST':
        entryData = db.execute("INSERT INTO PageTopic(pageid, topicid) VALUES (?,?) RETURNING id;",
            (pageid, topicid)).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200)

    elif request.method == 'DELETE':
        db.execute("DELETE FROM PageTopic WHERE pageid=(?) AND topicid=(?);", (pageid, topicid))
        db.commit()
        return Response(status=200)


@app.route('/assoc_topic_topic', methods=['POST', 'DELETE'])
def associateTopicTopic():
    db = get_db()
    lefttopicid = request.args['lefttopicid']
    righttopicid = request.args['righttopicid']
    relationshipid = request.args['relationshipid']

    if request.method == 'POST':
        entryData = db.execute("""
            INSERT INTO TopicTopicRelationship(relationshipid, lefttopicid, righttopicid)
            VALUES (?,?,  ?) RETURNING id;""",
            (relationshipid, lefttopicid, righttopicid) ).fetchone()
        db.commit()
        return Response('{"id":%s, "message":"added"}' % entryData['id'], status=200)

    elif request.method == 'DELETE':
        db.execute(
            """ DELETE FROM TopicTopicRelationship WHERE 
            relationshipid=(?) AND lefttopicid=(?) AND righttopicid=(?);""",
            (relationshipid, lefttopicid, righttopicid))
        db.commit()
        return Response(status=200)




