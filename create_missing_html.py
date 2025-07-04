#!/usr/bin/env python3
"""
Script to create missing HTML files for the price intelligence platform.
"""

import os

def create_html_file(filename, product_name, price, currency, vendor, color_variant=""):
    """Create a mock HTML file for a product."""
    
    # Create directory if it doesn't exist
    os.makedirs("mocks/html", exist_ok=True)
    
    # Determine product details based on name
    if "iphone" in product_name.lower():
        brand = "Apple"
        model = "iPhone 16 Pro"
        storage = "128GB"
        features = ["A17 Pro chip", "6.1-inch Super Retina XDR display", "Pro camera system"]
        if color_variant:
            features.append(f"{color_variant} finish")
    elif "macbook" in product_name.lower():
        brand = "Apple"
        model = "MacBook Pro"
        storage = "512GB"
        features = ["M3 Pro chip", "14-inch Liquid Retina XDR display", "16GB unified memory"]
        if color_variant:
            features.append(f"{color_variant} finish")
    elif "nike" in product_name.lower() or "air max" in product_name.lower():
        brand = "Nike"
        model = "Air Max 270"
        storage = "US 10"
        features = ["Air Max technology", "Comfortable cushioning", "Breathable mesh upper"]
        if color_variant:
            features.append(f"{color_variant} colorway")
    elif "samsung" in product_name.lower():
        brand = "Samsung"
        model = "Galaxy S24"
        storage = "128GB"
        features = ["Snapdragon 8 Gen 3", "6.2-inch Dynamic AMOLED display", "AI-powered camera"]
        if color_variant:
            features.append(f"{color_variant} color")
    else:
        brand = "Unknown"
        model = product_name
        storage = ""
        features = ["High quality", "Great value", "Popular choice"]
    
    # Create HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vendor} - {brand} {model}</title>
</head>
<body>
    <div class="product-page">
        <header>
            <h1>{brand} {model}</h1>
            <div class="product-rating">
                <span class="stars">★★★★★</span>
                <span class="review-count">(1,234 reviews)</span>
            </div>
        </header>
        
        <main>
            <div class="product-info">
                <div class="product-title">
                    <h2>{brand} {model}, {storage}{f', {color_variant}' if color_variant else ''}</h2>
                </div>
                
                <div class="price-section">
                    <span class="price">{price}</span>
                    <span class="currency">{currency}</span>
                </div>
                
                <div class="product-features">
                    <ul>
"""
    
    for feature in features:
        html_content += f"                        <li>{feature}</li>\n"
    
    html_content += f"""                    </ul>
                </div>
                
                <div class="availability">
                    <span class="in-stock">In Stock</span>
                    <span class="delivery">Free delivery available</span>
                </div>
            </div>
        </main>
    </div>
    <div class="vendor">{vendor}</div>
</body>
</html>"""
    
    # Write the file
    with open(f"mocks/html/{filename}", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Created: {filename}")

def main():
    """Create all missing HTML files."""
    
    # List of missing files to create
    missing_files = [
        # iPhone variants
        ("apple_iphone16pro_titanium.html", "Apple iPhone 16 Pro", "999", "USD", "Apple", "Natural Titanium"),
        ("apple_iphone16pro_silver.html", "Apple iPhone 16 Pro", "999", "USD", "Apple", "Silver"),
        ("apple_iphone16pro_blue.html", "Apple iPhone 16 Pro", "999", "USD", "Apple", "Blue"),
        
        # MacBook variants
        ("apple_macbookpro_silver.html", "Apple MacBook Pro", "1999", "USD", "Apple", "Silver"),
        ("apple_macbookpro_spacegray.html", "Apple MacBook Pro", "1999", "USD", "Apple", "Space Gray"),
        
        # Nike variants
        ("nike_airmax270_white.html", "Nike Air Max 270", "150", "USD", "Nike", "White"),
        ("nike_airmax270_red.html", "Nike Air Max 270", "150", "USD", "Nike", "Red"),
        
        # Samsung Galaxy S24
        ("amazon_samsunggalaxys24.html", "Samsung Galaxy S24", "799", "USD", "Amazon"),
        ("bestbuy_samsunggalaxys24.html", "Samsung Galaxy S24", "799", "USD", "Best Buy"),
        ("apple_samsunggalaxys24.html", "Samsung Galaxy S24", "799", "USD", "Apple"),
        
        # India variants
        ("amazon_in_samsunggalaxys24.html", "Samsung Galaxy S24", "69999", "INR", "Amazon.in"),
        ("flipkart_samsunggalaxys24.html", "Samsung Galaxy S24", "69999", "INR", "Flipkart"),
        ("croma_samsunggalaxys24.html", "Samsung Galaxy S24", "69999", "INR", "Croma"),
        ("reliancedigital_samsunggalaxys24.html", "Samsung Galaxy S24", "69999", "INR", "Reliance Digital"),
        
        # UK variants
        ("amazon_co_uk_iphone16pro.html", "Apple iPhone 16 Pro", "999", "GBP", "Amazon.co.uk"),
        ("amazon_co_uk_macbookpro.html", "Apple MacBook Pro", "1999", "GBP", "Amazon.co.uk"),
        ("amazon_co_uk_nikeairmax270.html", "Nike Air Max 270", "150", "GBP", "Amazon.co.uk"),
        ("amazon_co_uk_samsunggalaxys24.html", "Samsung Galaxy S24", "799", "GBP", "Amazon.co.uk"),
        
        # Germany variants
        ("amazon_de_iphone16pro.html", "Apple iPhone 16 Pro", "1199", "EUR", "Amazon.de"),
        ("amazon_de_macbookpro.html", "Apple MacBook Pro", "2499", "EUR", "Amazon.de"),
        ("amazon_de_nikeairmax270.html", "Nike Air Max 270", "180", "EUR", "Amazon.de"),
        ("amazon_de_samsunggalaxys24.html", "Samsung Galaxy S24", "899", "EUR", "Amazon.de"),
    ]
    
    print("🔧 Creating missing HTML files...")
    
    for filename, product_name, price, currency, vendor, *args in missing_files:
        color_variant = args[0] if args else ""
        create_html_file(filename, product_name, price, currency, vendor, color_variant)
    
    print("✅ All missing HTML files created successfully!")

if __name__ == "__main__":
    main() 