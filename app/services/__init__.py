"""
Core ETL pipeline functionality for processing bank statements.
"""

from .extractor import DataExtractor
from .parser import AIParser
from .transformer import DataTransformer, Transaction
from .loader import DataLoader
from .pipeline import Pipeline
from .data_input import DataInput
