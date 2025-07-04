#!/usr/bin/env python3
"""
Price Intelligence Platform - Streamlit Web Interface
Provides a user-friendly web interface for searching and comparing product prices globally.
"""

import streamlit as st
import pandas as pd
from src.orchestrator.interface import Orchestrator
import os

# Page configuration
st.set_page_config(
    page_title="🎯 Global Price Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize orchestrator
@st.cache_resource
def get_orchestrator():
    """Initialize and cache the orchestrator to avoid reloading."""
    config_path = os.path.join("config", "phase1_config.yaml")
    return Orchestrator(config_path)

def format_price(price, currency):
    """Format price with currency symbol."""
    currency_symbols = {
        "USD": "$",
        "INR": "₹",
        "GBP": "£",
        "EUR": "€"
    }
    symbol = currency_symbols.get(currency, currency)
    return f"{symbol}{price}"

def create_clickable_link(url, text):
    """Create a clickable link for Streamlit."""
    return f"[{text}]({url})"

def main():
    # Header
    st.title("🎯 Global Price Intelligence")
    st.markdown("Compare product prices across multiple e-commerce sites globally.")
    
    # Sidebar for additional info
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This platform searches across multiple e-commerce sites to find the best prices for your products.
        
        **Supported Categories:**
        - 📱 Smartphones (iPhone, Samsung, etc.)
        - 💻 Laptops (MacBook, Dell, HP, etc.)
        - 👟 Sports (Nike, Adidas, etc.)
        
        **Supported Countries:**
        - 🇺🇸 US (USD)
        - 🇮🇳 India (INR)
        - 🇬🇧 UK (GBP)
        - 🇩🇪 Germany (EUR)
        """)
        
        st.header("🔍 Example Queries")
        st.markdown("""
        - `iPhone 16 Pro, 128GB`
        - `MacBook Pro`
        - `Nike Air Max 270`
        - `Samsung Galaxy S24`
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Search inputs
        query = st.text_input(
            "What product are you looking for?",
            placeholder="e.g., iPhone 16 Pro, 128GB or MacBook Pro",
            help="Enter the product name, model, and any specifications"
        )
    
    with col2:
        country = st.selectbox(
            "Select country",
            ["US", "IN", "UK", "DE"],
            help="Choose your target market for price comparison"
        )
    
    # Search button
    if st.button("🔍 Search Prices", type="primary", use_container_width=True):
        if not query.strip():
            st.warning("⚠️ Please enter a product query.")
            return
        
        # Show loading spinner
        with st.spinner("🔍 Searching for the best prices..."):
            try:
                # Get orchestrator and run search
                orchestrator = get_orchestrator()
                results = orchestrator.run({"query": query, "country": country})
                
                # Display results
                if results:
                    st.success(f"✅ Found {len(results)} products!")
                    
                    # Create DataFrame for display
                    df_data = []
                    for i, product in enumerate(results, 1):
                        df_data.append({
                            "Rank": i,
                            "Product": product.get("productName", "Unknown"),
                            "Price": format_price(product.get("price", "0"), product.get("currency", "USD")),
                            "Link": create_clickable_link(
                                product.get("link", "#"),
                                "View Product"
                            )
                        })
                    
                    df = pd.DataFrame(df_data)
                    
                    # Display as table with custom styling
                    st.markdown("### 📊 Price Comparison Results")
                    
                    # Use st.dataframe with custom formatting
                    st.dataframe(
                        df,
                        column_config={
                            "Rank": st.column_config.NumberColumn(
                                "Rank",
                                help="Price ranking (1 = best value)",
                                format="%d"
                            ),
                            "Product": st.column_config.TextColumn(
                                "Product Name",
                                help="Product name and specifications"
                            ),
                            "Price": st.column_config.TextColumn(
                                "Price",
                                help="Formatted price with currency"
                            ),
                            "Link": st.column_config.LinkColumn(
                                "Product Link",
                                help="Click to view product on retailer site"
                            )
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                    
                    # Additional insights
                    if len(results) > 1:
                        prices = [float(p.get("price", 0)) for p in results]
                        min_price = min(prices)
                        max_price = max(prices)
                        price_diff = max_price - min_price
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Lowest Price", format_price(str(min_price), results[0].get("currency", "USD")))
                        with col2:
                            st.metric("Highest Price", format_price(str(max_price), results[0].get("currency", "USD")))
                        with col3:
                            st.metric("Price Range", format_price(str(price_diff), results[0].get("currency", "USD")))
                
                else:
                    st.warning("⚠️ No products found for your search.")
                    st.info("💡 Try adjusting your search terms or selecting a different country.")
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 This might be due to missing mock data for your specific query. Try a different product or country.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>🔧 Built with Streamlit | 📊 Mock data for demonstration | 🚀 Ready for production deployment</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 