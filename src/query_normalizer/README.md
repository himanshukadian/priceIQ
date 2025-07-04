# Query Normalizer Module

## 🧩 Purpose
Standardizes and structures user input queries for consistent processing across the price intelligence pipeline. Converts raw text queries into structured data with extracted metadata like brand, model, storage, and category. **Category detection is built-in and not all queries map to all categories.**

## 🔁 Input & Output

- **Input**: 
  - `query` (str): Raw product query string (e.g., "iPhone 16 Pro, 128GB", "Nike Air Max 270")
  - `country` (str): Country code for context (e.g., "US", "IN", "UK")

- **Output**: 
  - `Dict[str, Any]`: Structured data containing:
    - `normalized` (str): Cleaned query string
    - `brand` (str): Extracted brand name
    - `model` (str): Extracted model name
    - `storage` (str): Extracted storage capacity
    - `category` (str): Product category classification (e.g., "Smartphone", "Laptop", "Sports")

## ⚙️ Mock Behavior

- Controlled via `phase1_config.yaml` under `query_normalizer.use_mock`
- Returns predefined normalized data from `mock_outputs` configuration for each category
- Fallback to basic normalization if query not found in mock data
- Mock data stored in `mocks/normalized_queries.yaml`

## 🛣️ Future Upgrade Path

- Replace mock logic with:
  - LLM-based query understanding and entity extraction
  - Product database lookups for brand/model validation
  - Multi-language query processing
  - Fuzzy matching for misspelled brands/models
  - Context-aware normalization based on country/region
- Keep interface unchanged for pluggability

## 🧪 Example Usage
```python
from src.query_normalizer.interface import QueryNormalizer

# Initialize with config
dict_or_path = ...
normalizer = QueryNormalizer(dict_or_path)

# Normalize a smartphone query
result = normalizer.normalize("iPhone 16 Pro, 128GB")
# Returns: {
#     "normalized": "iPhone 16 Pro 128GB",
#     "brand": "Apple",
#     "model": "iPhone 16 Pro",
#     "storage": "128GB",
#     "category": "Smartphone"
# }

# Normalize a sports query
result = normalizer.normalize("Nike Air Max 270")
# Returns: {
#     "normalized": "Nike Air Max 270",
#     "brand": "Nike",
#     "model": "Air Max",
#     "storage": "Standard",
#     "category": "Sports"
# }

# Normalize a laptop query
result = normalizer.normalize("MacBook Pro")
# Returns: {
#     "normalized": "MacBook Pro",
#     "brand": "Apple",
#     "model": "MacBook Pro",
#     "storage": "512GB",
#     "category": "Laptop"
# }
``` 