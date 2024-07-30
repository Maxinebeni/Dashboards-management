import streamlit as st
import matplotlib.colors as mcolors
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


data = pd.read_csv('cleaned_data_visit.csv', encoding='ISO-8859-1')

data['visit_created_on'] = pd.to_datetime('1899-12-30') + pd.to_timedelta(data['visit_created_on'], 'D')


year = st.sidebar.selectbox("Year", options=["All"] + [2023, 2024])
quarter = st.sidebar.selectbox("Quarter", options=["All", "Q1", "Q2", "Q3", "Q4"])
month = st.sidebar.selectbox("Month", options=["All"] + [f"{pd.to_datetime(month, format='%m').strftime('%b')}" for month in range(1, 13)])
visit_type = st.sidebar.selectbox("Visit Type", options=["All"] + data['visit_type'].unique().tolist())


filtered_data = data.copy()
if year != "All":
    filtered_data = filtered_data[filtered_data['visit_created_on'].dt.year == int(year)]
if quarter != "All":
    quarters = {"Q1": [1, 2, 3], "Q2": [4, 5, 6], "Q3": [7, 8, 9], "Q4": [10, 11, 12]}
    filtered_data = filtered_data[filtered_data['visit_created_on'].dt.month.isin(quarters[quarter])]
if month != "All":
    month_num = pd.to_datetime(month, format='%b').month
    filtered_data = filtered_data[filtered_data['visit_created_on'].dt.month == month_num]
if visit_type != "All":
    filtered_data = filtered_data[filtered_data['visit_type'] == visit_type]


# Calculate day and night visits
day_visits = filtered_data[filtered_data['DayOrNight'] == 'Day'].shape[0]
night_visits = filtered_data[filtered_data['DayOrNight'] == 'Night'].shape[0]

# Plot Seasonal Visits using Plotly for interactivity

fig_seasonal_visits = go.Figure(data=[go.Pie(
    labels=["Day", "Night"],
    values=[day_visits, night_visits],
    textinfo='label+percent',  # Show labels, values, and percentages
    hoverinfo='label+percent',  
    marker=dict(colors=['#1d340d', '#FF4500']),
)])  


# Calculate total visits, average day visits, and average night visits
total_visits = filtered_data.shape[0]
average_day_visits = filtered_data[filtered_data['DayOrNight'] == 'Day'].shape[0] / 12  # Average per month
average_night_visits = filtered_data[filtered_data['DayOrNight'] == 'Night'].shape[0] / 12  # Average per month
average_visits = total_visits / filtered_data['visit_created_on'].dt.to_period('M').nunique()  # Average visits per month

filtered_data['visit_month'] = filtered_data['visit_created_on'].dt.to_period('M')
visits_by_month = filtered_data['visit_month'].value_counts().sort_index()
max_month = visits_by_month.idxmax()
max_month_visits = visits_by_month.max()
max_month_str = max_month.strftime('%b %Y')

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

st.markdown('<h1 class="main-title">SERVICE PROVIDER VISITS DASHBOARD</h1>', unsafe_allow_html=True)



filtered_data["preauth_date"] = pd.to_datetime(filtered_data["visit_created_on"])

# Get minimum and maximum dates for the date input
start_date = filtered_data["preauth_date"].min()
end_date = filtered_data["preauth_date"].max()

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
    date1 = pd.to_datetime(display_date_input(col1, "Start Date", start_date, start_date, end_date))

with col2:
    date2 = pd.to_datetime(display_date_input(col2, "End Date", end_date, start_date, end_date))

filtered_data= filtered_data[(filtered_data["preauth_date"] >= date1) & (filtered_data["preauth_date"] <= date2)].copy()



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
display_metric(col1, "Total Visits", f"{total_visits:.0f}")
display_metric(col2, "Total Day Visits", f"{day_visits:.0f}")
display_metric(col3, "Total Night Visits", f"{night_visits:.0f}")
display_metric(col4, "Average Visits", f"{average_visits:.2f}")
# Aggregate the data to count the number of preauthorizations by status


# Row 3: Rate Change Graph
col1, col2 = st.columns((2))

with col1:
    st.markdown('<h2 class="custom-subheader">Monthly Visits and Rate of Change</h2>', unsafe_allow_html=True)    

    monthly_change = visits_by_month.pct_change() * 100  

    # Create the bar chart for visits
    bar_trace = go.Bar(
        x=visits_by_month.index.astype(str),
        y=visits_by_month.values,
        name='Number of Visits',
        marker_color='#008040',
        opacity=0.7
    )

    # Create the line chart for rate of change
    line_trace = go.Scatter(
        x=visits_by_month.index.astype(str),
        y=monthly_change,
        name='Rate of Change (%)',
        mode='lines+markers',
        marker=dict(color='#FF4500'),
        line=dict(color='#FF4500', width=2)
    )

    # Create the figure and add both traces
    fig = go.Figure()
    fig.add_trace(bar_trace)
    fig.add_trace(line_trace)

    # Update layout
    fig.update_layout(
        xaxis=dict(title='Month'),
        yaxis=dict(title='Number of Visits'),
        yaxis2=dict(title='Rate of Change (%)', overlaying='y', side='right'),
        legend=dict(
            x=0.01,  # Position the legend inside the chart, close to the left
            y=0.99,  # Position the legend at the top
            xanchor='left',
            yanchor='top',
        ),
        height=600,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
    
with col2:
    st.markdown('<h2 class="custom-subheader">Seasonal Visits</h2>', unsafe_allow_html=True)    
    st.plotly_chart(fig_seasonal_visits, use_container_width=True)


cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Rate Of Change ViewData"):
        # Convert Series to DataFrame for styling
        monthly_change_df = monthly_change.to_frame(name='Rate of Change')
        st.write(monthly_change_df.style.background_gradient(cmap="YlOrBr"))

with cl2:
    with st.expander("Day and Night Visits"):
        day_night_visits = pd.DataFrame({
            "Type": ["Day", "Night"],
            "Count": [day_visits, night_visits]
        })
        st.write(day_night_visits.style.background_gradient(cmap="YlOrBr"))

# Visit Type Data
   
    
# Create pie chart for visit types
visits_by_type = filtered_data['visit_type'].value_counts()
labels = visits_by_type.index.tolist()
values = visits_by_type.values.tolist()
colors = ["#1d340d", "#e66c37", "#3b9442", "#f8a785", "#CC3636"]  # Example color palette

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.5,
    marker=dict(colors=colors[:len(labels)]),  # Ensure colors match number of labels
    textinfo='label+percent',  # Show label and percentage
    hoverinfo='label+percent'
)])

fig.update_layout(
    font=dict(color='black'),
    width=800,  
    height=600
)

# Top 10 Attending Doctor Specializations
top_specializations = filtered_data['attending_doctor_specialisation'].value_counts().head(10)
fig_specializations = go.Figure()

fig_specializations.add_trace(go.Bar(
    y=top_specializations.index,
    x=top_specializations.values,
    orientation='h',
    marker=dict(color='#008040'),
    text=top_specializations.values,
    textposition='none',  
    hoverinfo='x+text'
))

fig_specializations.update_layout(
    xaxis_title="Number of Visits",
    yaxis_title="Doctor Specialization",
    font=dict(color='white'),
    xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
    yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
    margin=dict(l=0, r=0, t=30, b=50)
)

# Displaying charts side by side
col1, col2 = st.columns((2))

with col1:
    st.markdown('<h2 class="custom-subheader">Visits by Visit Type</h2>', unsafe_allow_html=True) 
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<h2 class="custom-subheader">Top 10 Attending Doctor Specializations</h2>', unsafe_allow_html=True) 
    st.plotly_chart(fig_specializations, use_container_width=True)
 
cols1, cols2 = st.columns((2))

with cols1:
    with st.expander("Visit Type ViewData"):
        visit_count = filtered_data["visit_type"].value_counts().reset_index()
        visit_count.columns = ["Visit_type", "Count"]    
        st.write(visit_count.style.background_gradient(cmap="YlOrBr"))    

with cols2:
    with st.expander("Specializations ViewData"):
        # Convert Series to DataFrame for styling
        spec_count = filtered_data["attending_doctor_specialisation"].value_counts().reset_index()
        spec_count.columns = ["attending_doctor_specialisation", "Count"]  
        st.write(spec_count.style.background_gradient(cmap="YlOrBr"))


 
# AREA CHART# Group data by month and count visits
monthly_visits = data.groupby(data['visit_created_on'].dt.to_period('M')).size()
monthly_visits.index = monthly_visits.index.to_timestamp()


# Create a DataFrame for the monthly visits
monthly_visits_df = monthly_visits.reset_index()
monthly_visits_df.columns = ['Month', 'Number of Visits']
# Create area chart for visits per month
fig_area = go.Figure()

fig_area.add_trace(go.Scatter(
    x=monthly_visits.index,
    y=monthly_visits.values,
    fill='tozeroy',
    mode='lines+markers',
    marker=dict(color='#008040'),
    line=dict(color='#008040'),
    name='Number of Visits'
))

fig_area.update_layout(
    xaxis_title="Month",
    yaxis_title="Number of Visits",
    font=dict(color='white'),
    width=1200,  # Adjust width as needed
    height=600   # Adjust height as needed
)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.markdown('<h2 class="custom-subheader">Number of Visits Each Month</h2>', unsafe_allow_html=True)    

# Use a single column that spans the full width for the chart
st.plotly_chart(fig_area, use_container_width=True)

 
with st.expander("Time Series ViewData"):
    st.write(monthly_visits_df.style.background_gradient(cmap="YlOrBr"))
    
# Data
st.markdown("""
    <style>
    .chart-container {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .chart-container:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h2 class="custom-subheader">Month-Wise Visit Type Summary</h2>', unsafe_allow_html=True)

with st.expander("Summary Table"):
    colors = ["#527853", "#F9E8D9", "#F7B787", "#EE7214", "#B99470"]
    custom_cmap = mcolors.LinearSegmentedColormap.from_list("EarthyPalette", colors)
    
    st.markdown("Month-Wise Preauthorization By Amount Table")
    filtered_data["month"] = filtered_data["visit_created_on"].dt.month_name()
    
    # Create the pivot table
    sub_specialisation_Year = pd.pivot_table(
        data=filtered_data,
        values="visit_id",  # Assuming "PreAuth Amount" is the correct column name
        index=["visit_type"],
        columns="month",
        aggfunc='count'
    )
    
    st.write(sub_specialisation_Year.style.background_gradient(cmap="YlOrBr"))