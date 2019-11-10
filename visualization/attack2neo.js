//
// powered by NeoVis
// https://github.com/neo4j-contrib/neovis.js
//
var viz;

function draw() {
	var config = {
		container_id: "viz",
		server_url: "bolt://localhost:7687",
		server_user: "neo4j",
		server_password: "test",
		labels: {
			"Alias": 	{ "caption": "name", "size":2 },
			"Group": 	{ "caption": "name", "size":2 },
			"Software": { "caption": "name", "size":1 },
			"Tool": 	{ "caption": "name", "size":1 },
		},
		relationships: {
			"alias": 		{ "caption": true },
			"uses": 		{ "caption": true },
			"revoked-by": 	{ "caption": true },
		},
		arrows: true,
		hierarchical: false,
		hierarchical_sort_method: "directed",
		console_debug: false,
		//initial_cypher: "MATCH (n)-[r]-(m) WHERE n.name=\"APT1\" RETURN n,r,m"
		initial_cypher: "MATCH (n)-[r]-(m) RETURN n,r,m"
	};

	viz = new NeoVis.default(config);
	viz.render();
}
