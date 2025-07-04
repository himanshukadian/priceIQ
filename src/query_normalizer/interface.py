"""
Query Normalizer Interface
Normalizes product queries for consistent processing across modules.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import yaml


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
            Dict containing normalized query and extracted metadata
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
                # Default fallback
                return {
                    'normalized': query,
                    'brand': None,
                    'model': None,
                    'storage': None,
                    'category': 'default'
                }
        except Exception:
            return {
                'normalized': query,
                'brand': None,
                'model': None,
                'storage': None,
                'category': 'default'
            }


class RealQueryNormalizer(QueryNormalizerInterface):
    """Real implementation of query normalizer."""
    
    def normalize_query(self, query: str, country: str) -> Dict[str, Any]:
        """
        Real implementation for query normalization.
        This would use NLP techniques, product databases, etc.
        """
        # TODO: Implement real query normalization logic
        # For now, return a basic normalized version
        normalized = query.strip().replace(',', ' ').replace('  ', ' ')
        
        return {
            'normalized': normalized,
            'brand': self._extract_brand(normalized),
            'model': self._extract_model(normalized),
            'storage': self._extract_storage(normalized),
            'category': self._extract_category(normalized)
        }
    
    def _extract_brand(self, query: str) -> Optional[str]:
        """Extract brand from query."""
        # TODO: Implement brand extraction
        return None
    
    def _extract_model(self, query: str) -> Optional[str]:
        """Extract model from query."""
        # TODO: Implement model extraction
        return None
    
    def _extract_storage(self, query: str) -> Optional[str]:
        """Extract storage capacity from query."""
        # TODO: Implement storage extraction
        return None
    
    def _extract_category(self, query: str) -> str:
        """Extract product category from query."""
        # TODO: Implement category extraction
        return 'default'


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
        self.mock_output = self.config.get('modules', {}).get('query_normalizer', {}).get('mock_output', {})

    def normalize(self, query: str) -> dict:
        """
        Normalize a product query string.
        In mock mode, returns mock output from config.
        Args:
            query (str): Raw product query string.
        Returns:
            dict: Normalized product info.
        """
        if self.use_mock:
            return self.mock_output.copy()
        # Real logic would go here
        return {
            "brand": None,
            "model": None,
            "storage": None,
            "category": None
        } 