"""
Ranker Interface
Ranks products by price and other factors for optimal presentation.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import yaml


class RankerInterface(ABC):
    """Interface for product ranker."""
    
    @abstractmethod
    def rank_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank products by price and other factors.
        
        Args:
            products: List of product dictionaries
            
        Returns:
            List of ranked products
        """
        pass


class MockRanker(RankerInterface):
    """Mock implementation of ranker."""
    
    def __init__(self, mock_data_path: str):
        self.mock_data_path = mock_data_path
        
    def rank_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Mock implementation that returns predefined ranked data."""
        try:
            with open(self.mock_data_path, 'r') as f:
                mock_data = yaml.safe_load(f)
                
            return mock_data.get('ranked_results', [])
                
        except Exception:
            # Return products sorted by price
            return sorted(products, key=lambda x: float(x.get('price', 0)))


class RealRanker(RankerInterface):
    """Real implementation of ranker."""
    
    def rank_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Real implementation for product ranking.
        This would use ML models, business rules, etc.
        """
        # TODO: Implement real ranking logic
        # For now, sort by price
        return sorted(products, key=lambda x: float(x.get('price', 0))) 


class Ranker:
    """
    Ranker sorts deduplicated products by best value criteria.
    In mock mode, returns predefined ranked results from configuration.
    """
    
    def __init__(self, config):
        """
        Initialize Ranker with config dict or YAML path.
        
        Args:
            config (dict or str): Config dict or path to YAML config file.
        """
        if isinstance(config, str):
            with open(config, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = config
            
        self.use_mock = self.config.get('modules', {}).get('ranker', {}).get('use_mock', True)
        self.mock_results = self.config.get('modules', {}).get('ranker', {}).get('mock_ranked_results', {})
    
    def rank(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank products by best value criteria.
        
        Args:
            products (List[Dict[str, Any]]): List of deduplicated product entries
            
        Returns:
            List[Dict[str, Any]]: Ranked list of products (best value first)
            
        Raises:
            NotImplementedError: If use_mock is False (real ranking not implemented)
        """
        if self.use_mock:
            # Check if input matches mock input pattern
            mock_input = self.mock_results.get('input_products', [])
            if self._lists_match(products, mock_input):
                return self.mock_results.get('output_products', []).copy()
            else:
                # If no exact match, perform basic price-based ranking
                return self._basic_rank(products)
        else:
            # TODO: Real implementation would use multi-factor scoring
            raise NotImplementedError("Real ranking not implemented yet")
    
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
    
    def _basic_rank(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Perform basic price-based ranking when mock input doesn't match.
        
        Args:
            products (List[Dict[str, Any]]): List of products to rank
            
        Returns:
            List[Dict[str, Any]]: Ranked list (lowest price first)
        """
        if not products:
            return []
        
        # Convert price strings to floats for comparison
        def get_price(product):
            try:
                return float(product.get('price', '0'))
            except (ValueError, TypeError):
                return float('inf')  # Put invalid prices at the end
        
        # Sort by price (ascending - lowest price first)
        ranked_products = sorted(products, key=get_price)
        
        return ranked_products
    
    def _calculate_score(self, product: Dict[str, Any]) -> float:
        """
        Calculate a composite score for a product (for future real implementation).
        
        Args:
            product (Dict[str, Any]): Product to score
            
        Returns:
            float: Composite score (higher is better)
        """
        # TODO: Implement multi-factor scoring
        # Factors to consider:
        # - Price (lower is better)
        # - Vendor trust score
        # - Delivery speed
        # - Local availability
        # - User ratings
        # - Return policy
        # - Warranty coverage
        
        base_price = float(product.get('price', '0'))
        if base_price <= 0:
            return 0.0
        
        # For now, just return inverse of price (lower price = higher score)
        return 1000.0 / base_price 