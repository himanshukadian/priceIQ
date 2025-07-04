# Extractor Module

## 🧩 Purpose
Parses HTML content and extracts structured product information including product names, prices, currencies, and links. Converts raw webpage content into machine-readable product data for downstream processing.

## 🔁 Input & Output

- **Input**: 
  - `html` (str): Raw HTML content from product page
  - `url` (str): Source URL of the product page

- **Output**: 
  - `Dict[str, Any]`: Structured product data containing:
    - `productName` (str): Extracted product name
    - `price` (str): Product price as string
    - `currency` (str): Currency code (e.g., "USD", "INR")
    - `link` (str): Product page URL

## ⚙️ Mock Behavior

- Controlled via `phase1_config.yaml` under `extractor.use_mock`
- Returns predefined product data from `mock_extracts` configuration
- Maps URLs to specific mock extraction results
- Provides fallback default structure if URL not found in config
- Mock data stored in `mocks/extracts/` directory

## 🛣️ Future Upgrade Path

- Replace mock logic with:
  - HTML parsing using BeautifulSoup or lxml
  - CSS selector and XPath-based extraction
  - Machine learning models for data extraction
  - LLM-based content understanding
  - Site-specific extraction rules and templates
  - Price normalization and currency conversion
  - Confidence scoring for extracted data
- Keep interface unchanged for pluggability

## 🧪 Example Usage
```python
from src.extractor.interface import Extractor

# Initialize with config
extractor = Extractor(config)

# Extract product data from HTML
html_content = "<html>...</html>"
url = "https://amazon.com/iphone16pro"
product_data = extractor.extract(html_content, url)
# Returns: {
#     "productName": "Apple iPhone 16 Pro 128GB",
#     "price": "999",
#     "currency": "USD", 
#     "link": "https://amazon.com/iphone16pro"
# }
```

## Interface

### Class: `Extractor`

#### Constructor
```python
__init__(self, config)
```
- **Parameters**: `config` (dict or str) - Configuration dictionary or path to YAML config file
- **Purpose**: Initializes the extractor with configuration settings

#### Main Method
```python
extract(self, html: str, url: str) -> Dict[str, Any]
```
- **Parameters**: 
  - `html` (str) - Raw HTML content from the product page
  - `url` (str) - Source URL of the product page
- **Returns**: Dict[str, Any] - Structured product data
- **Raises**: 
  - `NotImplementedError`: If real extraction is attempted
  - Returns default structure for unknown URLs in mock mode

## Configuration

The module uses the following configuration structure in `phase1_config.yaml`:

```yaml
extractor:
  use_mock: true
  mock_extracts:
    https://amazon.com/iphone16pro:
      productName: "Apple iPhone 16 Pro 128GB"
      price: "999"
      currency: "USD"
      link: "https://amazon.com/iphone16pro"
    https://bestbuy.com/iphone16pro:
      productName: "Apple iPhone 16 Pro 128GB - Silver"
      price: "979"
      currency: "USD"
      link: "https://bestbuy.com/iphone16pro"
```

## Integration

This module integrates with:
- **Scraper**: Receives HTML content and source URL
- **Validator**: Provides structured data for validation
- **Orchestrator**: Coordinates the extraction process

## Future: HTML Parser/LLM Hybrid

The mock implementation will be replaced with intelligent extraction capabilities:

### Phase 1: Basic HTML Parsing
- **BeautifulSoup**: Parse HTML structure
- **CSS Selectors**: Target specific elements
- **Regex Patterns**: Extract price and text data
- **Site-specific rules**: Handle different e-commerce layouts

### Phase 2: LLM Integration
- **Large Language Models**: Understand context and extract meaning
- **Prompt Engineering**: Structured prompts for consistent extraction
- **Fallback Logic**: Use LLM when parsing fails
- **Confidence Scoring**: Rate extraction quality

### Phase 3: Hybrid Approach
- **Rule-based + LLM**: Combine parsing speed with LLM accuracy
- **Learning System**: Improve extraction based on feedback
- **Multi-modal**: Handle images, text, and structured data
- **Adaptive Parsing**: Learn site-specific patterns

### Phase 4: Production Features
- **Real-time Updates**: Handle dynamic content changes
- **Error Recovery**: Graceful handling of parsing failures
- **Performance Optimization**: Fast extraction for high-volume processing
- **Quality Assurance**: Validation and verification of extracted data

## Error Handling

The module handles various scenarios:
- Unknown URLs (returns default structure)
- Missing HTML content
- Malformed configuration
- Real mode attempts (raises NotImplementedError)

## Testing

Use the test file to validate:
- Mock extraction for known URLs
- Default behavior for unknown URLs
- Configuration loading
- Error handling scenarios 