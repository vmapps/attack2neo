#!/usr/bin/env python3

import json
import sys
from py2neo import Graph, Node, Relationship, NodeMatcher

# -----------------------------------------------------------------
# BUILD_LABEL
# -----------------------------------------------------------------
def build_label(txt):

	if txt.startswith('intrusion-set'):		return 'Group'
	if txt.startswith('malware'):			return 'Software'
	if txt.startswith('tool'):				return 'Tool'
	if txt.startswith('attack-pattern'):	return 'Technique'
	if txt.startswith('course-of-action'):	return 'Technique'
	return 'Unknown'

# -----------------------------------------------------------------
# BUILD ALIASES
# -----------------------------------------------------------------
def build_aliases(obj,key):

	label = build_label(obj['type'])

	# create node for the group
	node_main = Node(label, name=obj['name'], id=obj['id'])
	graph.merge(node_main,label,'name')
	print('%s: "%s"' % (label,obj['name']),end='')

	# dealing with aliases
	if obj.get(key):
		for alias in obj[key]:
			if alias != obj['name']:
				node_alias = Node('Alias', name=alias)
				relation = Relationship.type('alias')
				graph.merge(relation(node_main,node_alias),label,'name')
				print(' -[alias]-> "%s"' % (alias),end='')
	print()

# -----------------------------------------------------------------
# BUILD RELATIONS
# -----------------------------------------------------------------
def build_relations(obj):

	if not gnames.get(obj['source_ref']): return
	if not gnames.get(obj['target_ref']): return
	
	m = NodeMatcher(graph)

	source = m.match( build_label(obj['source_ref']), name=gnames[obj['source_ref']] ).first()
	target = m.match( build_label(obj['target_ref']), name=gnames[obj['target_ref']] ).first()

	# source = Node( build_label(obj['source_ref']), name=gnames[obj['source_ref']], id=obj['source_ref'] )
	# target = Node( build_label(obj['target_ref']), name=gnames[obj['target_ref']], id=obj['target_ref'] )
	relation = Relationship.type( obj['relationship_type'] )

	graph.merge(relation(source,target),build_label(obj['source_ref']),'name')
	print('Relation: "%s" -[%s]-> "%s"' % (gnames[obj['source_ref']],obj['relationship_type'],gnames[obj['target_ref']]) )

# -----------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------

# load JSON data from file
#json_file = 'mitre-enterprise-attack.json'
json_file = sys.argv[1]

with open(json_file) as fh:
    data = json.load(fh)
fh.close()

# open graph connection
graph_bolt = "bolt://127.0.0.1:7687"
graph_auth = ("neo4j","test")

graph = Graph(graph_bolt,auth=graph_auth)

# Delete existing nodes and edges
graph.delete_all()

# global names
gnames = {}

# Walk through JSON objects to create nodes
for obj in data['objects']:

	# if JSON object is about Groups
	if obj['type']=='intrusion-set':
		gnames[ obj['id'] ] = obj['name']
		build_aliases(obj,'aliases')

	# if JSON object is about Softwares
	if obj['type']=='malware':
		gnames[ obj['id'] ] = obj['name']
		build_aliases(obj,'x_mitre_aliases')

	# if JSON object is about Tools
	if obj['type']=='tool':
		gnames[ obj['id'] ] = obj['name']
		build_aliases(obj,'x_mitre_aliases')

	# if JSON object is about Techniques
	if obj['type']=='attack-pattern' or obj['type']=='course-of-action':
		gnames[ obj['id'] ] = obj['name']
		label = build_label(obj['type'])
		node_main = Node(label, name=obj['name'], id=obj['id'])
		graph.merge(node_main,label,'name')
		print('%s: "%s"' % (label,obj['name']) )

# Walk through JSON objects to create edges
for obj in data['objects']:

	# if JSON object is about Relationships
	if obj['type']=='relationship':
		build_relations(obj)

