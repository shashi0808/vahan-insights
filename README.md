# Vahan Vehicle Registration Analytics Dashboard

An interactive dashboard for analyzing vehicle registration data from India's Vahan platform, built with investor insights in mind.

## 🎯 Objective

This project creates a comprehensive dashboard that analyzes vehicle registration trends across different categories (2W/3W/4W) and manufacturers, providing Year-over-Year (YoY) and Quarter-over-Quarter (QoQ) growth metrics for investment analysis.

## 🚀 Features

- **Interactive Dashboard**: Clean, investor-friendly UI built with Streamlit
- **Growth Analytics**: YoY and QoQ growth calculations for all vehicle categories and manufacturers
- **Advanced Filtering**: Date range selection, vehicle category, and manufacturer filters
- **Visual Analytics**: Trend charts, growth matrices, and performance comparisons
- **Key Metrics**: Total registrations, growth rates, market leaders, and investment insights

## 📊 Dashboard Components

1. **Key Performance Indicators**: Total registrations, monthly averages, top categories/manufacturers
2. **Growth Analysis**: Category-wise trends and growth comparison charts
3. **Manufacturer Performance**: Top performers ranking and growth matrix analysis
4. **Detailed Data Tables**: Quarterly breakdown with growth metrics
5. **Investment Insights**: Automated insights and market observations

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**:
   ```bash
   cd C:\Users\91766\Downloads\vahan-insights
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

4. **Access the dashboard**:
   - Open your browser and go to `http://localhost:8501`
   - The dashboard will automatically load with sample data

## 📁 Project Structure

```
vahan-insights/
│
├── dashboard.py           # Main Streamlit dashboard application
├── data_collector.py      # Data collection and processing module
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── Requirement.txt.txt   # Original project requirements
```

## 📈 Data Sources & Assumptions

### Data Collection
- **Primary Source**: Vahan Dashboard (https://vahan.parivahan.gov.in)
- **Sample Data**: For demonstration purposes, the project generates realistic sample data
- **Real Implementation**: The `data_collector.py` module can be extended to scrape actual Vahan data

### Data Assumptions
- **Vehicle Categories**: 2W (Two-Wheeler), 3W (Three-Wheeler), 4W (Four-Wheeler)
- **Time Period**: 3 years of historical data for trend analysis
- **Manufacturers**: Top manufacturers in each category included
- **Data Frequency**: Monthly registration data aggregated by quarters
- **Growth Calculations**: 
  - YoY Growth: Compared to same quarter previous year
  - QoQ Growth: Compared to previous quarter

## 🔧 Technical Implementation

### Technology Stack
- **Frontend**: Streamlit for interactive dashboard
- **Data Processing**: Pandas for data manipulation
- **Visualization**: Plotly for interactive charts
- **Data Collection**: Requests + BeautifulSoup for web scraping
- **Storage**: CSV files for data persistence

### Key Functions
- `VahanDataCollector`: Handles data collection and sample data generation
- `calculate_growth_metrics()`: Computes YoY and QoQ growth rates
- `create_trend_chart()`: Generates trend visualization charts
- `create_growth_chart()`: Creates growth percentage charts

## 📊 Dashboard Usage

### Navigation
1. **Filters Panel**: Use sidebar to select date ranges, vehicle categories, and manufacturers
2. **KPI Section**: View high-level metrics and performance indicators
3. **Growth Analysis**: Analyze trends and growth patterns
4. **Manufacturer Performance**: Compare top manufacturers and their growth
5. **Data Tables**: Access detailed quarterly data with growth metrics

### Key Insights Available
- Total vehicle registration volumes
- Category-wise market share and trends
- Manufacturer performance and market position
- Seasonal patterns and growth cycles
- Investment-grade insights and observations

## 🎯 Investment Insights

The dashboard provides several key insights valuable for investors:

1. **Market Size**: Total addressable market size and growth trajectory
2. **Category Performance**: Which vehicle segments are growing fastest
3. **Manufacturer Analysis**: Market leaders and emerging players
4. **Seasonal Trends**: Understanding cyclical patterns for investment timing
5. **Growth Metrics**: Quantified YoY and QoQ growth for performance tracking

## 🛣️ Feature Roadmap

If development continues, consider implementing:

### Phase 2 Features
- [ ] Real-time data integration with Vahan API
- [ ] State-wise registration breakdown
- [ ] Electric vehicle trend analysis
- [ ] Predictive analytics and forecasting
- [ ] Export functionality for reports

### Phase 3 Enhancements
- [ ] Machine learning models for trend prediction
- [ ] Advanced statistical analysis
- [ ] Multi-dashboard architecture
- [ ] Real-time alerts for significant changes
- [ ] Integration with financial data sources

### Technical Improvements
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Automated data pipeline with scheduling
- [ ] Performance optimization for large datasets
- [ ] Mobile-responsive design
- [ ] User authentication and role management

## 🎥 Demo Video

**Dashboard Walkthrough Video:** [Watch Demo](https://drive.google.com/file/d/1PsQURXKM_BqsOzw8GRcl51TylJMSsMoG/view?usp=sharing)

*This video demonstrates the dashboard functionality, key features, and investment insights available through the interactive interface.*

## 📝 Notes

- This is a demonstration version using sample data
- For production use, implement proper data collection from Vahan APIs
- Consider rate limiting and ethical scraping practices
- Ensure compliance with data usage policies

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for improvements.

## 📄 License

This project is created for educational and demonstration purposes.