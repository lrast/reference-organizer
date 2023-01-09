# Basic visual file organizer

## To run it:
1. set environment variables:
```
export FLASK_APP=run
export FLASK_ENV=development
export FLASK_DEBUG=True
export FLASK_SECRET_KEY=[key]
export FLASK_DATABASE_URL=[url]
```

2. flask run


## organization scheme:
1. track a database of webpages and local resources
2. resources are organized by tagging them with topic labels
3. organization is done at the level of topics, for example by make subsets of topics


## to do:
1. improve input interface
    - local file dialog
    - fetch names for webpages, autofill
    - pdf ingestion: title, authors, references
2. API design:
    - GET page: can fetch related topics (todo)
3. dockerize
4. importing from mendeley and session buddy records
5. Far future: shareability, searchability of libraries
6. UI for comment adding and editing
    - fetch and save editable content
7. Front end:
    - topic and citation graph visualization
    - table view for pages including title, authors, journal, year
