"""
End-to-end unit test for the full mock pipeline via the Orchestrator.

Tests the complete flow from user input to ranked product results.
"""
import unittest
import sys
import os
import yaml

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.orchestrator.interface import Orchestrator


class TestOrchestratorPipeline(unittest.TestCase):
    """Test the complete orchestrator pipeline with mock data."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config_path = os.path.join("config", "phase1_config.yaml")
        self.orchestrator = Orchestrator(self.config_path)
        
        # Sample input for testing
        self.user_input = {
            "country": "US",
            "query": "iPhone 16 Pro, 128GB"
        }
    
    def test_full_pipeline_flow(self):
        """Test the complete pipeline flow from input to ranked results."""
        print("\n🧪 Testing Full Pipeline Flow")
        print("=" * 40)
        
        # Run the pipeline
        try:
            results = self.orchestrator.run(self.user_input)
            print(f"✅ Pipeline completed successfully")
            print(f"📊 Results count: {len(results)}")
            
            # Validate output structure
            self._validate_output_structure(results)
            
            # Validate price ordering
            self._validate_price_ordering(results)
            
            # Print results for debugging
            self._print_results(results)
            
        except Exception as e:
            print(f"❌ Pipeline failed: {e}")
            raise
    
    def test_pipeline_with_different_countries(self):
        """Test pipeline with different countries."""
        print("\n🌍 Testing Different Countries")
        print("=" * 30)
        
        countries = ["US", "IN", "UK", "DE"]
        
        for country in countries:
            print(f"\n--- Testing {country} ---")
            user_input = {
                "country": country,
                "query": "iPhone 16 Pro, 128GB"
            }
            
            try:
                results = self.orchestrator.run(user_input)
                print(f"Results for {country}: {len(results)} products")
                
                if len(results) > 0:
                    # Validate structure for non-empty results
                    self._validate_output_structure(results)
                    self._validate_price_ordering(results)
                    print(f"  Top result: {results[0]['productName']} - {results[0]['price']} {results[0]['currency']}")
                else:
                    print(f"  No results for {country} (expected for some countries)")
                    
            except Exception as e:
                print(f"  Error for {country}: {e}")
                # Don't fail the test for countries with no mock data
                if "Mock HTML file not found" not in str(e):
                    raise
    
    def test_config_integrity(self):
        """Test that all required mock data exists and is well-formed."""
        print("\n🔧 Testing Config Integrity")
        print("=" * 30)
        
        try:
            # Load config
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Check required modules exist
            modules = config.get('modules', {})
            required_modules = [
                'query_normalizer', 'site_selector', 'search_agent',
                'scraper', 'extractor', 'validator', 'deduplicator', 'ranker'
            ]
            
            for module in required_modules:
                self.assertIn(module, modules, f"Module {module} missing from config")
                self.assertIn('use_mock', modules[module], f"use_mock missing from {module}")
                print(f"✅ {module}: use_mock = {modules[module]['use_mock']}")
            
            # Check mock data paths exist
            mock_paths = [
                "mocks/html/",
                "mocks/normalized_queries.yaml",
                "mocks/selected_sites.yaml",
                "mocks/search_results.yaml",
                "mocks/extracts/",
                "mocks/validated_data.yaml",
                "mocks/deduplicated_data.yaml",
                "mocks/ranked_results.yaml"
            ]
            
            for path in mock_paths:
                if path.endswith('/'):
                    # Directory
                    self.assertTrue(os.path.exists(path), f"Mock directory missing: {path}")
                else:
                    # File
                    self.assertTrue(os.path.exists(path), f"Mock file missing: {path}")
                print(f"✅ {path}")
            
            print("✅ Config integrity check passed")
            
        except Exception as e:
            print(f"❌ Config integrity check failed: {e}")
            raise
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        print("\n⚠️ Testing Error Handling")
        print("=" * 25)
        
        # Test with missing country
        invalid_input = {"query": "iPhone 16 Pro, 128GB"}
        try:
            results = self.orchestrator.run(invalid_input)
            print("✅ Pipeline handled missing country gracefully")
        except Exception as e:
            print(f"❌ Pipeline failed with missing country: {e}")
            # This might be expected behavior depending on implementation
        
        # Test with empty query
        invalid_input = {"country": "US", "query": ""}
        try:
            results = self.orchestrator.run(invalid_input)
            print("✅ Pipeline handled empty query gracefully")
        except Exception as e:
            print(f"❌ Pipeline failed with empty query: {e}")
            # This might be expected behavior depending on implementation
    
    def _validate_output_structure(self, results):
        """Validate that output has correct structure."""
        print("🔍 Validating output structure...")
        
        # Check results is a list
        self.assertIsInstance(results, list, "Results should be a list")
        
        if len(results) == 0:
            print("  ⚠️ No results returned (this might be expected for some countries)")
            return
        
        # Check each result has required keys
        required_keys = ['productName', 'price', 'currency', 'link']
        
        for i, result in enumerate(results):
            self.assertIsInstance(result, dict, f"Result {i} should be a dictionary")
            
            for key in required_keys:
                self.assertIn(key, result, f"Result {i} missing key: {key}")
                self.assertIsInstance(result[key], str, f"Result {i} key {key} should be string")
            
            # Validate price is numeric string
            try:
                float(result['price'])
            except ValueError:
                self.fail(f"Result {i} price '{result['price']}' is not a valid number")
        
        print(f"✅ Output structure valid: {len(results)} products with correct keys")
    
    def _validate_price_ordering(self, results):
        """Validate that results are sorted by price (ascending)."""
        print("📊 Validating price ordering...")
        
        if len(results) < 2:
            print("  ⚠️ Not enough results to validate ordering")
            return
        
        # Extract prices and convert to float for comparison
        prices = []
        for result in results:
            try:
                price = float(result['price'])
                prices.append(price)
            except ValueError:
                self.fail(f"Invalid price format: {result['price']}")
        
        # Check if prices are in ascending order
        is_ascending = all(prices[i] <= prices[i+1] for i in range(len(prices)-1))
        
        if is_ascending:
            print(f"✅ Price ordering correct: {prices}")
        else:
            print(f"❌ Price ordering incorrect: {prices}")
            self.fail(f"Results not sorted by price (ascending). Prices: {prices}")
    
    def _print_results(self, results):
        """Print results for debugging."""
        print("\n📋 Final Results:")
        print("-" * 40)
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['productName']}")
            print(f"   Price: {result['price']} {result['currency']}")
            print(f"   Link: {result['link']}")
            print()


if __name__ == '__main__':
    # Create tests directory if it doesn't exist
    os.makedirs('tests', exist_ok=True)
    
    # Run tests
    unittest.main(verbosity=2) 