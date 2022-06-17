from enum import Enum


class FileFormat(str, Enum):
    APACHE_PARQUET = "apache_parquet"
    CSV = "csv"
    NEO4J_CSV = "neo4j_csv"
    CONSOLE = "console"
    TSV = "tsv"
    TXT = "txt"


class DataType(str, Enum):
    NODES = "nodes"
    EDGES = "edges"


class NodeType(str, Enum):
    PROTEIN = "protein"
    CLAIM = "claim"


class RelationshipType(str, Enum):
    ASSOCIATES = "associates"


class InteractionType(str, Enum):
    NEIGHBORHOOD = "neighborhood",
    FUSION = "fusion",
    COOCCURENCE = "cooccurence",
    COEXPRESSION = "coexpression",
    EXPERIMENTS = "experiments",
    DATABASE = "database",
    TEXTMINING = "textmining"
