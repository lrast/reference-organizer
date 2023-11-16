# Visual Reference Organizer

A flexible and visual reference management tool, focused on personal organization and curation of your reference library.

The aim of this project is to address the problem of the volume and noise level of information that is we are inundated with by providing tools to organize that information.
Eventually, the goal is to have curated libraries be shareable.

The organizational structure is simple: references can be related to each other, for example through citation, or tagged with one or more topic labels.
The topic labels themselves can also be organized into multi-tree hierarchies.
This topic based organization can capture the ideas of 'tags' and 'directories' for the files, while allowing for additional flexibility.


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
