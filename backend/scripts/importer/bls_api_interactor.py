import requests
import json
import os
import datetime
import math
from pydantic import BaseModel

from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.inspection import inspect
from pydantic import BaseModel


class BLSApiInteractor:
    def __init__(self, logger, rdbms_interactor, batch_size=3000):
        self.__logger = logger
        self.rdbms_interactor = rdbms_interactor
        self.batch_size = batch_size

    class UnexpectedStatusCode(Exception):
        def __init__(self, status_code):
            self.message = f"Status code {status_code} received from API."
            super().__init__(self.message)

    @property
    def base_endpoint(self):
        return f"https://download.bls.gov/pub/time.series/ce/"

    def generate_endpoint_url(self, suffix="ce.series"):
        return os.path.join(self.base_endpoint.strip("/"), suffix)

    def generate_headers(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7,pt-BR;q=0.6,pt;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "download.bls.gov",
            "Pragma": "no-cache",
            "Referer": "https://download.bls.gov/pub/time.series/ce/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
        }
        return headers

    def validate_status(self, status_code):
        self.__logger.info(f"Validating API status code.")
        if status_code != 200:
            raise self.UnexpectedStatusCode(status_code)

    def retrieve_data(self, url_suffix, model, table):
        self.__logger.info(f"Retrieving {url_suffix} data.")
        headers = self.generate_headers()
        endpoint_url = self.generate_endpoint_url(url_suffix)
        response = requests.get(endpoint_url, headers=headers, stream=True)
        self.validate_status(response.status_code)

        first_line = True
        values_to_insert = []
        total_records = 0
        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                if first_line:
                    headers = [header.strip() for header in data.split("\t")]
                    first_line = False
                    continue

                data_list = data.split("\t")
                data_dict = dict(zip(headers, data_list))
                model_obj = model.model_validate(data_dict)
                values_to_insert.append(model_obj.dict())
                total_records += 1
                if len(values_to_insert) >= self.batch_size:
                    self.__logger.info(f"inserting, {len(values_to_insert)} records, index {total_records}")
                    self.rdbms_interactor.insert_data_to_rdbms(table, values_to_insert)
                    values_to_insert = []

        self.rdbms_interactor.insert_data_to_rdbms(table, values_to_insert)
        self.__logger.info(f"inserted remaining {len(values_to_insert)} records, total of {total_records} records.")

        return data
