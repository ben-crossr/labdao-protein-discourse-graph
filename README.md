# knowledge-graph-pipeline

### Description

A pyspark pipeline to build a biomedical discourse graph.

### Useful Links

[Pyspark save to s3](https://stackoverflow.com/questions/45869510/pyspark-save-dataframe-to-s3)
[Pyspark Example Project](https://github.com/AlexIoannides/pyspark-example-project)
[Running a Spark ETL Job](https://github.com/AlexIoannides/pyspark-example-project#running-the-etl-job)
[Batch Importer Neo4J Docs](https://neo4j.com/developer/guide-import-csv/#batch-importer)
[Neo4j Admin Import Tool Manual](https://neo4j.com/docs/operations-manual/current/tools/neo4j-admin/neo4j-admin-import)
[Accessing Nested Data in PySpark](https://stackoverflow.com/questions/34043031/accessing-nested-data-in-spark/34044373)
[Parquet FileFormat](https://jaceklaskowski.gitbooks.io/mastering-spark-sql/content/spark-sql-ParquetFileFormat.html)
[Merge Multiple Columns To Json Pyspark](https://stackoverflow.com/questions/60435907/pyspark-merge-multiple-columns-into-a-json-column)
[Deploy Neo4J With AWS Docs](https://neo4j.com/developer/neo4j-cloud-aws-ec2-ami/)

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

##### Workflow

- Store partitioned csv data in s3
- Create AWS key pair for SSH
- [Or create using aws console](https://neo4j.com/developer/neo4j-cloud-aws-ec2-ami/)
- NB: modify the storage volume to have 50GB disk space.
- assign ec2 iam role `s3FullAccess`
- if new security group - make sure it exposes neo4j ports see `Enable public access to AWS security group`
  
- Once up and running view app at https://[PublicDnsName]:7474.
- initial username/pass = neo4j/neo4j.
  
- chmod 600 $KEY_NAME.pem (for new private key).
- ssh into instance using AWS the downloaded private key from pair.
  `ssh -i $KEY_NAME.pem ubuntu@[PublicDnsName]`
  `ssh -i creds/neo4j-useast-1.pem ubuntu@ec2-3-235-242-133.compute-1.amazonaws.com`
  
- update  /etc/neo4j/neo4j.template (use / search in vim to find line).
`sudo vi /etc/neo4j/neo4j.template`
`uncomment dbms.security.procedures.unrestricted=apoc.*,bloom.*,gds.*`
`uncomment dbms.directories.plugins=/var/lib/neo4j/plugins`

- Increase disk space for ec2 instance of neo4j. 
https://www.howtoforge.com/how-to-increase-the-disk-space-of-an-aws-ec2-ubuntu-instance/

- execute script `infra/bin/bootstrap-aws-neo4j.sh` 

- create database
`
  CREATE DATABASE <DATABASE_NAME>
`

- create api user + grant permissions
`CREATE USER api SET PASSWORD "<PWD>"`
`GRANT ACCESS ON DATABASE * TO `publisher``
`GRANT role `publisher` to api`
- use browser to change api user pass.
- update bolt url (IP format), user, pass in api env - local then remote.



##### Run Spark Submit (With AWS Jar) (in bash not zsh)

`
spark-submit \
--master local[*] \
--properties-file configs/secret/secret.conf \
--jars jars/org.apache.hadoop_hadoop-aws-3.3.1.jar,jars/aws-java-sdk-bundle-1.11.375.jar \
--py-files packages.zip \
--files configs/local_etl_config.json app/jobs/build_discourse_graph/build_discourse_graph.py
`

#### Example `neo4j-admin` CSV Import

```
../bin/neo4j-admin import --database orders
     --nodes=Order="orders_header.csv,orders1.csv,orders2.csv"
    --nodes=Product="products_header.csv,products1.csv,products2.csv"
     --relationships=ORDERED="customer_orders_header.csv,orders1.csv,orders2.csv"
     --trim-strings=true
```

#### APOC command to query nested json for context/evidence
`apoc.convert.fromJsonMap(n.context)` 

#### Exec into Docker Image

`docker run -it --entrypoint=/bin/bash <IMAGE_NAME>`

#### Run Neo4j Docker in background

docker run -d --volume=dummy:/var/lib/neo4j/import/dummy neo4j

`docker run -d neo4j`
`docker exec -it <CONTAINER_ID> bin/bash`


### Enable public access to AWS security group
```
GROUP="<group_name>"
for port in 22 7474 7473 7687; do
  aws ec2 authorize-security-group-ingress --group-name $GROUP --protocol tcp --port $port --cidr 0.0.0.0/0
done
```

#### Run Neo4j-Admin on local container

`
docker exec --interactive --tty <CONTAINER_ID> neo4j-admin import --nodes "infra/resources/neo4j/nodes-headers.csv,data/output/test-nodes.csv" --database <DATABASE_NAME> --relationships "infra/resources/neo4j/relationships-headers.csv,var/lib/neo4j/import/relationships/.*.csv"
docker exec --interactive --tty <CONTAINER_ID> neo4j-admin import --nodes "infra/resources/neo4j/nodes-headers.csv,data/output/test-nodes.csv" --database <DATABASE_NAME>
`
#### Neo4J Ports

http: 7474
https: 7473
bolt: 7683
``
