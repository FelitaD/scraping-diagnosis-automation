from gspread_dataframe import get_as_dataframe
import boto3
import botocore
from pathlib import Path
import pandas as pd
from pandas import DataFrame
from typing import List

from config import PROJECT_PATH
from helpers.interface.pensieve_interface import PensieveBasic


class SampleExtractor:
    """Extract sample data from Google Sheet API"""
    COLS_TO_KEEP = ['Nom', 'URL', 'Scrapé ?', 'Diagnostic Non Scrapé']

    def __init__(self, sheet):
        self.sheet = sheet
        self.docs = None
        self.unscraped_docs = None
        
    def get_raw_data(self):
        """Raw data including empty dimensions"""
        return get_as_dataframe(self.sheet)

    def get_unscraped_docs(self, raw_data):
        """Document that haven't been scraped"""
        docs = raw_data[self.COLS_TO_KEEP]
        return docs[(docs['Scrapé ?'] == 0) | (docs['Scrapé ?'] == "N'a pas été scrapé")]


class AWSExtractor:
    """Extract json file from AWS API and save file"""
    ADMIN_DOC_BUCKET = 's3-admindoc-config'
    PRD_RAW_FILES_BUCKET = 's3-prd-raw-files'

    DENY_CONFIG_KEY = 'crawler_deny_config.json'
    STRUCTURED_COLLECTS_KEY = 'collecte_monitoring/structured_collects.csv'

    deny_config_path = Path(PROJECT_PATH, 'data/crawler_deny_config.json')
    structured_collects_path = Path(PROJECT_PATH, 'data/structured_collects.csv')

    s3 = boto3.resource('s3')

    @classmethod
    def get_crawler_deny_config(cls):
        try:
            cls.s3.Bucket(cls.ADMIN_DOC_BUCKET).download_file(cls.DENY_CONFIG_KEY, str(cls.deny_config_path))
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

    @classmethod
    def get_structured_collects(cls):
        try:
            cls.s3.Bucket(cls.PRD_RAW_FILES_BUCKET).download_file(cls.STRUCTURED_COLLECTS_KEY, str(cls.structured_collects_path))
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise


class OfficialUrlsExtractor:
    """Extract sample territories information from Pensieve API"""

    def __init__(self, infos_sheet):
        self.infos_sheet = infos_sheet

    def get_official_urls(self) -> DataFrame:
        sample_uids = self.get_sample_uids()
        sample_database_infos = self.request_database(sample_uids)
        return self.remove_null_values(sample_database_infos)

    def get_sample_uids(self) -> List:
        sample_infos = get_as_dataframe(self.infos_sheet, usecols=['Kind', 'Code'])
        sample_infos.dropna(how='all', inplace=True)
        sample_infos['Code'] = sample_infos['Code'].map(lambda y: self.add_leading_zero(y), na_action='ignore')
        sample_infos['uids'] = sample_infos.apply(lambda z: str(z['Kind']) + z['Code'], axis=1)
        return list(set(sample_infos['uids']))

    @staticmethod
    def add_leading_zero(y):
        while len(str(int(y))) < 5:
            return '0' + str(int(y))
        return str(int(y))

    @staticmethod
    def request_database(sample_uids: List) -> List:
        sample_database_infos = []
        for uid in sample_uids:
            response = PensieveBasic.request(f'/territories/{uid}', method='GET')
            sample_database_infos.append(response)
        return sample_database_infos

    @staticmethod
    def remove_null_values(sample_database_infos: List) -> DataFrame:
        cleaned_sample_database_infos = []
        for val in sample_database_infos:
            if val:
                cleaned_sample_database_infos.append(val)
        return pd.DataFrame(cleaned_sample_database_infos)
