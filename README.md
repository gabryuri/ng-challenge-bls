# Bureau of Labor statistics CES Data pipeline
This project ingests, processes and presents data from the Current Employment Statistics of the U.S. Bureau of Labor Statistics. The main concepts adopted in this project are: 


**Infrastructure**
- Containerization
- Makefile commands - Dev experience
- PostgREST API


**Good practices**
- Ingestion through data streaming
- Data quality and validation (pydantic)
- ORM for a safe and RDBMS-agnostic approach
- Code testing
- Object Oriented Programming
  

## Usage 
to deploy this project, one can just use:

``` 
make deploy
 ```

Five containers will be created: 
1. Postgresql instance
2. PostgREST API
3. Swagger for the PostgREST API
4. Table initialization, Data import and processing (ephemeral)
5. Streamlit application

>Chrome tabs for both the swagger and the Streamlit application will also be opened (if you're using linux)

In case the chrome tabs don't open automatically, you can open the [swagger](http://127.0.0.1:8080/) and [Streamlit](http://localhost:8501/) in your browser.
## Key Components
This project is divided between backend (Ingestion and processing) and frontend (rendering of charts based on the data). 

**Backend**
- **`ingest_and_process.py`**: Responsible for setting up the database tables and triggering the data import process, which uses two interactors: 
  - **`BlsApiInteractor`**: Interacts with the API and consumes data in a streaming fashion into our database.
  - **`RDBMSInteractor`**: Entity used to insert data into the Postgres database, as well as execute SQL scripts.
- **Pydantic Modeling**: Located in `models/api_input/bls_validators.py`, it validates and adjusts incoming data.
- **ORM**: Within `backend/models/database/orm.py` is all the ORM modelling with SQLAlchemy, allowing us to have a standardized, safe and tool-agnostic modelling.
- **Data Processing**: Data processing between `landing` and `processed` schemas is done through SQL insert statements. Even though that could also be done through ORM, I wanted to showcase a simpler and faster approach to the data transformation.


## Querying data
> **Important:** Only processed datasets are available to be queried.
### Women employment in government data
The total women employment in government can be queried like so:
``` 
curl -X 'GET' \
  'http://0.0.0.0:3000/women_employment_decades' \
  -H 'accept: application/json' \
  -H 'Range-Unit: items'
```
Expected output: 
```
[
  {
    "date": "1964-01-01",
    "women_employment_thousands": 3640,
    "total_employment_thousands": 9562,
    "percentage_of_women": 0.3806734992679356
},
{
    "date": "1964-02-01",
    "women_employment_thousands": 3655,
    "total_employment_thousands": 9581,
    "percentage_of_women": 0.3814841874543367
},
{
    "date": "1964-03-01",
    "women_employment_thousands": 3674,
    "total_employment_thousands": 9611,
    "percentage_of_women": 0.38227031526376026
}
 ...]

```

### Women empolyment in government - Decade average
Similarly, one might query the decade average for the women employment in government positions like so: 

``` 
curl -X 'GET' \
  'http://0.0.0.0:3000/women_employment_decades' \
  -H 'accept: application/json' \
  -H 'Range-Unit: items'
```
Expected output:

```
[
  {
    "decade": 1990,
    "women_employment_thousands": 10600,
    "total_employment_thousands": 19285.75,
    "percentage_of_women": 0.549628611798867
  },
  {
    "decade": 1980,
    "women_employment_thousands": 8489.266666666666,
    "total_employment_thousands": 16669.266666666666,
    "percentage_of_women": 0.5092765528577542
  },
  ...]
```

### Supervisory vs production employees - Decade average
Lastly, the amount of production vs supervisory employees might be queried like so:
``` 
curl -X 'GET' \
  'http://0.0.0.0:3000/supervisory_vs_production' \
  -H 'accept: application/json' \
  -H 'Range-Unit: items'
```
Expected output: 
```
[
    {
        "decade": 1960,
        "total_private_production_employees": 43271,
        "total_supervisory_employees": 8552,
        "pct_production_employees": 0.834976747776084,
        "pct_supervisory_employees": 0.16502325222391603
    },
    {
        "decade": 1970,
        "total_private_production_employees": 53109,
        "total_supervisory_employees": 11256,
        "pct_production_employees": 0.8251223491027733,
        "pct_supervisory_employees": 0.17487765089722676
    },
    ...]
```

## Tests
The code inside this project is tested. In order to make sure a contribution does not break the pipeline, one can simply use: 

``` 
make test
 ```


## Final considerations 
- SQL vs ORM 
- Dataviz
- Ingestion - parameters
- Access control and secrets
