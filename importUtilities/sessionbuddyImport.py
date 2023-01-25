# import from session buddy records encoded as JSON
import json
import requests
import os

from datetime import datetime


def importSessionBuddy(sessionBuddyFile):
    """import a full browsing session from a session buddy file"""
    apiendpoint = 'http://' + os.environ['FLASK_SERVER_NAME'] + '/api'

    archive = json.loads( sessionBuddyFile.read().strip('\ufeff') )

    for session in archive['sessions']:
        today = datetime.today().strftime('%Y-%m-%d')
        sessionName = 'browser session ' + today +': ' + session['name'] 

        resp = requests.post(apiendpoint + '/topic', data={'name': sessionName})
        rootid = json.loads( resp.content )['id']
        requests.post( apiendpoint+'/topic/18/topic?relationshipid=1&side=left', {'relatedtopicid': rootid} )

        for windownum, window in enumerate(session['windows']):
            resp = requests.post(apiendpoint + '/topic', data={'name': sessionName+': window ' + str(windownum)})
            windowid = json.loads( resp.content )['id']
            requests.post( apiendpoint+'/topic/'+str(rootid)+'/topic?relationshipid=1&side=left', {'relatedtopicid': windowid} )

            for tab in window['tabs']:
                resp = requests.post(apiendpoint+'/page', data={'url':tab['url'], 'name': tab['title']})
                tabid = json.loads( resp.content )['id']
                requests.post(apiendpoint+'/page/'+str(tabid)+'/topic', {'topicid':windowid})






