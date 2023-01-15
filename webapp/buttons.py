import requests
import json

from flask import Blueprint, request, render_template, redirect, url_for

button = Blueprint('button', __name__)

################################### Front End Drivers ###################################
# eventually, these will moved to the front end

@button.route('/delete')
def delete():
    # delete button action
    if 'topicid' in request.args.keys():
        topicid = request.args['topicid']
        requests.delete( url_for('api.topic.info', topicid=topicid, _external=True))
        return redirect( url_for('viewEntry', topic='all') )

    elif 'pageid' in request.args.keys():
        pageid = request.args['pageid']
        requests.delete( url_for('api.page.info', pageid=pageid, _external=True) )
        return redirect( url_for('viewEntry', page='all') )


@button.route('/remove_pair')
def remove_pair():
    # delete topic button action
    topicid = request.args['topicid']
    pageid = request.args['pageid']
    base = request.args['base']

    requests.delete( url_for('api.topic.related_pages_id', topicid=topicid, relatedpageid=pageid, _external=True) )

    if base == 'topic':
        return redirect( url_for('viewEntry', topic=topicid) )
    else:
        return redirect( url_for('viewEntry', page=pageid) )


@button.route('/add_PTR')
def add_PTR():
    if 'pageid' in request.args and 'topicid' in request.args:
        topicid = request.args['topicid']
        pageid = request.args['pageid']
        callback = request.args['callback']

        requests.put(url_for('api.topic.related_pages_id', topicid=topicid, relatedpageid=pageid, _external=True))
        if callback == 'topic':
            return redirect( url_for('viewEntry', topic=topicid) )
        if callback == 'page':
            return redirect( url_for('viewEntry', page=pageid) )

    elif 'pageid' in request.args: # adding a topic to a specific page
        currentPage = request.args['pageid']
        topicsData = requests.get( url_for('api.topic.all_topics', _external=True)).json()
        for entry in topicsData:
            entry['link'] = url_for('button.add_PTR', topicid=entry['id'], pageid=currentPage, callback='page')

        return render_template("addpairdialog.html",
            tableEntries=topicsData, tableTitle='Topics',
            cancel=url_for('viewEntry', page=currentPage) )

    elif 'topicid' in request.args: # adding a page to a specific topic
        currentTopic = request.args['topicid']

        pagesData = requests.get(url_for('api.page.all_pages', _external=True)).json()
        for entry in pagesData:
            entry['link'] = url_for('button.add_PTR', topicid=currentTopic, pageid=entry['id'], callback='topic')

        return render_template("addpairdialog.html",
            tableEntries=pagesData, tableTitle='Pages',
            cancel=url_for('viewEntry', topic=currentTopic))


@button.route('/add_TTR')
def add_TTR():
    """Driver for topic-topic relationship addtion"""
    # hard coded for now
    relationshipid = 1

    if 'lefttopicid' in request.args and 'righttopicid' in request.args:
        lefttopicid = request.args['lefttopicid']
        righttopicid = request.args['righttopicid']

        requests.put(url_for('api.topic.related_topics_id', 
            topicid=lefttopicid, relatedtopicid=righttopicid, relationshipid=relationshipid,
            primaryside='left', _external=True))

        return redirect( url_for('viewEntry', topic=righttopicid, showRelationships='1') )

    elif 'righttopicid' in request.args:
        currentTopic = request.args['righttopicid']
        topicsData = requests.get( url_for('api.topic.all_topics', _external=True)).json()
        for entry in topicsData:
            entry['link'] = url_for('button.add_TTR', lefttopicid=entry['id'], righttopicid=currentTopic)

        return render_template("addpairdialog.html", tableEntries=topicsData, tableTitle='Topics',
            cancel=url_for('viewEntry', topic=currentTopic))


@button.route('/remove_TTR')
def remove_TTR():
    # delete topic button action
    lefttopicid = request.args['lefttopicid']
    righttopicid = request.args['righttopicid']
    relationshipid = 1

    requests.delete( url_for('api.topic.related_topics_id', 
        topicid=lefttopicid, relatedtopicid=righttopicid, relationshipid=relationshipid,
        primaryside='left', _external=True) )

    return redirect( url_for('viewEntry', topic=righttopicid, showRelationships=1 ) )


@button.route('/editTopic', methods=["POST"])
def editTopic():
    topicid = request.form['id']
    topicname = request.form['name']

    requests.put( url_for('api.topic.info', topicid=topicid, _external=True), 
        data={'name': topicname})
    return redirect( url_for('viewEntry', topic=topicid) )


@button.route('/editPage', methods=["POST"])
def editPage():
    pageid = request.form['id']
    pagename = request.form['name']
    pageurl = request.form['url']

    requests.put( url_for('api.page.info', pageid=pageid, _external=True), 
        data={'name': pagename, 'url': pageurl})
    return redirect( url_for('viewEntry', page=pageid) )

