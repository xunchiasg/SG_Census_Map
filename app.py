# Import libraries
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd

#----------------------------------------------------------------------------------------
# Import cleaned data from Jupyter Notebook as new dataframe
try:
    # Load cleaned census data (CSV)
    df = pd.read_csv('./data/census_cleaned.csv')
    
    # Load cleaned geospatial data (GEOJSON)
    gdf = gpd.read_file('./data/gdf_cleaned.geojson')
    
    # Merge on shared key
    df['Subzone'] = df['Subzone'].astype(str)
    gdf['Subzone'] = gdf['Subzone'].astype(str)
    df_merged = gdf.merge(df, on='Subzone', how='left')
    
    if df_merged.empty:
        raise ValueError("Merge resulted in empty DataFrame")
        
except Exception as e:
    print(f"Error loading data: {str(e)}")
    raise

#----------------------------------------------------------------------------------------

# def get_region_totals(region_name):
#     """
#     Function to sum all population totals for a given region.
#     """
#     region_data = df_merged[df_merged['Region'] == region_name]
#     return region_data['Subzone Total'].sum()

#----------------------------------------------------------------------------------------
# Dash App 

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# ***SIDEBAR***

# Sidebar Style 

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# About Accordion component (Sidebar)

about_card = dcc.Markdown(
    """
    The Singapore Department of Statistics (DOS) conducts demographic censuses every decade, with the most recent in 2020.
    This includes statistical information such as population demographics, housing and economic distributions.
    This app visualizes the 2020 census data in a geospatial format ustilizing Plotly Dash and GeoPandas against demarcated zoning regions and subzone within the 2019 Master Plan by the Urban Redevelopment Authority (URA).
    """)

data_card = dcc.Markdown(
    """
    The census data displayed sources its data from [data.gov.sg](https://data.gov.sg/), which serves as 
    the Singapore Goverement's offical open data portal, which usage is covered under its [open data license.](https://data.gov.sg/open-data-licence)
    
    [Census Data Source](https://data.gov.sg/datasets/d_e7ae90176a68945837ad67892b898466/view?dataExplorerPage=39)
    
    [Geospatial Data Source](https://data.gov.sg/datasets?query=URA+masterplan&resultId=d_8594ae9ff96d0c708bc2af633048edfb&page=1)
    
    """)

# Accordian to contain above cards 
info_dropdown = dbc.Accordion([
    dbc.AccordionItem(about_card, title="About"),
    dbc.AccordionItem(data_card, title="Data Sources"),
], start_collapsed=True)

# Sidebar component 

sidebar = html.Div(
    [
        html.H4("Singapore Census Map", className="display-4"),
        html.Hr(),
        html.P("A geospatial dashboard of census data", className="lead"),
        info_dropdown], style=SIDEBAR_STYLE,
)

# ***MAIN CONTENT***

# Main content styling 
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Content component 

content = html.Div(id="page-content", style=CONTENT_STYLE)

#----------------------------------------------------------------------------------------
# App layout 

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# ------------------------------------
# Callbacks
# ------------------------------------
# @app.callback(
#     Output('region-map', 'figure'),
#     Output('region-total', 'children'),
#     Input('region-dropdown', 'value')
# )
# def update_map(region_name):
#     filtered = df_merged[df_merged['Region'] == region_name]

#     fig = px.choropleth_mapbox(
#         filtered,
#         geojson=filtered.__geo_interface__,
#         locations=filtered.index,
#         color="Subzone Total",  # or change to another variable
#         mapbox_style="carto-positron",
#         zoom=10,
#         center=map_center,
#         color_continuous_scale="Viridis",
#         hover_name="Subzone",
#         labels={"Subzone Total": "Unemployment Rate"},
#     )

#     fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

#     total = get_region_total(region_name)
#     total_text = f"Total Subzone Population: {int(total):,}"

#     return fig, total_text

# ------------------------------------
# Run App
# ------------------------------------
if __name__ == '__main__':
    app.run(debug=True)