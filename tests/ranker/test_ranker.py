"""
Test file for Ranker Module
Tests ranking functionality with mock configuration and asserts output ranking correctness.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.ranker.interface import Ranker


def test_ranker_mock_config():
    """Test the ranker with mock configuration."""
    print("Testing Ranker Module - Mock Config")
    print("=" * 40)
    
    # Initialize ranker
    config_path = "config/phase1_config.yaml"
    ranker = Ranker(config_path)
    
    # Test input from config
    input_products = [
        {
            "productName": "Apple iPhone 16 Pro 128GB",
            "price": "999",
            "currency": "USD",
            "link": "https://apple.com/iphone16pro"
        },
        {
            "productName": "Apple iPhone 16 Pro 128GB - Silver",
            "price": "979",
            "currency": "USD",
            "link": "https://bestbuy.com/iphone16pro"
        },
        {
            "productName": "Apple iPhone 16 Pro 128GB - Natural Titanium",
            "price": "999",
            "currency": "USD",
            "link": "https://apple.com/iphone16pro"
        },
        {
            "productName": "Apple iPhone 16 Pro 128GB - Space Black",
            "price": "1049",
            "currency": "USD",
            "link": "https://walmart.com/iphone16pro"
        }
    ]
    
    print(f"Input products count: {len(input_products)}")
    for i, product in enumerate(input_products, 1):
        print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
    
    # Perform ranking
    try:
        result = ranker.rank(input_products)
        
        print(f"\nOutput products count: {len(result)}")
        for i, product in enumerate(result, 1):
            print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
        
        # Verify ranking worked correctly
        if len(result) == len(input_products):
            print(f"✅ Ranking successful: {len(input_products)} products ranked")
            
            # Check if first product has lowest price
            first_price = float(result[0]['price'])
            last_price = float(result[-1]['price'])
            if first_price <= last_price:
                print(f"✅ Ranking order correct: {first_price} ≤ {last_price}")
            else:
                print(f"❌ Ranking order incorrect: {first_price} > {last_price}")
        else:
            print(f"❌ Ranking failed: expected {len(input_products)}, got {len(result)}")
            
    except Exception as e:
        print(f"❌ Error during ranking: {e}")


def test_ranker_basic_logic():
    """Test basic ranking logic with custom input."""
    print("\nTesting Basic Ranking Logic")
    print("-" * 30)
    
    config_path = "config/phase1_config.yaml"
    ranker = Ranker(config_path)
    
    # Test with custom input (not in mock config)
    custom_products = [
        {
            "productName": "Samsung Galaxy S24",
            "price": "899",
            "currency": "USD",
            "link": "https://samsung.com/galaxys24"
        },
        {
            "productName": "Samsung Galaxy S24 Ultra",
            "price": "1199",
            "currency": "USD",
            "link": "https://samsung.com/galaxys24ultra"
        },
        {
            "productName": "Samsung Galaxy S24+",
            "price": "999",
            "currency": "USD",
            "link": "https://samsung.com/galaxys24plus"
        }
    ]
    
    print(f"Custom input products count: {len(custom_products)}")
    for i, product in enumerate(custom_products, 1):
        print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
    
    try:
        result = ranker.rank(custom_products)
        
        print(f"\nCustom output products count: {len(result)}")
        for i, product in enumerate(result, 1):
            print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
        
        # Verify basic ranking
        expected_order = ["899", "999", "1199"]
        actual_order = [product['price'] for product in result]
        
        if actual_order == expected_order:
            print(f"✅ Basic ranking correct: {actual_order}")
        else:
            print(f"❌ Basic ranking failed: expected {expected_order}, got {actual_order}")
            
    except Exception as e:
        print(f"❌ Error during basic ranking: {e}")


def test_ranker_real_mode():
    """Test that real mode raises NotImplementedError."""
    print("\nTesting Real Mode (Not Implemented)")
    print("-" * 35)
    
    # Create config with use_mock: false
    config_dict = {
        "modules": {
            "ranker": {
                "use_mock": False,
                "mock_ranked_results": {}
            }
        }
    }
    
    ranker = Ranker(config_dict)
    
    try:
        ranker.rank([
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
            "ranker": {
                "use_mock": True,
                "mock_ranked_results": {
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
    
    ranker = Ranker(config_dict)
    
    try:
        result = ranker.rank([
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
    ranker = Ranker(config_path)
    
    # Test 1: Empty list
    print("\n1. Testing empty list:")
    try:
        result = ranker.rank([])
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
        result = ranker.rank(single_product)
        print(f"   Result: {len(result)} products")
        if len(result) == 1:
            print("   ✅ Single product handled correctly")
        else:
            print("   ❌ Single product not handled correctly")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Invalid prices
    print("\n3. Testing invalid prices:")
    try:
        invalid_prices = [
            {"productName": "Valid", "price": "100", "currency": "USD"},
            {"productName": "Invalid", "price": "abc", "currency": "USD"},
            {"productName": "Missing", "price": "", "currency": "USD"}
        ]
        result = ranker.rank(invalid_prices)
        print(f"   Result: {len(result)} products")
        print(f"   First product: {result[0]['productName']} - {result[0]['price']}")
        if len(result) == 3 and result[0]['productName'] == "Valid":
            print("   ✅ Invalid prices handled correctly")
        else:
            print("   ❌ Invalid prices not handled correctly")
    except Exception as e:
        print(f"   Error: {e}")


def test_different_currencies():
    """Test ranking with different currencies."""
    print("\nTesting Different Currencies")
    print("-" * 30)
    
    config_path = "config/phase1_config.yaml"
    ranker = Ranker(config_path)
    
    # Test products with different currencies
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
        },
        {
            "productName": "Apple iPhone 16 Pro 128GB",
            "price": "899",
            "currency": "EUR",
            "link": "https://amazon.de/iphone16pro"
        }
    ]
    
    print(f"Mixed currency products count: {len(mixed_currency_products)}")
    for i, product in enumerate(mixed_currency_products, 1):
        print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
    
    try:
        result = ranker.rank(mixed_currency_products)
        
        print(f"\nMixed currency result count: {len(result)}")
        for i, product in enumerate(result, 1):
            print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
        
        # Should rank by raw price values (not currency-converted)
        expected_order = ["899", "999", "89999"]
        actual_order = [product['price'] for product in result]
        
        if actual_order == expected_order:
            print("✅ Different currencies ranked correctly by raw price")
        else:
            print(f"❌ Different currencies not ranked correctly: expected {expected_order}, got {actual_order}")
            
    except Exception as e:
        print(f"❌ Error testing different currencies: {e}")


def test_ranking_order():
    """Test that ranking maintains correct order."""
    print("\nTesting Ranking Order")
    print("-" * 20)
    
    config_path = "config/phase1_config.yaml"
    ranker = Ranker(config_path)
    
    # Test with known price order
    test_products = [
        {
            "productName": "Product C",
            "price": "300",
            "currency": "USD",
            "link": "https://example.com/c"
        },
        {
            "productName": "Product A",
            "price": "100",
            "currency": "USD",
            "link": "https://example.com/a"
        },
        {
            "productName": "Product B",
            "price": "200",
            "currency": "USD",
            "link": "https://example.com/b"
        }
    ]
    
    print("Input order:")
    for i, product in enumerate(test_products, 1):
        print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
    
    try:
        result = ranker.rank(test_products)
        
        print("\nOutput order:")
        for i, product in enumerate(result, 1):
            print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
        
        # Verify ascending price order
        prices = [float(product['price']) for product in result]
        is_ascending = all(prices[i] <= prices[i+1] for i in range(len(prices)-1))
        
        if is_ascending:
            print("✅ Ranking order correct (ascending prices)")
        else:
            print("❌ Ranking order incorrect")
            
    except Exception as e:
        print(f"❌ Error testing ranking order: {e}")


def test_duplicate_prices():
    """Test ranking with duplicate prices."""
    print("\nTesting Duplicate Prices")
    print("-" * 25)
    
    config_path = "config/phase1_config.yaml"
    ranker = Ranker(config_path)
    
    # Test products with same prices
    duplicate_price_products = [
        {
            "productName": "Product A",
            "price": "100",
            "currency": "USD",
            "link": "https://example.com/a"
        },
        {
            "productName": "Product B",
            "price": "100",
            "currency": "USD",
            "link": "https://example.com/b"
        },
        {
            "productName": "Product C",
            "price": "200",
            "currency": "USD",
            "link": "https://example.com/c"
        }
    ]
    
    print(f"Duplicate price products count: {len(duplicate_price_products)}")
    for i, product in enumerate(duplicate_price_products, 1):
        print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
    
    try:
        result = ranker.rank(duplicate_price_products)
        
        print(f"\nDuplicate price result count: {len(result)}")
        for i, product in enumerate(result, 1):
            print(f"  {i}. {product['productName']} - {product['price']} {product['currency']}")
        
        # Should maintain order for same prices
        prices = [product['price'] for product in result]
        if prices == ["100", "100", "200"]:
            print("✅ Duplicate prices handled correctly")
        else:
            print(f"❌ Duplicate prices not handled correctly: {prices}")
            
    except Exception as e:
        print(f"❌ Error testing duplicate prices: {e}")


if __name__ == "__main__":
    test_ranker_mock_config()
    test_ranker_basic_logic()
    test_ranker_real_mode()
    test_config_loading()
    test_edge_cases()
    test_different_currencies()
    test_ranking_order()
    test_duplicate_prices() 