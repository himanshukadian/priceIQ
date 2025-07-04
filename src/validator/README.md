# Validator Module

## 🧩 Purpose
Ensures that extracted product data matches the original user query. Validates product accuracy by comparing extracted information against the canonicalized query structure to filter out irrelevant or incorrect results.

## 🔁 Input & Output

- **Input**: 
  - `query_struct` (Dict[str, Any]): Canonicalized query from QueryNormalizer
  - `product_data` (Dict[str, Any]): Extracted product data from Extractor

- **Output**: 
  - `bool`: True if product matches query, False otherwise

## ⚙️ Mock Behavior

- Controlled via `phase1_config.yaml` under `validator.use_mock`
- Returns predefined validation results from `mock_validations` configuration
- Performs exact matching against configured validation cases
- Falls back to partial matching logic if exact match not found
- Mock data stored in `mocks/validated_data.yaml`

## 🛣️ Future Upgrade Path

- Replace mock logic with:
  - LLM-based semantic matching and validation
  - Machine learning models for product similarity
  - Fuzzy string matching algorithms
  - Brand and model recognition systems
  - Price range validation and outlier detection
  - Multi-language product name matching
  - Confidence scoring for validation results
- Keep interface unchanged for pluggability

## 🧪 Example Usage
```python
from src.validator.interface import Validator

# Initialize with config
validator = Validator(config)

# Validate product against query
query_struct = {
    "brand": "Apple",
    "model": "iPhone 16 Pro", 
    "storage": "128GB"
}
product_data = {
    "productName": "Apple iPhone 16 Pro 128GB - Silver",
    "price": "999",
    "currency": "USD"
}
is_valid = validator.validate(query_struct, product_data)
# Returns: True
```

## Interface

### Class: `Validator`

#### Constructor
```python
__init__(self, config)
```
- **Parameters**: `config` (dict or str) - Configuration dictionary or path to YAML config file
- **Purpose**: Initializes the validator with configuration settings

#### Main Method
```python
validate(self, query_struct: Dict[str, Any], product_data: Dict[str, Any]) -> bool
```
- **Parameters**: 
  - `query_struct` (Dict[str, Any]) - Canonicalized query from QueryNormalizer
  - `product_data` (Dict[str, Any]) - Extracted product data from Extractor
- **Returns**: bool - True if product matches query, False otherwise
- **Raises**: 
  - `NotImplementedError`: If real validation is attempted

## Configuration

The module uses the following configuration structure in `phase1_config.yaml`:

```yaml
validator:
  use_mock: true
  mock_validations:
    - query:
        brand: "Apple"
        model: "iPhone 16 Pro"
        storage: "128GB"
        category: "Smartphone"
      product:
        productName: "Apple iPhone 16 Pro 128GB"
        price: "999"
        currency: "USD"
        link: "https://amazon.com/iphone16pro"
      is_valid: true
    - query:
        brand: "Apple"
        model: "iPhone 16 Pro"
        storage: "128GB"
        category: "Smartphone"
      product:
        productName: "Apple iPhone 16 Mini"
        price: "899"
        currency: "USD"
        link: "https://example.com/iphone16mini"
      is_valid: false
```

## Mocking Strategy

The validator uses a two-tier approach:

1. **Exact Match**: First tries to find an exact match between query and product in the configuration
2. **Partial Match**: If no exact match is found, performs basic validation:
   - Brand and model must be present in product name
   - Storage capacity must match (if specified)
   - Price must be reasonable (positive value)

## Integration

This module integrates with:
- **QueryNormalizer**: Receives canonicalized query structure
- **Extractor**: Receives extracted product data
- **Deduplicator**: Provides validated products for deduplication
- **Orchestrator**: Coordinates the validation process

## Future: LLM Integration

The mock implementation will be replaced with intelligent validation capabilities:

### Phase 1: Rule-Based Validation
- **Fuzzy Matching**: Handle slight variations in product names
- **Synonym Recognition**: Understand equivalent terms
- **Category Validation**: Ensure product category matches
- **Price Range Validation**: Check if price is within expected range

### Phase 2: LLM-Powered Validation
- **Semantic Understanding**: Use LLMs to understand product similarity
- **Context Awareness**: Consider market context and product relationships
- **Confidence Scoring**: Provide confidence levels for matches
- **Learning System**: Improve validation based on user feedback

### Phase 3: Advanced Features
- **Multi-Modal Validation**: Handle images and text together
- **Market Intelligence**: Consider current market trends and availability
- **User Preference Learning**: Adapt to user's validation preferences
- **Real-time Updates**: Handle dynamic product information

### Phase 4: Production Features
- **Performance Optimization**: Fast validation for high-volume processing
- **Quality Metrics**: Track validation accuracy and performance
- **A/B Testing**: Test different validation strategies
- **Compliance**: Ensure validation meets business requirements

## Validation Criteria

The validator checks for:

### Exact Matches (from config)
- Complete query structure match
- Complete product data match
- Predefined validation result

### Partial Matches (fallback logic)
- **Brand Match**: Brand name present in product name
- **Model Match**: Model name present in product name
- **Storage Match**: Storage capacity matches (if specified)
- **Price Validation**: Price is positive and reasonable
- **Category Validation**: Product category is appropriate

## Error Handling

The module handles various scenarios:
- Missing query or product data
- Malformed configuration
- Real mode attempts (raises NotImplementedError)
- Partial matching when exact match not found

## Testing

Use the test file to validate:
- Mock validation cases from configuration
- Partial matching logic
- Error handling scenarios
- Configuration loading
- Integration with other modules 