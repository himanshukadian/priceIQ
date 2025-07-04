"""
Test file for Query Normalizer Module
Tests query normalization functionality with mock configuration.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.query_normalizer.interface import MockQueryNormalizer, RealQueryNormalizer, QueryNormalizer


def test_mock_query_normalizer():
    """Test the mock query normalizer with sample data."""
    normalizer = MockQueryNormalizer("mocks/normalized_queries.yaml")
    
    # Test with known query
    result = normalizer.normalize_query("iPhone 16 Pro, 128GB", "US")
    print("Mock Query Normalizer Test:")
    print(f"Input: iPhone 16 Pro, 128GB")
    print(f"Output: {result}")
    print()
    
    # Test with unknown query
    result2 = normalizer.normalize_query("Unknown Product", "US")
    print(f"Input: Unknown Product")
    print(f"Output: {result2}")
    print()


def test_real_query_normalizer():
    """Test the real query normalizer."""
    normalizer = RealQueryNormalizer()
    
    result = normalizer.normalize_query("iPhone 16 Pro, 128GB", "US")
    print("Real Query Normalizer Test:")
    print(f"Input: iPhone 16 Pro, 128GB")
    print(f"Output: {result}")
    print()


if __name__ == "__main__":
    test_mock_query_normalizer()
    test_real_query_normalizer() 