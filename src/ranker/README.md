# Ranker Module

## 🧩 Purpose
Sorts deduplicated products by best value criteria to present users with the most attractive options first. Implements ranking algorithms to optimize the order of product listings based on price, quality, and other relevant factors.

## 🔁 Input & Output

- **Input**: 
  - `products` (List[Dict[str, Any]]): List of deduplicated product entries from Deduplicator

- **Output**: 
  - `List[Dict[str, Any]]`: Ranked list of products (best value first)

## ⚙️ Mock Behavior

- Controlled via `phase1_config.yaml` under `ranker.use_mock`
- Returns predefined ranked results from `mock_ranked_results` configuration
- Performs exact list matching against configured input patterns
- Falls back to basic price-based ranking if exact match not found
- Mock data stored in `mocks/ranked_results.yaml`

## 🛣️ Future Upgrade Path

- Replace mock logic with:
  - Multi-factor scoring algorithms
  - Machine learning-based ranking models
  - User preference learning and personalization
  - Vendor trust and reliability scoring
  - Delivery speed and availability weighting
  - Price history and trend analysis
  - Review and rating integration
  - Geographic proximity optimization
- Keep interface unchanged for pluggability

## 🧪 Example Usage
```python
from src.ranker.interface import Ranker

# Initialize with config
ranker = Ranker(config)

# Rank products by best value
products = [
    {"productName": "Apple iPhone 16 Pro 128GB", "price": "999"},
    {"productName": "Apple iPhone 16 Pro 128GB", "price": "979"},
    {"productName": "Apple iPhone 16 Pro 128GB", "price": "999"}
]
ranked_products = ranker.rank(products)
# Returns: [
#     {"productName": "Apple iPhone 16 Pro 128GB", "price": "979"},  # Best price first
#     {"productName": "Apple iPhone 16 Pro 128GB", "price": "999"},
#     {"productName": "Apple iPhone 16 Pro 128GB", "price": "999"}
# ]
```

## Interface

### Class: `Ranker`

#### Constructor
```python
__init__(self, config)
```
- **Parameters**: `config` (dict or str) - Configuration dictionary or path to YAML config file
- **Purpose**: Initializes the ranker with configuration settings

#### Main Method
```python
rank(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]
```
- **Parameters**: 
  - `products` (List[Dict[str, Any]]) - List of deduplicated product entries
- **Returns**: List[Dict[str, Any]] - Ranked list of products (best value first)
- **Raises**: 
  - `NotImplementedError`: If real ranking is attempted

## Configuration

The module uses the following configuration structure in `phase1_config.yaml`:

```yaml
ranker:
  use_mock: true
  mock_ranked_results:
    input_products:
      - productName: "Apple iPhone 16 Pro 128GB"
        price: "999"
        currency: "USD"
        link: "https://apple.com/iphone16pro"
      - productName: "Apple iPhone 16 Pro 128GB - Silver"
        price: "979"
        currency: "USD"
        link: "https://bestbuy.com/iphone16pro"
    output_products:
      - productName: "Apple iPhone 16 Pro 128GB - Silver"
        price: "979"
        currency: "USD"
        link: "https://bestbuy.com/iphone16pro"
      - productName: "Apple iPhone 16 Pro 128GB"
        price: "999"
        currency: "USD"
        link: "https://apple.com/iphone16pro"
```

## Ranking Strategy

The module uses a two-tier approach:

### 1. Mock Configuration Matching
- First tries to find exact input match in configuration
- Returns predefined ranked output if match found
- Ensures consistent test results

### 2. Basic Price-Based Ranking (Fallback)
- Sorts products by price (ascending - lowest price first)
- Handles invalid prices gracefully
- Preserves product data integrity

## Integration

This module integrates with:
- **Deduplicator**: Receives deduplicated product entries
- **Orchestrator**: Provides ranked products for final output
- **Validator**: Works with validated product data

## Future: Multi-Factor Scoring Weights

The mock implementation will be replaced with intelligent ranking:

### Phase 1: Enhanced Price-Based Ranking
- **Price Normalization**: Convert all prices to common currency
- **Price History**: Consider price trends and historical data
- **Price Alerts**: Flag unusually high or low prices
- **Bundle Analysis**: Evaluate package deals and promotions

### Phase 2: Vendor Trust and Reliability
- **Vendor Ratings**: Incorporate user reviews and ratings
- **Trust Scores**: Historical reliability and customer satisfaction
- **Return Policy**: Evaluate return and refund policies
- **Warranty Coverage**: Consider warranty terms and coverage

### Phase 3: Availability and Delivery
- **Local Availability**: Stock levels and local pickup options
- **Delivery Speed**: Estimated delivery times and shipping costs
- **Shipping Options**: Free shipping, express delivery, etc.
- **Inventory Status**: Real-time stock availability

### Phase 4: Advanced Value Scoring
- **Composite Scoring**: Weighted combination of all factors
- **User Preferences**: Personalized ranking based on user history
- **Market Analysis**: Competitive pricing and market positioning
- **Seasonal Factors**: Holiday sales, seasonal pricing patterns

### Phase 5: Machine Learning Ranking
- **ML Models**: Train models on user behavior and preferences
- **A/B Testing**: Continuously optimize ranking algorithms
- **Feedback Loops**: Learn from user interactions and conversions
- **Predictive Scoring**: Anticipate user preferences and market trends

## Ranking Criteria

The module considers:

### Current Implementation (Mock)
- **Price**: Primary ranking factor (lower is better)
- **Configuration Matching**: Exact input/output mapping

### Future Implementation (Real)
- **Price (40%)**: Primary value indicator
- **Vendor Trust (25%)**: Reliability and customer satisfaction
- **Local Availability (15%)**: Stock and pickup options
- **Delivery Speed (10%)**: Shipping times and costs
- **Return Policy (5%)**: Ease of returns and refunds
- **Warranty (3%)**: Coverage and terms
- **User Ratings (2%)**: Customer reviews and feedback

## Scoring Algorithm

### Basic Scoring (Current)
```python
score = 1000.0 / price  # Lower price = higher score
```

### Advanced Scoring (Future)
```python
score = (
    price_weight * normalize_price(price) +
    trust_weight * vendor_trust_score +
    availability_weight * local_availability_score +
    delivery_weight * delivery_speed_score +
    return_weight * return_policy_score +
    warranty_weight * warranty_coverage_score +
    rating_weight * user_rating_score
)
```

## Error Handling

The module handles various scenarios:
- Empty input lists
- Invalid price formats
- Missing product data
- Configuration errors
- Real mode attempts (raises NotImplementedError)

## Testing

Use the test file to validate:
- Mock ranking cases from configuration
- Basic price-based ranking logic
- Input/output validation
- Error handling scenarios
- Configuration loading
- Integration with other modules
- Ranking order correctness
- Edge cases and boundary conditions 