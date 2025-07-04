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
        
        category = self._extract_category(normalized)
        base_attrs = {
            'normalized': normalized,
            'brand': self._extract_brand(normalized),
            'model': self._extract_model(normalized),
            'category': category
        }
        
        # Add category-specific attributes
        if category == 'Smartphone':
            base_attrs.update({
                'storage': self._extract_storage(normalized),
                'color': self._extract_color(normalized),
                'screen_size': self._extract_screen_size(normalized)
            })
        elif category == 'Laptop':
            base_attrs.update({
                'storage': self._extract_storage(normalized),
                'ram': self._extract_ram(normalized),
                'screen_size': self._extract_screen_size(normalized),
                'processor': self._extract_processor(normalized)
            })
        elif category == 'Sports':
            base_attrs.update({
                'size': self._extract_size(normalized),
                'color': self._extract_color(normalized),
                'type': self._extract_type(normalized)
            })
        
        return base_attrs
    
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
        query_lower = query.lower()
        if 'macbook' in query_lower or 'laptop' in query_lower:
            return 'Laptop'
        elif 'iphone' in query_lower or 'smartphone' in query_lower or 'phone' in query_lower:
            return 'Smartphone'
        elif 'nike' in query_lower or 'air max' in query_lower or 'sports' in query_lower or 'shoes' in query_lower or 'running' in query_lower:
            return 'Sports'
        else:
            return 'Smartphone'  # Default fallback
    
    def _extract_color(self, query: str) -> Optional[str]:
        """Extract color from query."""
        # TODO: Implement color extraction
        return None
    
    def _extract_screen_size(self, query: str) -> Optional[str]:
        """Extract screen size from query."""
        # TODO: Implement screen size extraction
        return None
    
    def _extract_ram(self, query: str) -> Optional[str]:
        """Extract RAM from query."""
        # TODO: Implement RAM extraction
        return None
    
    def _extract_processor(self, query: str) -> Optional[str]:
        """Extract processor from query."""
        # TODO: Implement processor extraction
        return None
    
    def _extract_size(self, query: str) -> Optional[str]:
        """Extract size from query."""
        # TODO: Implement size extraction
        return None
    
    def _extract_type(self, query: str) -> Optional[str]:
        """Extract type from query."""
        # TODO: Implement type extraction
        return None


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
        
        # Real logic would go here
        # For now, return basic attributes based on category detection
        query_lower = query.lower()
        if 'macbook' in query_lower or 'laptop' in query_lower:
            return {
                "brand": None,
                "model": None,
                "storage": None,
                "ram": None,
                "screen_size": None,
                "processor": None,
                "category": "Laptop"
            }
        elif 'nike' in query_lower or 'air max' in query_lower or 'sports' in query_lower or 'shoes' in query_lower or 'running' in query_lower:
            return {
                "brand": None,
                "model": None,
                "size": None,
                "color": None,
                "type": None,
                "category": "Sports"
            }
        else:
            # Default to smartphone attributes
            return {
                "brand": None,
                "model": None,
                "storage": None,
                "color": None,
                "screen_size": None,
                "category": "Smartphone"
            } 