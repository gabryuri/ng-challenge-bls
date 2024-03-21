import os

from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.inspection import inspect


class RDBMSInteractor:
    def __init__(self, logger, engine):
        self.__logger = logger
        self.engine = engine

        self.session = Session(bind=self.engine)

    def insert_data_to_rdbms(self, table, values_to_insert: list[dict]) -> None:
        """
        Inserts a list of dictionary values into the specified table in the database.
        It also fetches the primary key to be able to use the ON CONFICT DO NOTHING statement.

        Parameters:
            table (Type[Base]): The SQLAlchemy table class into which data will be inserted.
            values_to_insert (list[dict]): A list of dictionaries representing the records to be inserted.

        Returns:
            None
        """
        primary_keys = self.__fetch_table_primary_key(table)

        insert_stmt = insert(table).values(values_to_insert)
        conflict_stmt = insert_stmt.on_conflict_do_nothing(index_elements=primary_keys)
        self.session.execute(conflict_stmt)
        self.session.commit()

    def run_single_sql_script(self, file_path: str) -> None:
        """
        Executes a SQL script from a specified file path.

        Parameters:
            file_path (str): The path to the SQL script file to be executed.

        Returns:
            None
        """
        try:
            with open(file_path, "r") as file:
                sql_script = file.read()
            with self.engine.connect() as connection:
                connection.execute(text(sql_script))
                connection.commit()
            self.__logger.info(f"Successfully executed SQL script: {file_path}")
        except Exception as e:
            self.__logger.error(f"Failed to execute SQL script {file_path}: {e}")

    def run_sql_scripts_from_directory(self, directory_path: str) -> None:
        """
        Executes all SQL scripts found in a specified directory.

        Parameters:
            directory_path (str): The path to the directory containing SQL script files.

        Returns:
            None
        """
        self.__logger.info(f"Running SQL scripts from directory {directory_path}")

        for filename in os.listdir(directory_path):
            if filename.endswith(".sql"):
                file_path = os.path.join(directory_path, filename)
                self.run_single_sql_script(file_path)

    def __fetch_table_primary_key(self, table) -> list[str]:
        primary_keys = [key.name for key in inspect(table).primary_key]
        return primary_keys
