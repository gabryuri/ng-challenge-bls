import unittest
from unittest.mock import patch, MagicMock
from requests.models import Response
from backend.scripts.importer.bls_api_interactor import BLSApiInteractor
from sqlalchemy import Column, String, Float, Boolean, DateTime, PrimaryKeyConstraint
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base


from unittest.mock import patch, MagicMock, mock_open
import json
import os

Base = declarative_base()


class MockTable(Base):
    __tablename__ = "mock_tbl"
    id = Column(Float)
    name = Column(Float)
    is_lat_long_complete = Column(Boolean)
    __table_args__ = (PrimaryKeyConstraint("id"),)


class MockModel(BaseModel):
    id: float
    name: str

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def iter_lines(self, decode_unicode=False):
            for item in self.json_data:
                yield json.dumps(item).encode("utf-8")

    if args[0].endswith("ce.series"):
        return MockResponse([{"id": 1, "name": "this_is_a_mock_name"}], 200)
    elif args[0].endswith("ce.supersector"):
        return MockResponse([{"id": 2, "name": "this_is_another_mock_name"}], 200)

    return MockResponse(None, 404)


class TestBLSApiInteractor(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock()
        self.mock_rdbms_interactor = MagicMock()
        self.bls_api_interactor = BLSApiInteractor(
            logger=self.mock_logger, rdbms_interactor=self.mock_rdbms_interactor, batch_size=2
        )

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_should_insert_when_200_response(self, mock_get):
        self.bls_api_interactor.retrieve_data(url_suffix="ce.series", model=MockModel, table=MockTable)

        self.mock_rdbms_interactor.insert_data_to_rdbms.assert_called()

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_should_raise_error_when_error_response(self, mock_get):
        with self.assertRaises(self.bls_api_interactor.UnexpectedStatusCode):
            self.bls_api_interactor.retrieve_data(url_suffix="invalid.endpoint", model=MockModel, table=MockTable)

        self.mock_rdbms_interactor.insert_data_to_rdbms.assert_not_called()


if __name__ == "__main__":
    unittest.main()
