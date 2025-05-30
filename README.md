# SG Census Map
Geospatial dashboard app of Singapore population metrices with data from data.gov.sg

[Streamlit App](https://sgcensusmap-squidoo.streamlit.app/)

![screencap_1](https://github.com/user-attachments/assets/d9f4b301-3377-4b08-b3e2-8cd5b193c9a7)

## About 
[data.gov.sg](https://data.gov.sg/) is an open data platform by Open Goverment Products (OGP) which collates and maintains all publicly available datasets by various agencies and ministries under the Singapore government. The datasets and API endpoints on the portal are freely available for personal and commercial use [(Open data license)](https://data.gov.sg/open-data-licence).

## Population Metrices 
The Singapore Department of Statistics (DOS) is responsible for conducting census studies on the population of Singapore for policy planning and formulation. This includes the population distribution within the planning areas of the island as deliniated by the Urban Redevelopment Authority (URA) masterplan. 

As of 2024, Singapore has a total of 5 regions, subdivied into 55 planning areas and 332 subzones. 

## Census Data 
The following datasets within data.gov.sg were used.

[Resident Population by Planning Area/Subzone of Residence, Ethnic Group and Sex (Census of Population 2020)](https://data.gov.sg/datasets/d_e7ae90176a68945837ad67892b898466/view?dataExplorerPage=39)

[Master Plan 2019 Subzone Boundary (No Sea) (GEOJSON)](https://data.gov.sg/datasets?query=URA+masterplan&resultId=d_8594ae9ff96d0c708bc2af633048edfb&page=1)

Access to the above raw data would be done via the platform's Dataset API within the Jupyter Notebook environment via a standard GET request prior to further data manipulation via Pandas dataframe. 

```
import requests

dataset_id = "d_e7ae90176a68945837ad67892b898466"
url = "https://data.gov.sg/api/action/datastore_search?resource_id="  + dataset_id
        
response = requests.get(url)
print(response.json())
https
```
## Workflow 
This section provides an overview on the key steps undertaken to clean and import the data. For detailed steps, refer to 'SG_Census.ipynb'

### Preparation and Cleaning 

#### Census Dataset (pandas)
Access to the dataset was done via API query, where general cleaning and data manipulation using pandas was required. This included: 

- General Change of Object Dtype to INT64
- Copy record of dataset totals at index 1 to new df copy
- Copy records which contain additions of subzones E.g. "Ang Mo Kio - Total' to new df copy as these indicate rounding up of subzone population for each district

#### Geospatial Dataset (geopandas, beautifulsoup)
Access to the dataset was done via API query. The response output was in in GEOJSON, along with data within a column containing tabled data in HTML format. This included variables such as subzones and their respective regions which had to be parsed via Beautiful Soup into the target dataframe. 

```
<center><table><tr><th colspan='2' align='center'><em>Attributes</em></th></tr><tr bgcolor="#E3E3F3"> <th>SUBZONE_NO</th> <td>12</td> </tr><tr bgcolor=""> <th>SUBZONE_N</th> <td>DEPOT ROAD</td> </tr><tr bgcolor="#E3E3F3"> <th>SUBZONE_C</th> <td>BMSZ12</td> </tr><tr bgcolor=""> <th>CA_IND</th> <td>N</td> </tr><tr bgcolor="#E3E3F3"> <th>PLN_AREA_N</th> <td>BUKIT MERAH</td> </tr><tr bgcolor=""> <th>PLN_AREA_C</th> <td>BM</td> </tr><tr bgcolor="#E3E3F3"> <th>REGION_N</th> <td>CENTRAL REGION</td> </tr><tr bgcolor=""> <th>REGION_C</th> <td>CR</td> </tr><tr bgcolor="#E3E3F3"> <th>INC_CRC</th> <td>C22DED671DE2A940</td> </tr><tr bgcolor=""> <th>FMEL_UPD_D</th> <td>20191223152313</td> </tr></table></center>
```
![SG_data_HTML](https://github.com/user-attachments/assets/a59ae490-9b6c-4f2a-b9ff-d6b1e1814f37)

gdf output post-cleaning: 
![SG_subzone](https://github.com/user-attachments/assets/83ecc789-eec5-4242-ae03-4ccf57e173c2)
*Subzone Map*
![SG_region](https://github.com/user-attachments/assets/734723d9-057e-40c7-9edd-3bb8b8179948)
*Region Map*

## Python Script (Streamlit)
[Streamlit](https://streamlit.io/) platform and library was used to create and deploy a Python script/dashboard containing the above demographic data derived through the above steps, and includes the use of Plotly graphing library within. 
