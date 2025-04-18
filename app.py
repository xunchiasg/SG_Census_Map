# Import libraries
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import geopandas as gpd

# Import cleaned data from Jupyter Notebook
try:
    # Load census data (CSV)
    df = pd.read_csv('./data/census_cleaned.csv')
    
    # Load GeoJSON
    gdf = gpd.read_file('./data/gdf_cleaned.geojson')
    
    # Merge on shared key
    df['Subzone'] = df['Subzone'].astype(str)
    gdf['Subzone'] = gdf['Subzone'].astype(str)
    merged = gdf.merge(df, on='Subzone', how='left')
    
    if merged.empty:
        raise ValueError("Merge resulted in empty DataFrame")
        
except Exception as e:
    print(f"Error loading data: {str(e)}")
    raise

# Initialize Dash app
app = Dash(__name__, title="Singapore Census Map")

# Calculate map center
gdf_projected = merged.to_crs(epsg=3857)
centroid = gdf_projected.geometry.centroid
map_center = {
    "lat": centroid.to_crs(epsg=4326).y.mean(),
    "lon": centroid.to_crs(epsg=4326).x.mean()
}

# Create the choropleth figure
fig = px.choropleth_mapbox(
    merged,
    geojson=merged.__geo_interface__,
    locations=merged.index,
    color="Subzone Total",  # Changed to show population total
    mapbox_style="carto-positron",
    zoom=10,
    center=map_center,
    color_continuous_scale="Viridis",
    hover_name="Subzone",
    hover_data=["Planning Area", "Region", "Subzone Total"],
    labels={
        "Subzone Total": "Population",
        "Planning Area": "Planning Area",
        "Region": "Region"
    }
)

# Simple bar chart of Total Population by Subzone
fig = px.bar(
    df,
    x='Subzone',
    y='Subzone Total',
    title='Total Population by Subzone',
    labels={'Subzone Total': 'Population'},
    color='Subzone Total',
    color_continuous_scale='Viridis'
)

fig.show()

# Update layout
fig.update_layout(
    margin={"r":0, "t":0, "l":0, "b":0},
    mapbox=dict(
        bearing=0,
        pitch=0
    )
)

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Singapore Census Choropleth Map", 
           style={
               "textAlign": "center",
               "padding": "20px",
               "backgroundColor": "#f8f9fa"
           }),
    dcc.Graph(
        id='census-map',
        figure=fig,
        style={"height": "90vh"}
    )
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
