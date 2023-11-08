# Work in progress: development scratchbook

This file tracks features, bugs, and other development objectives that are on-going. It is mostly a scratchbook during development, and will be updated frequently as changes are made.


## to do:
Majory priorities:

1. usability features for viewing: better visualization
    - the lists are just too long
    - As I populate the database, it's becoming clear that this is _the_ most important feature
2. usability features for adding: 
    - loading from mendeley archives 
    - reading in papers: authors, journal, referenced papers


### Short term:
- zotero integration
- table view for pages including title, authors, journal, year
    - update backend data models
- improve database migrations
- move sorting into the table itself
- debounce things that are slow moving
- replace favicon
- local files: opening jupyter notebooks


### Long term:
- visual interface to relationships
    * topic and citation graph visualization
- update to the new version of react table
- easy tools for moving / merging topics
- improve installation
    * dockerize to a local application?
- improve input interface
    * pdf ingestion: title, authors, references
    * importing from mendeley and session buddy records
        > important for populating the database
- improve port selection
- store page favicons
- multiple entries for page, topic entry
- Far future: shareability, searchability of remote libraries


### bugs:
- infinite query recursion when there are subtopic loops
    * replace all recursive queries by sqlalchemy common table expressions
- opening urls: doesn't work on remote device
    * this is due to how the open page link functions
- adding pages from ipad


### minor improvements:
- improve URL origin testing
- improve local file dialog -- difficult because the browser is explicitly sandboxed to hide local file locations
- ability to abbreviate column values?
