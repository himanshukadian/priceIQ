"""
Extractor Interface
Extracts product data (name, price, etc.) from HTML content.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import yaml


class ExtractorInterface(ABC):
    """Interface for data extractor."""
    
    @abstractmethod
    def extract_product_data(self, html: str, url: str) -> Optional[Dict[str, Any]]:
        """
        Extract product data from HTML content.
        
        Args:
            html: HTML content as string
            url: Source URL
            
        Returns:
            Dictionary with product data, or None if failed
        """
        pass


class MockExtractor(ExtractorInterface):
    """Mock implementation of extractor."""
    
    def __init__(self, mock_data_path: str):
        self.mock_data_path = mock_data_path
        
    def extract_product_data(self, html: str, url: str) -> Optional[Dict[str, Any]]:
        """Mock implementation that returns predefined extracted data."""
        import os
        
        try:
            # Extract site name from URL for mock file lookup
            site_name = url.split('/')[2].replace('.', '_')
            mock_file = os.path.join(self.mock_data_path, f"{site_name}_iphone.yaml")
            
            if os.path.exists(mock_file):
                with open(mock_file, 'r') as f:
                    return yaml.safe_load(f)
            else:
                # Return basic mock data
                return {
                    "product_name": "Mock Product",
                    "price": "999.00",
                    "currency": "USD",
                    "link": url,
                    "site": site_name,
                    "extraction_timestamp": "2024-01-15T10:30:00Z",
                    "confidence_score": 0.8
                }
                
        except Exception:
            return None


class RealExtractor(ExtractorInterface):
    """Real implementation of extractor."""
    
    def extract_product_data(self, html: str, url: str) -> Optional[Dict[str, Any]]:
        """
        Real implementation for data extraction.
        This would use BeautifulSoup, regex, ML models, etc.
        """
        # TODO: Implement real extraction logic
        # For now, return None
        return None 


class Extractor:
    """
    Extractor parses HTML content and extracts structured product information.
    In mock mode, returns predefined product data based on URL.
    """
    
    def __init__(self, config):
        """
        Initialize Extractor with config dict or YAML path.
        
        Args:
            config (dict or str): Config dict or path to YAML config file.
        """
        if isinstance(config, str):
            with open(config, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = config
            
        self.use_mock = self.config.get('modules', {}).get('extractor', {}).get('use_mock', True)
        self.mock_extracts = self.config.get('modules', {}).get('extractor', {}).get('mock_extracts', {})
    
    def extract(self, html: str, url: str) -> Dict[str, Any]:
        """
        Extract structured product data from HTML content.
        
        Args:
            html (str): Raw HTML content from the product page
            url (str): Source URL of the product page
            
        Returns:
            Dict[str, Any]: Structured product data including name, price, currency, link
            
        Raises:
            NotImplementedError: If use_mock is False (real extraction not implemented)
            KeyError: If URL not found in mock extracts
        """
        if self.use_mock:
            if url not in self.mock_extracts:
                # Return default structure if URL not found
                return {
                    "productName": "Unknown Product",
                    "price": "0",
                    "currency": "USD",
                    "link": url
                }
            
            return self.mock_extracts[url].copy()
        else:
            # TODO: Real implementation would use HTML parsing, LLM, etc.
            raise NotImplementedError("Real extraction not implemented yet") 