#!/usr/bin/env python3
"""
Script to create Samsung Galaxy S24 HTML files.
"""

import os

def create_samsung_html_files():
    """Create Samsung Galaxy S24 HTML files."""
    
    # Create directory if it doesn't exist
    os.makedirs("mocks/html", exist_ok=True)
    
    # Samsung Galaxy S24 files
    samsung_files = [
        ("samsung_galaxys24.html", "Samsung Galaxy S24", "799", "USD", "Samsung"),
        ("samsung_galaxys24_black.html", "Samsung Galaxy S24", "799", "USD", "Samsung", "Phantom Black"),
    ]
    
    for filename, product_name, price, currency, vendor, *args in samsung_files:
        color_variant = args[0] if args else ""
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vendor} - {product_name}</title>
</head>
<body>
    <div class="product-page">
        <header>
            <h1>{product_name}</h1>
            <div class="product-rating">
                <span class="stars">★★★★★</span>
                <span class="review-count">(1,567 reviews)</span>
            </div>
        </header>
        
        <main>
            <div class="product-info">
                <div class="product-title">
                    <h2>{product_name}, 128GB{f', {color_variant}' if color_variant else ''}</h2>
                </div>
                
                <div class="price-section">
                    <span class="price">{price}</span>
                    <span class="currency">{currency}</span>
                </div>
                
                <div class="product-features">
                    <ul>
                        <li>Snapdragon 8 Gen 3 processor</li>
                        <li>6.2-inch Dynamic AMOLED display</li>
                        <li>AI-powered camera system</li>
                        <li>25W fast charging</li>
                        <li>5G connectivity</li>
                        {f'<li>{color_variant} color</li>' if color_variant else ''}
                    </ul>
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

if __name__ == "__main__":
    create_samsung_html_files() 