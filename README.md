# attack2neo
Import Mitre Att&amp;ck into Neo4j database

## Purpose 
Purpose of this very simple tool is to :
- read JSON data from Mitre Att&amp;ck
- import data into Neo4j database
This small project has been first been developed to be able to 
easily query Mitre Att&amp;ck data using Cypher Query Language.

## Requirements
Following python modules are required :
- [pyn2neo](https://py2neo.org/)

Modules could be installed using following commands:
```
$ pip install -r requirements.txt
```
## Configuration
Settings have to be defined directly inyo python script :
```
# open graph connection
graph_bolt = "bolt://127.0.0.1:7687"
graph_auth = ("neo4j","test")

## Usage
```
usage: attack2neo.py <filename>
  
where <filename> contains JSON data from Mitre Att&amp;ck
```
## Mitre Att&amp;ck database
The Mitre Atta7amp;ck database in JSON format could be
found out at [Mitre CTI Github](https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json)

