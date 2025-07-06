#!/usr/bin/env python3
"""
Price Intelligence Platform - Streamlit Web Interface
Provides a user-friendly web interface for searching and comparing product prices globally.
"""

import streamlit as st
import pandas as pd
from src.orchestrator.interface import Orchestrator
import os
from pathlib import Path

# Example queries with country
EXAMPLES = [
    {"label": "iPhone 16 Pro, 128GB (US)", "query": "iPhone 16 Pro, 128GB", "country": "US"},
    {"label": "MacBook Pro (IN)", "query": "MacBook Pro", "country": "IN"},
    {"label": "Nike Air Max 270 (UK)", "query": "Nike Air Max 270", "country": "UK"},
    {"label": "Samsung Galaxy S24 (DE)", "query": "Samsung Galaxy S24", "country": "DE"},
]

# Page configuration
st.set_page_config(
    page_title="🎯 Global Price Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize orchestrator
@st.cache_resource
def get_orchestrator():
    """Initialize and cache the orchestrator to avoid reloading."""
    config_path = os.path.join("config", "phase1_config.yaml")
    return Orchestrator(config_path)

def format_price(price, currency):
    """Format price with currency symbol."""
    currency_symbols = {
        "USD": "$",
        "INR": "₹",
        "GBP": "£",
        "EUR": "€"
    }
    symbol = currency_symbols.get(currency, currency)
    return f"{symbol}{price}"

def create_clickable_link(url, text):
    """Create a clickable link for Streamlit."""
    return f"[{text}]({url})"

def show_implementation_plan():
    """Display the full implementation plan documentation as a single scrollable page, hardcoded (no file dependency)."""
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #fff;
        text-align: center;
        margin-bottom: 2rem;
        margin-top: 1rem;
    }
    .section-header, .phase-header {
        font-size: 1.4rem;
        font-weight: bold;
        color: #90caf9;
        margin-top: 2.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1976d2;
        padding-left: 0.7rem;
        background: none !important;
    }
    .highlight-box, .status-complete, .status-pending, .timeline-item {
        background: none !important;
        color: inherit !important;
        border: none !important;
        font-weight: inherit !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">📋 Implementation Plan</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #bbb;">Price Intelligence Platform - Complete Roadmap</h2>', unsafe_allow_html=True)
    st.markdown("""
## Executive Summary

This document outlines the complete implementation roadmap for the Price Intelligence Platform, a global price comparison and intelligence system. The platform is currently in **Phase 1** with a robust mock-first architecture and modular microservices design.

## Current Status (Phase 1 Complete)

### ✅ Completed Features
- **Modular Architecture**: 9 core modules with clean interfaces
- **Multi-Country Support**: US, UK, DE, IN with extensible design
- **Multi-Category Support**: Smartphone, Laptop, Sports with category-aware logic
- **Mock-First Development**: All modules have mock implementations for rapid development
- **Docker Support**: Containerized deployment with docker-compose
- **Streamlit Interface**: Modern web UI for user interaction
- **Cache Module**: Redis and Mock caching with TTL support
- **Comprehensive Testing**: Unit tests and integration tests
- **Documentation**: Detailed READMEs and API documentation
- **Git Version Control**: Complete history and collaboration setup

## 🏗️ Architecture Overview
```
User Interface Layer
┌───────────────────────────────┐
│  Streamlit UI / CLI / API     │
└──────────────┬────────────────┘
               │
               ▼
        ┌───────────────┐
        │ Orchestrator  │
        └──────┬────────┘
               │
               ▼
      ┌────────────────────┐
      │ Query Normalizer   │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Site Selector      │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Search Agent       │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Scraper            │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Extractor          │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Validator          │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Deduplicator       │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Ranker             │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Cache              │
      └────────────────────┘
```

## Phase 2: Core Real Implementations (Priority: HIGH)

### 2.1 Query Normalizer - Real Implementation
**Timeline**: 2-3 sprints
**Priority**: Critical

#### Requirements
- **LLM-based Understanding**: Use Large Language Models to extract product names, brands, models
- **Category Detection**: Auto-detect product categories from queries using LLMs
- **Query Standardization**: Normalize variations (iPhone 16 Pro vs iPhone 16Pro)
- **Brand Recognition**: Identify and standardize brand names
- **Model Matching**: Handle model variations and aliases

#### Technical Implementation
```python
# Example real implementation
class RealQueryNormalizer:
    def __init__(self):
        self.llm_model = load_llm_model("openai/gpt-4")
        self.brand_aliases = self.load_brand_aliases()
        self.category_keywords = self.load_category_keywords()
    
    def normalize(self, query: str) -> Dict:
        # LLM-based understanding
        # Brand detection
        # Category classification
        # Query standardization
        pass
```

#### Dependencies
- OpenAI GPT-4 or similar LLM
- Custom brand/category datasets
- Product database integration

### 2.2 Site Selector - Real Implementation
**Timeline**: 1-2 sprints
**Priority**: High

#### Requirements
- **Dynamic Site Discovery**: Find relevant sites for products/countries
- **Site Ranking**: Rank sites by reliability and coverage
- **Category-Site Mapping**: Map product categories to appropriate sites
- **Geographic Targeting**: Country-specific site selection
- **Site Health Monitoring**: Track site availability and performance

#### Technical Implementation
```python
class RealSiteSelector:
    def __init__(self):
        self.site_database = SiteDatabase()
        self.site_ranker = SiteRanker()
        self.health_monitor = HealthMonitor()
    
    def select_sites(self, query: str, category: str, country: str) -> List[str]:
        # Dynamic site discovery
        # Category-based filtering
        # Geographic targeting
        # Health-based ranking
        pass
```

### 2.3 Search Agent - Real Implementation
**Timeline**: 3-4 sprints
**Priority**: Critical

#### Requirements
- **Multi-Site Search**: Search across multiple e-commerce sites
- **API Integration**: Integrate with site APIs (Amazon, Best Buy, etc.)
- **Web Scraping**: Fallback to web scraping when APIs unavailable
- **Rate Limiting**: Respect site rate limits and robots.txt
- **Search Optimization**: Optimize search queries for better results
- **Result Validation**: Validate search results quality

#### Technical Implementation
```python
class RealSearchAgent:
    def __init__(self):
        self.api_clients = self.initialize_api_clients()
        self.scrapers = self.initialize_scrapers()
        self.rate_limiter = RateLimiter()
    
    def search(self, query: str, site: str) -> List[str]:
        # API-first approach
        # Web scraping fallback
        # Rate limiting
        # Result validation
        pass
```

#### Dependencies
- Selenium/Playwright for web scraping
- Site-specific API clients
- Proxy rotation system
- User agent management

### 2.4 Scraper - Real Implementation
**Timeline**: 4-5 sprints
**Priority**: Critical

#### Requirements
- **Dynamic Content Handling**: Handle JavaScript-rendered content
- **Anti-Bot Detection**: Bypass anti-bot measures
- **Proxy Rotation**: Rotate IPs to avoid blocking
- **Session Management**: Maintain sessions across requests
- **Error Recovery**: Handle network errors and retries
- **Content Extraction**: Extract HTML content efficiently

#### Technical Implementation
```python
class RealScraper:
    def __init__(self):
        self.browser_pool = BrowserPool()
        self.proxy_manager = ProxyManager()
        self.session_manager = SessionManager()
    
    def scrape(self, url: str) -> str:
        # Browser automation
        # Proxy rotation
        # Anti-bot bypass
        # Error handling
        pass
```

#### Dependencies
- Playwright/Selenium
- Proxy service integration
- Browser automation tools
- CAPTCHA solving service

### 2.5 Extractor - Real Implementation
**Timeline**: 3-4 sprints
**Priority**: High

#### Requirements
- **Dynamic Selectors**: Auto-generate and update CSS selectors
- **Machine Learning**: ML-based content extraction
- **Multi-Format Support**: Handle different page layouts
- **Data Validation**: Validate extracted data quality
- **Selector Learning**: Learn from successful extractions
- **Fallback Mechanisms**: Multiple extraction strategies

#### Technical Implementation
```python
class RealExtractor:
    def __init__(self):
        self.ml_model = ExtractionModel()
        self.selector_engine = SelectorEngine()
        self.validator = DataValidator()
    
    def extract(self, html: str, site: str, category: str) -> Dict:
        # ML-based extraction
        # Dynamic selector generation
        # Data validation
        # Fallback strategies
        pass
```

#### Dependencies
- TensorFlow/PyTorch for ML models
- BeautifulSoup/lxml for parsing
- Training datasets
- Validation frameworks

## Phase 3: Advanced Features (Priority: MEDIUM)

### 3.1 Validator - Real Implementation
**Timeline**: 2-3 sprints

#### Requirements
- **Price Validation**: Validate price ranges and formats
- **Product Matching**: Match products across sites
- **Data Quality Scoring**: Score data quality and reliability
- **Anomaly Detection**: Detect price anomalies and errors
- **Historical Analysis**: Compare with historical data

### 3.2 Deduplicator - Real Implementation
**Timeline**: 2-3 sprints

#### Requirements
- **Fuzzy Matching**: Fuzzy string matching for product names
- **Image Similarity**: Use product images for deduplication
- **Attribute Comparison**: Compare product attributes
- **Confidence Scoring**: Score match confidence
- **Manual Review**: Interface for manual deduplication

### 3.3 Ranker - Real Implementation
**Timeline**: 2-3 sprints

#### Requirements
- **Multi-Factor Ranking**: Price, reliability, availability, shipping
- **User Preferences**: Personalized ranking based on user preferences
- **Market Analysis**: Consider market trends and demand
- **A/B Testing**: Test different ranking algorithms
- **Performance Metrics**: Track ranking performance

## Phase 4: Production Infrastructure (Priority: HIGH)

### 4.1 Database Implementation
**Timeline**: 2-3 sprints

#### Requirements
- **Product Database**: Store product information and prices
- **User Database**: User accounts and preferences
- **Analytics Database**: Store usage analytics and metrics
- **Cache Database**: Redis for caching and sessions
- **Data Warehousing**: Historical data for analysis

#### Technical Stack
```yaml
databases:
  primary: PostgreSQL
  cache: Redis
  analytics: ClickHouse
  search: Elasticsearch
```

### 4.2 API Gateway
**Timeline**: 2-3 sprints

#### Requirements
- **RESTful API**: Standard REST API endpoints
- **Authentication**: JWT-based authentication
- **Rate Limiting**: API rate limiting and quotas
- **Documentation**: OpenAPI/Swagger documentation
- **Monitoring**: API usage monitoring and analytics

#### API Endpoints
```python
# Core endpoints
GET /api/v1/search?query=iPhone&country=US
GET /api/v1/products/{product_id}
GET /api/v1/prices/{product_id}/history
POST /api/v1/alerts
GET /api/v1/analytics
```

### 4.3 Monitoring & Observability
**Timeline**: 2-3 sprints

#### Requirements
- **Application Monitoring**: APM with distributed tracing
- **Infrastructure Monitoring**: System metrics and health checks
- **Error Tracking**: Error aggregation and alerting
- **Performance Metrics**: Response times and throughput
- **Business Metrics**: User engagement and conversion tracking

#### Tools
```yaml
monitoring:
  apm: DataDog/New Relic
  metrics: Prometheus + Grafana
  logging: ELK Stack
  alerting: PagerDuty
```

### 4.4 Security Implementation
**Timeline**: 2-3 sprints

#### Requirements
- **Authentication**: Multi-factor authentication
- **Authorization**: Role-based access control
- **Data Encryption**: Encrypt data at rest and in transit
- **API Security**: API key management and validation
- **Compliance**: GDPR, CCPA compliance

## Phase 5: Advanced Analytics & ML (Priority: LOW)

### 5.1 Price Prediction
**Timeline**: 4-6 sprints

#### Requirements
- **Price Forecasting**: Predict future price movements
- **Demand Analysis**: Analyze demand patterns
- **Seasonal Trends**: Identify seasonal price patterns
- **Market Intelligence**: Competitive price analysis
- **Recommendation Engine**: Product recommendations

### 5.2 Market Intelligence
**Timeline**: 3-4 sprints

#### Requirements
- **Competitive Analysis**: Track competitor pricing
- **Market Trends**: Identify market trends and patterns
- **Price Optimization**: Suggest optimal pricing strategies
- **Inventory Analysis**: Track product availability
- **Geographic Analysis**: Regional price variations

## Legal & Compliance

### Web Scraping Compliance
- **Terms of Service**: Respect site terms of service
- **Robots.txt**: Follow robots.txt directives
- **Rate Limiting**: Implement reasonable rate limits
- **Data Usage**: Clear data usage policies
- **Legal Consultation**: Regular legal review

### Data Privacy
- **GDPR Compliance**: European data protection
- **CCPA Compliance**: California privacy laws
- **Data Retention**: Clear data retention policies
- **User Consent**: Explicit user consent for data collection
- **Data Portability**: User data export capabilities

## Implementation Timeline

### Phase 2: Core Real Implementations
- **Sprint 1**: Query Normalizer + Site Selector
- **Sprint 2**: Search Agent + Scraper
- **Sprint 3**: Extractor + Testing

### Phase 3: Advanced Features
- **Sprint 1**: Validator + Deduplicator
- **Sprint 2**: Ranker + Integration Testing

### Phase 4: Production Infrastructure
- **Sprint 1**: Database + API Gateway
- **Sprint 2**: Monitoring + Security

### Phase 5: Advanced Analytics
- **Sprint 1**: Price Prediction
- **Sprint 2**: Market Intelligence

## Conclusion

This implementation plan provides a comprehensive roadmap for building a production-ready price intelligence platform. The modular architecture and mock-first approach ensure rapid development and testing while maintaining flexibility for future enhancements.

The phased approach allows for incremental delivery of value while managing risks and resource requirements effectively. Each phase builds upon the previous one, ensuring a solid foundation for the next level of functionality.
    
    """)

def main():
    # URL-based navigation (robust)
    query_params = st.query_params
    page_param = query_params.get("page", "search")
    tab_labels = ["🎯 Price Search", "📋 Implementation Plan"]
    tab_keys = ["search", "plan"]
    default_tab = tab_keys.index(page_param) if page_param in tab_keys else 0

    # Use a radio button for navigation
    selected_tab_label = st.radio(
        "Navigation",
        tab_labels,
        index=default_tab,
        horizontal=True,
        key="main_nav_radio"
    )
    selected_tab = tab_labels.index(selected_tab_label)
    # Update URL if changed
    if tab_keys[selected_tab] != page_param:
        st.query_params["page"] = tab_keys[selected_tab]
        st.rerun()

    # Render the selected page
    if tab_keys[selected_tab] == "search":
        with st.sidebar:
            st.header("🔍 Example Queries")
            example_labels = [ex["label"] for ex in EXAMPLES]
            example_choice = st.selectbox(
                "Choose an example to auto-fill query and country:",
                ["(None)"] + example_labels,
                index=0
            )
            st.markdown("""
            - `iPhone 16 Pro, 128GB` (Country: US)
            - `MacBook Pro` (Country: IN)
            - `Nike Air Max 270` (Country: UK)
            - `Samsung Galaxy S24` (Country: DE)
            """)
            st.header("ℹ️ About")
            st.markdown("""
            This platform searches across multiple e-commerce sites to find the best prices for your products.
            
            **Supported Categories:**
            - 📱 Smartphones (iPhone, Samsung, etc.)
            - 💻 Laptops (MacBook, Dell, HP, etc.)
            - 👟 Sports (Nike, Adidas, etc.)
            
            **Supported Countries:**
            - 🇺🇸 US (USD)
            - 🇮🇳 India (INR)
            - 🇬🇧 UK (GBP)
            - 🇩🇪 Germany (EUR)
            """)
        show_price_search(example_choice)
    elif tab_keys[selected_tab] == "plan":
        show_implementation_plan()

def show_price_search(example_choice=None):
    """Display the main price search interface."""
    # Header
    st.title("🎯 Global Price Intelligence")
    st.markdown("Compare product prices across multiple e-commerce sites globally.")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    # Determine default values from example selection
    if example_choice and example_choice != "(None)":
        selected = next(ex for ex in EXAMPLES if ex["label"] == example_choice)
        default_query = selected["query"]
        default_country = selected["country"]
    else:
        default_query = ""
        default_country = "US"
    
    with col1:
        # Search inputs
        query = st.text_input(
            "What product are you looking for?",
            value=default_query,
            placeholder="e.g., iPhone 16 Pro, 128GB or MacBook Pro",
            help="Enter the product name, model, and any specifications"
        )
    
    with col2:
        country = st.selectbox(
            "Select country",
            ["US", "IN", "UK", "DE"],
            index=["US", "IN", "UK", "DE"].index(default_country) if default_country in ["US", "IN", "UK", "DE"] else 0,
            help="Choose your target market for price comparison"
        )
    
    # Search button
    if st.button("🔍 Search Prices", type="primary", use_container_width=True):
        if not query.strip():
            st.warning("⚠️ Please enter a product query.")
            return
        
        # Show loading spinner
        with st.spinner("🔍 Searching for the best prices..."):
            try:
                # Get orchestrator and run search
                orchestrator = get_orchestrator()
                results = orchestrator.run({"query": query, "country": country})
                
                # Display results
                if results:
                    st.success(f"✅ Found {len(results)} products!")
                    
                    # Create DataFrame for display
                    df_data = []
                    for i, product in enumerate(results, 1):
                        df_data.append({
                            "Rank": i,
                            "Product": product.get("productName", "Unknown"),
                            "Price": format_price(product.get("price", "0"), product.get("currency", "USD")),
                            "Link": create_clickable_link(
                                product.get("link", "#"),
                                "View Product"
                            )
                        })
                    
                    df = pd.DataFrame(df_data)
                    
                    # Display as table with custom styling
                    st.markdown("### 📊 Price Comparison Results")
                    
                    # Use st.dataframe with custom formatting
                    st.dataframe(
                        df,
                        column_config={
                            "Rank": st.column_config.NumberColumn(
                                "Rank",
                                help="Price ranking (1 = best value)",
                                format="%d"
                            ),
                            "Product": st.column_config.TextColumn(
                                "Product Name",
                                help="Product name and specifications"
                            ),
                            "Price": st.column_config.TextColumn(
                                "Price",
                                help="Formatted price with currency"
                            ),
                            "Link": st.column_config.LinkColumn(
                                "Product Link",
                                help="Click to view product on retailer site"
                            )
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                    
                    # Additional insights
                    if len(results) > 1:
                        prices = [float(p.get("price", 0)) for p in results]
                        min_price = min(prices)
                        max_price = max(prices)
                        price_diff = max_price - min_price
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Lowest Price", format_price(str(min_price), results[0].get("currency", "USD")))
                        with col2:
                            st.metric("Highest Price", format_price(str(max_price), results[0].get("currency", "USD")))
                        with col3:
                            st.metric("Price Range", format_price(str(price_diff), results[0].get("currency", "USD")))
                
                else:
                    st.warning("⚠️ No products found for your search.")
                    st.info("💡 Try adjusting your search terms or selecting a different country.")
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 This might be due to missing mock data for your specific query. Try a different product or country.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        🎯 Price Intelligence Platform | 
        <a href="https://github.com/himanshukadian/priceIQ" target="_blank">GitHub Repository</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 