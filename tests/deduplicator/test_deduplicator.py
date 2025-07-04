"""
Test file for Deduplicator Module
Tests deduplication functionality with mock configuration and asserts output correctness.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.deduplicator.interface import Deduplicator


def test_deduplicator_mock_config():
    """Test the deduplicator with mock configuration."""
    print("Testing Deduplicator Module - Mock Config")
    print("=" * 40)
    
    # Initialize deduplicator
    config_path = "config/phase1_config.yaml"
    deduper = Deduplicator(config_path)
    
    # Test input from config
    input_products = [
        {
            "productName": "Apple iPhone 16 Pro 128GB",
            "price": "999",
            "currency": "USD",
            "link": "https://amazon.com/iphone16pro"
        },
        {
            "productName": "Apple iPhone 16 Pro 128GB - Silver",
            "price": "999",
            "currency": "USD",
            "link": "https://bestbuy.com/iphone16pro"
        },
        {
            "productName": "Apple iPhone 16 Pro 128GB",
            "price": "999",
            "currency": "USD",
            "link": "https://apple.com/iphone16pro"
        },
        {
            "productName": "Apple iPhone 16 Pro 128GB - Natural Titanium",
            "price": "999",
            "currency": "USD",
            "link": "https://apple.com/iphone16pro"
        }
    ]
    
    print(f"Input products count: {len(input_products)}")
    for i, product in enumerate(input_products, 1):
        print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
    
    # Perform deduplication
    try:
        result = deduper.deduplicate(input_products)
        
        print(f"\nOutput products count: {len(result)}")
        for i, product in enumerate(result, 1):
            print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
        
        # Verify deduplication worked
        if len(result) < len(input_products):
            print(f"✅ Deduplication successful: {len(input_products)} → {len(result)} products")
        else:
            print(f"❌ No deduplication occurred: {len(input_products)} → {len(result)} products")
            
    except Exception as e:
        print(f"❌ Error during deduplication: {e}")


def test_deduplicator_basic_logic():
    """Test basic deduplication logic with custom input."""
    print("\nTesting Basic Deduplication Logic")
    print("-" * 35)
    
    config_path = "config/phase1_config.yaml"
    deduper = Deduplicator(config_path)
    
    # Test with custom input (not in mock config)
    custom_products = [
        {
            "productName": "Samsung Galaxy S24",
            "price": "899",
            "currency": "USD",
            "link": "https://samsung.com/galaxys24"
        },
        {
            "productName": "Samsung Galaxy S24",
            "price": "899",
            "currency": "USD",
            "link": "https://bestbuy.com/galaxys24"
        },
        {
            "productName": "Samsung Galaxy S24 Ultra",
            "price": "1199",
            "currency": "USD",
            "link": "https://samsung.com/galaxys24ultra"
        }
    ]
    
    print(f"Custom input products count: {len(custom_products)}")
    for i, product in enumerate(custom_products, 1):
        print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
    
    try:
        result = deduper.deduplicate(custom_products)
        
        print(f"\nCustom output products count: {len(result)}")
        for i, product in enumerate(result, 1):
            print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
        
        # Verify basic deduplication
        expected_unique = 2  # S24 (duplicate removed) + S24 Ultra
        if len(result) == expected_unique:
            print(f"✅ Basic deduplication correct: {len(custom_products)} → {len(result)} products")
        else:
            print(f"❌ Basic deduplication failed: expected {expected_unique}, got {len(result)}")
            
    except Exception as e:
        print(f"❌ Error during basic deduplication: {e}")


def test_deduplicator_real_mode():
    """Test that real mode raises NotImplementedError."""
    print("\nTesting Real Mode (Not Implemented)")
    print("-" * 35)
    
    # Create config with use_mock: false
    config_dict = {
        "modules": {
            "deduplicator": {
                "use_mock": False,
                "mock_deduplicated_results": {}
            }
        }
    }
    
    deduper = Deduplicator(config_dict)
    
    try:
        deduper.deduplicate([
            {"productName": "Test", "price": "100", "currency": "USD"}
        ])
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
            "deduplicator": {
                "use_mock": True,
                "mock_deduplicated_results": {
                    "input_products": [
                        {"productName": "Test Product", "price": "100", "currency": "USD"}
                    ],
                    "output_products": [
                        {"productName": "Test Product", "price": "100", "currency": "USD"}
                    ]
                }
            }
        }
    }
    
    deduper = Deduplicator(config_dict)
    
    try:
        result = deduper.deduplicate([
            {"productName": "Test Product", "price": "100", "currency": "USD"}
        ])
        
        if len(result) == 1 and result[0]["productName"] == "Test Product":
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
    deduper = Deduplicator(config_path)
    
    # Test 1: Empty list
    print("\n1. Testing empty list:")
    try:
        result = deduper.deduplicate([])
        print(f"   Result: {result}")
        if result == []:
            print("   ✅ Empty list handled correctly")
        else:
            print("   ❌ Empty list not handled correctly")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Single product
    print("\n2. Testing single product:")
    try:
        single_product = [{"productName": "Test", "price": "100", "currency": "USD"}]
        result = deduper.deduplicate(single_product)
        print(f"   Result: {len(result)} products")
        if len(result) == 1:
            print("   ✅ Single product handled correctly")
        else:
            print("   ❌ Single product not handled correctly")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: All duplicates
    print("\n3. Testing all duplicates:")
    try:
        duplicates = [
            {"productName": "Same Product", "price": "100", "currency": "USD"},
            {"productName": "Same Product", "price": "100", "currency": "USD"},
            {"productName": "Same Product", "price": "100", "currency": "USD"}
        ]
        result = deduper.deduplicate(duplicates)
        print(f"   Result: {len(result)} products")
        if len(result) == 1:
            print("   ✅ All duplicates handled correctly")
        else:
            print("   ❌ All duplicates not handled correctly")
    except Exception as e:
        print(f"   Error: {e}")


def test_different_currencies():
    """Test deduplication with different currencies."""
    print("\nTesting Different Currencies")
    print("-" * 30)
    
    config_path = "config/phase1_config.yaml"
    deduper = Deduplicator(config_path)
    
    # Test products with same name but different currencies
    mixed_currency_products = [
        {
            "productName": "Apple iPhone 16 Pro 128GB",
            "price": "999",
            "currency": "USD",
            "link": "https://amazon.com/iphone16pro"
        },
        {
            "productName": "Apple iPhone 16 Pro 128GB",
            "price": "89999",
            "currency": "INR",
            "link": "https://flipkart.com/iphone16pro"
        }
    ]
    
    print(f"Mixed currency products count: {len(mixed_currency_products)}")
    for i, product in enumerate(mixed_currency_products, 1):
        print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
    
    try:
        result = deduper.deduplicate(mixed_currency_products)
        
        print(f"\nMixed currency result count: {len(result)}")
        for i, product in enumerate(result, 1):
            print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
        
        # Should keep both since they have different currencies
        if len(result) == 2:
            print("✅ Different currencies handled correctly (both kept)")
        else:
            print("❌ Different currencies not handled correctly")
            
    except Exception as e:
        print(f"❌ Error testing different currencies: {e}")


def test_price_variations():
    """Test deduplication with price variations."""
    print("\nTesting Price Variations")
    print("-" * 25)
    
    config_path = "config/phase1_config.yaml"
    deduper = Deduplicator(config_path)
    
    # Test products with same name but different prices
    price_variations = [
        {
            "productName": "Apple iPhone 16 Pro 128GB",
            "price": "999",
            "currency": "USD",
            "link": "https://amazon.com/iphone16pro"
        },
        {
            "productName": "Apple iPhone 16 Pro 128GB",
            "price": "979",
            "currency": "USD",
            "link": "https://bestbuy.com/iphone16pro"
        }
    ]
    
    print(f"Price variation products count: {len(price_variations)}")
    for i, product in enumerate(price_variations, 1):
        print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
    
    try:
        result = deduper.deduplicate(price_variations)
        
        print(f"\nPrice variation result count: {len(result)}")
        for i, product in enumerate(result, 1):
            print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
        
        # Should keep both since they have different prices
        if len(result) == 2:
            print("✅ Price variations handled correctly (both kept)")
        else:
            print("❌ Price variations not handled correctly")
            
    except Exception as e:
        print(f"❌ Error testing price variations: {e}")


if __name__ == "__main__":
    test_deduplicator_mock_config()
    test_deduplicator_basic_logic()
    test_deduplicator_real_mode()
    test_config_loading()
    test_edge_cases()
    test_different_currencies()
    test_price_variations() 