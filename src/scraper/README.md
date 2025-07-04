# Scraper Module

## 🧩 Purpose
Fetches HTML content from product pages for downstream data extraction. Handles the retrieval of raw webpage content that will be parsed to extract product information like prices, names, and availability.

## 🔁 Input & Output

- **Input**: 
  - `url_entry` (Dict[str, Any]): Dictionary containing:
    - `url` (str): Product page URL
    - `html_file` (str): Path to mock HTML file (required in mock mode)

- **Output**: 
  - `str`: Raw HTML content as string for processing by the Extractor module

## ⚙️ Mock Behavior

- Controlled via `phase1_config.yaml` under `scraper.use_mock`
- Reads predefined HTML files from the filesystem
- Maps URLs to specific mock HTML files in `mocks/html/` directory
- **Not all sites/products/categories will have mock HTML files. This is expected in a modular, category-aware system.**
- Raises `FileNotFoundError` if mock HTML file doesn't exist
- Raises `NotImplementedError` if real scraping is attempted

## 🛣️ Future Upgrade Path

- Replace mock logic with:
  - Real web scraping using Playwright/Selenium
  - HTTP client with proper headers and session management
  - Anti-bot detection bypass techniques
  - Proxy rotation and IP management
  - Rate limiting and respectful crawling
  - JavaScript rendering for dynamic content
  - Error handling and retry mechanisms
- Keep interface unchanged for pluggability

## 🧪 Example Usage
```python
from src.scraper.interface import Scraper

# Initialize with config
scraper = Scraper(config)

# Fetch HTML content
url_entry = {
    "url": "https://amazon.com/iphone16pro",
    "html_file": "mocks/html/amazon_iphone16pro.html"
}
html_content = scraper.fetch_html(url_entry)
# Returns: "<!DOCTYPE html><html>...</html>"
```

## Interface

### Class: `Scraper`

#### Constructor
```python
__init__(self, config)
```
- **Parameters**: `config` (dict or str) - Configuration dictionary or path to YAML config file
- **Purpose**: Initializes the scraper with configuration settings

#### Main Method
```python
fetch_html(self, url_entry: Dict[str, Any]) -> str
```
- **Parameters**: 
  - `url_entry` (Dict[str, Any]) - Dictionary containing:
    - `url`: Product URL (for reference)
    - `html_file`: Path to mock HTML file
- **Returns**: str - HTML content as string
- **Raises**: 
  - `NotImplementedError`: If real scraping is attempted
  - `FileNotFoundError`: If mock HTML file doesn't exist
  - `ValueError`: If html_file path is missing in mock mode

## Configuration

The module uses the following configuration in `phase1_config.yaml`:

```yaml
scraper:
  use_mock: true
  mock_data_path: "mocks/html/"
```

## Mock HTML Files

The module expects mock HTML files in the `mocks/html/` directory. These files should contain realistic product page HTML structure to test the extraction pipeline effectively. **If a file is missing, it means the site/product/category is not supported in the current mock scenario.**

### Sample Mock Files
- `amazon_iphone16pro.html` - Amazon product page structure
- `bestbuy_iphone16pro.html` - Best Buy product page structure

### HTML Structure Guidelines
Mock HTML files should include:
- Product title/name
- Price information
- Product specifications
- Availability status
- Realistic CSS classes and structure

## Integration

This module integrates with:
- **SearchAgent**: Receives URL entries with HTML file paths
- **Extractor**: Provides HTML content for data extraction
- **Orchestrator**: Coordinates the scraping process

## Error Handling

The module handles various error scenarios:
- Missing HTML files in mock mode (expected for unsupported site/category/product)
- Network errors in real mode (future)
- Invalid URL entries
- Configuration issues

## Testing

Use the test file to validate:
- Mock HTML file reading
- Error handling for missing files
- Configuration loading
- Integration with other modules 