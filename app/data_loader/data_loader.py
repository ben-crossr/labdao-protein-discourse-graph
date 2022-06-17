from pyspark.sql import SparkSession, DataFrame

from app.enums import FileFormat


def load_data(spark: SparkSession, data_path: str, file_format=FileFormat.APACHE_PARQUET, contains_header=True, sep=' ') -> DataFrame:
    if file_format == FileFormat.APACHE_PARQUET:
        df = spark.read.parquet(data_path)
    elif file_format == FileFormat.TSV:
        df = spark.read.csv(data_path, sep=r'\t', header=contains_header)
    elif file_format == FileFormat.TXT:
        df = spark.read.csv(data_path, sep=sep, header=contains_header)
    else:
        raise NotImplementedError()
    return df
