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
Majory priorities:

1. usability features for adding: loading from archives 
2. usability features for viewing: better visualization
    - the lists are just too damn long
    - As I populate the database, it's becoming clear that this is _the_ most important feature

### Short term:
- API design:
    * Finish implementing new API
- improve input interface
    * local file dialog -- difficult because the browser is explicitly sandboxed to hide local file locations
    * pdf ingestion: title, authors, references
    * importing from mendeley and session buddy records
        > important for populating the database
- table view for pages including title, authors, journal, year
- multiple entries for page, topic entry


### Long term:
- interface to relationships
- dockerize to a local application
- topic and citation graph visualization
    - to start: a series of trees with each unique root
- improve URL origin testing
- searching
- API design:
    * GET page: can fetch related topics (todo)
- Far future: shareability, searchability of libraries


### bugs:
- commenting: new lines become spaces
- 'maximum recursion depth' when there are subtopic loops
- fix topic tree wedges
