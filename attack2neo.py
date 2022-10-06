#!/usr/bin/env python3

import argparse
import json
import re
import sys
from py2neo import Graph, Node, Relationship, NodeMatcher, cypher

# -----------------------------------------------------------------
# BUILD_LABEL
# -----------------------------------------------------------------
def build_label(txt):

	if txt.startswith('intrusion-set'):		return 'Group'
	if txt.startswith('malware'):			return 'Software'
	if txt.startswith('tool'):				return 'Tool'
	if txt.startswith('attack-pattern'):	return 'Technique'
	if txt.startswith('course-of-action'):	return 'Technique'
	if txt.startswith('x-mitre-tactic'):	return 'Technique'
	return 'Unknown'

# -----------------------------------------------------------------
# BUILD ALIASES
# -----------------------------------------------------------------
def build_objects(obj,key):

	label = build_label(obj['type'])

	# add properties
	props = {}
	props['name'] = obj['name']
	props['id'] = obj['id']
	props['type'] = obj['type']
	if obj.get('description'):		props['description'] = obj['description'] # cypher.cypher_escape( obj['description'] )
	if obj.get('created'):			props['created'] = obj['created']
	if obj.get('modified'):			props['modified'] = obj['modified']
	if obj.get('x_mitre_version'):	props['version'] = obj['x_mitre_version']

	# kem Add TechniqueID ( the T/TA numbers) from each data['object']
	if obj.get('external_references'):
		for ref in obj['external_references']:
			if ref.get('external_id'):
#				if ref.get('external_id').startswith('T'): 
#				props.setdefault('technique_id', []).append(ref['external_id']) 
				props['technique_id'] = ref['external_id']		# capture T/TA# and change name to technique_id
			else: 
				continue 
	
	# create node for the group
	node_main = Node(label, **props)
	# merge node to graph
	graph.merge(node_main,label,'name')
	print('%s: "%s"' % (label,obj['name']),end='') if dbg_mode else None

	# dealing with aliases
	if obj.get('aliases'): 
		aliases = obj['aliases']
	elif obj.get('x_mitre_aliases'): 
		aliases = obj['x_mitre_aliases']
	else:
		aliases = None
	if aliases:
		for alias in aliases:
			if alias != obj['name']:
				node_alias = Node('Alias', name=alias, type=obj['type'])
				relation = Relationship.type('alias')
				graph.merge(relation(node_main,node_alias),label,'name')
				print(' -[alias]-> "%s"' % (alias),end='') if dbg_mode else None
	print() if dbg_mode else None

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
	print('Relation: "%s" -[%s]-> "%s"' % (gnames[obj['source_ref']],obj['relationship_type'],gnames[obj['target_ref']]) ) if dbg_mode else None

# -----------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------

#
# set command-line arguments and parsing options
parser = argparse.ArgumentParser()
parser.add_argument('-d','--debug', help='enter debug mode', default=False, action='store_true')
parser.add_argument('-f', help='input file name', metavar='<filename>', action='store', required=True)
parser.add_argument('-g','--groups', help='import Groups objects (type:intrusion-set)', default=False, action='store_true')
parser.add_argument('-s','--softwares', help='import Softwares objects (type:malware)', default=False, action='store_true')
parser.add_argument('-o','--tools', help='import Tools objects (type:tool)', default=False, action='store_true')
parser.add_argument('-t','--techniques', help='import Techniques objects (type:attack-pattern and type:course-of-action)', default=False, action='store_true')
parser.add_argument('-r','--relations', help='import Relations objects (type:relationship)', default=False, action='store_true')
args = parser.parse_args()

#
# checks arguments and options
dbg_mode = True if args.debug else None
json_file = args.f if args.f else None

#
# load JSON data from file
try:
	with open(json_file, encoding='utf-8') as fh:
		data = json.load(fh)
	fh.close()
except Exception as e:
	sys.stderr.write( '[ERROR] reading configuration file %s\n' % json_file )
	sys.stderr.write( '[ERROR] %s\n' % str(e) )
	sys.exit(1)

#
# open graph connection
graph_bolt = "bolt://127.0.0.1:7687"
graph_auth = ("neo4j","test")

graph = Graph(graph_bolt,auth=graph_auth)

# 
# Delete existing nodes and edges
graph.delete_all()

# 
# Global names
gnames = {}

# 
# Walk through JSON objects to create nodes
for obj in data['objects']:

	# if JSON object is about Groups
	if args.groups and obj['type']=='intrusion-set':
		gnames[ obj['id'] ] = obj['name']
		build_objects(obj,'aliases')

	# if JSON object is about Softwares
	if args.softwares and obj['type']=='malware':
		gnames[ obj['id'] ] = obj['name']
		build_objects(obj,'x_mitre_aliases')

	# if JSON object is about Tools
	if args.tools and obj['type']=='tool':
		gnames[ obj['id'] ] = obj['name']
		build_objects(obj,'x_mitre_aliases')

	# if JSON object is about Techniques
	if args.techniques and (obj['type']=='attack-pattern' or obj['type']=='course-of-action' or obj['type']=='x-mitre-tactic'):
		gnames[ obj['id'] ] = obj['name']
		build_objects(obj,None)
		# label = build_label(obj['type'])
		# node_main = Node(label, name=obj['name'], id=obj['id'])
		# graph.merge(node_main,label,'name')
		# print('%s: "%s"' % (label,obj['name']) ) if dbg_mode else None

# 
# Walk through JSON objects to create edges
for obj in data['objects']:

	# if JSON object is about Relationships
	if args.relations and obj['type']=='relationship':
		build_relations(obj)

#
# End
