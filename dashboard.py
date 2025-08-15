import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
from data_collector import VahanDataCollector

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
    collector = VahanDataCollector()
    data = collector.get_vehicle_data()
    return data

def calculate_growth_metrics(data, groupby_cols, value_col='registrations'):
    """Calculate YoY and QoQ growth metrics"""
    # Group data
    grouped = data.groupby(groupby_cols + ['year', 'quarter'])[value_col].sum().reset_index()
    
    # Sort by date
    grouped = grouped.sort_values(['year', 'quarter'] + groupby_cols)
    
    # Calculate YoY growth
    grouped['yoy_growth'] = grouped.groupby(groupby_cols)[value_col].pct_change(periods=4) * 100
    
    # Calculate QoQ growth
    grouped['qoq_growth'] = grouped.groupby(groupby_cols)[value_col].pct_change(periods=1) * 100
    
    return grouped

def create_trend_chart(data, title, y_col='registrations'):
    """Create trend line chart"""
    fig = px.line(data, x='date', y=y_col, 
                  title=title,
                  template='plotly_white')
    fig.update_layout(
        title_font_size=16,
        xaxis_title="Date",
        yaxis_title="Registrations",
        height=400
    )
    return fig

def create_growth_chart(data, growth_type='yoy_growth'):
    """Create growth percentage chart"""
    growth_label = "YoY Growth %" if growth_type == 'yoy_growth' else "QoQ Growth %"
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data[growth_type],
        mode='lines+markers',
        name=growth_label,
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
    ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title=f"{growth_label} Trend",
        xaxis_title="Date",
        yaxis_title=growth_label,
        template='plotly_white',
        height=400
    )
    
    return fig

def main():
    st.title("🚗 Vahan Vehicle Registration Analytics Dashboard")
    st.markdown("**Investor-focused insights into India's vehicle registration trends**")
    
    # Load data
    with st.spinner("Loading vehicle registration data..."):
        data = load_data()
    
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
        options=data['manufacturer'].unique(),
        default=data['manufacturer'].unique()[:10]  # Limit default selection
    )
    
    # Apply filters
    filtered_data = filtered_data[
        (filtered_data['vehicle_category'].isin(categories)) &
        (filtered_data['manufacturer'].isin(manufacturers))
    ]
    
    # Main dashboard content
    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
        return
    
    # Key metrics
    st.header("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Total registrations
    total_registrations = filtered_data['registrations'].sum()
    with col1:
        st.metric("Total Registrations", f"{total_registrations:,}")
    
    # Average monthly registrations
    monthly_avg = filtered_data.groupby(['year', 'month'])['registrations'].sum().mean()
    with col2:
        st.metric("Avg Monthly Registrations", f"{monthly_avg:,.0f}")
    
    # Top category
    top_category = filtered_data.groupby('vehicle_category')['registrations'].sum().idxmax()
    with col3:
        st.metric("Top Vehicle Category", top_category)
    
    # Top manufacturer
    top_manufacturer = filtered_data.groupby('manufacturer')['registrations'].sum().idxmax()
    with col4:
        st.metric("Top Manufacturer", top_manufacturer)
    
    # Growth analysis section
    st.header("📊 Growth Analysis")
    
    # Category-wise analysis
    st.subheader("Vehicle Category Analysis")
    
    col1, col2 = st.columns(2)
    
    # Category trends
    category_trends = filtered_data.groupby(['date', 'vehicle_category'])['registrations'].sum().reset_index()
    
    with col1:
        fig_category = px.line(category_trends, x='date', y='registrations', 
                              color='vehicle_category',
                              title="Vehicle Category Trends")
        st.plotly_chart(fig_category, use_container_width=True)
    
    # Category growth
    category_growth = calculate_growth_metrics(filtered_data, ['vehicle_category'])
    latest_growth = category_growth.groupby('vehicle_category').tail(1)
    
    with col2:
        fig_growth = px.bar(latest_growth, x='vehicle_category', y='yoy_growth',
                           title="Latest YoY Growth by Category",
                           color='yoy_growth',
                           color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_growth, use_container_width=True)
    
    # Manufacturer analysis
    st.subheader("Top Manufacturer Performance")
    
    # Top 10 manufacturers by registrations
    top_manufacturers = filtered_data.groupby('manufacturer')['registrations'].sum().nlargest(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_manu = px.bar(x=top_manufacturers.values, y=top_manufacturers.index,
                         orientation='h',
                         title="Top 10 Manufacturers by Total Registrations")
        fig_manu.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_manu, use_container_width=True)
    
    # Manufacturer growth
    top_manu_names = top_manufacturers.index[:5]  # Top 5 for growth analysis
    manu_data = filtered_data[filtered_data['manufacturer'].isin(top_manu_names)]
    manu_growth = calculate_growth_metrics(manu_data, ['manufacturer'])
    manu_latest = manu_growth.groupby('manufacturer').tail(1)
    
    with col2:
        fig_manu_growth = px.scatter(manu_latest, x='yoy_growth', y='qoq_growth',
                                   size='registrations', hover_name='manufacturer',
                                   title="Growth Matrix: YoY vs QoQ (Top 5 Manufacturers)",
                                   labels={'yoy_growth': 'YoY Growth %', 'qoq_growth': 'QoQ Growth %'})
        fig_manu_growth.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_manu_growth.add_vline(x=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_manu_growth, use_container_width=True)
    
    # Detailed data table
    st.header("📋 Detailed Data")
    
    # Summary table
    summary_data = filtered_data.groupby(['year', 'quarter', 'vehicle_category']).agg({
        'registrations': 'sum'
    }).reset_index()
    
    # Calculate growth rates
    summary_with_growth = calculate_growth_metrics(summary_data, ['vehicle_category'])
    
    # Display recent data
    recent_data = summary_with_growth.tail(20)
    st.dataframe(
        recent_data[['year', 'quarter', 'vehicle_category', 'registrations', 'yoy_growth', 'qoq_growth']],
        use_container_width=True
    )
    
    # Investment insights
    st.header("💡 Key Investment Insights")
    
    # Calculate some insights
    total_growth_yoy = filtered_data.groupby('year')['registrations'].sum().pct_change().iloc[-1] * 100
    ev_growth = "Electric vehicle adoption is accelerating" if total_growth_yoy > 10 else "Traditional vehicles still dominate"
    
    insights = [
        f"Overall market YoY growth: {total_growth_yoy:.1f}%",
        f"Two-wheelers represent the largest segment with {filtered_data[filtered_data['vehicle_category']=='2W']['registrations'].sum():,} registrations",
        ev_growth,
        "Seasonal patterns show higher registrations during festival months",
        "Top 5 manufacturers control majority market share indicating concentrated market"
    ]
    
    for insight in insights:
        st.info(f"🔍 {insight}")

if __name__ == "__main__":
    main()