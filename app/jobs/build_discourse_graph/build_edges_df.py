from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit, struct, to_json, split

from app.enums import RelationshipType
from app.utils import udf_build_association_edge_id


def build_protein_associations_df(discourse_nodes_df, protein_index: int):
     return discourse_nodes_df \
        .filter(discourse_nodes_df.type == 'claim') \
        .withColumn('target_id', split(discourse_nodes_df['name'], '_').getItem(protein_index)) \
        .select(
        lit(udf_build_association_edge_id(col("id"), col("target_id"))).alias("edge_id"),
        col("id").alias("source_id"),
        col("target_id").alias("target_id"),
        lit(RelationshipType.ASSOCIATES).alias("relation"),
        lit('string').alias("provenance")
    )


def build_edges_df(discourse_nodes_df: DataFrame) -> DataFrame:
    return build_protein_associations_df(discourse_nodes_df, 0) \
        .union(build_protein_associations_df(discourse_nodes_df, 1))
