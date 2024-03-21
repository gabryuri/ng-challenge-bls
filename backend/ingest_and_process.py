import logging

from sqlalchemy import create_engine

from scripts.importer.bls_api_interactor import BLSApiInteractor
from scripts.importer.rdbms_interactor import RDBMSInteractor
from scripts.configuration.configuration import ConfigurationHelper

from models.database.orm import (
    SeriesDefinitionsTable,
    SuperSectorTable,
    PeriodTable,
    DatatypeIndexesTable,
    CESSeriesTable,
    Base,
)
from models.api_input.bls_validators import (
    SeriesDataValidator,
    SuperSectorDataValidator,
    PeriodDataValidator,
    DatatypeDataValidator,
    CESSeriesDataValidator,
)


logging.basicConfig(
    format="[%(levelname)s] [%(asctime)s][%(filename)-15s][%(lineno)4d] : %(message)s",
    level=logging.INFO,
    force=True,
)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
log = logging.getLogger()

config = ConfigurationHelper(log)
engine = create_engine(config.database_uri, echo=False)
Base.metadata.create_all(engine)

rdbms_interactor = RDBMSInteractor(log, engine=engine)
blsapi = BLSApiInteractor(log, rdbms_interactor=rdbms_interactor)
blsapi.retrieve_data(url_suffix="ce.series", model=SeriesDataValidator, table=SeriesDefinitionsTable)
blsapi.retrieve_data(url_suffix="ce.supersector", model=SuperSectorDataValidator, table=SuperSectorTable)
blsapi.retrieve_data(url_suffix="ce.period", model=PeriodDataValidator, table=PeriodTable)
blsapi.retrieve_data(url_suffix="ce.datatype", model=DatatypeDataValidator, table=DatatypeIndexesTable)
# blsapi.retrieve_data(url_suffix="ce.data.0.AllCESSeries", model=CESSeriesDataValidator, table=CESSeriesTable)


rdbms_interactor.run_sql_scripts_from_directory("models/database/")
