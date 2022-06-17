// FROM Base of Neo4J VM Image (Neo4J Community Edition for Compute Engine - for example)

datetime="2022-06-15"

sudo aws s3 cp --recursive --include "*.csv" s3://biomedical-discourse-graph/nodes_${datetime} var/lib/neo4j/import/nodes

sudo aws s3 cp s3://biomedical-discourse-graph/neo4j/nodes-headers.csv var/lib/neo4j/import/nodes-headers.csv

sudo aws s3 cp --recursive --include "*.csv" s3://biomedical-discourse-graph/relationships_${datetime} var/lib/neo4j/import/relationships

sudo aws s3 cp s3://biomedical-discourse-graph/neo4j/relationships-headers.csv var/lib/neo4j/import/relationships-headers.csv

sudo usr/bin/neo4j-admin import --delimiter="§" --nodes "var/lib/neo4j/import/nodes-headers.csv,var/lib/neo4j/import/nodes/.*.csv" --database discourse --relationships "var/lib/neo4j/import/relationships-headers.csv,var/lib/neo4j/import/relationships/.*.csv"

sudo chown -R neo4j:neo4j /var/lib/neo4j/data/transactions/discourse

sudo chown -R neo4j:neo4j /var/lib/neo4j/data/databases/discourse


// Cypher commands to run after for bootstrapping.

CREATE DATABASE discourse


// to delete if testing

sudo rm -rf var/lib/neo4j/import/nodes
sudo rm  var/lib/neo4j/import/relationships
sudo rm -rf /var/lib/neo4j/data/transactions/discourse
sudo rm -rf /var/lib/neo4j/data/databases/discourse

DROP DATABASE discourse


// delete directories if need be.