# Basic visual file organizer

## To run it:
1. set environment variables:
```
export FLASK_APP=run
export FLASK_SERVER_NAME=127.0.0.1:5000
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
4. Key restriction: there is only one type of relationship between topics and pages


## to do:
Majory priorities:
1. usability features for viewing: better visualization
    - the lists are just too damn long
    - As I populate the database, it's becoming clear that this is _the_ most important feature
2. usability features for adding: loading from mendeley archives 


### Short term:
- find basic set of components
    * eg: https://react-table-v7.tanstack.com/
- tables view: filtering and sorting
- API design:
    * more expressive queries
- multiple entries for page, topic entry
- fix style issues: table centering
- clean-up css, html, and view code.
- interface to relationships
    * topic and citation graph visualization
        > to start: a series of trees with each unique root
- local files: opening jupyter notebooks
- ability to abbreviate column values


### Long term:
- table view for pages including title, authors, journal, year
- dockerize to a local application
- improve URL origin testing
- searching
- API design:
    * GET page: can fetch related topics (todo)
- Far future: shareability, searchability of libraries
- improve input interface
    * local file dialog -- difficult because the browser is explicitly sandboxed to hide local file locations
    * pdf ingestion: title, authors, references
    * importing from mendeley and session buddy records
        > important for populating the database

### bugs:
- 'maximum recursion depth' when there are subtopic loops
- fix topic tree wedges
- fix style issues: table centering
- pages that are tagged more than once are listed multiple times in the tables


