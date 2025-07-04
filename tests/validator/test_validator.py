"""
Test file for Validator Module
Tests validation functionality with mock cases from configuration and asserts correctness.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.validator.interface import Validator


def test_validator_mock_cases():
    """Test the validator with mock cases from configuration."""
    print("Testing Validator Module - Mock Cases")
    print("=" * 40)
    
    # Initialize validator
    config_path = "config/phase1_config.yaml"
    validator = Validator(config_path)
    
    # Test cases from config
    test_cases = [
        {
            "name": "Valid iPhone 16 Pro 128GB",
            "query": {
                "brand": "Apple",
                "model": "iPhone 16 Pro",
                "storage": "128GB",
                "category": "Smartphone"
            },
            "product": {
                "productName": "Apple iPhone 16 Pro 128GB",
                "price": "999",
                "currency": "USD",
                "link": "https://amazon.com/iphone16pro"
            },
            "expected": True
        },
        {
            "name": "Valid iPhone 16 Pro Silver",
            "query": {
                "brand": "Apple",
                "model": "iPhone 16 Pro",
                "storage": "128GB",
                "category": "Smartphone"
            },
            "product": {
                "productName": "Apple iPhone 16 Pro 128GB - Silver",
                "price": "979",
                "currency": "USD",
                "link": "https://bestbuy.com/iphone16pro"
            },
            "expected": True
        },
        {
            "name": "Invalid iPhone 16 Mini",
            "query": {
                "brand": "Apple",
                "model": "iPhone 16 Pro",
                "storage": "128GB",
                "category": "Smartphone"
            },
            "product": {
                "productName": "Apple iPhone 16 Mini",
                "price": "899",
                "currency": "USD",
                "link": "https://example.com/iphone16mini"
            },
            "expected": False
        },
        {
            "name": "Invalid Samsung Galaxy",
            "query": {
                "brand": "Apple",
                "model": "iPhone 16 Pro",
                "storage": "128GB",
                "category": "Smartphone"
            },
            "product": {
                "productName": "Samsung Galaxy S24",
                "price": "999",
                "currency": "USD",
                "link": "https://example.com/galaxys24"
            },
            "expected": False
        },
        {
            "name": "Invalid iPhone 16 Pro 256GB",
            "query": {
                "brand": "Apple",
                "model": "iPhone 16 Pro",
                "storage": "128GB",
                "category": "Smartphone"
            },
            "product": {
                "productName": "Apple iPhone 16 Pro 256GB",
                "price": "1099",
                "currency": "USD",
                "link": "https://example.com/iphone16pro256"
            },
            "expected": False
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        try:
            result = validator.validate(test_case['query'], test_case['product'])
            expected = test_case['expected']
            
            if result == expected:
                print(f"✅ Validation correct: {result}")
            else:
                print(f"❌ Validation failed: expected {expected}, got {result}")
                
        except Exception as e:
            print(f"❌ Error during validation: {e}")


def test_validator_partial_matching():
    """Test partial matching logic when exact match not found."""
    print("\nTesting Partial Matching")
    print("-" * 25)
    
    config_path = "config/phase1_config.yaml"
    validator = Validator(config_path)
    
    # Test cases for partial matching
    partial_test_cases = [
        {
            "name": "Valid partial match - brand and model",
            "query": {
                "brand": "Apple",
                "model": "iPhone 16 Pro",
                "storage": "128GB",
                "category": "Smartphone"
            },
            "product": {
                "productName": "Apple iPhone 16 Pro 128GB - Natural Titanium",
                "price": "999",
                "currency": "USD",
                "link": "https://apple.com/iphone16pro"
            },
            "expected": True
        },
        {
            "name": "Invalid partial match - wrong brand",
            "query": {
                "brand": "Apple",
                "model": "iPhone 16 Pro",
                "storage": "128GB",
                "category": "Smartphone"
            },
            "product": {
                "productName": "Samsung Galaxy S24 Ultra",
                "price": "999",
                "currency": "USD",
                "link": "https://samsung.com/galaxys24"
            },
            "expected": False
        },
        {
            "name": "Invalid partial match - wrong model",
            "query": {
                "brand": "Apple",
                "model": "iPhone 16 Pro",
                "storage": "128GB",
                "category": "Smartphone"
            },
            "product": {
                "productName": "Apple iPhone 16 Mini 128GB",
                "price": "899",
                "currency": "USD",
                "link": "https://apple.com/iphone16mini"
            },
            "expected": False
        },
        {
            "name": "Invalid partial match - wrong storage",
            "query": {
                "brand": "Apple",
                "model": "iPhone 16 Pro",
                "storage": "128GB",
                "category": "Smartphone"
            },
            "product": {
                "productName": "Apple iPhone 16 Pro 256GB",
                "price": "1099",
                "currency": "USD",
                "link": "https://apple.com/iphone16pro256"
            },
            "expected": False
        },
        {
            "name": "Invalid partial match - zero price",
            "query": {
                "brand": "Apple",
                "model": "iPhone 16 Pro",
                "storage": "128GB",
                "category": "Smartphone"
            },
            "product": {
                "productName": "Apple iPhone 16 Pro 128GB",
                "price": "0",
                "currency": "USD",
                "link": "https://example.com/iphone16pro"
            },
            "expected": False
        }
    ]
    
    for test_case in partial_test_cases:
        print(f"\nTesting: {test_case['name']}")
        try:
            result = validator.validate(test_case['query'], test_case['product'])
            expected = test_case['expected']
            
            if result == expected:
                print(f"✅ Partial match correct: {result}")
            else:
                print(f"❌ Partial match failed: expected {expected}, got {result}")
                
        except Exception as e:
            print(f"❌ Error during partial matching: {e}")


def test_validator_real_mode():
    """Test that real mode raises NotImplementedError."""
    print("\nTesting Real Mode (Not Implemented)")
    print("-" * 35)
    
    # Create config with use_mock: false
    config_dict = {
        "modules": {
            "validator": {
                "use_mock": False,
                "mock_validations": []
            }
        }
    }
    
    validator = Validator(config_dict)
    
    try:
        validator.validate(
            {"brand": "Apple", "model": "iPhone"},
            {"productName": "Apple iPhone", "price": "999"}
        )
        print("❌ Should have raised NotImplementedError")
    except NotImplementedError as e:
        print(f"✅ Correctly raised NotImplementedError: {e}")


def test_config_loading():
    """Test config loading functionality."""
    print("\nTesting Config Loading")
    print("-" * 20)
    
    # Test with config dict
    config_dict = {
        "modules": {
            "validator": {
                "use_mock": True,
                "mock_validations": [
                    {
                        "query": {"brand": "Test", "model": "Product"},
                        "product": {"productName": "Test Product", "price": "100"},
                        "is_valid": True
                    }
                ]
            }
        }
    }
    
    validator = Validator(config_dict)
    
    try:
        result = validator.validate(
            {"brand": "Test", "model": "Product"},
            {"productName": "Test Product", "price": "100"}
        )
        
        if result == True:
            print("✅ Dict config loading PASS")
        else:
            print("❌ Dict config loading FAIL")
    except Exception as e:
        print(f"❌ Dict config loading FAIL: {e}")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("\nTesting Edge Cases")
    print("-" * 20)
    
    config_path = "config/phase1_config.yaml"
    validator = Validator(config_path)
    
    # Test 1: Empty query
    print("\n1. Testing empty query:")
    try:
        result = validator.validate({}, {"productName": "Test", "price": "100"})
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Empty product
    print("\n2. Testing empty product:")
    try:
        result = validator.validate({"brand": "Test"}, {})
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Invalid price format
    print("\n3. Testing invalid price format:")
    try:
        result = validator.validate(
            {"brand": "Apple", "model": "iPhone"},
            {"productName": "Apple iPhone", "price": "invalid"}
        )
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Error: {e}")


def test_case_sensitivity():
    """Test case sensitivity in partial matching."""
    print("\nTesting Case Sensitivity")
    print("-" * 25)
    
    config_path = "config/phase1_config.yaml"
    validator = Validator(config_path)
    
    # Test case insensitive matching
    test_cases = [
        {
            "name": "Lowercase brand and model",
            "query": {
                "brand": "apple",
                "model": "iphone 16 pro",
                "storage": "128gb",
                "category": "smartphone"
            },
            "product": {
                "productName": "Apple iPhone 16 Pro 128GB",
                "price": "999",
                "currency": "USD",
                "link": "https://example.com/iphone16pro"
            },
            "expected": True
        },
        {
            "name": "Mixed case product name",
            "query": {
                "brand": "Apple",
                "model": "iPhone 16 Pro",
                "storage": "128GB",
                "category": "Smartphone"
            },
            "product": {
                "productName": "APPLE IPHONE 16 PRO 128GB",
                "price": "999",
                "currency": "USD",
                "link": "https://example.com/iphone16pro"
            },
            "expected": True
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        try:
            result = validator.validate(test_case['query'], test_case['product'])
            expected = test_case['expected']
            
            if result == expected:
                print(f"✅ Case sensitivity test passed: {result}")
            else:
                print(f"❌ Case sensitivity test failed: expected {expected}, got {result}")
                
        except Exception as e:
            print(f"❌ Error during case sensitivity test: {e}")


if __name__ == "__main__":
    test_validator_mock_cases()
    test_validator_partial_matching()
    test_validator_real_mode()
    test_config_loading()
    test_edge_cases()
    test_case_sensitivity() 