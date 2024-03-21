from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

landing_schema_name = "landing"
processed_schema_name = "processed"
Base = declarative_base()


class SeriesDefinitionsTable(Base):
    """
    SQLAlchemy model representing satellite location data in a database table.

    It stores geographic locations of satellites along with their corresponding details.
    The 'satellite_locations' table contains:
        object_id (the satellite's unique identifier),
        creation date,
        geographic location,
        longitude,
        latitude,
        is_lat_long_complete, a flag to indicate if both latitude and longitude are complete.
    """

    __tablename__ = "series_definitions"
    series_id = Column(String(255), primary_key=True)
    supersector_code = Column(String(255))
    industry_code = Column(String(255))
    data_type_code = Column(String(255))
    seasonal = Column(String(255))
    series_title = Column(String(255))
    footnote_codes = Column(String(255))
    begin_year = Column(Integer)
    begin_period = Column(String(255))
    end_year = Column(Integer)
    end_period = Column(String(255))

    __table_args__ = (PrimaryKeyConstraint("series_id"), {"schema": landing_schema_name})


class SuperSectorTable(Base):
    """
    SQLAlchemy model representing satellite location data in a database table.

    It stores geographic locations of satellites along with their corresponding details.
    The 'satellite_locations' table contains:
        object_id (the satellite's unique identifier),
        creation date,
        geographic location,
        longitude,
        latitude,
        is_lat_long_complete, a flag to indicate if both latitude and longitude are complete.
    """

    __tablename__ = "supersector"
    supersector_code = Column(String(255), primary_key=True)
    supersector_name = Column(String(255))

    __table_args__ = (PrimaryKeyConstraint("supersector_code"), {"schema": landing_schema_name})


class PeriodTable(Base):
    """
    SQLAlchemy model representing satellite location data in a database table.

    It stores geographic locations of satellites along with their corresponding details.
    The 'satellite_locations' table contains:
        object_id (the satellite's unique identifier),
        creation date,
        geographic location,
        longitude,
        latitude,
        is_lat_long_complete, a flag to indicate if both latitude and longitude are complete.
    """

    __tablename__ = "period"
    period = Column(String(255), primary_key=True)
    mm = Column(String(255))
    month = Column(String(255))

    __table_args__ = (PrimaryKeyConstraint("period"), {"schema": landing_schema_name})


class DatatypeIndexesTable(Base):
    __tablename__ = "datatype_indexes"
    data_type_code = Column(String(255), primary_key=True)
    data_type_text = Column(String(255))

    __table_args__ = (PrimaryKeyConstraint("data_type_code"), {"schema": landing_schema_name})


class CESSeriesTable(Base):
    __tablename__ = "ces_series"
    series_id = Column(String(255), primary_key=True)
    year = Column(Integer, primary_key=True)
    period = Column(String(255), primary_key=True)
    value = Column(Float)
    footnote_codes = Column(String(255))

    __table_args__ = (PrimaryKeyConstraint("series_id", "year", "period"), {"schema": landing_schema_name})


## Processed tables


class SupervisoryVsProduction(Base):
    __tablename__ = "supervisory_vs_production"

    decade = Column(Integer, primary_key=True)
    total_private_production_employees = Column(Float)
    total_supervisory_employees = Column(Float)
    pct_production_employees = Column(Float)
    pct_supervisory_employees = Column(Float)

    __table_args__ = (PrimaryKeyConstraint("decade"), {"schema": processed_schema_name})


class WomenEmploymentDecades(Base):
    __tablename__ = "women_employment_decades"

    decade = Column(Integer, primary_key=True)
    women_employment_thousands = Column(Float)
    total_employment_thousands = Column(Float)
    percentage_of_women = Column(Float)

    __table_args__ = (PrimaryKeyConstraint("decade"), {"schema": processed_schema_name})


class WomenEmployment(Base):
    __tablename__ = "women_employment"

    date = Column(String(255), primary_key=True)
    women_employment_thousands = Column(Float)
    total_employment_thousands = Column(Float)
    percentage_of_women = Column(Float)

    __table_args__ = (PrimaryKeyConstraint("date"), {"schema": processed_schema_name})