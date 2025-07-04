"""
Test file for Scraper Module
Tests HTML fetching functionality with mock files and validates error handling.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.scraper.interface import Scraper


def test_scraper_mock_mode():
    """Test the scraper in mock mode with existing HTML files."""
    print("Testing Scraper Module - Mock Mode")
    print("=" * 40)
    
    # Initialize scraper
    config_path = "config/phase1_config.yaml"
    scraper = Scraper(config_path)
    
    # Test cases with existing mock files
    test_cases = [
        {
            "name": "Amazon iPhone",
            "url_entry": {
                "url": "https://amazon.com/iphone16pro",
                "html_file": "mocks/html/amazon_iphone16pro.html"
            }
        },
        {
            "name": "Best Buy iPhone",
            "url_entry": {
                "url": "https://bestbuy.com/iphone16pro",
                "html_file": "mocks/html/bestbuy_iphone16pro.html"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        try:
            html_content = scraper.fetch_html(test_case['url_entry'])
            
            # Verify HTML content
            if html_content and len(html_content) > 0:
                print(f"✅ HTML content fetched successfully")
                print(f"   Content length: {len(html_content)} characters")
                print(f"   Contains 'iPhone': {'iPhone' in html_content}")
                print(f"   Contains price: {'$' in html_content}")
            else:
                print("❌ HTML content is empty")
                
        except Exception as e:
            print(f"❌ Error fetching HTML: {e}")


def test_scraper_error_handling():
    """Test error handling for various scenarios."""
    print("\nTesting Error Handling")
    print("-" * 25)
    
    config_path = "config/phase1_config.yaml"
    scraper = Scraper(config_path)
    
    # Test 1: Missing html_file
    print("\n1. Testing missing html_file:")
    try:
        scraper.fetch_html({"url": "https://test.com"})
        print("❌ Should have raised ValueError")
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    
    # Test 2: Non-existent HTML file
    print("\n2. Testing non-existent HTML file:")
    try:
        scraper.fetch_html({
            "url": "https://test.com",
            "html_file": "mocks/html/nonexistent.html"
        })
        print("❌ Should have raised FileNotFoundError")
    except FileNotFoundError as e:
        print(f"✅ Correctly raised FileNotFoundError: {e}")


def test_scraper_real_mode():
    """Test that real mode raises NotImplementedError."""
    print("\nTesting Real Mode (Not Implemented)")
    print("-" * 35)
    
    # Create config with use_mock: false
    config_dict = {
        "modules": {
            "scraper": {
                "use_mock": False
            }
        }
    }
    
    scraper = Scraper(config_dict)
    
    try:
        scraper.fetch_html({
            "url": "https://test.com",
            "html_file": "mocks/html/test.html"
        })
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
            "scraper": {
                "use_mock": True
            }
        }
    }
    
    scraper = Scraper(config_dict)
    
    # Test that it works with dict config
    try:
        html_content = scraper.fetch_html({
            "url": "https://amazon.com/iphone16pro",
            "html_file": "mocks/html/amazon_iphone16pro.html"
        })
        if html_content:
            print("✅ Dict config loading PASS")
        else:
            print("❌ Dict config loading FAIL")
    except Exception as e:
        print(f"❌ Dict config loading FAIL: {e}")


def test_html_content_structure():
    """Test that HTML content has expected structure."""
    print("\nTesting HTML Content Structure")
    print("-" * 30)
    
    config_path = "config/phase1_config.yaml"
    scraper = Scraper(config_path)
    
    url_entry = {
        "url": "https://amazon.com/iphone16pro",
        "html_file": "mocks/html/amazon_iphone16pro.html"
    }
    
    try:
        html_content = scraper.fetch_html(url_entry)
        
        # Check for expected HTML elements
        checks = [
            ("DOCTYPE", "DOCTYPE" in html_content),
            ("html tag", "<html" in html_content),
            ("body tag", "<body" in html_content),
            ("iPhone mention", "iPhone" in html_content),
            ("Price mention", "$" in html_content),
            ("Product title", "h1" in html_content or "h2" in html_content)
        ]
        
        print("HTML Structure Checks:")
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {check_name}")
            
    except Exception as e:
        print(f"❌ Error testing HTML structure: {e}")


if __name__ == "__main__":
    test_scraper_mock_mode()
    test_scraper_error_handling()
    test_scraper_real_mode()
    test_config_loading()
    test_html_content_structure() 