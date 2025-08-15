import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os

# Page configuration
st.set_page_config(
    page_title="Vahan Vehicle Registration Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for investor-friendly styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .growth-positive {
        color: #28a745;
        font-weight: bold;
    }
    .growth-negative {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load vehicle registration data"""
    csv_path = "vehicle_data.csv"
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        # Generate sample data if CSV doesn't exist
        return generate_sample_data()

def generate_sample_data():
    """Generate sample vehicle registration data"""
    categories = ['2W', '3W', '4W']
    manufacturers = {
        '2W': ['Hero MotoCorp', 'Honda', 'TVS', 'Bajaj', 'Yamaha'],
        '3W': ['Bajaj', 'Mahindra', 'TVS', 'Piaggio', 'Atul Auto'],
        '4W': ['Maruti Suzuki', 'Hyundai', 'Tata', 'Mahindra', 'Kia']
    }
    
    data_points = []
    start_date = datetime.now() - timedelta(days=365*3)
    current_date = start_date
    
    while current_date <= datetime.now():
        for category in categories:
            for manufacturer in manufacturers[category]:
                base_registrations = {
                    '2W': np.random.randint(8000, 15000),
                    '3W': np.random.randint(1000, 3000),
                    '4W': np.random.randint(5000, 12000)
                }
                
                month_factor = 1 + 0.1 * np.sin(2 * np.pi * current_date.month / 12)
                year_growth = 1 + 0.05 * (current_date.year - start_date.year)
                registrations = int(base_registrations[category] * month_factor * year_growth)
                
                data_points.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'year': current_date.year,
                    'quarter': f"Q{((current_date.month-1)//3)+1}",
                    'month': current_date.month,
                    'vehicle_category': category,
                    'manufacturer': manufacturer,
                    'registrations': registrations
                })
        
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    
    return pd.DataFrame(data_points)

def calculate_growth_metrics(data, groupby_cols, value_col='registrations'):
    """Calculate YoY and QoQ growth metrics"""
    try:
        grouped = data.groupby(groupby_cols + ['year', 'quarter'])[value_col].sum().reset_index()
        grouped = grouped.sort_values(['year', 'quarter'] + groupby_cols)
        grouped['yoy_growth'] = grouped.groupby(groupby_cols)[value_col].pct_change(periods=4) * 100
        grouped['qoq_growth'] = grouped.groupby(groupby_cols)[value_col].pct_change(periods=1) * 100
        return grouped
    except Exception as e:
        st.error(f"Error calculating growth metrics: {e}")
        return pd.DataFrame()

def main():
    st.title("🚗 Vahan Vehicle Registration Analytics Dashboard")
    st.markdown("**Investor-focused insights into India's vehicle registration trends**")
    
    try:
        # Load data
        with st.spinner("Loading vehicle registration data..."):
            data = load_data()
        
        if data.empty:
            st.error("No data available. Please check your data source.")
            return
        
        # Convert date column
        data['date'] = pd.to_datetime(data['date'])
        
        # Sidebar filters
        st.sidebar.header("📊 Dashboard Filters")
        
        # Date range selection
        min_date = data['date'].min().date()
        max_date = data['date'].max().date()
        
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_data = data[(data['date'].dt.date >= start_date) & 
                               (data['date'].dt.date <= end_date)]
        else:
            filtered_data = data
        
        # Vehicle category filter
        categories = st.sidebar.multiselect(
            "Vehicle Categories",
            options=data['vehicle_category'].unique(),
            default=data['vehicle_category'].unique()
        )
        
        # Manufacturer filter
        manufacturers = st.sidebar.multiselect(
            "Manufacturers",
            options=sorted(data['manufacturer'].unique()),
            default=sorted(data['manufacturer'].unique())[:10]
        )
        
        # Apply filters
        filtered_data = filtered_data[
            (filtered_data['vehicle_category'].isin(categories)) &
            (filtered_data['manufacturer'].isin(manufacturers))
        ]
        
        if filtered_data.empty:
            st.warning("No data available for the selected filters.")
            return
        
        # Key metrics
        st.header("📈 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_registrations = filtered_data['registrations'].sum()
        with col1:
            st.metric("Total Registrations", f"{total_registrations:,}")
        
        monthly_avg = filtered_data.groupby(['year', 'month'])['registrations'].sum().mean()
        with col2:
            st.metric("Avg Monthly Registrations", f"{monthly_avg:,.0f}")
        
        top_category = filtered_data.groupby('vehicle_category')['registrations'].sum().idxmax()
        with col3:
            st.metric("Top Vehicle Category", top_category)
        
        top_manufacturer = filtered_data.groupby('manufacturer')['registrations'].sum().idxmax()
        with col4:
            st.metric("Top Manufacturer", top_manufacturer)
        
        # Growth analysis section
        st.header("📊 Growth Analysis")
        
        # Category trends
        st.subheader("Vehicle Category Analysis")
        col1, col2 = st.columns(2)
        
        category_trends = filtered_data.groupby(['date', 'vehicle_category'])['registrations'].sum().reset_index()
        
        with col1:
            fig_category = px.line(category_trends, x='date', y='registrations', 
                                  color='vehicle_category',
                                  title="Vehicle Category Trends")
            st.plotly_chart(fig_category, use_container_width=True)
        
        # Category growth chart
        category_growth = calculate_growth_metrics(filtered_data, ['vehicle_category'])
        if not category_growth.empty:
            latest_growth = category_growth.groupby('vehicle_category').tail(1)
            
            with col2:
                fig_growth = px.bar(latest_growth, x='vehicle_category', y='yoy_growth',
                                   title="Latest YoY Growth by Category",
                                   color='yoy_growth',
                                   color_continuous_scale='RdYlGn')
                st.plotly_chart(fig_growth, use_container_width=True)
        
        # Manufacturer analysis
        st.subheader("Top Manufacturer Performance")
        
        top_manufacturers = filtered_data.groupby('manufacturer')['registrations'].sum().nlargest(10)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_manu = px.bar(x=top_manufacturers.values, y=top_manufacturers.index,
                             orientation='h',
                             title="Top 10 Manufacturers by Total Registrations")
            fig_manu.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_manu, use_container_width=True)
        
        # Manufacturer growth matrix
        top_manu_names = top_manufacturers.index[:5]
        manu_data = filtered_data[filtered_data['manufacturer'].isin(top_manu_names)]
        manu_growth = calculate_growth_metrics(manu_data, ['manufacturer'])
        
        if not manu_growth.empty:
            manu_latest = manu_growth.groupby('manufacturer').tail(1)
            
            with col2:
                fig_manu_growth = px.scatter(manu_latest, x='yoy_growth', y='qoq_growth',
                                           size='registrations', hover_name='manufacturer',
                                           title="Growth Matrix: YoY vs QoQ (Top 5 Manufacturers)")
                fig_manu_growth.add_hline(y=0, line_dash="dash", line_color="gray")
                fig_manu_growth.add_vline(x=0, line_dash="dash", line_color="gray")
                st.plotly_chart(fig_manu_growth, use_container_width=True)
        
        # Summary data table
        st.header("📋 Recent Data Summary")
        summary_data = filtered_data.groupby(['year', 'quarter', 'vehicle_category']).agg({
            'registrations': 'sum'
        }).reset_index()
        
        summary_with_growth = calculate_growth_metrics(summary_data, ['vehicle_category'])
        if not summary_with_growth.empty:
            recent_data = summary_with_growth.tail(15)
            st.dataframe(
                recent_data[['year', 'quarter', 'vehicle_category', 'registrations', 'yoy_growth', 'qoq_growth']],
                use_container_width=True
            )
        
        # Investment insights
        st.header("💡 Key Investment Insights")
        
        insights = [
            f"📊 Dataset contains {len(filtered_data):,} registration records",
            f"🏆 {top_category} segment leads with {filtered_data[filtered_data['vehicle_category']==top_category]['registrations'].sum():,} registrations",
            f"🏭 {top_manufacturer} is the top manufacturer by volume",
            "📈 Dashboard shows quarterly trends and growth patterns",
            "🔍 Use filters to analyze specific segments and time periods"
        ]
        
        for insight in insights:
            st.info(insight)
        
        # Data source note
        st.markdown("---")
        st.caption("💡 This dashboard uses sample data for demonstration. In production, connect to live Vahan Dashboard APIs.")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("Please check the data source and try again.")

if __name__ == "__main__":
    main()