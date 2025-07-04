"""
Test the updated orchestrator with full mock pipeline.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.orchestrator.interface import Orchestrator


def test_full_pipeline():
    """Test the complete orchestrator pipeline."""
    print("Testing Full Orchestrator Pipeline")
    print("=" * 50)
    
    # Initialize orchestrator
    config_path = "config/phase1_config.yaml"
    orchestrator = Orchestrator(config_path)
    
    # Test input
    user_input = {
        "country": "US",
        "query": "iPhone 16 Pro, 128GB"
    }
    
    print(f"Input: {user_input}")
    print()
    
    # Run the pipeline
    try:
        results = orchestrator.run(user_input)
        
        print(f"\nFinal Results ({len(results)} products):")
        print("-" * 40)
        for i, product in enumerate(results, 1):
            print(f"{i}. {product['productName']} - {product['price']} {product['currency']}")
            print(f"   Link: {product['link']}")
            print()
        
        # Verify we got some results
        if len(results) > 0:
            print(f"✅ Pipeline successful! Found {len(results)} products")
        else:
            print("❌ Pipeline returned no results")
            
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()


def test_flow_description():
    """Test the flow description method."""
    print("\nTesting Flow Description")
    print("=" * 30)
    
    config_path = "config/phase1_config.yaml"
    orchestrator = Orchestrator(config_path)
    
    flow_desc = orchestrator.describe_flow()
    print(flow_desc)


def test_different_countries():
    """Test pipeline with different countries."""
    print("\nTesting Different Countries")
    print("=" * 30)
    
    config_path = "config/phase1_config.yaml"
    orchestrator = Orchestrator(config_path)
    
    countries = ["US", "UK", "DE", "IN"]
    
    for country in countries:
        print(f"\n--- Testing {country} ---")
        user_input = {
            "country": country,
            "query": "iPhone 16 Pro, 128GB"
        }
        
        try:
            results = orchestrator.run(user_input)
            print(f"Results for {country}: {len(results)} products")
            
            if len(results) > 0:
                print(f"  Top result: {results[0]['productName']} - {results[0]['price']} {results[0]['currency']}")
            
        except Exception as e:
            print(f"  Error for {country}: {e}")


if __name__ == "__main__":
    test_full_pipeline()
    test_flow_description()
    test_different_countries() 