import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🚗 Vahan Vehicle Registration Test Dashboard")

# Test if basic Streamlit works
st.write("Dashboard is working!")

# Create simple test data
data = {
    'Vehicle_Type': ['2W', '3W', '4W', '2W', '3W', '4W'],
    'Registrations': [12000, 3000, 8000, 13000, 3200, 8500],
    'Month': ['Jan', 'Jan', 'Jan', 'Feb', 'Feb', 'Feb']
}

df = pd.DataFrame(data)

st.subheader("Sample Data")
st.dataframe(df)

# Simple chart
fig = px.bar(df, x='Vehicle_Type', y='Registrations', color='Month', 
             title="Vehicle Registrations by Type")
st.plotly_chart(fig, use_container_width=True)

st.success("Test dashboard is working properly!")