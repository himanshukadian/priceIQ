"""
Test file for Extractor Module
Tests extraction functionality with mock data and validates output structure.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.extractor.interface import Extractor


def test_extractor_mock_mode():
    """Test the extractor in mock mode with known URLs."""
    print("Testing Extractor Module - Mock Mode")
    print("=" * 40)
    
    # Initialize extractor
    config_path = "config/phase1_config.yaml"
    extractor = Extractor(config_path)
    
    # Test cases with known URLs
    test_cases = [
        {
            "name": "Amazon iPhone",
            "url": "https://amazon.com/iphone16pro",
            "html": "<html><body><h1>Apple iPhone 16 Pro</h1><span>$999.00</span></body></html>",
            "expected": {
                "productName": "Apple iPhone 16 Pro 128GB",
                "price": "999",
                "currency": "USD",
                "link": "https://amazon.com/iphone16pro"
            }
        },
        {
            "name": "Best Buy iPhone",
            "url": "https://bestbuy.com/iphone16pro",
            "html": "<html><body><h1>Apple iPhone 16 Pro</h1><span>$979.00</span></body></html>",
            "expected": {
                "productName": "Apple iPhone 16 Pro 128GB - Silver",
                "price": "979",
                "currency": "USD",
                "link": "https://bestbuy.com/iphone16pro"
            }
        },
        {
            "name": "Apple Store iPhone",
            "url": "https://apple.com/iphone16pro",
            "html": "<html><body><h1>Apple iPhone 16 Pro</h1><span>$999.00</span></body></html>",
            "expected": {
                "productName": "Apple iPhone 16 Pro 128GB - Natural Titanium",
                "price": "999",
                "currency": "USD",
                "link": "https://apple.com/iphone16pro"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        try:
            result = extractor.extract(test_case['html'], test_case['url'])
            
            # Verify result structure
            expected = test_case['expected']
            if result == expected:
                print(f"✅ Extraction successful")
                print(f"   Product: {result['productName']}")
                print(f"   Price: {result['price']} {result['currency']}")
                print(f"   Link: {result['link']}")
            else:
                print(f"❌ Extraction failed")
                print(f"   Expected: {expected}")
                print(f"   Got: {result}")
                
        except Exception as e:
            print(f"❌ Error during extraction: {e}")


def test_extractor_unknown_url():
    """Test behavior with unknown URLs."""
    print("\nTesting Unknown URL Handling")
    print("-" * 30)
    
    config_path = "config/phase1_config.yaml"
    extractor = Extractor(config_path)
    
    # Test with unknown URL
    unknown_url = "https://unknown-site.com/product"
    html = "<html><body><h1>Some Product</h1></body></html>"
    
    try:
        result = extractor.extract(html, unknown_url)
        
        # Should return default structure
        expected_default = {
            "productName": "Unknown Product",
            "price": "0",
            "currency": "USD",
            "link": unknown_url
        }
        
        if result == expected_default:
            print(f"✅ Unknown URL handled correctly")
            print(f"   Default result: {result}")
        else:
            print(f"❌ Unexpected result for unknown URL")
            print(f"   Expected: {expected_default}")
            print(f"   Got: {result}")
            
    except Exception as e:
        print(f"❌ Error handling unknown URL: {e}")


def test_extractor_real_mode():
    """Test that real mode raises NotImplementedError."""
    print("\nTesting Real Mode (Not Implemented)")
    print("-" * 35)
    
    # Create config with use_mock: false
    config_dict = {
        "modules": {
            "extractor": {
                "use_mock": False,
                "mock_extracts": {}
            }
        }
    }
    
    extractor = Extractor(config_dict)
    
    try:
        extractor.extract("<html></html>", "https://test.com")
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
            "extractor": {
                "use_mock": True,
                "mock_extracts": {
                    "https://test.com/product": {
                        "productName": "Test Product",
                        "price": "100",
                        "currency": "USD",
                        "link": "https://test.com/product"
                    }
                }
            }
        }
    }
    
    extractor = Extractor(config_dict)
    
    try:
        result = extractor.extract("<html></html>", "https://test.com/product")
        expected = {
            "productName": "Test Product",
            "price": "100",
            "currency": "USD",
            "link": "https://test.com/product"
        }
        
        if result == expected:
            print("✅ Dict config loading PASS")
        else:
            print("❌ Dict config loading FAIL")
    except Exception as e:
        print(f"❌ Dict config loading FAIL: {e}")


def test_output_structure():
    """Test that output has correct structure."""
    print("\nTesting Output Structure")
    print("-" * 25)
    
    config_path = "config/phase1_config.yaml"
    extractor = Extractor(config_path)
    
    url = "https://amazon.com/iphone16pro"
    html = "<html><body><h1>Test</h1></body></html>"
    
    try:
        result = extractor.extract(html, url)
        
        # Check required fields
        required_fields = ["productName", "price", "currency", "link"]
        missing_fields = [field for field in required_fields if field not in result]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
        else:
            print("✅ All required fields present")
            
        # Check field types
        type_checks = [
            ("productName", str),
            ("price", str),
            ("currency", str),
            ("link", str)
        ]
        
        print("Field Type Checks:")
        for field, expected_type in type_checks:
            if isinstance(result[field], expected_type):
                print(f"  ✅ {field}: {type(result[field]).__name__}")
            else:
                print(f"  ❌ {field}: expected {expected_type.__name__}, got {type(result[field]).__name__}")
                
    except Exception as e:
        print(f"❌ Error testing output structure: {e}")


def test_multiple_currencies():
    """Test extraction with different currencies."""
    print("\nTesting Multiple Currencies")
    print("-" * 25)
    
    config_path = "config/phase1_config.yaml"
    extractor = Extractor(config_path)
    
    # Test INR currency
    inr_url = "https://flipkart.com/iphone16pro"
    html = "<html><body><h1>iPhone</h1></body></html>"
    
    try:
        result = extractor.extract(html, inr_url)
        
        if result["currency"] == "INR" and result["price"] == "89999":
            print(f"✅ INR currency extraction successful")
            print(f"   Price: {result['price']} {result['currency']}")
        else:
            print(f"❌ INR currency extraction failed")
            print(f"   Expected: 89999 INR")
            print(f"   Got: {result['price']} {result['currency']}")
            
    except Exception as e:
        print(f"❌ Error testing INR currency: {e}")


if __name__ == "__main__":
    test_extractor_mock_mode()
    test_extractor_unknown_url()
    test_extractor_real_mode()
    test_config_loading()
    test_output_structure()
    test_multiple_currencies() 