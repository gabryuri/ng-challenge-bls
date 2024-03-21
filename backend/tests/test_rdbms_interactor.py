import os

import unittest
from unittest.mock import patch, MagicMock

from backend.scripts.importer.rdbms_interactor import RDBMSInteractor


def build_test_base_path():
    return "/".join(os.path.dirname(os.path.realpath(__file__)).split("/"))


class MockModel:
    id: float
    name: str


class TestRDBMSInteractor(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock()
        self.mock_engine = MagicMock()
        self.rdbms_interactor = RDBMSInteractor(self.mock_logger, self.mock_engine)

    @patch("backend.scripts.importer.rdbms_interactor.RDBMSInteractor.run_single_sql_script")
    def test_run_single_sql_script(self, mock_run_single_script):
        mock_directory_path = "path/to/sql/directory"
        mock_sql_file_name = "dummy_query.sql"

        with patch("os.listdir", return_value=[mock_sql_file_name]), patch(
            "os.path.join", return_value=mock_directory_path + "/" + mock_sql_file_name
        ):
            self.rdbms_interactor.run_sql_scripts_from_directory(mock_directory_path)

            mock_run_single_script.assert_called_once_with(mock_directory_path + "/" + mock_sql_file_name)

    @patch("backend.scripts.importer.rdbms_interactor.RDBMSInteractor.run_single_sql_script")
    def test_run_sql_scripts_from_directory(self, mock_run_single):
        directory_path = f"{build_test_base_path()}/fixtures"

        self.rdbms_interactor.run_sql_scripts_from_directory(directory_path)

        expected_calls = [
            unittest.mock.call(f"{directory_path}/dummy_query.sql"),
            unittest.mock.call(f"{directory_path}/test_query.sql"),
        ]
        mock_run_single.assert_has_calls(expected_calls, any_order=True)

        self.assertEqual(mock_run_single.call_count, 2)


if __name__ == "__main__":
    unittest.main()
