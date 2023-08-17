import re
from pandas import DataFrame
from typing import Dict

from config import MAX_TIMEOUT_PROPORTION


class Diagnoser:
    def diagnose(self, docs: DataFrame, denied_urls: Dict):
        """Factory function : processes sample data until all diagnostics are run."""

        # Perform diagnostics
        docs['Denied domain'] = docs.apply(
            lambda x: self.is_denied_domain(x, denied_urls), axis=1)
        docs['Denied pattern'] = docs['URL'].map(
            lambda x: self.is_denied_pattern(x, denied_urls), na_action='ignore')
        docs['Not official URL'] = docs.apply(lambda x: self.is_not_official_url(x), axis=1)
        docs['Timeout over 50'] = docs.apply(lambda x: self.is_max_timeout_proportion(x), axis=1)

        # Gather diagnostics in one column
        docs.loc[docs['Denied pattern'] == True, 'Diagnostic Non Scrapé'] = 'Denied pattern'
        docs.loc[docs['Denied domain'] == True, 'Diagnostic Non Scrapé'] = 'Denied domain'
        docs.loc[docs['Not official URL'] == True, 'Diagnostic Non Scrapé'] = 'Not official URL'
        docs.loc[docs['Timeout over 50'] == True, 'Diagnostic Non Scrapé'] = 'Timeout over 50'
        return docs

    @staticmethod
    def is_denied_domain(x, denied_urls):
        return x['document_domain'] in denied_urls['denyDomain']

    @staticmethod
    def is_denied_pattern(x, denied_urls):
        for pattern in denied_urls['denyPattern']:
            re_obj = re.compile(pattern)
            return bool(re_obj.search(x))

    @staticmethod
    def is_not_official_url(x):
        """Compare sample domain with Pensieve domain."""
        regex = '(?:www\\.)?(.*)'
        official_match = re.search(regex, x['official_domain'])
        document_match = re.search(regex, x['document_domain'])
        return official_match.groups() != document_match.groups()

    @staticmethod
    def is_max_timeout_proportion(x):
        """Identify territories for which collects have finished in timeout in more than 50% cases."""
        return x['timeout_proportion'] > MAX_TIMEOUT_PROPORTION
