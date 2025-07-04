"""
Deduplicator Interface
Removes duplicate product entries based on similarity matching.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import yaml


class DeduplicatorInterface(ABC):
    """Interface for data deduplicator."""
    
    @abstractmethod
    def deduplicate_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicate products from a list.
        
        Args:
            products: List of product dictionaries
            
        Returns:
            List of unique products
        """
        pass


class MockDeduplicator(DeduplicatorInterface):
    """Mock implementation of deduplicator."""
    
    def __init__(self, mock_data_path: str):
        self.mock_data_path = mock_data_path
        
    def deduplicate_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Mock implementation that returns predefined deduplicated data."""
        try:
            with open(self.mock_data_path, 'r') as f:
                mock_data = yaml.safe_load(f)
                
            return mock_data.get('deduplicated_products', [])
                
        except Exception:
            # Return products with basic deduplication
            return products


class RealDeduplicator(DeduplicatorInterface):
    """Real implementation of deduplicator."""
    
    def deduplicate_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Real implementation for product deduplication.
        This would use fuzzy matching, ML models, etc.
        """
        # TODO: Implement real deduplication logic
        # For now, return products as-is
        return products 


class Deduplicator:
    """
    Deduplicator removes duplicate products from a list of validated entries.
    In mock mode, returns predefined deduplicated results from configuration.
    """
    
    def __init__(self, config):
        """
        Initialize Deduplicator with config dict or YAML path.
        
        Args:
            config (dict or str): Config dict or path to YAML config file.
        """
        if isinstance(config, str):
            with open(config, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = config
            
        self.use_mock = self.config.get('modules', {}).get('deduplicator', {}).get('use_mock', True)
        self.mock_results = self.config.get('modules', {}).get('deduplicator', {}).get('mock_deduplicated_results', {})
    
    def deduplicate(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicate products from the input list.
        
        Args:
            products (List[Dict[str, Any]]): List of validated product entries
            
        Returns:
            List[Dict[str, Any]]: Deduplicated list of products
            
        Raises:
            NotImplementedError: If use_mock is False (real deduplication not implemented)
        """
        if self.use_mock:
            # Check if input matches mock input pattern
            mock_input = self.mock_results.get('input_products', [])
            if self._lists_match(products, mock_input):
                return self.mock_results.get('output_products', []).copy()
            else:
                # If no exact match, perform basic deduplication
                return self._basic_deduplicate(products)
        else:
            # TODO: Real implementation would use semantic embeddings or ML
            raise NotImplementedError("Real deduplication not implemented yet")
    
    def _lists_match(self, list1: List[Dict[str, Any]], list2: List[Dict[str, Any]]) -> bool:
        """
        Check if two lists of products match (for mock input validation).
        
        Args:
            list1: First list of products
            list2: Second list of products
            
        Returns:
            bool: True if lists match, False otherwise
        """
        if len(list1) != len(list2):
            return False
        
        # Sort both lists by product name for comparison
        sorted1 = sorted(list1, key=lambda x: x.get('productName', ''))
        sorted2 = sorted(list2, key=lambda x: x.get('productName', ''))
        
        return sorted1 == sorted2
    
    def _basic_deduplicate(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Perform basic deduplication when mock input doesn't match.
        
        Args:
            products (List[Dict[str, Any]]): List of products to deduplicate
            
        Returns:
            List[Dict[str, Any]]: Deduplicated list
        """
        seen = set()
        unique_products = []
        
        for product in products:
            # Create a key based on product name and price for deduplication
            product_key = f"{product.get('productName', '')}_{product.get('price', '')}_{product.get('currency', '')}"
            
            if product_key not in seen:
                seen.add(product_key)
                unique_products.append(product)
        
        return unique_products 