"""
Site Selector Interface
Selects relevant e-commerce sites based on country and product category.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import yaml


class SiteSelectorInterface(ABC):
    """Interface for site selection."""
    
    @abstractmethod
    def select_sites(self, country: str, category: str = "default") -> List[str]:
        """
        Select relevant e-commerce sites for a given country and category.
        
        Args:
            country: Country code (e.g., "US", "UK", "DE")
            category: Product category (e.g., "smartphone", "laptop")
            
        Returns:
            List of site URLs to search
        """
        pass


class MockSiteSelector(SiteSelectorInterface):
    """Mock implementation of site selector."""
    
    def __init__(self, mock_data_path: str):
        self.mock_data_path = mock_data_path
        
    def select_sites(self, country: str, category: str = "default") -> List[str]:
        """Mock implementation that returns predefined site lists."""
        try:
            with open(self.mock_data_path, 'r') as f:
                mock_data = yaml.safe_load(f)
                
            sites_data = mock_data.get('sites', {})
            country_sites = sites_data.get(country, {})
            
            # Try category-specific sites first, fall back to default
            if category in country_sites:
                return country_sites[category]
            elif 'default' in country_sites:
                return country_sites['default']
            else:
                return []
                
        except Exception:
            return []


class RealSiteSelector(SiteSelectorInterface):
    """Real implementation of site selector."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def select_sites(self, country: str, category: str = "default") -> List[str]:
        """
        Real implementation for site selection.
        This would use a database of e-commerce sites, rankings, etc.
        """
        # TODO: Implement real site selection logic
        # For now, return sites from config
        country_config = self.config.get('countries', {}).get(country, {})
        return country_config.get('sites', []) 


class SiteSelector:
    """
    SiteSelector determines which e-commerce sites to search for products.
    In mock mode, returns predefined site lists from configuration.
    """
    
    def __init__(self, config):
        """
        Initialize SiteSelector with config dict or YAML path.
        
        Args:
            config (dict or str): Config dict or path to YAML config file.
        """
        if isinstance(config, str):
            with open(config, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = config
            
        self.use_mock = self.config.get('modules', {}).get('site_selector', {}).get('use_mock', True)
        self.sites_by_country = self.config.get('modules', {}).get('site_selector', {}).get('sites_by_country', {})
        # Add comprehensive India support
        if 'IN' not in self.sites_by_country:
            self.sites_by_country['IN'] = [
                'amazon.in',
                'flipkart.com', 
                'croma.com',
                'reliancedigital.in',
                'paytmmall.com',
                'snapdeal.com',
                'shopclues.com',
                'indiamart.com'
            ]
    
    def select_sources(self, country: str) -> List[str]:
        """
        Select e-commerce sites to search for the given country.
        
        Args:
            country (str): Country code (e.g., 'US', 'IN', 'UK')
            
        Returns:
            List[str]: List of e-commerce site URLs to search
        """
        if self.use_mock:
            # Return mock sites from config
            return self.sites_by_country.get(country, [])
        else:
            # TODO: Real implementation would use database or API
            # For now, return empty list
            return [] 