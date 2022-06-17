from typing import List

from pyspark.sql import DataFrame
from pyspark.sql.functions import explode, array, struct, lit, col, udf


def build_claim_id(node_a_id: str, node_b_id: str, relationship_type: str):
    return f"{node_a_id}_{node_b_id}_{relationship_type}"


udf_build_claim_id = udf(
    lambda node_a_id, node_b_id, relationship_type: build_claim_id(node_a_id, node_b_id, relationship_type))


def build_association_edge_id(node_id: str, claim_id: str):
    return f"{node_id}__{claim_id}"


udf_build_association_edge_id = udf(
    lambda node_id, claim_id: build_association_edge_id(node_id, claim_id))


def transpose_columns(df: DataFrame, by: List[str]) -> DataFrame:
    # https://stackoverflow.com/questions/37864222/transpose-column-to-row-with-spark

    # Filter dtypes and split into column names and type description
    cols, dtypes = zip(*((c, t) for (c, t) in df.dtypes if c not in by))
    # Spark SQL supports only homogeneous columns
    assert len(set(dtypes)) == 1, "All columns have to be of the same type"

    # Create and explode an array of (column_name, column_value) structs
    kvs = explode(array([
        struct(lit(c).alias("key"), col(c).alias("val")) for c in cols
    ])).alias("kvs")

    return df.select(by + [kvs]).select(by + ["kvs.key", "kvs.val"])
