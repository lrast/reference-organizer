# Visual Reference Organizer

A lightweight and flexible reference management tool focused on personal organization and curation of your reference library.

The organizational structure is simple: references are tagged with one or more topic labels. Organization is then done at the level of topics, which can be organized into multi-tree hierarchies. This can be thought of as capturing the ideas of 'tags' and 'directories' for the files, while allowing for additional flexibility.


## Technologies

The organizer has two key features that determine the design decisions: 1) expressive UI, and 2) use for any stage of a research project, regardless how preliminary. Thus, the organizer works like a jupyter notebook, running a local web server, and connecting through the browser for a UI.

The backend uses a sqlite database and Flask web framework, and provides an HTTP API, with support for Graph QL queries on GET requests.

The frontend runs on a node server, and uses Reactjs. 


## Installation and setup

Clone the repository and then run
```
./installScript.sh
```

To run the organizer,
```
./runOrganizer.sh
```


<br />
<br />
<br />


# Work in progress: development scratchbook

This section tracks features, bugs, and other development objectives that are on-going. It is mostly a scratchbook during development, and will be updated frequently as changes are made.


## to do:
Majory priorities:

1. usability features for viewing: better visualization
    - the lists are just too long
    - As I populate the database, it's becoming clear that this is _the_ most important feature
2. usability features for adding: 
    - loading from mendeley archives 
    - reading in papers: authors, journal, referenced papers


### Short term:
- table view for pages including title, authors, journal, year
    - migrate pages database
    - new author tables
- improve database migrations
- move sorting into the table itself
- debounce things that are slow moving
- replace favicon
- local files: opening jupyter notebooks



### Long term:
- visual interface to relationships
    * topic and citation graph visualization
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

### minor improvements:
- improve URL origin testing
- improve local file dialog -- difficult because the browser is explicitly sandboxed to hide local file locations
- ability to abbreviate column values?


