"""
Core ETL pipeline functionality for processing bank statements.
"""

from .data_input import DataInput
from .extractor import DataExtractor, ExtractedData
from .parser import AIParser
from .transformer import DataTransformer, RawTransaction, EnrichedTransaction
from .loader import DataLoader
from .pipeline import Pipeline