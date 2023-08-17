import unittest
from unittest.mock import patch

from processor.aggregator.aggregator import DeniedUrlsAggregator


class DeniedUrlsAggregatorTestCase(unittest.TestCase):
    def setUp(self):
        self.DeniedUrlsAggregator = DeniedUrlsAggregator()

    @patch('processor.aggregator.aggregator.json')
    def test_get_denied_urls(self, mocked_json):
        mocked_json.load.return_value = {'denyPattern': [".*www\\.bordeaux-metropole\\.fr/export/html/pdf", '.*www\\.lillemetropole\\.fr/communique-de-presse.*keywords'],
                                         'denyDomain': ['education.fr', 'fr-fr.facebook.com']}
        self.DeniedUrlsAggregator.get_denied_urls()
        mocked_json.load.assert_called_once()
        assert self.DeniedUrlsAggregator.get_denied_urls()['denyPattern'] == [".*www\\.bordeaux-metropole\\.fr/export/html/pdf", '.*www\\.lillemetropole\\.fr/communique-de-presse.*keywords']
        assert self.DeniedUrlsAggregator.get_denied_urls()['denyDomain'] == ['education.fr', 'fr-fr.facebook.com']

    def tearDown(self) -> None:
        self.PatternAggregator = None


if __name__ == '__main__':
    unittest.main()
