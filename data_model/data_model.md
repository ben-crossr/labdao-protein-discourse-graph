
### Data Model

### Node Generic Model
Tuple of the format (id, label, type, context)
- id: preferred ID (of format DATASET_ID:CODE, i.e. ENSEMBL:ENSG0001)
- name: preferred name of node (can be symbol for GeneProtein).
- type: node type i.e GeneProtein
- label: matches type but duplicated for neo4j labelling.
- context: {types: [<list of all types node fits in, i.e. Disease,Side Effect>],
           labels: {<dict of all labels i.e. description:"",synonym:"">}}


### Edge Generic Model
Tuple of the format (source_id, target_id, relation, score, provenance, evidence)
- source id, target id: identifiers of the nodes connected by an edge. 
- relation: the type of the relationship i.e. (contains).
- score: score (likely 1 for discourse graphs)
- provenance: the source data set identifier (or other provenance id).
- evidence: zero or more metadata columns associated with an edge.
    - i.e. {'log2fc': 4, 'fdr_value': 0.02}
    

### Discourse Graph Model
- Convert sub-interactions into nodes of type Claim.
- Create edge for associates between the original nodes (Protein) + new Claim node with type associates.


#### Neo4J Output Data Model

- Neo4J Requires a CSV for nodes + a CSV for relationships.
- For imports using neo4j admin tool, you also must include a headers file for both (stored in `infra/resources/neo4j-<data_type>-headers.csv`)
- Neo4J requires the following headers in node headers file (need same positioning in data file): `:ID`,`:LABEL`.
- Neo4J requires the following headers in relationship headers file (need same positioning in data file): `:START_ID`,`:END_ID`,`:TYPE`.
- The headers must be the same for every row in a file, meaning that for different node types, multiple files are required (1 for GeneProtein, 1 for Disease etc).