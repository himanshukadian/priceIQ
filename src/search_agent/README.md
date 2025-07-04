# Search Agent Module

## 🧩 Purpose
Finds product pages on e-commerce sites based on normalized queries. Simulates the process of searching for products across multiple platforms and returning relevant URLs with associated HTML file paths for scraping. **Not all sites return results for all categories or products.**

## 🔁 Input & Output

- **Input**: 
  - `query` (Dict[str, Any]): Normalized query from QueryNormalizer (must include `category`)
  - `sites` (List[str]): List of e-commerce site domains to search

- **Output**: 
  - `List[Dict[str, Any]]`: List of search results containing:
    - `site` (str): Source e-commerce site
    - `url` (str): Product page URL
    - `html_file` (str): Path to mock HTML file for scraping

## ⚙️ Mock Behavior

- Controlled via `phase1_config.yaml` under `search_agent.use_mock`
- Returns predefined search results from `mock_results` configuration
- **Category-specific search results**: Only returns results for supported (site, category) combinations
- Mock data stored in `mocks/search_results.yaml`

## 🛣️ Future Upgrade Path

- Replace mock logic with:
  - Real web scraping using Playwright/Selenium
  - E-commerce site API integrations
  - LLM-based search query optimization
  - Dynamic URL generation and validation
  - Search result ranking and filtering
  - Rate limiting and anti-bot detection handling
- Keep interface unchanged for pluggability

## 🧪 Example Usage
```python
from src.search_agent.interface import SearchAgent

# Initialize with config
agent = SearchAgent(config)

# Search for products in a category
query = {"brand": "Nike", "model": "Air Max", "category": "Sports"}
sites = ["amazon.com", "nike.com"]
results = agent.search(query, sites)
# Returns: [
#     {"site": "amazon.com", "url": "https://amazon.com/nikeairmax", "html_file": "mocks/html/amazon_nikeairmax.html"},
#     {"site": "nike.com", "url": "https://nike.com/airmax270", "html_file": "mocks/html/nike_airmax270.html"}
# ]
```

## Interface

### Class: `SearchAgent`

#### Constructor
```python
__init__(self, config)
```
- **Parameters**: `config` (dict or str) - Configuration dictionary or path to YAML config file
- **Purpose**: Initializes the search agent with configuration settings

#### Main Method
```python
search(self, query: Dict[str, Any], sites: List[str]) -> List[Dict[str, Any]]
```
- **Parameters**: 
  - `query` (Dict[str, Any]) - Normalized query structure from QueryNormalizer (must include `category`)
  - `sites` (List[str]) - List of e-commerce site domains to search
- **Returns**: List[Dict[str, Any]] - List of search results with site, URL, and HTML file
- **Purpose**: Searches for products on specified sites and returns results

## Input Structure

### Query Structure
The query parameter should be a dictionary from the QueryNormalizer and include a `category` key:
```python
{
    "brand": "Apple",
    "model": "MacBook Pro", 
    "storage": "512GB",
    "category": "Laptop"
}
```

### Sites List
A list of e-commerce site domains:
```python
["amazon.com", "bestbuy.com", "apple.com"]
```

## Mock Result Structure

Each result in the returned list contains:
```python
{
    "site": "amazon.com",                    # The e-commerce site domain
    "url": "https://amazon.com/macbookpro", # Product page URL
    "html_file": "mocks/html/amazon_macbookpro.html"  # Mock HTML file path
}
```

## Configuration Format

The module uses the following configuration structure in `phase1_config.yaml`:

```yaml
search_agent:
  use_mock: true
  mock_results:
    amazon.com:
      Smartphone:
        - url: https://amazon.com/iphone16pro
          html_file: mocks/html/amazon_iphone16pro.html
      Laptop:
        - url: https://amazon.com/macbookpro
          html_file: mocks/html/amazon_macbookpro.html
      Sports:
        - url: https://amazon.com/nikeairmax
          html_file: mocks/html/amazon_nikeairmax.html
    nike.com:
      Sports:
        - url: https://nike.com/airmax270
          html_file: mocks/html/nike_airmax270.html
    # ... other sites and categories
```

## Integration

This module integrates with:
- **QueryNormalizer**: Receives normalized query structure
- **SiteSelector**: Receives list of target sites
- **Scraper**: Provides HTML file paths for content extraction

## Future Upgrade Path

The mock implementation will be replaced with real search capabilities:

1. **LLM-based Search**: Use large language models to generate search queries and interpret results
2. **Site Search APIs**: Integrate with e-commerce site APIs where available
3. **Web Scraping**: Implement intelligent search result parsing
4. **Search Result Ranking**: Prioritize results based on relevance and confidence

## Mock HTML Files

The module references mock HTML files that will be used by the Scraper module for content extraction. These files should contain realistic product page HTML structure for testing the extraction pipeline. 