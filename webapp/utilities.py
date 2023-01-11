# utilities for use in the backend

def isURLWebOrLocal(url):
    """Use heuristics to determine whether a url is local or web"""

    if url[:7] == 'http://' or url[:8]=='https://':
        # well formatted webpage
        source = 'web'
    elif url[0] == '/' or url[0] == '~':
        # definitely a local file
        source = 'local'
    else:
        # try it like a webpage
        source = 'web'
        url = 'https://'+url

    return source, url

