# Basic visual file organizer

## Backend setup:
1. install requirements
```
pip install -r requirements.txt
```

2. set environment variables:
```
export FLASK_APP=run
export FLASK_SERVER_NAME=127.0.0.1:5000
export FLASK_ENV=development
export FLASK_DEBUG=True
export FLASK_SECRET_KEY=[key]
export FLASK_DATABASE_URL=[url]
export FLASK_SQLALCHEMY_DATABASE_URI='sqlite:///[url]'
```
3. ```flask run```


## Frontend setup:
1. install requirements
```
cd frontend
npm install package.json
```

2. ```npm start```



## organization scheme:
1. track a database of webpages and local resources
2. resources are organized by tagging them with topic labels
3. organization is done at the level of topics, for example by make subsets of topics
4. Key restriction: there is only one type of relationship between topics and pages



# Work in progress

## to do:
Majory priorities:
1. usability features for viewing: better visualization
    - the lists are just too damn long
    - As I populate the database, it's becoming clear that this is _the_ most important feature
2. usability features for adding: 
    - loading from mendeley archives 
    - reading in papers: authors, journal, referenced papers


### Short term:
- port fully to react app
    - add and remove topics relationships
        - inherit to parent?
- table view for pages including title, authors, journal, year
    - migrate pages database
    - new author tables


- move sorting into the table itself
- on pageview, topicview, topics don't need to be in a table, don't need filter bar


- debounce things that are slow moving
- replace favicon
- local files: opening jupyter notebooks



### Long term:
- visual interface to relationships
    * topic and citation graph visualization
- easy tools for moving / merging topics
- dockerize to a local application
- improve input interface
    * pdf ingestion: title, authors, references
    * importing from mendeley and session buddy records
        > important for populating the database
- store page favicons
- multiple entries for page, topic entry
- Far future: shareability, searchability of remote libraries


### bugs:
- 'maximum recursion depth' when there are subtopic loops
    * replace all recursive calls by graphql queries

### minor improvements:
- improve URL origin testing
- improve local file dialog -- difficult because the browser is explicitly sandboxed to hide local file locations
- ability to abbreviate column values?


