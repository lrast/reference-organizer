import requests
import json

from flask import request, render_template, redirect, url_for

from webapp import app


################################### Front End Drivers ###################################
# eventually, these will moved to the front end

@app.route('/button_delete')
def button_delete():
    # delete button action
    if 'topicid' in request.args.keys():
        topicid = request.args['topicid']
        requests.delete( url_for('api.topicInfo', topicid=topicid, _external=True))
        return redirect( url_for('viewEntry', topic='all') )

    elif 'pageid' in request.args.keys():
        pageid = request.args['pageid']
        requests.delete( url_for('api.pageInfo', pageid=pageid, _external=True) )
        return redirect( url_for('viewEntry', page='all') )


@app.route('/button_remove_pair')
def button_remove_pair():
    # delete topic button action
    topicid = request.args['topicid']
    pageid = request.args['pageid']
    base = request.args['base']

    requests.delete( url_for('api.associatePageTopic', topicid=topicid, pageid=pageid, _external=True) )

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

        requests.post(url_for('api.associatePageTopic', topicid=topicid, pageid=pageid, _external=True))
        if callback == 'topic':
            return redirect( url_for('viewEntry', topic=topicid) )
        if callback == 'page':
            return redirect( url_for('viewEntry', page=pageid) )

    elif 'pageid' in request.args: # adding a topic to a specific page
        currentPage = request.args['pageid']
        topicsData = requests.get( url_for('api.allTopics', _external=True)).json()
        for entry in topicsData:
            entry['link'] = url_for('button_add_PTR', topicid=entry['id'], pageid=currentPage, callback='page')

        return render_template("addpairdialog.html",
            tableEntries=topicsData, tableTitle='Topics',
            cancel=url_for('viewEntry', page=currentPage) )

    elif 'topicid' in request.args: # adding a page to a specific topic
        currentTopic = request.args['topicid']

        pagesData = requests.get(url_for('api.allPages', _external=True)).json()
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

        requests.post(url_for('api.associateTopicTopic', 
            lefttopicid=lefttopicid, righttopicid=righttopicid, relationshipid=relationshipid,
            _external=True))

        return redirect( url_for('viewEntry', topic=righttopicid, showRelationships='1') )

    elif 'righttopicid' in request.args:
        currentTopic = request.args['righttopicid']
        topicsData = requests.get( url_for('api.allTopics', _external=True)).json()
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

    requests.delete( url_for('api.associateTopicTopic', 
        lefttopicid=lefttopicid, righttopicid=righttopicid, relationshipid=relationshipid,
        _external=True) )

    return redirect( url_for('viewEntry', topic=righttopicid, showRelationships=1 ) )

