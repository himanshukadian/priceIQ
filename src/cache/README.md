# Cache Module

The cache module provides distributed caching functionality for the price intelligence platform, improving performance by storing frequently accessed data and reducing redundant operations.

## Features

- **Distributed Caching**: Redis-based caching for multi-instance deployments
- **Mock Implementation**: In-memory cache for development and testing
- **TTL Support**: Configurable time-to-live for cache entries
- **Query Result Caching**: Cache complete query results by query and country
- **Site Data Caching**: Cache site-specific data by site, category, and country
- **Product Data Caching**: Cache extracted product data by URL
- **Search Result Caching**: Cache search results by query and site
- **Cache Invalidation**: Methods to invalidate specific cache entries
- **Cache Statistics**: Monitor cache performance and usage

## Architecture

### CacheInterface
Abstract base class defining the cache contract:
- `get(key)`: Retrieve value from cache
- `set(key, value, ttl)`: Store value with optional TTL
- `delete(key)`: Delete value from cache
- `exists(key)`: Check if key exists
- `clear()`: Clear all cache entries

### RedisCache
Production-ready Redis implementation:
- Connection pooling and error handling
- JSON serialization for complex objects
- Configurable TTL and connection parameters
- Graceful fallback when Redis is unavailable

### MockCache
Development/testing implementation:
- In-memory storage with TTL simulation
- No external dependencies
- Automatic cleanup of expired entries

### CacheManager
High-level cache management:
- Domain-specific caching methods
- Consistent key generation
- Metadata storage (timestamps, source info)
- Cache statistics and monitoring

## Configuration

### Mock Cache (Default)
```yaml
modules:
  cache:
    use_mock: true
    ttl_default: 3600  # 1 hour
```

### Redis Cache
```yaml
modules:
  cache:
    use_mock: false
    redis:
      host: localhost
      port: 6379
      db: 0
      password: null
      ttl_default: 3600
```

## Usage Examples

### Basic Cache Operations
```python
from src.cache.interface import create_cache_manager

# Create cache manager from config
cache_manager = create_cache_manager(config)

# Cache query results
cache_manager.cache_query_results(
    query="iPhone 16 Pro",
    country="US",
    results=[...],
    ttl=1800  # 30 minutes
)

# Retrieve cached results
cached_results = cache_manager.get_cached_query_results("iPhone 16 Pro", "US")
```

### Site Data Caching
```python
# Cache site-specific data
cache_manager.cache_site_data(
    site="amazon.com",
    category="smartphone",
    country="US",
    data={"base_url": "https://amazon.com", "selectors": {...}},
    ttl=3600  # 1 hour
)

# Retrieve cached site data
site_data = cache_manager.get_cached_site_data("amazon.com", "smartphone", "US")
```

### Product Data Caching
```python
# Cache extracted product data
cache_manager.cache_product_data(
    url="https://amazon.com/iphone-16-pro",
    product_data={"name": "iPhone 16 Pro", "price": 999.99, ...},
    ttl=7200  # 2 hours
)

# Retrieve cached product data
product_data = cache_manager.get_cached_product_data("https://amazon.com/iphone-16-pro")
```

### Search Result Caching
```python
# Cache search results
cache_manager.cache_search_results(
    query="iPhone 16 Pro",
    site="amazon.com",
    results=["url1", "url2", "url3"],
    ttl=1800  # 30 minutes
)

# Retrieve cached search results
search_results = cache_manager.get_cached_search_results("iPhone 16 Pro", "amazon.com")
```

### Cache Invalidation
```python
# Invalidate specific cache entries
cache_manager.invalidate_query_cache("iPhone 16 Pro", "US")
cache_manager.invalidate_site_cache("amazon.com", "smartphone", "US")

# Clear all cache (use with caution)
cache_manager.cache.clear()
```

### Cache Statistics
```python
# Get cache performance statistics
stats = cache_manager.get_cache_stats()
print(f"Cache type: {stats['type']}")
print(f"Connected: {stats['connected']}")
if stats['type'] == 'mock':
    print(f"Entries: {stats['entries']}")
elif stats['type'] == 'redis' and stats['connected']:
    print(f"Memory usage: {stats['used_memory']}")
    print(f"Connected clients: {stats['connected_clients']}")
```

## Integration with Other Modules

### Orchestrator Integration
The orchestrator can use cache to:
- Check for existing query results before processing
- Cache final results for future requests
- Reduce processing time for repeated queries

### Search Agent Integration
The search agent can cache:
- Search results by query and site
- Site-specific search configurations
- Rate limiting and cooldown data

### Extractor Integration
The extractor can cache:
- Extracted product data by URL
- Site-specific extraction rules
- Parsing templates and selectors

## Performance Benefits

1. **Reduced API Calls**: Cache search results to avoid repeated API requests
2. **Faster Response Times**: Serve cached results for common queries
3. **Reduced Load**: Minimize scraping and extraction operations
4. **Cost Savings**: Reduce external API usage and bandwidth consumption
5. **Improved Reliability**: Fallback to cached data during outages

## Best Practices

1. **Appropriate TTL**: Set TTL based on data freshness requirements
2. **Key Naming**: Use consistent, descriptive cache keys
3. **Error Handling**: Always handle cache failures gracefully
4. **Monitoring**: Track cache hit rates and performance metrics
5. **Cleanup**: Regularly invalidate stale cache entries
6. **Security**: Use Redis authentication in production

## Dependencies

### Required for Mock Cache
- No external dependencies

### Required for Redis Cache
```bash
pip install redis
```

## Testing

The cache module includes comprehensive testing:
- Unit tests for all cache implementations
- Integration tests with Redis
- Performance benchmarks
- Error handling validation

Run tests:
```bash
python -m pytest tests/test_cache.py -v
```

## Production Deployment

### Redis Setup
1. Install Redis server
2. Configure authentication and security
3. Set up Redis clustering for high availability
4. Configure monitoring and alerting

### Docker Deployment
```yaml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --requirepass your_password
```

### Monitoring
- Cache hit/miss ratios
- Memory usage
- Response times
- Error rates
- Connection pool status 