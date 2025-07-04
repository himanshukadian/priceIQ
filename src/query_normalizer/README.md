# Query Normalizer Module

## 🧩 Purpose
Standardizes and structures user input queries for consistent processing across the price intelligence pipeline. Converts raw text queries into structured data with extracted metadata like brand, model, and category-specific attributes. **Category detection is built-in and returns different attributes based on product type.**

## 🔁 Input & Output

- **Input**: 
  - `query` (str): Raw product query string (e.g., "iPhone 16 Pro, 128GB", "Nike Air Max 270")
  - `country` (str): Country code for context (e.g., "US", "IN", "UK")

- **Output**: 
  - `Dict[str, Any]`: Structured data containing category-specific attributes:
    - `normalized` (str): Cleaned query string
    - `brand` (str): Extracted brand name
    - `model` (str): Extracted model name
    - `category` (str): Product category classification (e.g., "Smartphone", "Laptop", "Sports")
    - **Category-specific attributes** (see below)

## 🏷️ Category-Specific Attributes

The module returns different attributes based on the detected product category:

### Smartphone Attributes
- `storage` (str): Storage capacity (e.g., "128GB")
- `color` (str): Device color (e.g., "Natural Titanium")
- `screen_size` (str): Screen size (e.g., "6.1 inch")

### Laptop Attributes  
- `storage` (str): Storage capacity (e.g., "512GB")
- `ram` (str): RAM capacity (e.g., "16GB")
- `screen_size` (str): Screen size (e.g., "14 inch")
- `processor` (str): Processor model (e.g., "M3 Pro")

### Sports Attributes
- `size` (str): Product size (e.g., "US 10")
- `color` (str): Product color (e.g., "Black/White")
- `type` (str): Product type (e.g., "Running Shoes")

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
#     "brand": "Apple",
#     "model": "iPhone 16 Pro",
#     "storage": "128GB",
#     "color": "Natural Titanium",
#     "screen_size": "6.1 inch",
#     "category": "Smartphone"
# }

# Normalize a laptop query
result = normalizer.normalize("MacBook Pro")
# Returns: {
#     "brand": "Apple",
#     "model": "MacBook Pro",
#     "storage": "512GB",
#     "ram": "16GB",
#     "screen_size": "14 inch",
#     "processor": "M3 Pro",
#     "category": "Laptop"
# }

# Normalize a sports query
result = normalizer.normalize("Nike Air Max 270")
# Returns: {
#     "brand": "Nike",
#     "model": "Air Max 270",
#     "size": "US 10",
#     "color": "Black/White",
#     "type": "Running Shoes",
#     "category": "Sports"
# }
``` 