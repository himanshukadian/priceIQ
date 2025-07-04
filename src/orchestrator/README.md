# Orchestrator Module

## 🧩 Purpose
Coordinates the entire price intelligence pipeline by orchestrating all individual modules in sequence. Acts as the central controller that manages the flow from raw user input to final ranked product results.

## 🔁 Input & Output

- **Input**: 
  - `user_input` (Dict[str, Any]): User input containing:
    - `country` (str): Country code (e.g., "US", "IN", "UK")
    - `query` (str): Raw product query string

- **Output**: 
  - `List[Dict[str, Any]]`: Final ranked list of products with pricing information

## 📦 Module Dependencies

The Orchestrator depends on all other modules in the pipeline:

1. **QueryNormalizer** - Normalizes user queries
2. **SiteSelector** - Selects relevant e-commerce sites
3. **SearchAgent** - Finds product pages on sites
4. **Scraper** - Fetches HTML content from pages
5. **Extractor** - Extracts product data from HTML
6. **Validator** - Validates product matches
7. **Deduplicator** - Removes duplicate products
8. **Ranker** - Ranks products by best value

## 🔄 run(user_input) Flow

The `run()` method executes the complete pipeline in 8 sequential steps:

1. **Query Normalization** → Converts raw query to structured data
2. **Site Selection** → Determines which e-commerce sites to search
3. **Search Execution** → Finds product URLs on each site
4. **HTML Fetching** → Retrieves page content for each URL
5. **Data Extraction** → Parses product information from HTML
6. **Product Validation** → Filters products that match the query
7. **Deduplication** → Removes duplicate entries
8. **Ranking** → Sorts products by best value criteria

Each step provides progress logging and error handling for debugging.

## 📋 describe_flow() Method

The `describe_flow()` method returns a comprehensive description of the pipeline:

- **Purpose**: Documentation and debugging aid
- **Output**: Detailed text description of each pipeline step
- **Usage**: Helps developers understand the data flow and module interactions
- **Content**: Includes input/output specifications and purpose for each step

## ⚙️ Mock Behavior

- Controlled via `phase1_config.yaml` under individual module configurations
- Each module operates in mock mode by default
- Orchestrator coordinates mock data flow between modules
- Provides consistent end-to-end testing without external dependencies

## 🛣️ Future Upgrade Path

- Replace mock logic with:
  - Real implementations of all dependent modules
  - Parallel processing for improved performance
  - Pipeline optimization and caching
  - Real-time monitoring and metrics
  - Error recovery and retry mechanisms
  - A/B testing for different ranking algorithms
  - Multi-region deployment support
- Keep interface unchanged for pluggability

## 🧪 Example Usage
```python
from src.orchestrator.interface import Orchestrator

# Initialize with config
orchestrator = Orchestrator(config)

# Run complete pipeline
user_input = {
    "country": "US",
    "query": "iPhone 16 Pro, 128GB"
}
results = orchestrator.run(user_input)
# Returns: [
#     {"productName": "Apple iPhone 16 Pro 128GB", "price": "979", "currency": "USD"},
#     {"productName": "Apple iPhone 16 Pro 128GB", "price": "999", "currency": "USD"}
# ]

# Get pipeline description
flow_description = orchestrator.describe_flow()
print(flow_description)
``` 