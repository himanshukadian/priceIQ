"""
Query Normalizer Interface
Normalizes product queries for consistent processing across modules.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import yaml
from .real_normalizer import RealQueryNormalizer


class QueryNormalizerInterface(ABC):
    """Interface for query normalization."""
    
    @abstractmethod
    def normalize_query(self, query: str, country: str) -> Dict[str, Any]:
        """
        Normalize a product query.
        
        Args:
            query: Raw product query string
            country: Country code (e.g., "US", "UK", "DE")
            
        Returns:
            Dict containing normalized query and category-specific attributes
        """
        pass


class MockQueryNormalizer(QueryNormalizerInterface):
    """Mock implementation of query normalizer."""
    
    def __init__(self, mock_data_path: str):
        self.mock_data_path = mock_data_path
        
    def normalize_query(self, query: str, country: str) -> Dict[str, Any]:
        """Mock implementation that returns predefined normalized data."""
        try:
            with open(self.mock_data_path, 'r') as f:
                mock_data = yaml.safe_load(f)
                
            if query in mock_data.get('queries', {}):
                return mock_data['queries'][query]
            else:
                # Default fallback - return smartphone attributes
                return {
                    'normalized': query,
                    'brand': None,
                    'model': None,
                    'storage': None,
                    'color': None,
                    'screen_size': None,
                    'category': 'Smartphone'
                }
        except Exception:
            return {
                'normalized': query,
                'brand': None,
                'model': None,
                'storage': None,
                'color': None,
                'screen_size': None,
                'category': 'Smartphone'
            }



class QueryNormalizer:
    """
    QueryNormalizer normalizes product queries for downstream modules.
    In mock mode, returns predefined output from config.
    """
    def __init__(self, config):
        """
        Initialize QueryNormalizer with config dict or YAML path.
        Args:
            config (dict or str): Config dict or path to YAML config file.
        """
        if isinstance(config, str):
            with open(config, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = config
        self.use_mock = self.config.get('modules', {}).get('query_normalizer', {}).get('use_mock', True)
        self.mock_outputs = self.config.get('modules', {}).get('query_normalizer', {}).get('mock_outputs', {})
        
        # Initialize real normalizer if not using mock
        if not self.use_mock:
            self.real_normalizer = RealQueryNormalizer()

    def normalize(self, query: str) -> dict:
        """
        Normalize a product query string.
        In mock mode, returns mock output from config based on query content.
        Args:
            query (str): Raw product query string.
        Returns:
            dict: Normalized product info.
        """
        if self.use_mock:
            # Determine category based on query content
            query_lower = query.lower()
            if 'macbook' in query_lower or 'laptop' in query_lower:
                return self.mock_outputs.get('laptop', {}).copy()
            elif 'iphone' in query_lower or 'smartphone' in query_lower or 'phone' in query_lower:
                return self.mock_outputs.get('smartphone', {}).copy()
            elif 'nike' in query_lower or 'air max' in query_lower or 'sports' in query_lower or 'shoes' in query_lower or 'running' in query_lower:
                return self.mock_outputs.get('sports', {}).copy()
            elif 'samsung' in query_lower or 'galaxy' in query_lower:
                return self.mock_outputs.get('samsung', {}).copy()
            else:
                # Default to smartphone for backward compatibility
                return self.mock_outputs.get('smartphone', {}).copy()
        else:
            # Use real implementation
            return self.real_normalizer.normalize_query(query, country="US") 