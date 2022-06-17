from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit, to_json, struct

from app.enums import NodeType
from app.utils import transpose_columns, udf_build_claim_id


def build_protein_nodes(proteins_df):
    return proteins_df.select(
        col('#string_protein_id').alias('id'),
        col('preferred_name').alias('name'),
        lit(NodeType.PROTEIN).alias('type'),
        lit(NodeType.PROTEIN).alias('label'),
        to_json(struct(col('protein_size').alias('protein_size'), col('annotation').alias('annotation'))).alias(
            'context')
    )


def build_claim_nodes(interactions_df: DataFrame):
    filtered_interactions_df = interactions_df.select(
        col('protein1'),
        col('protein2'),
        col('neighborhood'),
        col('fusion'),
        col('cooccurence'),
        col('coexpression'),
        col('experiments'),
        col('database'),
        col('textmining')
    )
    transposed_interaction_df = transpose_columns(filtered_interactions_df, ['protein1', 'protein2'])
    return transposed_interaction_df \
        .filter(transposed_interaction_df.val != 0) \
        .select(
        lit(udf_build_claim_id(col('protein1'), col('protein2'), col('key'))).alias('id'),
        lit(udf_build_claim_id(col('protein1'), col('protein2'), col('key'))).alias('name'),
        lit(NodeType.CLAIM).alias('type'),
        lit(NodeType.CLAIM).alias('label'),
        to_json(struct(col('key').alias('interaction_type'), col('protein1'), col('protein2'), lit("string").alias('provenance'), col('val').alias('score'))).alias('context')
    )


def build_nodes_df(proteins_df, interactions_df):
    return build_protein_nodes(proteins_df) \
        .union(build_claim_nodes(interactions_df))
