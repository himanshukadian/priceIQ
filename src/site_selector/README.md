# Site Selector Module

## 🧩 Purpose
Determines which e-commerce sites to search based on the user's country and product category. Ensures that price comparisons are performed on relevant, geographically appropriate platforms. **Not all sites support all categories in every country.**

## 🔁 Input & Output

- **Input**: 
  - `country` (str): Country code (e.g., "US", "IN", "UK", "DE")
  - `category` (str): Product category for site selection (e.g., "Smartphone", "Laptop", "Sports").

- **Output**: 
  - `List[str]`: List of e-commerce site domains to search
  - Example: `["amazon.com", "bestbuy.com", "nike.com"]`

## ⚙️ Mock Behavior

- Controlled via `phase1_config.yaml` under `site_selector.use_mock`
- Returns predefined site lists from `sites_by_country_and_category` configuration
- **Category-specific site selection**: Only sites supporting the given category in the given country are returned
- Mock data stored in `mocks/selected_sites.yaml`

## 🛣️ Future Upgrade Path

- Replace mock logic with:
  - Dynamic site availability checking
  - Site performance and reliability scoring
  - User preference-based site selection
  - Real-time site status monitoring
  - API-based site discovery and validation
  - Geographic coverage optimization
- Keep interface unchanged for pluggability

## 🧪 Example Usage
```python
from src.site_selector.interface import SiteSelector

# Initialize with config
dict_or_path = ...
selector = SiteSelector(dict_or_path)

# Select sites for a country and category
sites = selector.select_sources("US", "Sports")
# Returns: ["amazon.com", "bestbuy.com", "nike.com"]

sites = selector.select_sources("IN", "Laptop")
# Returns: ["amazon.in", "flipkart.com", "croma.com", "reliancedigital.in"]
```

## Interface

### Class: `SiteSelector`

#### Constructor
```python
__init__(self, config)
```
- **Parameters**: `config` (dict or str) - Configuration dictionary or path to YAML config file
- **Purpose**: Initializes the site selector with configuration settings

#### Main Method
```python
select_sources(self, country: str, category: str = None) -> List[str]
```
- **Parameters**: 
  - `country` (str) - Country code (e.g., 'US', 'IN', 'UK', 'DE')
  - `category` (str) - Product category (e.g., 'Smartphone', 'Laptop', 'Sports')
- **Returns**: List[str] - List of e-commerce site URLs to search
- **Purpose**: Returns appropriate e-commerce sites for the given country and category

## Mock Configuration Format

The module uses the following configuration structure in `phase1_config.yaml`:

```yaml
site_selector:
  use_mock: true
  sites_by_country_and_category:
    US:
      Smartphone:
        - amazon.com
        - bestbuy.com
        - apple.com
      Laptop:
        - amazon.com
        - bestbuy.com
        - apple.com
      Sports:
        - amazon.com
        - bestbuy.com
        - nike.com
    IN:
      Smartphone:
        - amazon.in
        - flipkart.com
        - croma.com
        - reliancedigital.in
      Laptop:
        - amazon.in
        - flipkart.com
        - croma.com
        - reliancedigital.in
      Sports:
        - amazon.in
        - flipkart.com
        - paytmmall.com
        - snapdeal.com
    # ... other countries
```

## Integration

This module is called by the orchestrator to determine which sites to search for a given query. It ensures only relevant sites for the product category and country are used.

## Future Enhancements

- Dynamic category/site mapping
- Site ranking and prioritization
- Dynamic site availability checking
- Integration with site performance metrics 