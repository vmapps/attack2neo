# attack2neo
Import Mitre Entreprise Att&amp;ck data into Neo4j database

## Purpose 
Purpose of this very simple tool is to :
- read JSON data from Mitre Att&amp;ck
- import data into Neo4j database

This small project has been first been developed to easily 
query Mitre Att&amp;ck data using Cypher Query Language.

## Requirements
Following python modules are required :
- [py2neo](https://py2neo.org/)

Modules could be installed using following commands:
```
$ pip install -r requirements.txt
```
## Configuration
Settings have to be defined directly into python script :
```
# open graph connection
graph_bolt = "bolt://127.0.0.1:7687"
graph_auth = ("neo4j","test")
```
## Usage
```
usage: attack2neo.py [-h] [-d] -f <filename> [-g] [-s] [-o] [-t] [-r]

optional arguments:
  -h, --help        show this help message and exit
  -d, --debug       enter debug mode
  -f <filename>     input file name
  -g, --groups      import Groups objects (type:intrusion-set)
  -s, --softwares   import Softwares objects (type:malware)
  -o, --tools       import Tools objects (type:tool)
  -t, --techniques  import Techniques objects (type:attack-pattern and
                    type:course-of-action)
  -r, --relations   import Relations objects (type:relationship)
```
where <filename> contains JSON data from Mitre Att&amp;ck

## Mitre Att&amp;ck database
The Mitre Entreprise Atta&amp;ck database in JSON format could be
found out at [Mitre CTI Github](https://github.com/mitre/cti/blob/master/enterprise-attack/enterprise-attack.json)

## Sample 
![attack2neo](samples/attack2neo.png)
