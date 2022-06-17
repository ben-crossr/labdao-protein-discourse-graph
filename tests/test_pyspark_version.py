from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
print(spark.version)

sc = spark.sparkContext
print(f"Hadoop version = {sc._jvm.org.apache.hadoop.util.VersionInfo.getVersion()}")
