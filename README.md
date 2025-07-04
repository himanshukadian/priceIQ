# Price Intelligence Platform

A modular, mock-first Python monorepo for global price intelligence with microservice-like components. This platform provides end-to-end price comparison capabilities across multiple e-commerce sites and countries.

## 🏗️ Architecture

The platform follows a modular microservice architecture with clear separation of concerns:

```
priceIQ/
├── src/                    # Core modules
│   ├── query_normalizer/   # Normalizes user queries
│   ├── site_selector/      # Selects sites by country
│   ├── search_agent/       # Searches product pages
│   ├── scraper/           # Fetches HTML content
│   ├── extractor/         # Extracts product data
│   ├── validator/         # Validates product matches
│   ├── deduplicator/      # Removes duplicate products
│   ├── ranker/           # Ranks by best value
│   └── orchestrator/     # Coordinates the pipeline
├── tests/                 # Organized test suite
├── mocks/                 # Mock data and HTML files
├── config/               # Configuration files
└── main.py               # CLI entry point
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- No external dependencies (pure Python with standard library)

### Installation
```bash
git clone <repository-url>
cd priceIQ
```

### Basic Usage

#### Using the CLI directly:
```bash
# Query with direct arguments
python3 main.py --query "iPhone 16 Pro, 128GB" --country "US"

# Query with JSON file
python3 main.py --input_file sample_input.json
```

#### Using the convenience script:
```bash
# Make script executable (first time only)
chmod +x run.sh

# Run with query and country
./run.sh "iPhone 16 Pro, 128GB" "US"
./run.sh "Samsung Galaxy S24" "IN"
```

#### Using Make:
```bash
make test      # Run all tests
make run       # Run pipeline with default query
make all       # Run tests then pipeline
```

## 📋 Sample Output

```json
[
  {
    "productName": "Apple iPhone 16 Pro 128GB - Silver",
    "price": "979",
    "currency": "USD",
    "link": "https://bestbuy.com/iphone16pro"
  },
  {
    "productName": "Apple iPhone 16 Pro 128GB",
    "price": "999",
    "currency": "USD",
    "link": "https://amazon.com/iphone16pro"
  },
  {
    "productName": "Apple iPhone 16 Pro 128GB - Natural Titanium",
    "price": "999",
    "currency": "USD",
    "link": "https://apple.com/iphone16pro"
  }
]
```

## 🔧 Module Overview

### 1. Query Normalizer
- **Purpose**: Standardizes and structures user input
- **Input**: Raw query string (e.g., "iPhone 16 Pro, 128GB")
- **Output**: Structured data (brand, model, storage, category)
- **Mock Data**: `mocks/normalized_queries.yaml`

### 2. Site Selector
- **Purpose**: Determines relevant e-commerce sites by country
- **Input**: Country code (e.g., "US")
- **Output**: List of site domains
- **Mock Data**: `mocks/selected_sites.yaml`

### 3. Search Agent
- **Purpose**: Finds product pages on e-commerce sites
- **Input**: Normalized query + site list
- **Output**: Search results with URLs and HTML file paths
- **Mock Data**: `mocks/search_results.yaml`

### 4. Scraper
- **Purpose**: Fetches HTML content from product pages
- **Input**: URLs and HTML file paths
- **Output**: HTML content for extraction
- **Mock Data**: `mocks/html/` directory

### 5. Extractor
- **Purpose**: Parses product information from HTML
- **Input**: HTML content + URL
- **Output**: Structured product data (name, price, currency, link)
- **Mock Data**: `mocks/extracts/` directory

### 6. Validator
- **Purpose**: Ensures extracted data matches the original query
- **Input**: Normalized query + extracted product data
- **Output**: Boolean validation result
- **Mock Data**: `mocks/validated_data.yaml`

### 7. Deduplicator
- **Purpose**: Removes duplicate product entries
- **Input**: List of validated products
- **Output**: Deduplicated product list
- **Mock Data**: `mocks/deduplicated_data.yaml`

### 8. Ranker
- **Purpose**: Sorts products by best value criteria
- **Input**: Deduplicated product list
- **Output**: Ranked product list (best value first)
- **Mock Data**: `mocks/ranked_results.yaml`

### 9. Orchestrator
- **Purpose**: Coordinates the entire pipeline
- **Input**: User input (country, query)
- **Output**: Final ranked product results
- **Integration**: Calls all modules in sequence

## 🧪 Testing

### Test Structure
```
tests/
├── query_normalizer/
├── site_selector/
├── search_agent/
├── scraper/
├── extractor/
├── validator/
├── deduplicator/
├── ranker/
├── orchestrator/
└── run_all_tests.py
```

### Running Tests

#### Individual Module Tests:
```bash
python3 tests/query_normalizer/test_query_normalizer.py
python3 tests/orchestrator/test_orchestrator.py
```

#### All Tests:
```bash
python3 tests/run_all_tests.py
```

#### Using Make:
```bash
make test
```

### Test Coverage
- **Unit Tests**: Each module has comprehensive unit tests
- **Integration Tests**: End-to-end pipeline testing
- **Mock Validation**: Config integrity and mock data validation
- **Error Handling**: Edge cases and error scenarios
- **Multi-Country**: Tests for different country configurations

## ⚙️ Configuration

### Main Config File: `config/phase1_config.yaml`

```yaml
mode: mock
modules:
  query_normalizer:
    use_mock: true
    mock_output:
      brand: "Apple"
      model: "iPhone 16 Pro"
      storage: "128GB"
      category: "Smartphone"
  # ... other module configurations
```

### Key Configuration Options:
- **`use_mock`**: Toggle between mock and real implementations
- **`mock_data_path`**: Path to mock data files
- **`sites_by_country`**: E-commerce sites per country
- **`mock_results`**: Predefined mock outputs for testing

## 🌍 Supported Countries

| Country | Code | Sites | Currency |
|---------|------|-------|----------|
| United States | US | amazon.com, bestbuy.com, apple.com | USD |
| India | IN | flipkart.com, croma.com, reliancedigital.in | INR |
| United Kingdom | UK | amazon.co.uk, currys.co.uk, argos.co.uk | GBP |
| Germany | DE | amazon.de, mediamarkt.de, saturn.de | EUR |

## 🔄 Pipeline Flow

1. **Query Normalization** → Standardize user input
2. **Site Selection** → Choose relevant e-commerce sites
3. **Search Execution** → Find product pages
4. **HTML Fetching** → Retrieve page content
5. **Data Extraction** → Parse product information
6. **Product Validation** → Verify data accuracy
7. **Deduplication** → Remove duplicate entries
8. **Ranking** → Sort by best value

## 🚀 Development

### Adding New Modules
1. Create module directory in `src/`
2. Implement `interface.py` with main class
3. Add mock data configuration
4. Create test file in `tests/<module_name>/`
5. Update orchestrator to include new module

### Adding New Countries
1. Update `config/phase1_config.yaml` with country sites
2. Add mock HTML files in `mocks/html/`
3. Update mock data files as needed
4. Test with new country code

### Mock-First Development
- All modules start with mock implementations
- Real implementations raise `NotImplementedError`
- Mock data provides consistent test results
- Easy to extend with real implementations later

## 📁 Project Structure

```
priceIQ/
├── main.py                    # CLI entry point
├── run.sh                     # Convenience script
├── Makefile                   # Build automation
├── requirements.txt           # Dependencies
├── sample_input.json          # Sample input file
├── src/                       # Source code
│   ├── query_normalizer/
│   ├── site_selector/
│   ├── search_agent/
│   ├── scraper/
│   ├── extractor/
│   ├── validator/
│   ├── deduplicator/
│   ├── ranker/
│   └── orchestrator/
├── tests/                     # Test suite
│   ├── query_normalizer/
│   ├── site_selector/
│   ├── search_agent/
│   ├── scraper/
│   ├── extractor/
│   ├── validator/
│   ├── deduplicator/
│   ├── ranker/
│   ├── orchestrator/
│   └── run_all_tests.py
├── mocks/                     # Mock data
│   ├── html/                  # Mock HTML files
│   ├── normalized_queries.yaml
│   ├── selected_sites.yaml
│   ├── search_results.yaml
│   ├── extracts/
│   ├── validated_data.yaml
│   ├── deduplicated_data.yaml
│   └── ranked_results.yaml
└── config/                    # Configuration
    └── phase1_config.yaml
```

## 🔮 Future Enhancements

### Phase 1: Enhanced Mock Data
- More comprehensive mock scenarios
- Additional countries and sites
- Edge case testing data

### Phase 2: Real Implementations
- Web scraping with Playwright/Selenium
- API integrations for e-commerce sites
- LLM-based query normalization
- Machine learning for ranking

### Phase 3: Advanced Features
- Real-time price monitoring
- Price history tracking
- User preference learning
- Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🆘 Support

For questions or issues:
1. Check the test suite for usage examples
2. Review the configuration files
3. Run `make test` to verify setup
4. Create an issue with detailed description

---

**Built with ❤️ for global price intelligence** 