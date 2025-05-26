#######################
# Import libraries
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

#######################
# Setting Page Configuration (default state)

st.set_page_config(page_title= "SG Population",
        page_icon = None, layout= "wide", initial_sidebar_state = "expanded")


#######################
# Load/Merge datasets for app  

# Population data
pop_data = pd.read_csv("data/census_cleaned.csv")

# Geospatial data
geo_data = gpd.read_file("data/gdf_cleaned.geojson")
    
# Merge left join on Subzone
pop_data['Subzone'] = pop_data['Subzone'].astype(str)
geo_data['Subzone'] = geo_data['Subzone'].astype(str)
    
merged_data = geo_data.merge(pop_data, on='Subzone', how='left')
    
if merged_data.empty:
    raise ValueError("Merge resulted in empty DataFrame")

#######################
# Sidebar
with st.sidebar:
    st.title("SG Census Dashboard")
    
    # Region Filter
    regions = ['All'] + sorted(merged_data['Region'].unique().tolist())
    # Select box for region 
    selected_region = st.selectbox('Select Region:', regions)
    
    # Filter data based on selection
    if selected_region == 'All':
        filtered_data = merged_data.copy()
    else:
        filtered_data = merged_data[merged_data['Region'] == selected_region]
    
    # About dropdown
    with st.expander("About"):
        st.write('''
                 
        This app contains a dashboard that visualises the demographic distribution of Singapore by geography from the 
        Population Census of 2020 conducted by the Singapore Department of Statistics (DOS). 
                 
        **Data Sources:**
        
        [Census Data](https://data.gov.sg/datasets/d_e7ae90176a68945837ad67892b898466/view?dataExplorerPage=39)
        
        [Geospatial Data](https://data.gov.sg/datasets?query=URA+masterplan&resultId=d_8594ae9ff96d0c708bc2af633048edfb&page=1)
        
        **Repository:** 
        
        [GitHub](https://github.com/xunchiasg/SG_Census_Map)
        
        ''')
              
#######################
# Main Dashboard Panel

# Key Population Metrics
col1, col2, col3, col4 = st.columns(4, gap="small", border=True)

# Population 
with col1:
    total_pop = filtered_data['Subzone Total'].sum()
    st.metric("Population", f"{total_pop:,.0f}")
    
# Number of districts
with col2:
    num_districts = filtered_data['Region'].nunique()
    st.metric("Districts", num_districts)    

#Number of subzones
with col3:
    num_subzones = filtered_data['Subzone'].nunique()
    st.metric("Subzones", num_subzones)    

# Percentage of district population against total population
with col4:
    if selected_region != 'All' and total_pop > 0:
        # Calculate total population of all regions
        total_sg_pop = merged_data['Subzone Total'].sum()
        # Calculate percentage for selected region
        district_pop_percentage = (filtered_data['Subzone Total'].sum() / total_sg_pop) * 100
        st.metric(
            "Population %", 
            f"{district_pop_percentage:.2f}%",
        )
    else:
        st.metric(
            "Population %", 
            "100%" if selected_region == 'All' else "N/A",
        )

# Choropleth Map
with st.container():

    # Create choropleth map
    fig = px.choropleth(
    filtered_data,
    geojson=filtered_data.geometry,
    locations=filtered_data.index,
    color='Subzone Total',
    color_continuous_scale="viridis",
    range_color=(0, filtered_data['Subzone Total'].max()),
    labels={'Subzone Total': 'Population'},
    hover_data={
        'Subzone': True,
        'Region': True,
        'Subzone Total': ':,.0f'
    }
)

    # Update map layout
    fig.update_geos(
    center=dict(lat=1.3521, lon=103.8198),
    projection_scale=500,
    visible=True,
    showcoastlines=False,
    showland=False
)

    fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0}
)
    
    st.plotly_chart(fig, use_container_width=True)


col5, col6 = st.columns(2, gap="small", border=False)

# Gender Distribution
with col5:
    # Sum gender totals
    total_males = filtered_data['Total Males'].sum()
    total_females = filtered_data['Total Females'].sum()
    
    # Create data for pie chart
    gender_data = pd.DataFrame({
        'Gender': ['Males', 'Females'],
        'Count': [total_males, total_females]
    })
    
    # Create pie chart
    fig = px.pie(
        gender_data,
        names='Gender',
        values='Count',
        title="Gender Distribution",
        hole=0.3,
        color_discrete_sequence=['#B57EDC', '#4A8123'], 
    )
    
    # Update layout
    fig.update_traces(
        textposition='inside',
        textinfo='percent+value',
        hovertemplate="<br>".join([
            "Gender: %{label}",
            "Count: %{value:,.0f}",
            "Percentage: %{percent}"
        ])
    )
    
    # Display chart
    st.plotly_chart(fig, use_container_width=True)

# Ethnic Distribution
with col6:
    
    # Sum ethnic totals
    total_chinese = filtered_data['Total Chinese'].sum()
    total_malays = filtered_data['Total Malays'].sum()
    total_indian = filtered_data['Total Indians'].sum()
    total_others = filtered_data['Total Others'].sum()
    
    # Data for pie chart
    ethnic_data = pd.DataFrame({
        'Ethnicity': ['Chinese', 'Malays', 'Indians', 'Others'],
        'Count': [total_chinese, total_malays, total_indian, total_others]
    })
    
      # Create pie chart
    fig = px.pie(
        ethnic_data,
        names='Ethnicity',
        values='Count',
        title="Ethnic Distribution",
        hole=0.3,
        color_discrete_sequence=['#2E8BC0', '#DA3C7C', '#3EB489', '#FFB400'],  
        )

       # Update layout
    fig.update_traces(
        textposition='inside',
        textinfo='percent+value',
        hovertemplate="<br>".join([
            "Gender: %{label}",
            "Count: %{value:,.0f}",
            "Percentage: %{percent}"
        ])
    )
    
    # Display chart
    st.plotly_chart(fig, use_container_width=True)
    
# Subzone Table
with st.container():

    st.subheader(f"Most populated subzones {f'in {selected_region}' if selected_region != 'All' else ''}")
    top_10 = (filtered_data
            .sort_values('Subzone Total', ascending=False)
            .head(10)[['Subzone', 'Subzone Total']]
            .reset_index(drop=True)
            .assign(Rank=lambda x: x.index + 1)
            .set_index('Rank'))
    top_10['Subzone Total'] = top_10['Subzone Total'].map('{:,.0f}'.format)
    st.dataframe(top_10, use_container_width=True)