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
        baseURL = request.base_url[:-8]

        pageAdded = False
        if request.form['url'] != '':
            requests.post(baseURL + '/page', 
                {'url': request.form['url'], 'name': request.form['name']})
            pageAdded = True

        if request.form['topics'] != '':
            for topic in request.form['topics'].split(','):
                requests.post(baseURL + '/topic', {'name': topic})

                if pageAdded:
                    db = get_db()
                    addPageTopic(db, request.form['url'], topic)

        flash("ok")
        return render_template("entryform.html")


@app.route('/openpage/<int:pageID>', methods=['GET'])
def servePage(pageID):
    """Redirect to the URL of the requested page""" 
    db = get_db()
    url = db.execute("SELECT url FROM Page WHERE id=(?)", (pageID,)).fetchone()['url']

    print(url)
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

    if 'topic' in request.args.keys():
        if request.args['topic'] == 'all':
            #show all topics
            topicsData = json.loads( allTopics() )
            for entry in topicsData:
                entry['link'] = url_for('viewEntry', topic=entry['id'])
            return render_template('topiclist.html', entries=topicsData, tableTitle='Topics')
        else:
            topicid = int(request.args['topic'])
            topicData = json.loads( topicInfo( topicid ) )

            return render_template('viewtopic.html',
                topic=topicData["topic"],
                tableEntries=topicData["pages"])

    elif 'page' in request.args.keys():
        if request.args['page'] == 'all':
            #show all pages
            pagesData = json.loads( allPages() )
            for entry in pagesData:
                entry['link'] = url_for('viewEntry', page=entry['id'])
            return render_template('pagelist.html', entries=pagesData, tableTitle='Pages')

        else:
            pageid = int(request.args['page'])
            pageData = json.loads( pageInfo(pageid) )

            return render_template('viewpage.html', 
                page=pageData['page'],
                tableEntries=pageData['topics'])
    else:
        return render_template('home.html')


################################### Front End Drivers ###################################

# eventually, these will moved to the front end
# currently, they are all hacks
@app.route('/button_delete')
def button_delete():
    # delete button action
    baseURL = request.base_url[:-14]
    print(baseURL)

    if 'topicid' in request.args.keys():
        topicid = request.args['topicid']
        requests.delete(baseURL + '/topic/'+topicid)
        return redirect( url_for('viewEntry', topic='all') )

    elif 'pageid' in request.args.keys():
        pageid = request.args['pageid']
        requests.delete(baseURL + '/page/' + pageid,)
        return redirect( url_for('viewEntry', page='all') )


@app.route('/button_remove_pair')
def button_remove_pair():
    # delete topic button action
    baseURL = request.base_url[:-18]

    topicid = request.args['topicid']
    pageid = request.args['pageid']
    base = request.args['base']

    requests.delete(baseURL+url_for('associatePageTopic', topicid=topicid, pageid=pageid) )

    if base == 'topic':
        return redirect( url_for('viewEntry', topic=topicid) )
    else:
        return redirect( url_for('viewEntry', page=pageid) )


@app.route('/button_add_PTR')
def button_add_PTR():
    requestKeys = request.args.keys()

    baseURL = request.base_url[:-15]

    if 'pageid' in requestKeys and 'topicid' in requestKeys:
        topicid = request.args['topicid']
        pageid = request.args['pageid']
        callback = request.args['callback']

        requests.post(baseURL+url_for('associatePageTopic', topicid=topicid, pageid=pageid))
        print('here', topicid, pageid, callback)
        if callback == 'topic':
            print( url_for('viewEntry', topic=topicid) )
            return redirect( url_for('viewEntry', topic=topicid) )
        if callback == 'page':
            print( url_for('viewEntry', page=pageid) )
            return redirect( url_for('viewEntry', page=pageid) )


    elif 'pageid' in requestKeys:
        # adding a topic to a specific page
        topicsData = json.loads( allTopics() )
        for entry in topicsData:
            entry['link'] = url_for('button_add_PTR', topicid=entry['id'], pageid=request.args['pageid'], callback='page')
        return render_template("addPageTopic.html", entries=topicsData, tableTitle='Topics')


    elif 'topicid' in requestKeys:
        # adding a page to a specific topic
        pagesData = json.loads( allPages() )
        for entry in pagesData:
            entry['link'] = url_for('button_add_PTR', topicid=request.args['topicid'], pageid=entry['id'], callback='topic')
        return render_template("addPageTopic.html", entries=pagesData, tableTitle='Pages')







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


@app.route('/page/<int:pageID>', methods=['GET', 'PUT', 'DELETE'])
def pageInfo(pageID):
    """Page API"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific page
        pageInfo = db.execute("SELECT * FROM Page WHERE id=(?)", (pageID,)).fetchone()
        pageTopics = db.execute(
            """SELECT Topic.id, Topic.name FROM 
            Topic INNER JOIN PageTopic ON Topic.id = PageTopic.topicid
            WHERE PageTopic.pageid =(?)
            """, (pageID,)).fetchall()
        return packageRows(page=pageInfo, topics=pageTopics)

    if request.method == 'PUT':
        # over write the contents of the entry
        if 'name' in request.form.keys():
            db.execute("UPDATE Page SET name=(?) WHERE id=(?);", (request.form['name'], pageID) )
        if 'url' in request.form.keys():
            db.execute("UPDATE Page SET url=(?) WHERE id=(?);", (request.form['url'], pageID) )
        db.commit()
        return Response(status=200)

    if request.method == 'DELETE':
        db.execute("DELETE FROM Page WHERE id=(?);", (pageID,))
        db.execute("DELETE FROM PageTopic WHERE pageid=(?);", (pageID,))
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


@app.route('/topic/<int:topicID>', methods=['GET', 'PUT', 'DELETE'])
def topicInfo(topicID):
    """Topic API"""
    db = get_db()
    if request.method == 'GET':
        # info on a specific topic
        topicInfo = db.execute("SELECT * FROM Topic WHERE id=(?)", (topicID,) ).fetchone()
        topicPages = db.execute(
            """SELECT Page.id, Page.name FROM 
            Page INNER JOIN PageTopic ON Page.id = PageTopic.pageid
            WHERE PageTopic.topicid =(?)
            """, (topicID,)).fetchall()
        return packageRows(topic=topicInfo, pages=topicPages)

    if request.method == 'PUT':
        # over write the contents of the entry
        if 'name' in request.form.keys():
            db.execute("UPDATE Topic SET name=(?) WHERE id=(?);", (request.form['name'], topicID) )
        db.commit()
        return Response(status=200)

    if request.method == 'DELETE':
        db.execute("DELETE FROM Topic WHERE id=(?)", (topicID,))
        db.execute("DELETE FROM PageTopic WHERE topicid=(?);", (topicID,))
        db.execute("DELETE FROM TopicTopicRelationship WHERE lefttopicid=(?) OR righttopicid=(?)", 
            (topicID, topicID))

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





