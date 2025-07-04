# Site Selector Module

## 🧩 Purpose
Determines which e-commerce sites to search based on the user's country and product category. Ensures that price comparisons are performed on relevant, geographically appropriate platforms.

## 🔁 Input & Output

- **Input**: 
  - `country` (str): Country code (e.g., "US", "IN", "UK", "DE")
  - `category` (str): Product category for site selection (optional, defaults to "default")

- **Output**: 
  - `List[str]`: List of e-commerce site domains to search
  - Example: `["amazon.com", "bestbuy.com", "apple.com"]`

## ⚙️ Mock Behavior

- Controlled via `phase1_config.yaml` under `site_selector.use_mock`
- Returns predefined site lists from `sites_by_country` configuration
- Supports category-specific site selection
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
selector = SiteSelector(config)

# Select sites for a country
sites = selector.select_sources("US")
# Returns: ["amazon.com", "bestbuy.com", "apple.com"]

# Select sites for specific category
sites = selector.select_sources("IN")
# Returns: ["flipkart.com", "croma.com", "reliancedigital.in"]
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
select_sources(self, country: str) -> List[str]
```
- **Parameters**: `country` (str) - Country code (e.g., 'US', 'IN', 'UK', 'DE')
- **Returns**: List[str] - List of e-commerce site URLs to search
- **Purpose**: Returns appropriate e-commerce sites for the given country

## Mock Configuration Format

The module uses the following configuration structure in `phase1_config.yaml`:

```yaml
site_selector:
  use_mock: true
  sites_by_country:
    US:
      - amazon.com
      - bestbuy.com
      - apple.com
    IN:
      - flipkart.com
      - croma.com
      - reliancedigital.in
    UK:
      - amazon.co.uk
      - currys.co.uk
      - argos.co.uk
    DE:
      - amazon.de
      - mediamarkt.de
      - saturn.de
```

## Integration

This module will be integrated with the `search_agent` module to drive where product searches are performed. The orchestrator will call this module to get the list of sites, then pass each site to the search agent for product discovery.

## Future Enhancements

- Category-based site selection (different sites for electronics vs clothing)
- Site ranking and prioritization
- Dynamic site availability checking
- Integration with site performance metrics 