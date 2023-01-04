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
1. Editing pages / topics and improve input interface
2. topic-topic relationships, IV
3. fetch names for webpages, autofill
4. API design:
    - GET page: can fetch related topics (todo)
    - Endpoint for info
    - add comments to this effect
5. dockerize
6. local file adding dialog
7. importing from mendeley and session buddy records
8. Far future: shareability, searchability of libraries
