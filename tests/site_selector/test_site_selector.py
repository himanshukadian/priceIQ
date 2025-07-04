"""
Test file for Site Selector Module
Tests country to e-commerce site mapping functionality.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.site_selector.interface import MockSiteSelector, RealSiteSelector, SiteSelector


def test_mock_site_selector():
    """Test the mock site selector with sample data."""
    selector = MockSiteSelector("mocks/selected_sites.yaml")
    
    # Test smartphone category
    sites = selector.select_sites("US", "smartphone")
    print("Mock Site Selector Test - US Smartphone:")
    print(f"Sites: {sites}")
    print()
    
    # Test laptop category
    sites = selector.select_sites("US", "laptop")
    print("Mock Site Selector Test - US Laptop:")
    print(f"Sites: {sites}")
    print()
    
    # Test UK default
    sites = selector.select_sites("UK")
    print("Mock Site Selector Test - UK Default:")
    print(f"Sites: {sites}")
    print()


def test_real_site_selector():
    """Test the real site selector."""
    config = {
        'countries': {
            'US': {
                'sites': ['amazon.com', 'bestbuy.com', 'walmart.com']
            }
        }
    }
    
    selector = RealSiteSelector(config)
    sites = selector.select_sites("US", "smartphone")
    print("Real Site Selector Test:")
    print(f"Sites: {sites}")
    print()


def test_site_selector():
    """Test the site selector with different countries."""
    print("Testing Site Selector Module")
    print("=" * 40)
    
    # Initialize selector
    config_path = "config/phase1_config.yaml"
    selector = SiteSelector(config_path)
    
    # Test cases
    test_cases = [
        ("US", ["amazon.com", "bestbuy.com", "apple.com"]),
        ("IN", ["flipkart.com", "croma.com", "reliancedigital.in"]),
        ("UK", ["amazon.co.uk", "currys.co.uk", "argos.co.uk"]),
        ("DE", ["amazon.de", "mediamarkt.de", "saturn.de"]),
        ("XX", [])  # Unknown country should return empty list
    ]
    
    for country, expected_sites in test_cases:
        print(f"\nTesting country: {country}")
        sites = selector.select_sources(country)
        print(f"Expected: {expected_sites}")
        print(f"Actual:   {sites}")
        
        if sites == expected_sites:
            print("✅ PASS")
        else:
            print("❌ FAIL")
    
    print("\n" + "=" * 40)
    print("Site Selector tests completed!")


def test_config_loading():
    """Test config loading functionality."""
    print("\nTesting Config Loading")
    print("-" * 20)
    
    # Test with config dict
    config_dict = {
        "modules": {
            "site_selector": {
                "use_mock": True,
                "sites_by_country": {
                    "TEST": ["test1.com", "test2.com"]
                }
            }
        }
    }
    
    selector = SiteSelector(config_dict)
    sites = selector.select_sources("TEST")
    print(f"Dict config test: {sites}")
    
    if sites == ["test1.com", "test2.com"]:
        print("✅ Config dict loading PASS")
    else:
        print("❌ Config dict loading FAIL")


if __name__ == "__main__":
    test_mock_site_selector()
    test_real_site_selector()
    test_site_selector()
    test_config_loading() 