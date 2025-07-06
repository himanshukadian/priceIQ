#!/usr/bin/env python3
"""
Comprehensive test suite for the caching system.
Tests both MockCache and RedisCache implementations.
"""

import unittest
import time
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import cache modules
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from cache.interface import MockCache, RedisCache, CacheManager, create_cache_manager


class TestMockCache(unittest.TestCase):
    """Test cases for MockCache implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cache = MockCache(ttl_default=3600)
    
    def test_basic_set_get(self):
        """Test basic set and get operations."""
        # Test setting and getting a value
        self.assertTrue(self.cache.set("test_key", "test_value"))
        self.assertEqual(self.cache.get("test_key"), "test_value")
    
    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist."""
        self.assertIsNone(self.cache.get("nonexistent_key"))
    
    def test_delete_key(self):
        """Test deleting a key."""
        self.cache.set("test_key", "test_value")
        self.assertTrue(self.cache.delete("test_key"))
        self.assertIsNone(self.cache.get("test_key"))
    
    def test_delete_nonexistent_key(self):
        """Test deleting a key that doesn't exist."""
        self.assertTrue(self.cache.delete("nonexistent_key"))
    
    def test_exists_key(self):
        """Test checking if a key exists."""
        self.cache.set("test_key", "test_value")
        self.assertTrue(self.cache.exists("test_key"))
        self.assertFalse(self.cache.exists("nonexistent_key"))
    
    def test_clear_cache(self):
        """Test clearing all cache entries."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.assertTrue(self.cache.clear())
        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))
    
    def test_ttl_expiration(self):
        """Test TTL expiration."""
        # Set a value with 1 second TTL
        self.cache.set("test_key", "test_value", ttl=1)
        self.assertEqual(self.cache.get("test_key"), "test_value")
        
        # Wait for expiration
        time.sleep(1.1)
        self.assertIsNone(self.cache.get("test_key"))
    
    def test_default_ttl(self):
        """Test default TTL behavior."""
        self.cache.set("test_key", "test_value")
        # Should not expire immediately
        self.assertEqual(self.cache.get("test_key"), "test_value")
    
    def test_complex_data_types(self):
        """Test caching complex data types."""
        test_data = {
            "string": "test",
            "number": 42,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
            "boolean": True,
            "none": None
        }
        
        self.cache.set("complex_key", test_data)
        retrieved = self.cache.get("complex_key")
        self.assertEqual(retrieved, test_data)
    
    def test_multiple_operations(self):
        """Test multiple cache operations."""
        # Set multiple values
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        # Verify all exist
        self.assertTrue(self.cache.exists("key1"))
        self.assertTrue(self.cache.exists("key2"))
        self.assertTrue(self.cache.exists("key3"))
        
        # Delete one
        self.cache.delete("key2")
        self.assertTrue(self.cache.exists("key1"))
        self.assertFalse(self.cache.exists("key2"))
        self.assertTrue(self.cache.exists("key3"))


class TestRedisCache(unittest.TestCase):
    """Test cases for RedisCache implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use mock Redis for testing
        with patch('builtins.__import__') as mock_import:
            # Mock the redis module
            mock_redis_module = Mock()
            self.mock_redis_client = Mock()
            mock_redis_module.Redis.return_value = self.mock_redis_client
            self.mock_redis_client.ping.return_value = True
            
            # Make __import__ return our mock when 'redis' is requested
            def side_effect(name, *args, **kwargs):
                if name == 'redis':
                    return mock_redis_module
                return __import__(name, *args, **kwargs)
            
            mock_import.side_effect = side_effect
            
            self.cache = RedisCache(host='localhost', port=6379)
    
    def test_successful_connection(self):
        """Test successful Redis connection."""
        with patch('builtins.__import__') as mock_import:
            # Mock the redis module
            mock_redis_module = Mock()
            mock_client = Mock()
            mock_redis_module.Redis.return_value = mock_client
            mock_client.ping.return_value = True
            
            # Make __import__ return our mock when 'redis' is requested
            def side_effect(name, *args, **kwargs):
                if name == 'redis':
                    return mock_redis_module
                return __import__(name, *args, **kwargs)
            
            mock_import.side_effect = side_effect
            
            cache = RedisCache()
            self.assertTrue(cache.connected)
    
    def test_failed_connection(self):
        """Test failed Redis connection."""
        with patch('builtins.__import__') as mock_import:
            # Mock the redis module to raise an exception
            def side_effect(name, *args, **kwargs):
                if name == 'redis':
                    raise Exception("Connection failed")
                return __import__(name, *args, **kwargs)
            
            mock_import.side_effect = side_effect
            
            cache = RedisCache()
            self.assertFalse(cache.connected)
    
    def test_missing_redis_package(self):
        """Test behavior when Redis package is not installed."""
        with patch('builtins.__import__', side_effect=ImportError("No module named 'redis'")):
            with self.assertRaises(ImportError):
                RedisCache()
    
    def test_basic_set_get(self):
        """Test basic set and get operations."""
        # Mock successful operations
        self.mock_redis_client.setex.return_value = True
        self.mock_redis_client.get.return_value = json.dumps("test_value")
        
        self.assertTrue(self.cache.set("test_key", "test_value"))
        self.assertEqual(self.cache.get("test_key"), "test_value")
    
    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist."""
        self.mock_redis_client.get.return_value = None
        self.assertIsNone(self.cache.get("nonexistent_key"))
    
    def test_delete_key(self):
        """Test deleting a key."""
        self.mock_redis_client.delete.return_value = 1
        self.assertTrue(self.cache.delete("test_key"))
    
    def test_delete_nonexistent_key(self):
        """Test deleting a key that doesn't exist."""
        self.mock_redis_client.delete.return_value = 0
        self.assertFalse(self.cache.delete("nonexistent_key"))
    
    def test_exists_key(self):
        """Test checking if a key exists."""
        self.mock_redis_client.exists.return_value = 1
        self.assertTrue(self.cache.exists("test_key"))
        
        self.mock_redis_client.exists.return_value = 0
        self.assertFalse(self.cache.exists("nonexistent_key"))
    
    def test_clear_cache(self):
        """Test clearing all cache entries."""
        self.mock_redis_client.flushdb.return_value = True
        self.assertTrue(self.cache.clear())
    
    def test_get_ttl(self):
        """Test getting TTL for a key."""
        self.mock_redis_client.ttl.return_value = 300
        self.assertEqual(self.cache.get_ttl("test_key"), 300)
    
    def test_redis_errors(self):
        """Test handling of Redis errors."""
        # Test get error
        self.mock_redis_client.get.side_effect = Exception("Redis error")
        self.assertIsNone(self.cache.get("test_key"))
        
        # Test set error
        self.mock_redis_client.setex.side_effect = Exception("Redis error")
        self.assertFalse(self.cache.set("test_key", "test_value"))
    
    def test_disconnected_cache(self):
        """Test behavior when Redis is disconnected."""
        with patch('builtins.__import__') as mock_import:
            # Mock the redis module to raise an exception
            def side_effect(name, *args, **kwargs):
                if name == 'redis':
                    raise Exception("Connection failed")
                return __import__(name, *args, **kwargs)
            
            mock_import.side_effect = side_effect
            
            cache = RedisCache()
            self.assertFalse(cache.connected)
            self.assertIsNone(cache.redis_client)
            
            # Test all operations when disconnected
            self.assertIsNone(cache.get("test_key"))
            self.assertFalse(cache.set("test_key", "test_value"))
            self.assertFalse(cache.delete("test_key"))
            self.assertFalse(cache.exists("test_key"))
            self.assertFalse(cache.clear())


class TestCacheManager(unittest.TestCase):
    """Test cases for CacheManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_cache = Mock()
        self.cache_manager = CacheManager(self.mock_cache)
    
    def test_generate_key(self):
        """Test cache key generation."""
        key1 = self.cache_manager._generate_key("query_results", "iPhone", "US")
        key2 = self.cache_manager._generate_key("query_results", "iPhone", "US")
        key3 = self.cache_manager._generate_key("query_results", "iPhone", "UK")
        
        # Same inputs should generate same key
        self.assertEqual(key1, key2)
        # Different inputs should generate different keys
        self.assertNotEqual(key1, key3)
        # Keys should start with prefix
        self.assertTrue(key1.startswith("priceiq:"))
    
    def test_cache_query_results(self):
        """Test caching query results."""
        results = [{"product": "iPhone", "price": "999"}]
        self.mock_cache.set.return_value = True
        
        success = self.cache_manager.cache_query_results("iPhone", "US", results)
        
        self.assertTrue(success)
        self.mock_cache.set.assert_called_once()
        
        # Verify the cached data structure
        call_args = self.mock_cache.set.call_args
        cached_data = call_args[0][1]  # Second argument is the value
        self.assertIn('results', cached_data)
        self.assertIn('timestamp', cached_data)
        self.assertIn('query', cached_data)
        self.assertIn('country', cached_data)
    
    def test_get_cached_query_results(self):
        """Test retrieving cached query results."""
        cached_data = {
            'results': [{"product": "iPhone", "price": "999"}],
            'timestamp': datetime.now().isoformat(),
            'query': "iPhone",
            'country': "US"
        }
        self.mock_cache.get.return_value = cached_data
        
        results = self.cache_manager.get_cached_query_results("iPhone", "US")
        
        self.assertEqual(results, cached_data['results'])
    
    def test_get_cached_query_results_none(self):
        """Test retrieving non-existent cached query results."""
        self.mock_cache.get.return_value = None
        
        results = self.cache_manager.get_cached_query_results("iPhone", "US")
        
        self.assertIsNone(results)
    
    def test_cache_site_data(self):
        """Test caching site data."""
        site_data = {"sites": ["amazon.com", "bestbuy.com"]}
        self.mock_cache.set.return_value = True
        
        success = self.cache_manager.cache_site_data("amazon.com", "Smartphone", "US", site_data)
        
        self.assertTrue(success)
        self.mock_cache.set.assert_called_once()
    
    def test_get_cached_site_data(self):
        """Test retrieving cached site data."""
        cached_data = {
            'data': {"sites": ["amazon.com", "bestbuy.com"]},
            'timestamp': datetime.now().isoformat(),
            'site': "amazon.com",
            'category': "Smartphone",
            'country': "US"
        }
        self.mock_cache.get.return_value = cached_data
        
        data = self.cache_manager.get_cached_site_data("amazon.com", "Smartphone", "US")
        
        self.assertEqual(data, cached_data['data'])
    
    def test_cache_product_data(self):
        """Test caching product data."""
        product_data = {"name": "iPhone", "price": "999"}
        self.mock_cache.set.return_value = True
        
        success = self.cache_manager.cache_product_data("https://amazon.com/iphone", product_data)
        
        self.assertTrue(success)
        self.mock_cache.set.assert_called_once()
    
    def test_get_cached_product_data(self):
        """Test retrieving cached product data."""
        cached_data = {
            'product_data': {"name": "iPhone", "price": "999"},
            'timestamp': datetime.now().isoformat(),
            'url': "https://amazon.com/iphone"
        }
        self.mock_cache.get.return_value = cached_data
        
        data = self.cache_manager.get_cached_product_data("https://amazon.com/iphone")
        
        self.assertEqual(data, cached_data['product_data'])
    
    def test_cache_search_results(self):
        """Test caching search results."""
        search_results = ["https://amazon.com/iphone1", "https://amazon.com/iphone2"]
        self.mock_cache.set.return_value = True
        
        success = self.cache_manager.cache_search_results("iPhone", "amazon.com", search_results)
        
        self.assertTrue(success)
        self.mock_cache.set.assert_called_once()
    
    def test_get_cached_search_results(self):
        """Test retrieving cached search results."""
        cached_data = {
            'results': ["https://amazon.com/iphone1", "https://amazon.com/iphone2"],
            'timestamp': datetime.now().isoformat(),
            'query': "iPhone",
            'site': "amazon.com"
        }
        self.mock_cache.get.return_value = cached_data
        
        results = self.cache_manager.get_cached_search_results("iPhone", "amazon.com")
        
        self.assertEqual(results, cached_data['results'])
    
    def test_invalidate_query_cache(self):
        """Test invalidating query cache."""
        self.mock_cache.delete.return_value = True
        
        success = self.cache_manager.invalidate_query_cache("iPhone", "US")
        
        self.assertTrue(success)
        self.mock_cache.delete.assert_called_once()
    
    def test_invalidate_site_cache(self):
        """Test invalidating site cache."""
        self.mock_cache.delete.return_value = True
        
        success = self.cache_manager.invalidate_site_cache("amazon.com", "Smartphone", "US")
        
        self.assertTrue(success)
        self.mock_cache.delete.assert_called_once()
    
    def test_get_cache_stats_mock(self):
        """Test getting cache stats for mock cache."""
        mock_cache = MockCache()
        cache_manager = CacheManager(mock_cache)
        
        stats = cache_manager.get_cache_stats()
        
        self.assertEqual(stats['type'], 'mock')
        self.assertTrue(stats['connected'])
        self.assertIn('entries', stats)
    
    def test_get_cache_stats_redis_connected(self):
        """Test getting cache stats for connected Redis cache."""
        with patch('builtins.__import__') as mock_import:
            # Mock the redis module
            mock_redis_module = Mock()
            mock_client = Mock()
            mock_redis_module.Redis.return_value = mock_client
            mock_client.ping.return_value = True
            mock_client.info.return_value = {
                'used_memory_human': '1.0M',
                'connected_clients': 5,
                'total_commands_processed': 1000
            }
            
            # Make __import__ return our mock when 'redis' is requested
            def side_effect(name, *args, **kwargs):
                if name == 'redis':
                    return mock_redis_module
                return __import__(name, *args, **kwargs)
            
            mock_import.side_effect = side_effect
            
            redis_cache = RedisCache()
            cache_manager = CacheManager(redis_cache)
            
            stats = cache_manager.get_cache_stats()
            
            self.assertEqual(stats['type'], 'redis')
            self.assertTrue(stats['connected'])
            self.assertIn('used_memory', stats)
    
    def test_get_cache_stats_redis_disconnected(self):
        """Test getting cache stats for disconnected Redis cache."""
        with patch('builtins.__import__') as mock_import:
            # Mock the redis module to raise an exception
            def side_effect(name, *args, **kwargs):
                if name == 'redis':
                    raise Exception("Connection failed")
                return __import__(name, *args, **kwargs)
            
            mock_import.side_effect = side_effect
            
            redis_cache = RedisCache()
            cache_manager = CacheManager(redis_cache)
            
            stats = cache_manager.get_cache_stats()
            
            self.assertEqual(stats['type'], 'redis')
            self.assertFalse(stats['connected'])


class TestCreateCacheManager(unittest.TestCase):
    """Test cases for create_cache_manager factory function."""
    
    def test_create_mock_cache_manager(self):
        """Test creating mock cache manager."""
        config = {
            'modules': {
                'cache': {
                    'use_mock': True,
                    'ttl_default': 1800
                }
            }
        }
        
        cache_manager = create_cache_manager(config)
        
        self.assertIsInstance(cache_manager, CacheManager)
        self.assertIsInstance(cache_manager.cache, MockCache)
        self.assertEqual(cache_manager.cache.ttl_default, 1800)
    
    def test_create_redis_cache_manager(self):
        """Test creating Redis cache manager."""
        config = {
            'modules': {
                'cache': {
                    'use_mock': False,
                    'redis': {
                        'host': 'localhost',
                        'port': 6379,
                        'db': 0,
                        'password': None,
                        'ttl_default': 3600
                    }
                }
            }
        }
        
        with patch('builtins.__import__') as mock_import:
            # Mock the redis module
            mock_redis_module = Mock()
            mock_client = Mock()
            mock_redis_module.Redis.return_value = mock_client
            mock_client.ping.return_value = True
            
            # Make __import__ return our mock when 'redis' is requested
            def side_effect(name, *args, **kwargs):
                if name == 'redis':
                    return mock_redis_module
                return __import__(name, *args, **kwargs)
            
            mock_import.side_effect = side_effect
            
            cache_manager = create_cache_manager(config)
            
            self.assertIsInstance(cache_manager, CacheManager)
            self.assertIsInstance(cache_manager.cache, RedisCache)
    
    def test_create_cache_manager_default_config(self):
        """Test creating cache manager with default config."""
        config = {}
        
        cache_manager = create_cache_manager(config)
        
        self.assertIsInstance(cache_manager, CacheManager)
        self.assertIsInstance(cache_manager.cache, MockCache)


class TestCacheIntegration(unittest.TestCase):
    """Integration tests for the caching system."""
    
    def test_end_to_end_caching_flow(self):
        """Test complete caching flow with mock cache."""
        cache_manager = CacheManager(MockCache())
        
        # Cache query results
        results = [{"product": "iPhone", "price": "999"}]
        self.assertTrue(cache_manager.cache_query_results("iPhone", "US", results))
        
        # Retrieve cached results
        cached_results = cache_manager.get_cached_query_results("iPhone", "US")
        self.assertEqual(cached_results, results)
        
        # Invalidate cache
        self.assertTrue(cache_manager.invalidate_query_cache("iPhone", "US"))
        
        # Verify cache is cleared
        self.assertIsNone(cache_manager.get_cached_query_results("iPhone", "US"))
    
    def test_cache_performance(self):
        """Test cache performance with multiple operations."""
        cache_manager = CacheManager(MockCache())
        
        # Cache multiple items
        start_time = time.time()
        
        for i in range(100):
            cache_manager.cache_query_results(f"query_{i}", "US", [{"id": i}])
        
        cache_time = time.time() - start_time
        
        # Retrieve multiple items
        start_time = time.time()
        
        for i in range(100):
            cache_manager.get_cached_query_results(f"query_{i}", "US")
        
        retrieve_time = time.time() - start_time
        
        # Performance should be reasonable
        self.assertLess(cache_time, 1.0)  # Less than 1 second for 100 operations
        self.assertLess(retrieve_time, 1.0)  # Less than 1 second for 100 operations
    
    def test_cache_ttl_integration(self):
        """Test TTL integration with cache manager."""
        cache_manager = CacheManager(MockCache(ttl_default=1))
        
        # Cache with short TTL
        results = [{"product": "iPhone", "price": "999"}]
        cache_manager.cache_query_results("iPhone", "US", results, ttl=1)
        
        # Should be available immediately
        self.assertEqual(cache_manager.get_cached_query_results("iPhone", "US"), results)
        
        # Wait for expiration
        time.sleep(1.1)
        
        # Should be expired
        self.assertIsNone(cache_manager.get_cached_query_results("iPhone", "US"))


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2) 