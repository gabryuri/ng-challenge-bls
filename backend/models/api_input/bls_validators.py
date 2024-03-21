from typing import Optional

from pydantic import BaseModel, Field, computed_field, validator


class SeriesDataValidator(BaseModel):
    series_id: str
    supersector_code: Optional[str]
    industry_code: Optional[str]
    data_type_code: Optional[str]
    seasonal: Optional[str]
    series_title: Optional[str]
    footnote_codes: Optional[str]
    begin_year: Optional[int]
    begin_period: Optional[str]
    end_year: Optional[int]
    end_period: Optional[str]

    @validator("series_id", pre=True)
    def strip_and_cast_to_float(cls, v):
        return v.strip()


class SuperSectorDataValidator(BaseModel):
    supersector_code: str
    supersector_name: Optional[str]


class PeriodDataValidator(BaseModel):
    period: str
    mm: Optional[str]
    month: Optional[str]


class DatatypeDataValidator(BaseModel):
    data_type_code: str
    data_type_text: Optional[str]


class CESSeriesDataValidator(BaseModel):
    series_id: str
    year: Optional[int]
    period: Optional[str]
    value: float
    footnote_codes: Optional[str]

    @validator("value", pre=True)
    def strip_and_cast_to_float(cls, v):
        if isinstance(v, str):
            try:
                return float(v.strip())
            except Exception as e:
                raise ValueError(f"Cannot convert to float: {e}")
        return v

    @validator("series_id", pre=True)
    def strip(cls, v):
        return v.strip()
