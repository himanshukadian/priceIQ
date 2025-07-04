"""
Search Agent Interface
Finds product URLs on e-commerce sites based on search queries.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import yaml


class SearchAgentInterface(ABC):
    """Interface for search agent."""
    
    @abstractmethod
    def search_products(self, site: str, query: str) -> List[str]:
        """
        Search for products on a given site.
        
        Args:
            site: E-commerce site URL
            query: Normalized product query
            
        Returns:
            List of product URLs found
        """
        pass


class MockSearchAgent(SearchAgentInterface):
    """Mock implementation of search agent."""
    
    def __init__(self, mock_data_path: str):
        self.mock_data_path = mock_data_path
        
    def search_products(self, site: str, query: str) -> List[str]:
        """Mock implementation that returns predefined search results."""
        try:
            with open(self.mock_data_path, 'r') as f:
                mock_data = yaml.safe_load(f)
                
            search_data = mock_data.get('search_results', {})
            site_results = search_data.get(site, {})
            
            return site_results.get(query, [])
                
        except Exception:
            return []


class RealSearchAgent(SearchAgentInterface):
    """Real implementation of search agent."""
    
    def search_products(self, site: str, query: str) -> List[str]:
        """
        Real implementation for product search.
        This would use web scraping, APIs, etc.
        """
        # TODO: Implement real search logic
        # For now, return empty list
        return [] 


class SearchAgent:
    """
    SearchAgent finds products on e-commerce sites based on normalized queries.
    In mock mode, returns predefined search results from configuration.
    """
    
    def __init__(self, config):
        """
        Initialize SearchAgent with config dict or YAML path.
        
        Args:
            config (dict or str): Config dict or path to YAML config file.
        """
        if isinstance(config, str):
            with open(config, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = config
            
        self.use_mock = self.config.get('modules', {}).get('search_agent', {}).get('use_mock', True)
        self.mock_results = self.config.get('modules', {}).get('search_agent', {}).get('mock_results', {})
    
    def search(self, query: Dict[str, Any], sites: List[str]) -> List[Dict[str, Any]]:
        """
        Search for products on the given sites using the normalized query.
        
        Args:
            query (Dict[str, Any]): Normalized query from QueryNormalizer
            sites (List[str]): List of e-commerce site domains to search
            
        Returns:
            List[Dict[str, Any]]: List of search results with site, URL, and HTML file
        """
        if self.use_mock:
            results = []
            for site in sites:
                if site in self.mock_results:
                    for result in self.mock_results[site]:
                        results.append({
                            "site": site,
                            "url": result.get("url", ""),
                            "html_file": result.get("html_file", "")
                        })
            return results
        else:
            # TODO: Real implementation would use LLM or site search APIs
            # For now, return empty list
            return [] 