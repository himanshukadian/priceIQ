"""
Cache Interface
Provides distributed caching functionality using Redis for the price intelligence platform.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import json
import hashlib
import time
from datetime import datetime, timedelta


class CacheInterface(ABC):
    """Abstract interface for cache implementations."""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache."""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Store value in cache with optional TTL."""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        """Clear all cache entries."""
        pass


class RedisCache(CacheInterface):
    """Redis-based distributed cache implementation."""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, 
                 password: Optional[str] = None, ttl_default: int = 3600):
        """
        Initialize Redis cache.
        
        Args:
            host: Redis server host
            port: Redis server port
            db: Redis database number
            password: Redis password (if required)
            ttl_default: Default TTL in seconds (1 hour)
        """
        try:
            import redis
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            self.ttl_default = ttl_default
            self.connected = True
        except ImportError:
            raise ImportError("Redis package not installed. Run: pip install redis")
        except Exception as e:
            print(f"Warning: Redis connection failed: {e}")
            self.connected = False
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache."""
        if not self.connected or not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Store value in cache with optional TTL."""
        if not self.connected or not self.redis_client:
            return False
        
        try:
            ttl = ttl or self.ttl_default
            serialized_value = json.dumps(value, default=str)
            return self.redis_client.setex(key, ttl, serialized_value)
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if not self.connected or not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if not self.connected or not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            print(f"Cache exists error: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache entries."""
        if not self.connected or not self.redis_client:
            return False
        
        try:
            self.redis_client.flushdb()
            return True
        except Exception as e:
            print(f"Cache clear error: {e}")
            return False
    
    def get_ttl(self, key: str) -> Optional[int]:
        """Get remaining TTL for a key."""
        if not self.connected or not self.redis_client:
            return None
        
        try:
            return self.redis_client.ttl(key)
        except Exception as e:
            print(f"Cache TTL error: {e}")
            return None


class MockCache(CacheInterface):
    """Mock cache implementation for testing and development."""
    
    def __init__(self, ttl_default: int = 3600):
        """Initialize mock cache."""
        self.cache = {}
        self.ttl_default = ttl_default
        self.expiry_times = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache."""
        if key not in self.cache:
            return None
        
        # Check if expired
        if key in self.expiry_times and time.time() > self.expiry_times[key]:
            del self.cache[key]
            del self.expiry_times[key]
            return None
        
        return self.cache[key]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Store value in cache with optional TTL."""
        try:
            self.cache[key] = value
            ttl = ttl or self.ttl_default
            self.expiry_times[key] = time.time() + ttl
            return True
        except Exception:
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            if key in self.cache:
                del self.cache[key]
            if key in self.expiry_times:
                del self.expiry_times[key]
            return True
        except Exception:
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if key not in self.cache:
            return False
        
        # Check if expired
        if key in self.expiry_times and time.time() > self.expiry_times[key]:
            del self.cache[key]
            del self.expiry_times[key]
            return False
        
        return True
    
    def clear(self) -> bool:
        """Clear all cache entries."""
        try:
            self.cache.clear()
            self.expiry_times.clear()
            return True
        except Exception:
            return False


class CacheManager:
    """
    High-level cache manager for the price intelligence platform.
    Provides caching for query results, site data, and extracted products.
    """
    
    def __init__(self, cache_impl: CacheInterface):
        """
        Initialize cache manager.
        
        Args:
            cache_impl: Cache implementation (Redis or Mock)
        """
        self.cache = cache_impl
        self.prefix = "priceiq"
    
    def _generate_key(self, *args) -> str:
        """Generate cache key from arguments."""
        key_string = ":".join(str(arg) for arg in args)
        return f"{self.prefix}:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    def cache_query_results(self, query: str, country: str, results: List[Dict], 
                           ttl: int = 1800) -> bool:
        """
        Cache query results.
        
        Args:
            query: Product query
            country: Country code
            results: List of product results
            ttl: Time to live in seconds (30 minutes default)
        
        Returns:
            bool: Success status
        """
        key = self._generate_key("query_results", query, country)
        return self.cache.set(key, {
            'results': results,
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'country': country
        }, ttl)
    
    def get_cached_query_results(self, query: str, country: str) -> Optional[List[Dict]]:
        """
        Get cached query results.
        
        Args:
            query: Product query
            country: Country code
        
        Returns:
            Optional[List[Dict]]: Cached results or None
        """
        key = self._generate_key("query_results", query, country)
        cached_data = self.cache.get(key)
        if cached_data:
            return cached_data.get('results')
        return None
    
    def cache_site_data(self, site: str, category: str, country: str, 
                       data: Dict, ttl: int = 3600) -> bool:
        """
        Cache site-specific data.
        
        Args:
            site: Site domain
            category: Product category
            country: Country code
            data: Site data
            ttl: Time to live in seconds (1 hour default)
        
        Returns:
            bool: Success status
        """
        key = self._generate_key("site_data", site, category, country)
        return self.cache.set(key, {
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'site': site,
            'category': category,
            'country': country
        }, ttl)
    
    def get_cached_site_data(self, site: str, category: str, country: str) -> Optional[Dict]:
        """
        Get cached site data.
        
        Args:
            site: Site domain
            category: Product category
            country: Country code
        
        Returns:
            Optional[Dict]: Cached site data or None
        """
        key = self._generate_key("site_data", site, category, country)
        cached_data = self.cache.get(key)
        if cached_data:
            return cached_data.get('data')
        return None
    
    def cache_product_data(self, url: str, product_data: Dict, ttl: int = 7200) -> bool:
        """
        Cache extracted product data.
        
        Args:
            url: Product URL
            product_data: Extracted product data
            ttl: Time to live in seconds (2 hours default)
        
        Returns:
            bool: Success status
        """
        key = self._generate_key("product_data", url)
        return self.cache.set(key, {
            'product_data': product_data,
            'timestamp': datetime.now().isoformat(),
            'url': url
        }, ttl)
    
    def get_cached_product_data(self, url: str) -> Optional[Dict]:
        """
        Get cached product data.
        
        Args:
            url: Product URL
        
        Returns:
            Optional[Dict]: Cached product data or None
        """
        key = self._generate_key("product_data", url)
        cached_data = self.cache.get(key)
        if cached_data:
            return cached_data.get('product_data')
        return None
    
    def cache_search_results(self, query: str, site: str, results: List[str], 
                           ttl: int = 1800) -> bool:
        """
        Cache search results.
        
        Args:
            query: Search query
            site: Site domain
            results: List of URLs
            ttl: Time to live in seconds (30 minutes default)
        
        Returns:
            bool: Success status
        """
        key = self._generate_key("search_results", query, site)
        return self.cache.set(key, {
            'results': results,
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'site': site
        }, ttl)
    
    def get_cached_search_results(self, query: str, site: str) -> Optional[List[str]]:
        """
        Get cached search results.
        
        Args:
            query: Search query
            site: Site domain
        
        Returns:
            Optional[List[str]]: Cached search results or None
        """
        key = self._generate_key("search_results", query, site)
        cached_data = self.cache.get(key)
        if cached_data:
            return cached_data.get('results')
        return None
    
    def invalidate_query_cache(self, query: str, country: str) -> bool:
        """Invalidate cached query results."""
        key = self._generate_key("query_results", query, country)
        return self.cache.delete(key)
    
    def invalidate_site_cache(self, site: str, category: str, country: str) -> bool:
        """Invalidate cached site data."""
        key = self._generate_key("site_data", site, category, country)
        return self.cache.delete(key)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if isinstance(self.cache, MockCache):
            return {
                'type': 'mock',
                'entries': len(self.cache.cache),
                'connected': True
            }
        elif isinstance(self.cache, RedisCache):
            if not self.cache.connected:
                return {'type': 'redis', 'connected': False}
            
            try:
                info = self.cache.redis_client.info()
                return {
                    'type': 'redis',
                    'connected': True,
                    'used_memory': info.get('used_memory_human'),
                    'connected_clients': info.get('connected_clients'),
                    'total_commands_processed': info.get('total_commands_processed')
                }
            except Exception:
                return {'type': 'redis', 'connected': False}
        
        return {'type': 'unknown', 'connected': False}


def create_cache_manager(config: Dict) -> CacheManager:
    """
    Factory function to create cache manager based on configuration.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        CacheManager: Configured cache manager
    """
    cache_config = config.get('modules', {}).get('cache', {})
    use_mock = cache_config.get('use_mock', True)
    
    if use_mock:
        ttl_default = cache_config.get('ttl_default', 3600)
        cache_impl = MockCache(ttl_default=ttl_default)
    else:
        redis_config = cache_config.get('redis', {})
        cache_impl = RedisCache(
            host=redis_config.get('host', 'localhost'),
            port=redis_config.get('port', 6379),
            db=redis_config.get('db', 0),
            password=redis_config.get('password'),
            ttl_default=redis_config.get('ttl_default', 3600)
        )
    
    return CacheManager(cache_impl) 