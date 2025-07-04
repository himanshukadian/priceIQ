"""
Scraper Interface
Fetches HTML content from product pages for price extraction.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import yaml


class ScraperInterface(ABC):
    """Interface for web scraper."""
    
    @abstractmethod
    def scrape_page(self, url: str) -> Optional[str]:
        """
        Scrape HTML content from a product page.
        
        Args:
            url: Product page URL
            
        Returns:
            HTML content as string, or None if failed
        """
        pass


class MockScraper(ScraperInterface):
    """Mock implementation of scraper."""
    
    def __init__(self, mock_data_path: str):
        self.mock_data_path = mock_data_path
        
    def scrape_page(self, url: str) -> Optional[str]:
        """Mock implementation that returns predefined HTML content."""
        import os
        
        try:
            # Extract site name from URL for mock file lookup
            site_name = url.split('/')[2].replace('.', '_')
            mock_file = os.path.join(self.mock_data_path, f"{site_name}_iphone.html")
            
            if os.path.exists(mock_file):
                with open(mock_file, 'r') as f:
                    return f.read()
            else:
                # Return a basic HTML template
                return f"""
                <!DOCTYPE html>
                <html>
                <head><title>Mock Product Page</title></head>
                <body>
                    <h1>Mock Product</h1>
                    <div class="price">$999.00</div>
                </body>
                </html>
                """
                
        except Exception:
            return None


class RealScraper(ScraperInterface):
    """Real implementation of scraper."""
    
    def scrape_page(self, url: str) -> Optional[str]:
        """
        Real implementation for web scraping.
        This would use requests, selenium, etc.
        """
        # TODO: Implement real scraping logic
        # For now, return None
        return None 


class Scraper:
    """
    Scraper fetches HTML content from product pages.
    In mock mode, reads predefined HTML files from the filesystem.
    """
    
    def __init__(self, config):
        """
        Initialize Scraper with config dict or YAML path.
        
        Args:
            config (dict or str): Config dict or path to YAML config file.
        """
        if isinstance(config, str):
            with open(config, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = config
            
        self.use_mock = self.config.get('modules', {}).get('scraper', {}).get('use_mock', True)
    
    def fetch_html(self, url_entry: Dict[str, Any]) -> str:
        """
        Fetch HTML content for a product URL.
        
        Args:
            url_entry (Dict[str, Any]): Dictionary containing:
                - url: Product URL
                - html_file: Path to mock HTML file
                
        Returns:
            str: HTML content as string
            
        Raises:
            NotImplementedError: If use_mock is False (real scraping not implemented)
            FileNotFoundError: If mock HTML file doesn't exist
        """
        if self.use_mock:
            html_file = url_entry.get('html_file', '')
            if not html_file:
                raise ValueError("html_file path is required in mock mode")
            
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"Mock HTML file not found: {html_file}")
        else:
            # TODO: Real implementation would use Playwright/Selenium
            raise NotImplementedError("Real scraping not implemented yet") 