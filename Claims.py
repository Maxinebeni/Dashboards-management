import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime
teal_color = '#008040'  # Teal green color code
green_EC = '#138024'
tangerine_color = '#E66C37'  # Tangerine orange color code
st.markdown(
    """
    <style>
    .main-title{
        color: #e66c37
        text_align: center;
        font_size: 3rem;
        font_wight: bold;
        margin_bottom=.5rem;
        text_shadow: 1px 1px 2px rgba(0,0,0.1);
    }
    .reportview-container {
        background-color: #013220;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #013220;
        color: white;
    }
    .metric .metric-value {
        color: #008040;
    }
    .metric .mertic-title {
        color: #FFA500;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('''
    <style>
        .main-title {
            color: #E66C37; /* Title color */
            text-align: center; /* Center align the title */
            font-size: 3rem; /* Title font size */
            font-weight: bold; /* Title font weight */
            margin-bottom: .5rem; /* Space below the title */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Subtle text shadow */
        }
        div.block-container {
            padding-top: 2rem; /* Padding for main content */
        }
    </style>
''', unsafe_allow_html=True)
# Your Streamlit app content
st.markdown('<h1 class = "main-title">CLAIMS DASHBOARD</h1>', unsafe_allow_html=True)


# Define colors to match the image
color_palette = ['#1d340d', '#DEB887', '#FF4500', '#556B2F', '#32CD32', '#8B4513', '#FFA07A', '#006400']
# Loading the data
@st.cache_data
def load_data():
    # Replace this with your actual data loading method
    df = df= pd.read_excel('Claims_2023_2024.xlsx')
    df['Date Of Diagnosis'] = pd.to_datetime(df['Date Of Diagnosis'])
    df['Claim Created Date'] = pd.to_datetime(df['Claim Created Date'])
    return df
df = load_data()
# Convert 'Date' column to datetime
df["Claim Created Date"] = pd.to_datetime(df["Claim Created Date"])
# Get minimum and maximum dates for the date input
startDate = df["Claim Created Date"].min()
endDate = df["Claim Created Date"].max()
# Define CSS for the styled date input boxes
st.markdown("""
    <style>
    .date-input-box {
        border-radius: 10px;
        text-align: left;
        margin: 5px;
        font-size: 1.2em;
        font-weight: bold;
    }
    .date-input-title {
        font-size: 1.2em;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Create 2-column layout for date inputs
col1, col2 = st.columns(2)
# Function to display date input in styled boxes
def display_date_input(col, title, default_date, min_date, max_date):
    col.markdown(f"""
        <div class="date-input-box">
            <div class="date-input-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    return col.date_input("", default_date, min_value=min_date, max_value=max_date)
# Display date inputs
with col1:
    date1 = pd.to_datetime(display_date_input(col1, "Start Date", startDate, startDate, endDate))
with col2:
    date2 = pd.to_datetime(display_date_input(col2, "End Date", endDate, startDate, endDate))
# Filter DataFrame based on the selected dates
df = df[(df["Claim Created Date"] >= date1) & (df["Claim Created Date"] <= date2)].copy()
# Sidebar
# Sidebar for filters
st.sidebar.header("Filters")
year = st.sidebar.multiselect("Select Year", options=sorted(df['Year'].unique()))
month = st.sidebar.multiselect("Select Month", options=sorted(df['Month'].unique()))
status = st.sidebar.multiselect("Select Status", options=df['Claim Status'].unique())
employers = st.sidebar.multiselect("Select Employers", options=df['Employer Name'].unique())
providers = st.sidebar.multiselect("Select Providers", options=df['Provider Name'].unique())
# Metrics change
# if st.sidebar.button('Update Metrics'):
#     st.experimental_rerun()
# Apply filters
filtered_df = df
if year:
    filtered_df = filtered_df[filtered_df['Year'].isin(year)]
if month:
    filtered_df = filtered_df[filtered_df['Month'].isin(month)]
if status:
    filtered_df = filtered_df[filtered_df['Claim Status'].isin(status)]
if employers:
    filtered_df = filtered_df[filtered_df['Employer Name'].isin(employers)]
if providers:
    filtered_df = filtered_df[filtered_df['Provider Name'].isin(providers)]
# Calculate metrics
total_claimed_amount = filtered_df['Claim Amount'].sum()
total_claims = len(filtered_df)
approved_claim_amount = filtered_df['Approved Claim Amount'].sum()
approval_percentage = (filtered_df['Claim Status'] == 'Approved').mean() * 100
average_claim_amount = total_claimed_amount / total_claims if total_claims > 0 else 0

# Top metrics

st.markdown("""
    <style>
    .custom-subheader {
        color: #E66C37;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        padding: 10px;
        border-radius: 5px;
        display: inline-block;
    }
    .metric-box {
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin: 10px;
        font-size: 1.2em;
        font-weight: bold;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid #ddd;
    }
    .metric-title {
        color: #E66C37; /* Change this color to your preferred title color */
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    .metric-value {
        color: #008040;
        font-size: 2em;
    }
    </style>
    """, unsafe_allow_html=True)

def display_metric(col, title, value):
    col.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
display_metric(col1,"Total Amount", f"{total_claimed_amount:,.0f}")
display_metric(col5,"Total Claims", f"{total_claims:,}")
display_metric(col2,"Approved Amount", f"{approved_claim_amount:,.0f}")
display_metric(col4,"Approval Percentage", f"{approval_percentage:.2f}%")
display_metric(col3,"Average Amount", f"{average_claim_amount:,.2f}")
# Function to create Seaborn plot
def create_seaborn_plot(data, x, y, title, kind='bar', **kwargs):
    plt.figure(figsize=(10, 6))
    if kind == 'bar':
        sns.barplot(data=data, x=x, y=y, **kwargs)
    elif kind == 'line':
        sns.lineplot(data=data, x=x, y=y, **kwargs)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt

# Create two columns for side-by-side charts
col1, col2 = st.columns(2)

with col1:
    container1 = st.container()
    with container1:
        # Claim Types' Popularity
        st.markdown('<h2 class="custom-subheader">Claim Types Popularity</h2>', unsafe_allow_html=True)
        claim_types = filtered_df['Claim Type'].value_counts().reset_index()
        claim_types.columns = ['Claim Type', 'Number of Claims']
        claim_types['Percentage'] = claim_types['Number of Claims'] / claim_types['Number of Claims'].sum() * 100
        fig_claim_types = px.bar(claim_types, x='Percentage', y='Claim Type', orientation='h')
        fig_claim_types.update_traces(text=claim_types['Percentage'].round(2).astype(str) + '%', textposition='auto', marker_color=teal_color)
        fig_claim_types.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_claim_types, use_container_width=True)

    
        # Average Claim Type Amount (Doughnut chart)
        st.markdown('<h2 class="custom-subheader">Average Claim Type Amount</h2>', unsafe_allow_html=True)
        avg_claim_by_type = filtered_df.groupby('Claim Type')['Claim Amount'].mean().reset_index()
        fig_avg_claim_type = px.pie(avg_claim_by_type, values='Claim Amount', names='Claim Type' , hole=0.5, color_discrete_sequence=color_palette, height=400)
        fig_avg_claim_type.update_traces(textposition='inside', textinfo='percent')
        fig_avg_claim_type.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=80))
        st.plotly_chart(fig_avg_claim_type, use_container_width=True)

with col2:
    container2 = st.container()
    with container2:
        # Claim Amount by Year (Pie chart)
        st.markdown('<h2 class="custom-subheader"> Claim Amount Each Year</h2>', unsafe_allow_html=True)
        claim_by_year = filtered_df.groupby('Year')['Claim Amount'].sum().reset_index()
        fig_claim_by_year = px.pie(claim_by_year, values='Claim Amount', names='Year', color_discrete_sequence=('#1d340d', '#e66c37'), height=400)
        fig_claim_by_year.update_traces(textposition='inside', textinfo='percent')
        fig_claim_by_year.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=80))
        st.plotly_chart(fig_claim_by_year, use_container_width=True)
        # Claim sources (Bar chart)
        st.markdown('<h2 class="custom-subheader"> Claim Sources</h2>', unsafe_allow_html=True)
        claim_sources = filtered_df['Source'].value_counts().reset_index()
        claim_sources.columns = ['Source', 'Count']
        claim_sources['Percentage'] = claim_sources['Count'] / claim_sources['Count'].sum() * 100
        fig_sources = px.bar(claim_sources, y='Source', x='Percentage', orientation='h')
        fig_sources.update_traces(text=claim_sources['Percentage'].round(2).astype(str) + '%', textposition='auto', marker_color=teal_color)
        fig_sources.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_sources)
    
        

# Claim Amount Over Time (Two separate charts)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<h2 class="custom-subheader"> Claim Amount Over Time(2023)</h2>', unsafe_allow_html=True)
    claim_over_time_2023 = filtered_df[(filtered_df['Claim Created Date'] >= '2023-03-01') & (filtered_df['Claim Created Date'] <= '2023-10-31')]
    claim_over_time_2023 = claim_over_time_2023.groupby('Claim Created Date')['Claim Amount'].sum().reset_index()
    fig_claim_time_2023 = px.area(claim_over_time_2023, x='Claim Created Date', y='Claim Amount')
    fig_claim_time_2023.update_traces(line_color=teal_color)
    st.plotly_chart(fig_claim_time_2023, use_container_width=True)

with col2:
    st.markdown('<h2 class="custom-subheader"> Claim Amount Over Time(2024)</h2>', unsafe_allow_html=True)
    claim_over_time_2024 = filtered_df[(filtered_df['Claim Created Date'] >= '2024-01-01') & (filtered_df['Claim Created Date'] <= '2024-06-30')]
    claim_over_time_2024 = claim_over_time_2024.groupby('Claim Created Date')['Claim Amount'].sum().reset_index()
    fig_claim_time_2024 = px.area(claim_over_time_2024, x='Claim Created Date', y='Claim Amount')
    fig_claim_time_2024.update_traces(line_color=teal_color)
    st.plotly_chart(fig_claim_time_2024, use_container_width=True)
# Create two columns for side-by-side display
col1, col2 = st.columns(2)


# Service Providers' Claim Amount
provider_claims = filtered_df.groupby('Provider Name')['Claim Amount'].sum().sort_values(ascending=False).reset_index()

with col1:
    with st.expander("Top 10 Service Providers' Claim Amount"):   
        st.write(provider_claims.style.background_gradient(cmap="YlOrBr"))


# Employer Names and Claim Amount
with col2:
    with st.expander("Top 10 Employer Names and Claim Amount"):
        employer_claims = filtered_df.groupby('Employer Name')['Claim Amount'].sum().sort_values(ascending=False).reset_index()
        st.write(employer_claims.style.background_gradient(cmap="YlOrBr"))



    
    
with col1:
    # Claims by Days of the Month
    st.markdown('<h2 class="custom-subheader">Claims by Days of the Month</h2>', unsafe_allow_html=True)
    filtered_df['Day'] = filtered_df['Date Of Diagnosis'].dt.day
    claims_by_day = filtered_df.groupby('Day').agg({
       'Claim Amount': 'mean',
       'Claim ID': 'count'
    }).reset_index()
    claims_by_day.columns = ['Day', 'Average Claim Amount', 'Number of Claims']

    fig_claims_by_day = go.Figure()
    fig_claims_by_day.add_trace(go.Bar(x=claims_by_day['Day'], y=claims_by_day['Average Claim Amount'], name='Average Claim Amount', yaxis='y', marker_color=teal_color))
    fig_claims_by_day.add_trace(go.Scatter(x=claims_by_day['Day'], y=claims_by_day['Number of Claims'], name='Number of Claims', yaxis='y2', line_color=tangerine_color))
    fig_claims_by_day.update_layout(
        yaxis=dict(title="Average Claim Amount"),
        yaxis2=dict(title="Number of Claims", overlaying="y", side="right")
    )
    fig_claims_by_day.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_claims_by_day)
    # Service Providers' Claim Amount (Scrollable bar chart)
    st.markdown('<h2 class="custom-subheader"> Service Providers Claim Amount</h2>', unsafe_allow_html=True)
    provider_claims = filtered_df.groupby('Provider Name')['Claim Amount'].sum().sort_values(ascending=False).reset_index()
    fig_providers = px.bar(provider_claims, x='Claim Amount', y='Provider Name', orientation='h', height=1000)
    # fig_providers.update_traces(text=provider_claims['Claim Amount'].round(2), textposition='auto')
    fig_providers.update_traces(marker_color=teal_color)
    st.plotly_chart(fig_providers, use_container_width=True)
with col2:
# Total Claim Amount by Claim Type (Pie chart)
    st.markdown('<h2 class="custom-subheader">Claim Type Total Amount</h2>', unsafe_allow_html=True)
    total_claim_by_type = filtered_df.groupby('Claim Type')['Claim Amount'].sum().reset_index()
    fig_total_claim_type = px.pie(total_claim_by_type, values='Claim Amount', names='Claim Type', color_discrete_sequence=color_palette, height=400)
    fig_total_claim_type.update_traces(textposition='inside', textinfo='percent')
    fig_total_claim_type.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=80))
    st.plotly_chart(fig_total_claim_type, use_container_width=True)




   # Employers' Claim Amount (Scrollable bar chart)
    st.markdown('<h2 class="custom-subheader"> Employers Claim Amount</h2>', unsafe_allow_html=True)
    employer_claims = filtered_df.groupby('Employer Name')['Claim Amount'].sum().sort_values(ascending=False).reset_index()
    fig_employers = px.bar(employer_claims, x='Claim Amount', y='Employer Name', orientation='h', height=1000)
    fig_employers.update_traces(text=employer_claims['Claim Amount'].round(2), textposition='outside', marker_color=teal_color )
    st.plotly_chart(fig_employers, use_container_width=True)

import plotly.figure_factory as ff

with st.expander("Summary Table"):
        
        # Create the pivot table
        sub_specialisation_Year = pd.pivot_table(
            data=filtered_df,
            values="Claim Amount",
            index=["Claim Type"],
            columns="Month"
        )
        st.write(sub_specialisation_Year.style.background_gradient(cmap="YlOrBr"))