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
