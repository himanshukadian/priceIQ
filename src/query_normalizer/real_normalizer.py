"""
Phase 2 implementation placeholder.

This file will include the real logic for query normalization, including:
- LLM-based query understanding and entity extraction
- Product database lookups for brand/model validation
- Multi-language query processing
- Fuzzy matching for misspelled brands/models
- Context-aware normalization based on country/region

To activate:
1. Set `use_mock: false` in config/phase1_config.yaml
2. Swap the logic in interface.py to call real_normalizer instead of returning mocks.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import re
from enum import Enum


class NormalizationMethod(Enum):
    """Methods available for query normalization."""
    LLM_EXTRACTION = "llm_extraction"
    DATABASE_LOOKUP = "database_lookup"
    FUZZY_MATCHING = "fuzzy_matching"
    RULE_BASED = "rule_based"
    MULTI_LANGUAGE = "multi_language"


@dataclass
class NormalizedQuery:
    """Result of query normalization with confidence scoring."""
    normalized: str
    brand: Optional[str]
    model: Optional[str]
    storage: Optional[str]
    category: str
    confidence_scores: Dict[str, float]
    normalization_methods: Dict[str, NormalizationMethod]
    metadata: Dict[str, Any]


class RealQueryNormalizer:
    """
    Real implementation of query normalizer using regex patterns and heuristics.
    
    This class will handle:
    - LLM-based query understanding and entity extraction
    - Product database lookups for brand/model validation
    - Multi-language query processing
    - Fuzzy matching for misspelled brands/models
    - Context-aware normalization based on country/region
    """
    
    def __init__(self):
        """Initialize the real query normalizer with pattern definitions."""
        # Brand patterns (case-insensitive)
        self.brand_patterns = {
            'Apple': r'\b(apple|iphone|macbook|ipad|imac)\b',
            'Samsung': r'\b(samsung|galaxy)\b',
            'Nike': r'\b(nike|air\s+max|air\s+force|air\s+jordan)\b',
            'Google': r'\b(google|pixel)\b',
            'Microsoft': r'\b(microsoft|surface|xbox)\b',
            'Dell': r'\b(dell|inspiron|xps|latitude)\b',
            'HP': r'\b(hp|hewlett|packard|pavilion|envy)\b',
            'Lenovo': r'\b(lenovo|thinkpad|ideapad)\b',
            'Asus': r'\b(asus|zenbook|vivobook)\b',
            'Acer': r'\b(acer|aspire|predator)\b',
            'Adidas': r'\b(adidas|ultraboost|nmd)\b',
            'Puma': r'\b(puma|suede|basket)\b',
            'OnePlus': r'\b(oneplus|one\s+plus)\b',
            'Xiaomi': r'\b(xiaomi|redmi|mi)\b',
            'Huawei': r'\b(huawei|mate|p\d+)\b'
        }
        
        # Storage patterns
        self.storage_pattern = re.compile(
            r'\b(\d+)\s*(gb|tb|gib|tib)\b', 
            re.IGNORECASE
        )
        
        # Model patterns for different categories
        self.smartphone_models = {
            'iPhone 16 Pro Max': r'\biphone\s*16\s*pro\s*max\b',
            'iPhone 16 Pro': r'\biphone\s*16\s*pro\b',
            'iPhone 16 Plus': r'\biphone\s*16\s*plus\b',
            'iPhone 16': r'\biphone\s*16\b',
            'iPhone 15 Pro Max': r'\biphone\s*15\s*pro\s*max\b',
            'iPhone 15 Pro': r'\biphone\s*15\s*pro\b',
            'iPhone 15 Plus': r'\biphone\s*15\s*plus\b',
            'iPhone 15': r'\biphone\s*15\b',
            'Galaxy S24 Ultra': r'\bgalaxy\s*s24\s*ultra\b',
            'Galaxy S24 Plus': r'\bgalaxy\s*s24\s*plus\b',
            'Galaxy S24': r'\bgalaxy\s*s24\b',
            'Galaxy S23': r'\bgalaxy\s*s23\b',
            'Pixel 8 Pro': r'\bpixel\s*8\s*pro\b',
            'Pixel 8': r'\bpixel\s*8\b'
        }
        
        self.laptop_models = {
            'MacBook Pro': r'\bmacbook\s*pro\b',
            'MacBook Air': r'\bmacbook\s*air\b',
            'Surface Laptop': r'\bsurface\s*laptop\b',
            'Surface Pro': r'\bsurface\s*pro\b',
            'ThinkPad': r'\bthinkpad\b',
            'XPS': r'\bxps\b',
            'Inspiron': r'\binspiron\b'
        }
        
        self.sports_models = {
            'Air Max 270': r'\bair\s*max\s*270\b',
            'Air Max 90': r'\bair\s*max\s*90\b',
            'Air Max 1': r'\bair\s*max\s*1\b',
            'Air Force 1': r'\bair\s*force\s*1\b',
            'Air Jordan 1': r'\bair\s*jordan\s*1\b',
            'UltraBoost': r'\bultraboost\b',
            'Stan Smith': r'\bstan\s*smith\b'
        }
        
        # Category detection patterns
        self.category_patterns = {
            'Smartphone': [
                r'\b(iphone|smartphone|phone|galaxy|pixel)\b',
                r'\b(android|ios|mobile)\b'
            ],
            'Laptop': [
                r'\b(laptop|macbook|notebook|ultrabook)\b',
                r'\b(thinkpad|surface|xps|inspiron)\b'
            ],
            'Sports': [
                r'\b(nike|adidas|puma|shoes|sneakers|running)\b',
                r'\b(air\s*max|air\s*force|ultraboost)\b',
                r'\b(basketball|tennis|football|soccer)\b'
            ]
        }
    
    def normalize_query(self, query: str, country: str = "US") -> Dict[str, Any]:
        """
        Normalize a product query using regex patterns and heuristics.
        
        Args:
            query: Raw product query string
            country: Country code (e.g., "US", "UK", "DE")
            
        Returns:
            Dict containing normalized query and category-specific attributes
        """
        normalized_query = query.strip().replace(',', ' ').replace('  ', ' ')
        query_lower = normalized_query.lower()
        
        # Extract category first
        category = self._extract_category(query_lower)
        
        # Extract common attributes
        brand = self._extract_brand(query_lower)
        model = self._extract_model(query_lower, category)
        storage = self._extract_storage(query_lower)
        
        # Build base attributes
        base_attrs = {
            'normalized': normalized_query,
            'brand': brand,
            'model': model,
            'category': category
        }
        
        # Add category-specific attributes
        if category == 'Smartphone':
            base_attrs.update({
                'storage': storage,
                'color': self._extract_color(query_lower),
                'screen_size': self._extract_screen_size(query_lower)
            })
        elif category == 'Laptop':
            base_attrs.update({
                'storage': storage,
                'ram': self._extract_ram(query_lower),
                'screen_size': self._extract_screen_size(query_lower),
                'processor': self._extract_processor(query_lower)
            })
        elif category == 'Sports':
            base_attrs.update({
                'size': self._extract_size(query_lower),
                'color': self._extract_color(query_lower),
                'type': self._extract_type(query_lower)
            })
        
        return base_attrs
    
    def _extract_brand(self, query: str) -> Optional[str]:
        """Extract brand from query using regex patterns."""
        for brand, pattern in self.brand_patterns.items():
            if re.search(pattern, query, re.IGNORECASE):
                return brand
        return None
    
    def _extract_model(self, query: str, category: str) -> Optional[str]:
        """Extract model from query based on category."""
        model_dict = {}
        
        if category == 'Smartphone':
            model_dict = self.smartphone_models
        elif category == 'Laptop':
            model_dict = self.laptop_models
        elif category == 'Sports':
            model_dict = self.sports_models
        
        for model, pattern in model_dict.items():
            if re.search(pattern, query, re.IGNORECASE):
                return model
        
        return None
    
    def _extract_storage(self, query: str) -> Optional[str]:
        """Extract storage capacity from query using regex."""
        # Find all storage matches
        matches = list(self.storage_pattern.finditer(query))
        if not matches:
            return None
        
        # Filter out RAM mentions and prefer larger storage values
        storage_candidates = []
        for match in matches:
            amount, unit = match.groups()
            # Check if this is RAM by looking for RAM words immediately after the match
            post_match_start = match.end()
            post_match_end = min(len(query), match.end() + 15)
            post_context = query[post_match_start:post_match_end].lower().strip()
            
            # Skip if RAM/memory keywords appear immediately after the storage value
            if any(post_context.startswith(ram_word) for ram_word in ['ram', 'memory', 'mem']):
                continue
                
            # Normalize unit
            unit = unit.upper()
            if unit in ['GIB', 'TIB']:
                unit = unit[:-1] + 'B'
            
            storage_candidates.append((int(amount), f"{amount}{unit}"))
        
        # Return the largest storage value found, or the first one if no clear storage
        if storage_candidates:
            # Sort by storage size and return the largest
            storage_candidates.sort(key=lambda x: x[0], reverse=True)
            return storage_candidates[0][1]
        
        # Fallback: return first match if no RAM context found
        if matches:
            amount, unit = matches[0].groups()
            unit = unit.upper()
            if unit in ['GIB', 'TIB']:
                unit = unit[:-1] + 'B'
            return f"{amount}{unit}"
        
        return None
    
    def _extract_category(self, query: str) -> str:
        """Extract product category from query using pattern matching."""
        category_scores = {}
        
        for category, patterns in self.category_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, query, re.IGNORECASE))
                score += matches
            category_scores[category] = score
        
        # Return category with highest score, default to Smartphone
        if category_scores:
            best_category = max(category_scores, key=lambda x: category_scores[x])
            if category_scores[best_category] > 0:
                return best_category
        
        return 'Smartphone'  # Default fallback
    
    def _extract_color(self, query: str) -> Optional[str]:
        """Extract color from query using common color patterns."""
        # Order matters: more specific patterns first
        color_patterns = [
            ('Natural Titanium', r'\b(natural\s*titanium|titanium)\b'),
            ('Space Gray', r'\b(space\s*gray|space\s*grey)\b'),
            ('Midnight', r'\b(midnight|noir)\b'),
            ('Black', r'\b(black|noir|schwarz|negro)\b'),
            ('White', r'\b(white|blanc|weiß|blanco)\b'),
            ('Silver', r'\b(silver|argent|silber|plata)\b'),
            ('Gold', r'\b(gold|or|dorado)\b'),
            ('Blue', r'\b(blue|bleu|blau|azul|navy)\b'),
            ('Red', r'\b(red|rouge|rot|rojo|crimson)\b'),
            ('Green', r'\b(green|vert|grün|verde)\b'),
            ('Purple', r'\b(purple|violet|lila|morado)\b'),
            ('Pink', r'\b(pink|rose|rosa)\b'),
            ('Gray', r'\b(gray|grey|gris|grau)\b'),
        ]
        
        for color, pattern in color_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return color
        
        return None
    
    def _extract_screen_size(self, query: str) -> Optional[str]:
        """Extract screen size from query."""
        # Pattern for screen sizes like "6.1 inch", "14-inch", "15.6""
        screen_patterns = [
            r'\b(\d+\.?\d*)\s*(inch|inches|in|"|'')\b',
            r'\b(\d+\.?\d*)-inch\b'
        ]
        
        for pattern in screen_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                size = match.group(1)
                return f"{size} inch"
        
        return None
    
    def _extract_ram(self, query: str) -> Optional[str]:
        """Extract RAM from query for laptops."""
        # Pattern for RAM like "8GB RAM", "16 GB", "32gb"
        ram_pattern = re.compile(
            r'\b(\d+)\s*(gb|mb)\s*(ram|memory|mem)?\b', 
            re.IGNORECASE
        )
        
        match = ram_pattern.search(query)
        if match:
            amount, unit = match.groups()[:2]
            unit = unit.upper()
            return f"{amount}{unit}"
        
        return None
    
    def _extract_processor(self, query: str) -> Optional[str]:
        """Extract processor from query for laptops."""
        processor_patterns = {
            'M3 Pro': r'\bm3\s*pro\b',
            'M3 Max': r'\bm3\s*max\b',
            'M3': r'\bm3\b',
            'M2 Pro': r'\bm2\s*pro\b',
            'M2 Max': r'\bm2\s*max\b',
            'M2': r'\bm2\b',
            'M1 Pro': r'\bm1\s*pro\b',
            'M1 Max': r'\bm1\s*max\b',
            'M1': r'\bm1\b',
            'Intel i9': r'\b(intel\s*)?i9\b',
            'Intel i7': r'\b(intel\s*)?i7\b',
            'Intel i5': r'\b(intel\s*)?i5\b',
            'Intel i3': r'\b(intel\s*)?i3\b',
            'AMD Ryzen 9': r'\b(amd\s*)?ryzen\s*9\b',
            'AMD Ryzen 7': r'\b(amd\s*)?ryzen\s*7\b',
            'AMD Ryzen 5': r'\b(amd\s*)?ryzen\s*5\b'
        }
        
        for processor, pattern in processor_patterns.items():
            if re.search(pattern, query, re.IGNORECASE):
                return processor
        
        return None
    
    def _extract_size(self, query: str) -> Optional[str]:
        """Extract size from query for sports items."""
        # Pattern for sizes like "US 10", "EU 42", "UK 8.5", "10.5", "Size 9"
        size_patterns = [
            r'\b(us|eu|uk)\s*(\d+\.?\d*)\b',
            r'\bsize\s*(\d+\.?\d*)\b',
            r'\b(\d+\.?\d*)\s*(us|eu|uk)\b',
            r'\b(\d+\.?\d*)\b(?=\s*(size|shoe|foot))'
        ]
        
        for pattern in size_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    region, size = match.groups()
                    return f"{region.upper()} {size}"
                else:
                    size = match.group(1)
                    return f"US {size}"  # Default to US sizing
        
        return None
    
    def _extract_type(self, query: str) -> Optional[str]:
        """Extract type from query for sports items."""
        type_patterns = {
            'Running Shoes': r'\b(running|run|runner|jogging)\b',
            'Basketball Shoes': r'\b(basketball|basket|court)\b',
            'Tennis Shoes': r'\b(tennis|court)\b',
            'Football Cleats': r'\b(football|cleats|soccer)\b',
            'Casual Shoes': r'\b(casual|lifestyle|everyday)\b',
            'Training Shoes': r'\b(training|trainer|cross)\b',
            'Hiking Boots': r'\b(hiking|hike|outdoor|trail)\b'
        }
        
        for type_name, pattern in type_patterns.items():
            if re.search(pattern, query, re.IGNORECASE):
                return type_name
        
        # Default based on brand/model
        if re.search(r'\b(air\s*max|air\s*force)\b', query, re.IGNORECASE):
            return 'Running Shoes'
        
        return None


# Example usage for future implementation:
"""
normalizer = RealQueryNormalizer()

query = "iPhone 16 Pro, 128GB"
result = normalizer.normalize_query(query, "US")

print(f"Brand: {result['brand']}")
print(f"Model: {result['model']}")
print(f"Storage: {result['storage']}")
print(f"Category: {result['category']}")
print(f"Confidence: {result['confidence_scores']}")
# Output:
# Brand: Apple
# Model: iPhone 16 Pro
# Storage: 128GB
# Category: smartphone
# Confidence: {'brand': 0.9, 'model': 0.9, 'storage': 0.8, 'category': 0.8}
"""
