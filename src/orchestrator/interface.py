"""
Orchestrator module interface.
Coordinates the entire price intelligence pipeline, calling individual modules in sequence.
"""
import yaml
from typing import Dict, List, Any
from src.query_normalizer.interface import QueryNormalizer
from src.site_selector.interface import SiteSelector
from src.search_agent.interface import SearchAgent
from src.scraper.interface import Scraper
from src.extractor.interface import Extractor
from src.validator.interface import Validator
from src.deduplicator.interface import Deduplicator
from src.ranker.interface import Ranker


class Orchestrator:
    """
    Orchestrator coordinates the price intelligence pipeline.
    Loads configuration, calls individual modules, and returns final results.
    """
    
    def __init__(self, config):
        """
        Initialize Orchestrator with config dict or YAML path.
        
        Args:
            config (dict or str): Config dict or path to YAML config file.
        """
        if isinstance(config, str):
            with open(config, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = config
            
        # Initialize all modules based on config
        self.query_normalizer = QueryNormalizer(self.config)
        self.site_selector = SiteSelector(self.config)
        self.search_agent = SearchAgent(self.config)
        self.scraper = Scraper(self.config)
        self.extractor = Extractor(self.config)
        self.validator = Validator(self.config)
        self.deduplicator = Deduplicator(self.config)
        self.ranker = Ranker(self.config)
        
    def run(self, user_input: dict) -> List[Dict[str, Any]]:
        """
        Run the complete price intelligence pipeline.
        
        Args:
            user_input (dict): User input containing 'country' and 'query' keys.
            
        Returns:
            List[Dict[str, Any]]: List of ranked product results with price information.
        """
        # Extract input parameters
        country = user_input.get('country', 'US')
        query = user_input.get('query', '')
        
        print(f"🚀 Starting price intelligence pipeline for: {query} in {country}")
        
        # Step 1: Normalize the query
        print("📝 Step 1: Normalizing query...")
        normalized_data = self.query_normalizer.normalize(query)
        print(f"   Normalized: {normalized_data}")
        
        # Step 2: Select websites based on country and category
        print("🌐 Step 2: Selecting websites...")
        category = normalized_data.get('category', 'Smartphone')
        site_list = self.site_selector.select_sources(country, category)
        print(f"   Selected sites: {site_list}")
        
        # Step 3: Search each site
        print("🔍 Step 3: Searching sites...")
        search_results = self.search_agent.search(normalized_data, site_list)
        print(f"   Found {len(search_results)} search results")
        
        # Step 4: Fetch HTML for each search result
        print("📄 Step 4: Fetching HTML content...")
        html_contents = []
        for result in search_results:
            url = result['url']
            html_file = result.get('html_file', '')
            site = result.get('site', '')
            html_content = self.scraper.fetch_html({'url': url, 'html_file': html_file})
            html_contents.append({
                'url': url,
                'html': html_content,
                'site': site
            })
        print(f"   Fetched {len(html_contents)} HTML contents")
        
        # Step 5: Extract product data from HTML
        print("🔧 Step 5: Extracting product data...")
        extracted_products = []
        for html_item in html_contents:
            extracted_data = self.extractor.extract(html_item['html'], html_item['url'])
            if extracted_data:
                extracted_products.append(extracted_data)
        print(f"   Extracted {len(extracted_products)} products")
        
        # Step 6: Validate products against query
        print("✅ Step 6: Validating products...")
        valid_products = []
        for product in extracted_products:
            is_valid = self.validator.validate(normalized_data, product)
            if is_valid:
                valid_products.append(product)
        print(f"   Validated {len(valid_products)} products")
        
        # Step 7: Deduplicate products
        print("🔄 Step 7: Deduplicating products...")
        deduped_products = self.deduplicator.deduplicate(valid_products)
        print(f"   Deduplicated: {len(valid_products)} → {len(deduped_products)} products")
        
        # Step 8: Rank products by best value
        print("🏆 Step 8: Ranking products...")
        ranked_products = self.ranker.rank(deduped_products)
        print(f"   Ranked {len(ranked_products)} products")
        
        print(f"✅ Pipeline complete! Returning {len(ranked_products)} ranked products")
        return ranked_products
    
    def describe_flow(self) -> str:
        """
        Describe the pipeline flow for documentation and debugging.
        
        Returns:
            str: Description of the pipeline steps
        """
        flow_description = """
Price Intelligence Pipeline Flow:
================================

1. Query Normalization (QueryNormalizer)
   - Input: Raw user query (e.g., "iPhone 16 Pro, 128GB")
   - Output: Structured data (brand, model, storage, category)
   - Purpose: Standardize and structure user input

2. Site Selection (SiteSelector)
   - Input: Country code (e.g., "US")
   - Output: List of relevant e-commerce sites
   - Purpose: Determine which sites to search based on location

3. Search Execution (SearchAgent)
   - Input: Normalized query + site list
   - Output: Search results with URLs and HTML file paths
   - Purpose: Find product pages on each site

4. HTML Fetching (Scraper)
   - Input: URLs and HTML file paths
   - Output: HTML content for each product page
   - Purpose: Retrieve actual page content for extraction

5. Data Extraction (Extractor)
   - Input: HTML content + URL
   - Output: Structured product data (name, price, currency, link)
   - Purpose: Parse product information from HTML

6. Product Validation (Validator)
   - Input: Normalized query + extracted product data
   - Output: Boolean validation result
   - Purpose: Ensure extracted data matches the original query

7. Deduplication (Deduplicator)
   - Input: List of validated products
   - Output: Deduplicated product list
   - Purpose: Remove duplicate entries

8. Ranking (Ranker)
   - Input: Deduplicated product list
   - Output: Ranked product list (best value first)
   - Purpose: Sort products by best value criteria

Final Output: Ranked list of unique, validated products with pricing information.
        """
        return flow_description 