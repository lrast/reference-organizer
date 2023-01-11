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
- improve input interface
    * local file dialog
    * pdf ingestion: title, authors, references
- API design:
    * GET page: can fetch related topics (todo)
    * modularize commenting api
- dockerize
- importing from mendeley and session buddy records
- Far future: shareability, searchability of libraries
- topic and citation graph visualization
- table view for pages including title, authors, journal, year
- improve URL origin testing
