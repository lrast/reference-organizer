# url routing logic

from webapp import app

from flask import request
from flask import render_template, send_from_directory, redirect, url_for


from webapp.CSVinterface import fetchEntry, addEntry

# home
@app.route('/')
def home():
    entries = fetchEntry(None)

    return render_template("home.html", entries=entries)


# interfaces to the database
@app.route('/entry/<string:entryID>')
def show_entry(entryID):
    ''' Fetches specific entry from the entry table '''
    toServe = fetchEntry(entryID)

    if toServe is None:
        return redirect(url_for('home'))

    return send_from_directory(toServe[0], toServe[1])


@app.route('/addEntry', methods=['GET', 'POST'])
def adderForm():
    print(request.method)
    if request.method == 'POST':
        addEntry(request.form['title'], request.form['date'], request.form['path'])
        return render_template("addEntry.html")
    else:
        return render_template("addEntry.html")

@app.route('/addFile', methods=['GET', 'POST'])
def adderRedirect():
    return redirect( url_for('adderForm') )


# serving page assets
@app.route('/Users/luke/<path:fileLoc>', methods=['GET'])
def serveAsset(fileLoc):
    ''' Fetches the corresponding file.
        This is useful for including images, but definitely a security risk.
        With a test server, its ok: the server is only listening on localhost
     '''
     # reconstruct the directory:
    lastSlash = fileLoc.rfind('/')
    directory = '/Users/luke/' + fileLoc[:lastSlash]
    file = fileLoc[lastSlash+1:]

    return send_from_directory(directory, file )


