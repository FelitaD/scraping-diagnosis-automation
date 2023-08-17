import json
import pandas as pd
from pandas import DataFrame
from typing import Dict
from pathlib import Path

from config import PROJECT_PATH


class DeniedUrlsAggregator:
    """Create list of denied patterns"""
    def __init__(self):
        self.path = Path(PROJECT_PATH / 'data' / 'crawler_deny_config.json')

    def get_denied_urls(self) -> Dict:
        with open(self.path, 'r') as file:
            return json.load(file)


class SampleAggregator:
    """Complete sample dataframe with information needed to perform diagnostic"""
    structured_collects_path = Path(PROJECT_PATH, 'data/structured_collects.csv')

    def __init__(self, unscraped_docs: DataFrame, official_urls: DataFrame):
        self.docs = unscraped_docs
        self.official_urls = official_urls
        self.aggregated_docs = None

    def aggregate(self):
        self.add_document_domain()
        self.add_official_domain()
        return self.add_timeout_proportion()

    @staticmethod
    def extract_dns(x):
        return x.split('/')[2]

    def add_document_domain(self):
        self.docs['document_domain'] = self.docs['URL'].map(lambda x: self.extract_dns(x), na_action='ignore')

    def add_official_domain(self):
        self.aggregated_docs = self.docs.merge(self.official_urls, left_on='Nom', right_on='name')
        self.aggregated_docs['official_domain'] = self.aggregated_docs['url']
        self.aggregated_docs['official_domain'] = self.aggregated_docs['official_domain'].map(lambda x: self.extract_dns(x), na_action='ignore')
        return self.aggregated_docs.drop(['url'], axis=1)

    def add_timeout_proportion(self):
        structured_collects = self.load_collects()
        structured_collects = structured_collects.pivot_table(index='territory_uid', columns='finish_reason', aggfunc='size', fill_value=0)
        sum_collects = structured_collects[['closespider_timeout', 'finished']].sum(axis=1)
        structured_collects['timeout_proportion'] = structured_collects['closespider_timeout'] / sum_collects
        self.aggregated_docs = structured_collects.merge(self.aggregated_docs, how='right', left_on='territory_uid', right_on='uid')
        return self.aggregated_docs

    @classmethod
    def load_collects(cls):
        return pd.read_csv(cls.structured_collects_path)
