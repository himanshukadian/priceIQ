"""
Validator Interface
Validates extracted product data for accuracy and completeness.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import yaml


class ValidatorInterface(ABC):
    """Interface for data validator."""
    
    @abstractmethod
    def validate_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate a list of product data.
        
        Args:
            products: List of product dictionaries
            
        Returns:
            List of validated products with validation scores
        """
        pass


class MockValidator(ValidatorInterface):
    """Mock implementation of validator."""
    
    def __init__(self, mock_data_path: str):
        self.mock_data_path = mock_data_path
        
    def validate_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Mock implementation that returns predefined validation results."""
        try:
            with open(self.mock_data_path, 'r') as f:
                mock_data = yaml.safe_load(f)
                
            return mock_data.get('validated_products', [])
                
        except Exception:
            # Return products with basic validation
            validated = []
            for product in products:
                validated.append({
                    **product,
                    'validation_score': 0.8,
                    'is_valid': True
                })
            return validated


class RealValidator(ValidatorInterface):
    """Real implementation of validator."""
    
    def validate_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Real implementation for data validation.
        This would use ML models, business rules, etc.
        """
        # TODO: Implement real validation logic
        # For now, return products with basic validation
        validated = []
        for product in products:
            validated.append({
                **product,
                'validation_score': 0.8,
                'is_valid': True
            })
        return validated 


class Validator:
    """
    Validator checks if extracted product data matches the original query.
    In mock mode, returns predefined validation results from configuration.
    """
    
    def __init__(self, config):
        """
        Initialize Validator with config dict or YAML path.
        
        Args:
            config (dict or str): Config dict or path to YAML config file.
        """
        if isinstance(config, str):
            with open(config, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = config
            
        self.use_mock = self.config.get('modules', {}).get('validator', {}).get('use_mock', True)
        self.mock_validations = self.config.get('modules', {}).get('validator', {}).get('mock_validations', [])
    
    def validate(self, query_struct: Dict[str, Any], product_data: Dict[str, Any]) -> bool:
        """
        Validate if product data matches the query structure.
        
        Args:
            query_struct (Dict[str, Any]): Canonicalized query from QueryNormalizer
            product_data (Dict[str, Any]): Extracted product data from Extractor
            
        Returns:
            bool: True if product matches query, False otherwise
            
        Raises:
            NotImplementedError: If use_mock is False (real validation not implemented)
        """
        if self.use_mock:
            # Find matching validation case in config
            for validation_case in self.mock_validations:
                if (validation_case.get('query') == query_struct and 
                    validation_case.get('product') == product_data):
                    return validation_case.get('is_valid', False)
            
            # If no exact match found, try partial matching
            return self._partial_match(query_struct, product_data)
        else:
            # TODO: Real implementation would use LLM or rule-based validation
            raise NotImplementedError("Real validation not implemented yet")
    
    def _partial_match(self, query_struct: Dict[str, Any], product_data: Dict[str, Any]) -> bool:
        """
        Perform partial matching when exact match not found in config.
        
        Args:
            query_struct (Dict[str, Any]): Query structure
            product_data (Dict[str, Any]): Product data
            
        Returns:
            bool: True if partial match found, False otherwise
        """
        # Check if brand and model are present in product name
        brand = query_struct.get('brand', '').lower()
        model = query_struct.get('model', '').lower()
        product_name = product_data.get('productName', '').lower()
        
        # Basic validation: brand and model should be in product name
        if brand and brand not in product_name:
            return False
        
        if model and model not in product_name:
            return False
        
        # Check if storage matches (if specified)
        storage = query_struct.get('storage', '')
        if storage and storage.lower() not in product_name:
            return False
        
        # Check if price is reasonable (not zero or negative)
        try:
            price = float(product_data.get('price', '0'))
            if price <= 0:
                return False
        except (ValueError, TypeError):
            return False
        
        return True 