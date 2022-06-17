from pyspark.sql import DataFrame

from app.enums import FileFormat


def store_data(df: DataFrame, destination_path: str, file_format=FileFormat.APACHE_PARQUET,
               mode='overwrite', partition_columns: list = None, sep: str = "§"):
    if file_format == FileFormat.APACHE_PARQUET:
        df.write.parquet(destination_path)
    elif file_format == FileFormat.CSV:
        if partition_columns:
            df.write.partitionBy(partition_columns).mode(mode).format("csv")\
                .option("quote", "\u0000").option("sep", sep).save(destination_path)
        else:
            df.write.option("quote", "\u0000").option("sep", sep).mode(mode).format("csv").save(destination_path)
    elif file_format == FileFormat.CONSOLE:
        df.show(5, False)
    else:
        raise NotImplementedError()
