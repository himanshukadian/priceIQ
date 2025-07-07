"""
Tests for Real Query Normalizer Implementation
Tests the basic regex-based attribute extraction functionality.
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from query_normalizer.real_normalizer import RealQueryNormalizer


class TestRealQueryNormalizer:
    """Test class for RealQueryNormalizer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.normalizer = RealQueryNormalizer()
    
    # Brand extraction tests
    def test_extract_brand_apple_iphone(self):
        """Test Apple brand extraction from iPhone queries."""
        result = self.normalizer.normalize_query("iPhone 16 Pro 128GB")
        assert result['brand'] == 'Apple'
    
    def test_extract_brand_apple_macbook(self):
        """Test Apple brand extraction from MacBook queries."""
        result = self.normalizer.normalize_query("MacBook Pro 14 inch")
        assert result['brand'] == 'Apple'
    
    def test_extract_brand_samsung(self):
        """Test Samsung brand extraction."""
        result = self.normalizer.normalize_query("Samsung Galaxy S24")
        assert result['brand'] == 'Samsung'
    
    def test_extract_brand_nike(self):
        """Test Nike brand extraction."""
        result = self.normalizer.normalize_query("Nike Air Max 270")
        assert result['brand'] == 'Nike'
    
    def test_extract_brand_case_insensitive(self):
        """Test brand extraction is case insensitive."""
        result = self.normalizer.normalize_query("iphone 16 pro")
        assert result['brand'] == 'Apple'
    
    def test_extract_brand_not_found(self):
        """Test brand extraction when no brand is found."""
        result = self.normalizer.normalize_query("random product query")
        assert result['brand'] is None
    
    # Storage extraction tests
    def test_extract_storage_gb(self):
        """Test storage extraction in GB."""
        result = self.normalizer.normalize_query("iPhone 16 Pro 128GB")
        assert result['storage'] == '128GB'
    
    def test_extract_storage_tb(self):
        """Test storage extraction in TB."""
        result = self.normalizer.normalize_query("MacBook Pro 1TB")
        assert result['storage'] == '1TB'
    
    def test_extract_storage_with_spaces(self):
        """Test storage extraction with spaces."""
        result = self.normalizer.normalize_query("iPhone 16 Pro 256 GB")
        assert result['storage'] == '256GB'
    
    def test_extract_storage_case_insensitive(self):
        """Test storage extraction is case insensitive."""
        result = self.normalizer.normalize_query("MacBook Pro 512gb")
        assert result['storage'] == '512GB'
    
    def test_extract_storage_not_found(self):
        """Test storage extraction when no storage is found."""
        result = self.normalizer.normalize_query("iPhone without storage info")
        assert result['storage'] is None
    
    # Model extraction tests
    def test_extract_model_iphone_16_pro(self):
        """Test iPhone 16 Pro model extraction."""
        result = self.normalizer.normalize_query("iPhone 16 Pro 128GB")
        assert result['model'] == 'iPhone 16 Pro'
    
    def test_extract_model_macbook_pro(self):
        """Test MacBook Pro model extraction."""
        result = self.normalizer.normalize_query("MacBook Pro 14 inch")
        assert result['model'] == 'MacBook Pro'
    
    def test_extract_model_air_max_270(self):
        """Test Air Max 270 model extraction."""
        result = self.normalizer.normalize_query("Nike Air Max 270")
        assert result['model'] == 'Air Max 270'
    
    def test_extract_model_galaxy_s24(self):
        """Test Galaxy S24 model extraction."""
        result = self.normalizer.normalize_query("Samsung Galaxy S24")
        assert result['model'] == 'Galaxy S24'
    
    def test_extract_model_not_found(self):
        """Test model extraction when no known model is found."""
        result = self.normalizer.normalize_query("Unknown smartphone")
        assert result['model'] is None
    
    # Category detection tests
    def test_category_smartphone_iphone(self):
        """Test smartphone category detection for iPhone."""
        result = self.normalizer.normalize_query("iPhone 16 Pro")
        assert result['category'] == 'Smartphone'
    
    def test_category_smartphone_galaxy(self):
        """Test smartphone category detection for Galaxy."""
        result = self.normalizer.normalize_query("Samsung Galaxy S24")
        assert result['category'] == 'Smartphone'
    
    def test_category_laptop_macbook(self):
        """Test laptop category detection for MacBook."""
        result = self.normalizer.normalize_query("MacBook Pro")
        assert result['category'] == 'Laptop'
    
    def test_category_laptop_thinkpad(self):
        """Test laptop category detection for ThinkPad."""
        result = self.normalizer.normalize_query("Lenovo ThinkPad")
        assert result['category'] == 'Laptop'
    
    def test_category_sports_nike(self):
        """Test sports category detection for Nike."""
        result = self.normalizer.normalize_query("Nike Air Max 270")
        assert result['category'] == 'Sports'
    
    def test_category_sports_shoes(self):
        """Test sports category detection for shoes."""
        result = self.normalizer.normalize_query("Running shoes")
        assert result['category'] == 'Sports'
    
    def test_category_default_fallback(self):
        """Test default category fallback."""
        result = self.normalizer.normalize_query("unknown product")
        assert result['category'] == 'Smartphone'  # Default fallback
    
    # Color extraction tests
    def test_extract_color_black(self):
        """Test black color extraction."""
        result = self.normalizer.normalize_query("iPhone 16 Pro Black")
        assert result['color'] == 'Black'
    
    def test_extract_color_natural_titanium(self):
        """Test Natural Titanium color extraction."""
        result = self.normalizer.normalize_query("iPhone 16 Pro Natural Titanium")
        assert result['color'] == 'Natural Titanium'
    
    def test_extract_color_space_gray(self):
        """Test Space Gray color extraction."""
        result = self.normalizer.normalize_query("MacBook Pro Space Gray")
        assert result['color'] == 'Space Gray'
    
    def test_extract_color_not_found(self):
        """Test color extraction when no color is found."""
        result = self.normalizer.normalize_query("iPhone 16 Pro")
        assert result['color'] is None
    
    # Screen size extraction tests
    def test_extract_screen_size_inch(self):
        """Test screen size extraction with inch."""
        result = self.normalizer.normalize_query("iPhone 16 Pro 6.1 inch")
        assert result['screen_size'] == '6.1 inch'
    
    def test_extract_screen_size_quotes(self):
        """Test screen size extraction with quotes."""
        result = self.normalizer.normalize_query('MacBook Pro 14"')
        assert result['screen_size'] == '14 inch'
    
    def test_extract_screen_size_dash(self):
        """Test screen size extraction with dash format."""
        result = self.normalizer.normalize_query("MacBook Pro 14-inch")
        assert result['screen_size'] == '14 inch'
    
    def test_extract_screen_size_not_found(self):
        """Test screen size extraction when no size is found."""
        result = self.normalizer.normalize_query("iPhone 16 Pro")
        assert result['screen_size'] is None
    
    # RAM extraction tests (laptop category)
    def test_extract_ram_gb(self):
        """Test RAM extraction for laptops."""
        result = self.normalizer.normalize_query("MacBook Pro 16GB RAM")
        assert result['ram'] == '16GB'
    
    def test_extract_ram_no_ram_word(self):
        """Test RAM extraction without RAM word."""
        result = self.normalizer.normalize_query("MacBook Pro 32GB memory")
        assert result['ram'] == '32GB'
    
    def test_extract_ram_not_found(self):
        """Test RAM extraction when no RAM is found."""
        result = self.normalizer.normalize_query("MacBook Pro")
        assert result['ram'] is None
    
    # Processor extraction tests (laptop category)
    def test_extract_processor_m3_pro(self):
        """Test M3 Pro processor extraction."""
        result = self.normalizer.normalize_query("MacBook Pro M3 Pro")
        assert result['processor'] == 'M3 Pro'
    
    def test_extract_processor_intel_i7(self):
        """Test Intel i7 processor extraction."""
        result = self.normalizer.normalize_query("Laptop Intel i7")
        assert result['processor'] == 'Intel i7'
    
    def test_extract_processor_amd_ryzen(self):
        """Test AMD Ryzen processor extraction."""
        result = self.normalizer.normalize_query("Laptop AMD Ryzen 7")
        assert result['processor'] == 'AMD Ryzen 7'
    
    def test_extract_processor_not_found(self):
        """Test processor extraction when no processor is found."""
        result = self.normalizer.normalize_query("MacBook Pro")
        assert result['processor'] is None
    
    # Size extraction tests (sports category)
    def test_extract_size_us_format(self):
        """Test US size extraction."""
        result = self.normalizer.normalize_query("Nike Air Max 270 US 10")
        assert result['size'] == 'US 10'
    
    def test_extract_size_eu_format(self):
        """Test EU size extraction."""
        result = self.normalizer.normalize_query("Nike Air Max 270 EU 42")
        assert result['size'] == 'EU 42'
    
    def test_extract_size_just_number(self):
        """Test size extraction with just number (defaults to US)."""
        result = self.normalizer.normalize_query("Nike Air Max 270 size 10.5")
        assert result['size'] == 'US 10.5'
    
    def test_extract_size_not_found(self):
        """Test size extraction when no size is found."""
        result = self.normalizer.normalize_query("Nike Air Max 270")
        assert result['size'] is None
    
    # Type extraction tests (sports category)
    def test_extract_type_running(self):
        """Test running shoes type extraction."""
        result = self.normalizer.normalize_query("Nike running shoes")
        assert result['type'] == 'Running Shoes'
    
    def test_extract_type_basketball(self):
        """Test basketball shoes type extraction."""
        result = self.normalizer.normalize_query("Nike basketball shoes")
        assert result['type'] == 'Basketball Shoes'
    
    def test_extract_type_air_max_default(self):
        """Test default type for Air Max (should be Running Shoes)."""
        result = self.normalizer.normalize_query("Nike Air Max 270")
        assert result['type'] == 'Running Shoes'
    
    def test_extract_type_not_found(self):
        """Test type extraction when no type is found."""
        result = self.normalizer.normalize_query("Nike shoes")
        assert result['type'] is None
    
    # Integration tests - full query processing
    def test_full_smartphone_query(self):
        """Test complete smartphone query processing."""
        result = self.normalizer.normalize_query("iPhone 16 Pro 128GB Natural Titanium 6.1 inch")
        
        assert result['brand'] == 'Apple'
        assert result['model'] == 'iPhone 16 Pro'
        assert result['storage'] == '128GB'
        assert result['color'] == 'Natural Titanium'
        assert result['screen_size'] == '6.1 inch'
        assert result['category'] == 'Smartphone'
        assert 'normalized' in result
    
    def test_full_laptop_query(self):
        """Test complete laptop query processing."""
        result = self.normalizer.normalize_query("MacBook Pro 14-inch M3 Pro 16GB RAM 512GB")
        
        assert result['brand'] == 'Apple'
        assert result['model'] == 'MacBook Pro'
        assert result['storage'] == '512GB'
        assert result['ram'] == '16GB'
        assert result['screen_size'] == '14 inch'
        assert result['processor'] == 'M3 Pro'
        assert result['category'] == 'Laptop'
    
    def test_full_sports_query(self):
        """Test complete sports query processing."""
        result = self.normalizer.normalize_query("Nike Air Max 270 Running US 10 Black")
        
        assert result['brand'] == 'Nike'
        assert result['model'] == 'Air Max 270'
        assert result['size'] == 'US 10'
        assert result['color'] == 'Black'
        assert result['type'] == 'Running Shoes'
        assert result['category'] == 'Sports'
    
    def test_query_normalization(self):
        """Test query string normalization."""
        result = self.normalizer.normalize_query("iPhone  16   Pro,  128GB")
        assert result['normalized'] == "iPhone  16   Pro  128GB"  # Commas removed, spaces normalized
    
    def test_country_parameter_acceptance(self):
        """Test that country parameter is accepted without errors."""
        result = self.normalizer.normalize_query("iPhone 16 Pro", "UK")
        assert result['brand'] == 'Apple'
        assert result['category'] == 'Smartphone'
    
    # Edge case tests
    def test_empty_query(self):
        """Test handling of empty query."""
        result = self.normalizer.normalize_query("")
        assert result['category'] == 'Smartphone'  # Default fallback
        assert result['brand'] is None
        assert result['model'] is None
    
    def test_special_characters_query(self):
        """Test handling of special characters in query."""
        result = self.normalizer.normalize_query("iPhone 16 Pro (128GB)")
        assert result['brand'] == 'Apple'
        assert result['storage'] == '128GB'
    
    def test_mixed_case_query(self):
        """Test handling of mixed case queries."""
        result = self.normalizer.normalize_query("IPHONE 16 PRO 128gb")
        assert result['brand'] == 'Apple'
        assert result['model'] == 'iPhone 16 Pro'
        assert result['storage'] == '128GB'
    
    def test_multiple_brands_query(self):
        """Test query with multiple potential brands (should pick first match)."""
        result = self.normalizer.normalize_query("Apple vs Samsung comparison")
        # Should pick Apple as it comes first in the patterns
        assert result['brand'] == 'Apple'


if __name__ == "__main__":
    pytest.main([__file__])