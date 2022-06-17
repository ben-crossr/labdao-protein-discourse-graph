from datetime import datetime

from app.data_loader.data_loader import load_data
from app.data_store.data_store import store_data
from app.dependencies.spark import start_spark
from app.enums import FileFormat
from app.jobs.build_discourse_graph.build_edges_df import build_edges_df
from app.jobs.build_discourse_graph.build_nodes_df import build_nodes_df


def run():
    spark, log, config = start_spark(
        app_name='build_discourse_graph',
        files=['configs/*etl_config.json'])

    spark.sparkContext.setLogLevel(config['log_level'])

    # log that ETL job is starting
    log.warn('biomedical_discourse_graph job is up-and-running')

    proteins_df = load_data(spark, f"{config['input_nodes_data_path']}", file_format=FileFormat.TSV)
    interactions_df = load_data(spark, f"{config['input_edges_data_path']}", file_format=FileFormat.TXT)

    discourse_nodes_df = build_nodes_df(proteins_df, interactions_df)
    discourse_edges_df = build_edges_df(discourse_nodes_df)

    store_data(df=discourse_nodes_df,
               destination_path=f"{config['aws_output_data_path']}/nodes_{datetime.now().strftime('%Y-%m-%d')}",
               file_format=FileFormat.CSV)
    store_data(df=discourse_edges_df,
               destination_path=f"{config['aws_output_data_path']}/relationships_{datetime.now().strftime('%Y-%m-%d')}",
               file_format=FileFormat.CSV)


if __name__ == "__main__":
    run()
