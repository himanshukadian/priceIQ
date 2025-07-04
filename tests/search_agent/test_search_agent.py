"""
Test file for Search Agent Module
Tests search functionality with mock configuration and verifies result structure.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.search_agent.interface import SearchAgent


def test_search_agent():
    """Test the search agent with mock configuration."""
    print("Testing Search Agent Module")
    print("=" * 40)
    
    # Initialize search agent
    config_path = "config/phase1_config.yaml"
    agent = SearchAgent(config_path)
    
    # Test query structure (from QueryNormalizer)
    query_struct = {
        "brand": "Apple",
        "model": "iPhone 16 Pro",
        "storage": "128GB",
        "category": "Smartphone"
    }
    
    # Test sites list (from SiteSelector)
    sites = ["amazon.com", "bestbuy.com", "apple.com"]
    
    print(f"Query: {query_struct}")
    print(f"Sites: {sites}")
    print()
    
    # Perform search
    results = agent.search(query_struct, sites)
    
    print("Search Results:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Site: {result['site']}")
        print(f"     URL: {result['url']}")
        print(f"     HTML File: {result['html_file']}")
        print()
    
    # Verify result structure
    print("Structure Validation:")
    for result in results:
        required_keys = ["site", "url", "html_file"]
        missing_keys = [key for key in required_keys if key not in result]
        
        if missing_keys:
            print(f"❌ Missing keys in result: {missing_keys}")
        else:
            print(f"✅ Result structure valid for {result['site']}")
    
    print("\n" + "=" * 40)
    print("Search Agent tests completed!")


def test_config_loading():
    """Test config loading functionality."""
    print("\nTesting Config Loading")
    print("-" * 20)
    
    # Test with config dict
    config_dict = {
        "modules": {
            "search_agent": {
                "use_mock": True,
                "mock_results": {
                    "test.com": [
                        {
                            "url": "https://test.com/product",
                            "html_file": "mocks/html/test_product.html"
                        }
                    ]
                }
            }
        }
    }
    
    agent = SearchAgent(config_dict)
    query = {"brand": "Test", "model": "Product"}
    sites = ["test.com"]
    
    results = agent.search(query, sites)
    print(f"Dict config test: {results}")
    
    if results and results[0]["site"] == "test.com":
        print("✅ Config dict loading PASS")
    else:
        print("❌ Config dict loading FAIL")


def test_empty_sites():
    """Test behavior with empty sites list."""
    print("\nTesting Empty Sites List")
    print("-" * 25)
    
    config_path = "config/phase1_config.yaml"
    agent = SearchAgent(config_path)
    
    query = {"brand": "Apple", "model": "iPhone"}
    sites = []
    
    results = agent.search(query, sites)
    print(f"Empty sites result: {results}")
    
    if results == []:
        print("✅ Empty sites handling PASS")
    else:
        print("❌ Empty sites handling FAIL")


def test_unknown_sites():
    """Test behavior with unknown sites."""
    print("\nTesting Unknown Sites")
    print("-" * 20)
    
    config_path = "config/phase1_config.yaml"
    agent = SearchAgent(config_path)
    
    query = {"brand": "Apple", "model": "iPhone"}
    sites = ["unknown-site.com", "another-unknown.com"]
    
    results = agent.search(query, sites)
    print(f"Unknown sites result: {results}")
    
    if results == []:
        print("✅ Unknown sites handling PASS")
    else:
        print("❌ Unknown sites handling FAIL")


if __name__ == "__main__":
    test_search_agent()
    test_config_loading()
    test_empty_sites()
    test_unknown_sites() 