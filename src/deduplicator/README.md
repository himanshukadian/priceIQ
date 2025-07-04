# Deduplicator Module

## 🧩 Purpose
Removes duplicate product entries from the validated product list. Identifies and eliminates redundant listings that represent the same product across different sources or with slight variations in naming.

## 🔁 Input & Output

- **Input**: 
  - `products` (List[Dict[str, Any]]): List of validated product entries from Validator

- **Output**: 
  - `List[Dict[str, Any]]`: Deduplicated list of unique products

## ⚙️ Mock Behavior

- Controlled via `phase1_config.yaml` under `deduplicator.use_mock`
- Returns predefined deduplicated results from `mock_deduplicated_results` configuration
- Performs exact list matching against configured input patterns
- Falls back to basic deduplication logic if exact match not found
- Mock data stored in `mocks/deduplicated_data.yaml`

## 🛣️ Future Upgrade Path

- Replace mock logic with:
  - Semantic embeddings for similarity matching
  - Machine learning models for duplicate detection
  - Fuzzy string matching algorithms
  - Product fingerprinting techniques
  - Multi-factor similarity scoring
  - Brand and model normalization
  - Price clustering for variant detection
- Keep interface unchanged for pluggability

## 🧪 Example Usage
```python
from src.deduplicator.interface import Deduplicator

# Initialize with config
deduplicator = Deduplicator(config)

# Deduplicate products
products = [
    {"productName": "Apple iPhone 16 Pro 128GB", "price": "999"},
    {"productName": "Apple iPhone 16 Pro 128GB - Silver", "price": "999"},
    {"productName": "Samsung Galaxy S24", "price": "899"}
]
unique_products = deduplicator.deduplicate(products)
# Returns: [
#     {"productName": "Apple iPhone 16 Pro 128GB", "price": "999"},
#     {"productName": "Samsung Galaxy S24", "price": "899"}
# ]
```

## Interface

### Class: `Deduplicator`

#### Constructor
```python
__init__(self, config)
```
- **Parameters**: `config` (dict or str) - Configuration dictionary or path to YAML config file
- **Purpose**: Initializes the deduplicator with configuration settings

#### Main Method
```python
deduplicate(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]
```
- **Parameters**: 
  - `products` (List[Dict[str, Any]]) - List of validated product entries
- **Returns**: List[Dict[str, Any]] - Deduplicated list of products
- **Raises**: 
  - `NotImplementedError`: If real deduplication is attempted

## Configuration

The module uses the following configuration structure in `phase1_config.yaml`:

```yaml
deduplicator:
  use_mock: true
  mock_deduplicated_results:
    input_products:
      - productName: "Apple iPhone 16 Pro 128GB"
        price: "999"
        currency: "USD"
        link: "https://amazon.com/iphone16pro"
      - productName: "Apple iPhone 16 Pro 128GB - Silver"
        price: "999"
        currency: "USD"
        link: "https://bestbuy.com/iphone16pro"
    output_products:
      - productName: "Apple iPhone 16 Pro 128GB"
        price: "999"
        currency: "USD"
        link: "https://amazon.com/iphone16pro"
```

## Deduplication Strategy

The module uses a two-tier approach:

### 1. Mock Configuration Matching
- First tries to find exact input match in configuration
- Returns predefined output if match found
- Ensures consistent test results

### 2. Basic Deduplication (Fallback)
- Creates unique keys based on product name, price, and currency
- Removes entries with identical keys
- Preserves order of first occurrence

## Integration

This module integrates with:
- **Validator**: Receives validated product entries
- **Ranker**: Provides deduplicated products for ranking
- **Orchestrator**: Coordinates the deduplication process

## Future: Semantic Embeddings and Normalized Comparison

The mock implementation will be replaced with intelligent deduplication:

### Phase 1: Enhanced Rule-Based Deduplication
- **Fuzzy Matching**: Handle slight variations in product names
- **Normalized Comparison**: Standardize product names before comparison
- **Price Tolerance**: Allow small price variations within same product
- **Vendor Consolidation**: Group products from same vendor

### Phase 2: Semantic Embeddings
- **Text Embeddings**: Use embeddings to find semantically similar products
- **Similarity Thresholds**: Configurable similarity scores for deduplication
- **Multi-language Support**: Handle products in different languages
- **Context Awareness**: Consider product context and attributes

### Phase 3: Machine Learning Approach
- **Classification Models**: Train models to identify duplicate products
- **Feature Engineering**: Extract meaningful features for comparison
- **Active Learning**: Improve models based on user feedback
- **Confidence Scoring**: Provide confidence levels for deduplication decisions

### Phase 4: Advanced Features
- **Real-time Deduplication**: Handle streaming product data
- **Incremental Updates**: Efficiently update deduplication results
- **Custom Rules**: Allow business-specific deduplication rules
- **Performance Optimization**: Fast deduplication for large datasets

## Deduplication Criteria

The module considers:

### Exact Matches (from config)
- Complete product data match
- Predefined deduplication results

### Basic Deduplication (fallback)
- **Product Name**: Primary identifier for deduplication
- **Price**: Same price indicates same product variant
- **Currency**: Same currency for fair comparison
- **Vendor**: Different vendors may have same product

## Error Handling

The module handles various scenarios:
- Empty input lists
- Malformed product data
- Configuration errors
- Real mode attempts (raises NotImplementedError)

## Testing

Use the test file to validate:
- Mock deduplication cases from configuration
- Basic deduplication logic
- Input/output validation
- Error handling scenarios
- Configuration loading
- Integration with other modules 