# SG Census Map
Geospatial analysis of Singapore population with data from data.gov.sg

## About 
[data.gov.sg](https://data.gov.sg/) is an open data platform by Open Goverment Products (OGP) which collates and maintains all publicly available datasets by various agencies and ministries under the Singapore government. The datasets and API endpoints on the portal are freely available for personal and commercial use [(Open data license)](https://data.gov.sg/open-data-licence).

## Population Metrices 
The Singapore Department of Statistics (DOS) is responsible for conducting census studies on the population of Singapore for policy planning and formulation. This includes the population distribution within the planning areas of the island as deliniated by the Urban Redevelopment Authority (URA) masterplan. 

![output](https://github.com/user-attachments/assets/8a3016b7-c6de-48c8-8be5-f4ce01de1650)

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

The workflow diagram the key criteria and processes undertaken to allow for key findings for the provided data. This includes the use of specific libraries (geopandas, beautifulsoup) in preparation to allow merging of the required datasets.

[]()

#### Census Dataset
Access to the dataset was done via API query, where general cleaning and data manipulation using pandas was required. This included: 

- General Change of Object Dtype to INT64
- Copy record of dataset totals at index 1 to new df copy
- Copy records which contain additions of subzones E.g. "Ang Mo Kio - Total' to new df copy as these indicate rounding up of subzone population for each district

#### Geospatial Dataset
Access to the dataset was done via API query. The response output was in in GEOJSON, along with data within a column containing tabled data in HTML format. This included variables such as subzones and their respective regions which had to be parsed via Beautiful Soup into the target dataframe. 

```
![SG_data_HTML](https://github.com/user-attachments/assets/33c08950-7253-4521-aac0-8ecf2d121d65)



```