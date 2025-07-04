# 🎯 Price Intelligence Streamlit App

A beautiful web interface for the Price Intelligence Platform that allows users to search for products and compare prices across multiple e-commerce sites globally.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Streamlit and other dependencies (see requirements.txt)

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install streamlit pandas pyyaml
```

### Running the App

#### Option 1: Using the convenience script
```bash
./run_streamlit.sh
```

#### Option 2: Direct command
```bash
streamlit run streamlit_app.py
```

#### Option 3: With custom settings
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

The app will open in your browser at `http://localhost:8501`

## 🎨 Features

### ✨ User Interface
- **Clean, Modern Design**: Beautiful Streamlit interface with emojis and clear layout
- **Responsive Layout**: Works on desktop and mobile devices
- **Sidebar Information**: Helpful tips and example queries
- **Loading States**: Visual feedback during search operations

### 🔍 Search Capabilities
- **Product Search**: Enter any product query (e.g., "iPhone 16 Pro, 128GB")
- **Country Selection**: Choose from US, India, UK, Germany
- **Category Detection**: Automatically detects product category
- **Real-time Results**: Instant price comparison results

### 📊 Results Display
- **Ranked Results**: Products sorted by best value
- **Price Formatting**: Proper currency symbols ($, ₹, £, €)
- **Clickable Links**: Direct links to product pages
- **Price Analytics**: Lowest, highest, and price range metrics
- **Interactive Table**: Sortable and filterable results

### 🛡️ Error Handling
- **Graceful Degradation**: Handles missing data gracefully
- **User Feedback**: Clear error messages and suggestions
- **Empty States**: Helpful messages when no results found

## 🧪 Example Queries

### Smartphones
- `iPhone 16 Pro, 128GB`
- `Samsung Galaxy S24`
- `Google Pixel 8`

### Laptops
- `MacBook Pro`
- `Dell XPS 13`
- `HP Spectre x360`

### Sports
- `Nike Air Max 270`
- `Adidas Ultraboost`
- `Puma RS-X`

## 🌍 Supported Countries

| Country | Currency | Example Sites |
|---------|----------|---------------|
| 🇺🇸 US | USD | Amazon, Best Buy, Apple |
| 🇮🇳 India | INR | Amazon.in, Flipkart, Croma |
| 🇬🇧 UK | GBP | Amazon.co.uk, Currys, Argos |
| 🇩🇪 Germany | EUR | Amazon.de, MediaMarkt, Saturn |

## 🔧 Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Backend**: Existing orchestrator pipeline
- **Data**: Mock data for demonstration
- **Caching**: Streamlit caching for performance

### Key Components
- `streamlit_app.py` - Main application file
- `src/orchestrator/interface.py` - Backend pipeline
- `config/phase1_config.yaml` - Configuration
- `mocks/` - Mock data and HTML files

### Dependencies
- `streamlit>=1.28.0` - Web framework
- `pandas>=2.0.0` - Data manipulation
- `pyyaml>=6.0` - Configuration parsing

## 🎯 Usage Examples

### Basic Search
1. Enter a product query in the search box
2. Select your target country
3. Click "🔍 Search Prices"
4. View ranked results in the table

### Advanced Features
- **Price Analytics**: See lowest, highest, and price range
- **Product Links**: Click "View Product" to visit retailer sites
- **Sorting**: Click column headers to sort results
- **Responsive Design**: Works on all screen sizes

## 🚀 Deployment

### Local Development
```bash
# Development mode with auto-reload
streamlit run streamlit_app.py --server.runOnSave true
```

### Production Deployment
```bash
# Production settings
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔍 Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
pip install -r requirements.txt
```

#### Port already in use
```bash
streamlit run streamlit_app.py --server.port 8502
```

#### No results found
- Try different search terms
- Check if the product/country combination is supported
- Use example queries from the sidebar

### Debug Mode
```bash
streamlit run streamlit_app.py --logger.level debug
```

## 🎉 Features in Action

### Category-Specific Attributes
The app leverages the platform's category-specific attribute system:
- **Smartphones**: storage, color, screen_size
- **Laptops**: storage, ram, screen_size, processor
- **Sports**: size, color, type

### Category-Aware Site Selection
Only relevant sites for each category/country combination are searched:
- **US Sports**: amazon.com, bestbuy.com, nike.com
- **India Laptops**: amazon.in, flipkart.com, croma.com, reliancedigital.in

### Multi-Country Support
Different pricing and sites for each country:
- **US**: USD pricing, US-specific retailers
- **India**: INR pricing, India-specific retailers
- **UK**: GBP pricing, UK-specific retailers
- **Germany**: EUR pricing, German-specific retailers

## 🚀 Future Enhancements

### Planned Features
- **Price History**: Track price changes over time
- **Price Alerts**: Notify when prices drop
- **User Accounts**: Save favorite searches
- **Advanced Filters**: Filter by price range, brand, etc.
- **Export Results**: Download results as CSV/PDF
- **Mobile App**: Native mobile application

### Technical Improvements
- **Real Data Integration**: Replace mock data with real scraping
- **Performance Optimization**: Caching and parallel processing
- **Advanced Analytics**: Price trends and market analysis
- **API Endpoints**: RESTful API for external integrations

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the main platform documentation
3. Test with example queries
4. Check browser console for errors

---

**🎯 Built with Streamlit | 📊 Mock data for demonstration | 🚀 Ready for production deployment** 