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

