# labdao-protein-discourse-graph

### Description

A pyspark pipeline to build a biomedical discourse graph.

### Useful Links

- [Pyspark save to s3](https://stackoverflow.com/questions/45869510/pyspark-save-dataframe-to-s3)
- [Pyspark Example Project](https://github.com/AlexIoannides/pyspark-example-project)
- [Running a Spark ETL Job](https://github.com/AlexIoannides/pyspark-example-project#running-the-etl-job)
- [Batch Importer Neo4J Docs](https://neo4j.com/developer/guide-import-csv/#batch-importer)
- [Neo4j Admin Import Tool Manual](https://neo4j.com/docs/operations-manual/current/tools/neo4j-admin/neo4j-admin-import)
- [Accessing Nested Data in PySpark](https://stackoverflow.com/questions/34043031/accessing-nested-data-in-spark/34044373)
- [Parquet FileFormat](https://jaceklaskowski.gitbooks.io/mastering-spark-sql/content/spark-sql-ParquetFileFormat.html)
- [Merge Multiple Columns To Json Pyspark](https://stackoverflow.com/questions/60435907/pyspark-merge-multiple-columns-into-a-json-column)
- [Deploy Neo4J With AWS Docs](https://neo4j.com/developer/neo4j-cloud-aws-ec2-ami/)

#### Pipelines

##### app/jobs/build_discourse_graph/build_discourse_graph.py
- input network graph.
- config file includes nodes types of interest + edge types of interest.
- pipeline builds discourse graph from input. 
- converts to neo4j output.
- stores to aws or local.

##### app/jobs/build_analytics_graph/build_analytics_graph.py
- input discourse graph.
- for each claim calculates the scores of each evidence piece.
- collapses the claim nodes to edges with the calculated score.

### Development Notes

#### Steps to Run Job

##### Build Dependencies

`./build_dependencies.sh`

#### AWS

#### only more recent versions Neo4J version are available

##### Run Spark Submit (With AWS Jar) (in bash not zsh)

`
spark-submit \
--master local[*] \
--properties-file configs/secret/secret.conf \
--jars jars/org.apache.hadoop_hadoop-aws-3.3.1.jar,jars/aws-java-sdk-bundle-1.11.375.jar \
--py-files packages.zip \
--files configs/local_etl_config.json app/jobs/build_discourse_graph/build_discourse_graph.py
`

#### Neo4J Ports

http: 7474
https: 7473
bolt: 7683
``
