import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotly.express as px
import pandas as pd
import openpyxl
import os
import warnings

warnings.filterwarnings('ignore')


# Centered and styled main title using inline styles
st.markdown('''
    <style>
        .main-title {
            color: #e66c37; /* Title color */
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

st.markdown('<h1 class="main-title">PREAUTHORISATION DASHBOARD</h1>', unsafe_allow_html=True)

df = pd.read_excel("preAuth_data.xlsx")


# Convert 'Date' column to datetime
df["preauth_date"] = pd.to_datetime(df["Date"])

# Get minimum and maximum dates for the date input
startDate = df["preauth_date"].min()
endDate = df["preauth_date"].max()

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
df = df[(df["preauth_date"] >= date1) & (df["preauth_date"] <= date2)].copy()

# Sidebar styling and logo
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content h2 {
        color: #007BFF; /* Change this color to your preferred title color */
        font-size: 1.5em;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-title {
        color: #e66c37;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-header {
        color: #e66c37; /* Change this color to your preferred header color */
        font-size: 2.5em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-multiselect {
        margin-bottom: 15px;
    }
    .sidebar .sidebar-content .logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content .logo img {
        max-width: 80%;
        height: auto;
        border-radius: 50%;
    }
            
    </style>
    """, unsafe_allow_html=True)

# Sidebar for filtering

# Year filter
st.sidebar.markdown('<div class="filter-title">Year</div>', unsafe_allow_html=True)
year = st.sidebar.multiselect("", df["year"].unique(), key='year', help="Select Year")

# Month filter
st.sidebar.markdown('<div class="filter-title">Month</div>', unsafe_allow_html=True)
month = st.sidebar.multiselect("", df["MonthName"].unique(), key='month', help="Select Month")

# Quarter filter
st.sidebar.markdown('<div class="filter-title">Quarter</div>', unsafe_allow_html=True)
quarter = st.sidebar.multiselect("", df["Quarter"].unique(), key='quarter', help="Select Quarter")

# Channel filter
st.sidebar.markdown('<div class="filter-title">Channel</div>', unsafe_allow_html=True)
channel = st.sidebar.multiselect("", df["Channel"].unique(), key='channel', help="Select Channel")

# Status filter
st.sidebar.markdown('<div class="filter-title">Status</div>', unsafe_allow_html=True)
status = st.sidebar.multiselect("", df["Status"].unique(), key='status', help="Select Status")

# Specialization filter
st.sidebar.markdown('<div class="filter-title">Specialization</div>', unsafe_allow_html=True)
specialization = st.sidebar.multiselect("", df["Specialisation"].unique(), key='specialization', help="Select Specialization")


# Apply filters using permutations and combinations with elif statements
if year and month and quarter and channel and status and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Quarter"].isin(quarter)) & (df["Channel"].isin(channel)) & 
                     (df["Status"].isin(status)) & (df["Specialisation"].isin(specialization))]
elif year and month and quarter and channel and status:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Quarter"].isin(quarter)) & (df["Channel"].isin(channel)) & 
                     (df["Status"].isin(status))]
elif year and month and quarter and channel and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Quarter"].isin(quarter)) & (df["Channel"].isin(channel)) & 
                     (df["Specialisation"].isin(specialization))]
elif year and month and quarter and status and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Quarter"].isin(quarter)) & (df["Status"].isin(status)) & 
                     (df["Specialisation"].isin(specialization))]
elif year and month and channel and status and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Channel"].isin(channel)) & (df["Status"].isin(status)) & 
                     (df["Specialisation"].isin(specialization))]
elif year and quarter and channel and status and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["Quarter"].isin(quarter)) & 
                     (df["Channel"].isin(channel)) & (df["Status"].isin(status)) & 
                     (df["Specialisation"].isin(specialization))]
elif month and quarter and channel and status and specialization:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Quarter"].isin(quarter)) & 
                     (df["Channel"].isin(channel)) & (df["Status"].isin(status)) & 
                     (df["Specialisation"].isin(specialization))]
elif year and month and quarter and channel:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Quarter"].isin(quarter)) & (df["Channel"].isin(channel))]
elif year and month and quarter and status:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Quarter"].isin(quarter)) & (df["Status"].isin(status))]
elif year and month and quarter and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Quarter"].isin(quarter)) & (df["Specialisation"].isin(specialization))]
elif year and month and channel and status:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Channel"].isin(channel)) & (df["Status"].isin(status))]
elif year and month and channel and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Channel"].isin(channel)) & (df["Specialisation"].isin(specialization))]
elif year and month and status and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Status"].isin(status)) & (df["Specialisation"].isin(specialization))]
elif year and quarter and channel and status:
    df_filtered = df[(df["year"].isin(year)) & (df["Quarter"].isin(quarter)) & 
                     (df["Channel"].isin(channel)) & (df["Status"].isin(status))]
elif year and quarter and channel and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["Quarter"].isin(quarter)) & 
                     (df["Channel"].isin(channel)) & (df["Specialisation"].isin(specialization))]
elif year and quarter and status and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["Quarter"].isin(quarter)) & 
                     (df["Status"].isin(status)) & (df["Specialisation"].isin(specialization))]
elif year and channel and status and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["Channel"].isin(channel)) & 
                     (df["Status"].isin(status)) & (df["Specialisation"].isin(specialization))]
elif month and quarter and channel and status:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Quarter"].isin(quarter)) & 
                     (df["Channel"].isin(channel)) & (df["Status"].isin(status))]
elif month and quarter and channel and specialization:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Quarter"].isin(quarter)) & 
                     (df["Channel"].isin(channel)) & (df["Specialisation"].isin(specialization))]
elif month and quarter and status and specialization:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Quarter"].isin(quarter)) & 
                     (df["Status"].isin(status)) & (df["Specialisation"].isin(specialization))]
elif month and channel and status and specialization:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Channel"].isin(channel)) & 
                     (df["Status"].isin(status)) & (df["Specialisation"].isin(specialization))]
elif quarter and channel and status and specialization:
    df_filtered = df[(df["Quarter"].isin(quarter)) & (df["Channel"].isin(channel)) & 
                     (df["Status"].isin(status)) & (df["Specialisation"].isin(specialization))]
elif year and month and quarter:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Quarter"].isin(quarter))]
elif year and month and channel:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Channel"].isin(channel))]
elif year and month and status:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Status"].isin(status))]
elif year and month and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month)) & 
                     (df["Specialisation"].isin(specialization))]
elif year and quarter and channel:
    df_filtered = df[(df["year"].isin(year)) & (df["Quarter"].isin(quarter)) & 
                     (df["Channel"].isin(channel))]
elif year and quarter and status:
    df_filtered = df[(df["year"].isin(year)) & (df["Quarter"].isin(quarter)) & 
                     (df["Status"].isin(status))]
elif year and quarter and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["Quarter"].isin(quarter)) & 
                     (df["Specialisation"].isin(specialization))]
elif year and channel and status:
    df_filtered = df[(df["year"].isin(year)) & (df["Channel"].isin(channel)) & 
                     (df["Status"].isin(status))]
elif year and channel and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["Channel"].isin(channel)) & 
                     (df["Specialisation"].isin(specialization))]
elif year and status and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["Status"].isin(status)) & 
                     (df["Specialisation"].isin(specialization))]
elif month and quarter and channel:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Quarter"].isin(quarter)) & 
                     (df["Channel"].isin(channel))]
elif month and quarter and status:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Quarter"].isin(quarter)) & 
                     (df["Status"].isin(status))]
elif month and quarter and specialization:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Quarter"].isin(quarter)) & 
                     (df["Specialisation"].isin(specialization))]
elif month and channel and status:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Channel"].isin(channel)) & 
                     (df["Status"].isin(status))]
elif month and channel and specialization:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Channel"].isin(channel)) & 
                     (df["Specialisation"].isin(specialization))]
elif month and status and specialization:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Status"].isin(status)) & 
                     (df["Specialisation"].isin(specialization))]
elif quarter and channel and status:
    df_filtered = df[(df["Quarter"].isin(quarter)) & (df["Channel"].isin(channel)) & 
                     (df["Status"].isin(status))]
elif quarter and channel and specialization:
    df_filtered = df[(df["Quarter"].isin(quarter)) & (df["Channel"].isin(channel)) & 
                     (df["Specialisation"].isin(specialization))]
elif quarter and status and specialization:
    df_filtered = df[(df["Quarter"].isin(quarter)) & (df["Status"].isin(status)) & 
                     (df["Specialisation"].isin(specialization))]
elif channel and status and specialization:
    df_filtered = df[(df["Channel"].isin(channel)) & (df["Status"].isin(status)) & 
                     (df["Specialisation"].isin(specialization))]
elif year and month:
    df_filtered = df[(df["year"].isin(year)) & (df["MonthName"].isin(month))]
elif year and quarter:
    df_filtered = df[(df["year"].isin(year)) & (df["Quarter"].isin(quarter))]
elif year and channel:
    df_filtered = df[(df["year"].isin(year)) & (df["Channel"].isin(channel))]
elif year and status:
    df_filtered = df[(df["year"].isin(year)) & (df["Status"].isin(status))]
elif year and specialization:
    df_filtered = df[(df["year"].isin(year)) & (df["Specialisation"].isin(specialization))]
elif month and quarter:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Quarter"].isin(quarter))]
elif month and channel:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Channel"].isin(channel))]
elif month and status:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Status"].isin(status))]
elif month and specialization:
    df_filtered = df[(df["MonthName"].isin(month)) & (df["Specialisation"].isin(specialization))]
elif quarter and channel:
    df_filtered = df[(df["Quarter"].isin(quarter)) & (df["Channel"].isin(channel))]
elif quarter and status:
    df_filtered = df[(df["Quarter"].isin(quarter)) & (df["Status"].isin(status))]
elif quarter and specialization:
    df_filtered = df[(df["Quarter"].isin(quarter)) & (df["Specialisation"].isin(specialization))]
elif channel and status:
    df_filtered = df[(df["Channel"].isin(channel)) & (df["Status"].isin(status))]
elif channel and specialization:
    df_filtered = df[(df["Channel"].isin(channel)) & (df["Specialisation"].isin(specialization))]
elif status and specialization:
    df_filtered = df[(df["Status"].isin(status)) & (df["Specialisation"].isin(specialization))]
elif year:
    df_filtered = df[df["year"].isin(year)]
elif month:
    df_filtered = df[df["MonthName"].isin(month)]
elif quarter:
    df_filtered = df[df["Quarter"].isin(quarter)]
elif channel:
    df_filtered = df[df["Channel"].isin(channel)]
elif status:
    df_filtered = df[df["Status"].isin(status)]
elif specialization:
    df_filtered = df[df["Specialisation"].isin(specialization)]
else:
    df_filtered = df


# Calculate metrics
total_preauth = float(df_filtered.shape[0])  # Convert to float
total_preauth_amount = df_filtered["PreAuth Amount"].sum()
total_approved_preauth = df_filtered[df_filtered["Status"] == "Approved"].shape[0]
approved_preauth_amount = df_filtered[df_filtered["Status"] == "Approved"]["PreAuth Amount"].sum()
percentage_approval = (total_approved_preauth / total_preauth) * 100

# Create 4-column layout for metric cards
col1, col2, col3, col4 = st.columns(4)

# Define CSS for the styled boxes
st.markdown("""
    <style>
    .custom-subheader {
        color: #e66c37;
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
        color: #e66c37; /* Change this color to your preferred title color */
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    .metric-value {
        color: #008040;
        font-size: 2em;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to display metrics in styled boxes
def display_metric(col, title, value):
    col.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)
# Display metrics
scaling_factor = 1_000_000  # For millions
scaled_total_preauth_amount = total_preauth_amount / scaling_factor
scaled_approved_preauth_amount = approved_preauth_amount / scaling_factor

# Display metrics
display_metric(col1, "Total PreAuths", f"{total_preauth:.0f}")
display_metric(col2, "Total PreAuth Amount", f"RWF {scaled_total_preauth_amount:.2f} M")
display_metric(col3, "Approved PreAuth Amount", f"RWF {scaled_approved_preauth_amount:.2f} M")
display_metric(col4, "Percentage of Approval", f"{percentage_approval:.2f}%")

specialization_count = df_filtered.groupby("Specialisation").size().reset_index(name='Number of PreAuth')

cols1, cols2 = st.columns((2))
# bar chart for PreAuth by Specialization

with cols1:
    st.markdown('<h2 class="custom-subheader">PreAuth By Specialization</h2>', unsafe_allow_html=True)    
    # Define custom colors
    custom_colors = ["#008040"] 
    
    # Create the bar chart with custom colors
    fig = px.bar(specialization_count, x="Specialisation", y="Number of PreAuth", template="seaborn",
                 color_discrete_sequence=custom_colors)
    
    fig.update_traces(textposition='outside')
    fig.update_layout(height=400) 
    
    st.plotly_chart(fig, use_container_width=True)
    

# Donut chart for PreAuth by Status
status_counts = df_filtered["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]
with cols2:
    st.markdown('<h2 class="custom-subheader">PreAuth By Status</h2>', unsafe_allow_html=True)    
 # Define custom colors
    custom_colors = ["#1d340d", "#e66c37", "#3b9442", "#f8a785", "#CC3636" ] 

    fig = px.pie(status_counts, names="Status", values="Count", hole=0.5, template = "plotly_dark", color_discrete_sequence=custom_colors)
    fig.update_traces(textposition='outside', textinfo='percent')
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=80))
    st.plotly_chart(fig, use_container_width=True, height = 200)


# view data in a table
cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Specialization ViewData"):
        st.write(specialization_count.style.background_gradient(cmap = "YlOrBr"))

with cl2:
    with st.expander("Status ViewData"):
        status_counts = df_filtered["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]    
        st.write(status_counts.style.background_gradient(cmap="YlOrBr"))    

# preauths by channel
channel = df_filtered["Channel"].value_counts().reset_index()
channel.columns = ["Channel", "Count"]

# pie chart for preauth by channel
with cl1:
    st.markdown('<h2 class="custom-subheader">PreAuth By Channel</h2>', unsafe_allow_html=True) 

    custom_colors = ["#461b09", "#e66c37", "#bf7353", "#1d340d", "#f8a785" ] 
   
    fig = px.pie(channel, names="Channel", values="Count", template = "seaborn", color_discrete_sequence=custom_colors)
    fig.update_traces(textposition='outside', textinfo='percent')
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=80))
    st.plotly_chart(fig, use_container_width=True, height = 200)

# bar chart for preauth amount

amount_df = df_filtered.groupby(by = ["Specialisation"], as_index = False)["PreAuth Amount"].sum()
with cl2:
    st.markdown('<h2 class="custom-subheader">PreAuth Amount By Specialization</h2>', unsafe_allow_html=True)    
    custom_colors = ["#008040"]  # Replace with your desired colors

    fig = px.histogram(amount_df, x="Specialisation", y="PreAuth Amount", template="seaborn", color_discrete_sequence=custom_colors)
    fig.update_traces(textposition='outside')
    fig.update_layout(height=400,
    )  # Adjust the height as needed
    st.plotly_chart(fig, use_container_width=True)

# view data for amount and channel

cls1, cls2 = st.columns((2))
with cls2:
    with st.expander("PreAuth Amount ViewData"):
        st.write(amount_df.style.format({'PreAuth Amount': '${:,.2f}'}).background_gradient(cmap="YlOrBr"))

with cls1:
    with st.expander("Channel ViewData"):
        channel = df_filtered["Channel"].value_counts().reset_index()
        channel.columns = ["Channel", "Count"]    
        st.write(channel.style.background_gradient(cmap="YlOrBr"))   

# time series chart
df_filtered["month_year"] = df_filtered["Date"].dt.to_period("M").dt.to_timestamp()


st.markdown('<h2 class="custom-subheader">PreAuth By Months Of The Year</h2>', unsafe_allow_html=True)    

custom_colors = ["#008040"]  # Replace with your desired colors

# Group by month_year and count the occurrences
area_chart = df_filtered.groupby(df_filtered["month_year"].dt.strftime("%Y:%b")).size().reset_index(name='Count')

    # Sort by the month_year
area_chart = area_chart.sort_values("month_year")

    # Plot the line chart
fig2 = px.area(area_chart, x="month_year", y="Count", height=500, template="gridon", color_discrete_sequence=custom_colors)
fig2.update_xaxes(tickangle=45)  # Rotate x-axis labels to 45 degrees for better readability
st.plotly_chart(fig2, use_container_width=True)


# time series view data

 
with st.expander("Time Series ViewData"):
    st.write(area_chart.style.background_gradient(cmap = "YlOrBr"))


st.markdown('<h2 class="custom-subheader">Month-Wise Preauthorization Summary</h2>', unsafe_allow_html=True)    

with st.expander("Summary_Table"):

    colors = ["#527853", "#F9E8D9", "#F7B787", "#EE7214", "#B99470"]
    custom_cmap = mcolors.LinearSegmentedColormap.from_list("EarthyPalette", colors)
    st.markdown("Month-Wise Preauthorization By Amount Table")
    df_filtered["month"] = df_filtered["Date"].dt.month_name()
    # Create the pivot table
    sub_specialisation_Year = pd.pivot_table(
        data=df_filtered,
        values="PreAuth Amount",
        index=["Specialisation"],
        columns="month"
    )
    st.write(sub_specialisation_Year.style.background_gradient(cmap="YlOrBr"))