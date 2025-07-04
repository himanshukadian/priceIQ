#!/bin/bash
# Run the Price Intelligence Streamlit App

echo "🚀 Starting Price Intelligence Streamlit App..."
echo "📊 This will open a web interface for price comparison"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the streamlit app
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 