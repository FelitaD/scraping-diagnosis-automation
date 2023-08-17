import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from botocore.exceptions import ClientError

from processor.extractor.extractor import SampleExtractor, DeniedUrlsExtractor


class SampleExtractorTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.SampleExtractor = SampleExtractor(sheet="Echantillonnage et vérification")

        cls.expected_raw_data = pd.DataFrame({'Nom': ['Bordeaux Métropole', 'Bordeaux Métropole', 'CA du Pays de Saint-Omer', 'Bouzel'],
                                                  'URL': ['https://www.bordeaux-metropole.fr/var/bdxmetro/storage/original/application/ce7dc6e05da7d379a06b1cefceadf22a.pdf',
                                                          'http://www.bordeaux-metropole.fr/export/html/pdf',
                                                          'http://213.32.116.52/webdelib/files/unzip//seance_21240/1_d1599047276402.pdf',
                                                          'http://www.bouzel.fr/fileadmin/Bouzel/2_Documents/CM_2014-2019/CM-16A291311.pdf'],
                                                  'Scrapé ?': ['A été scrapé', 0, "N'a pas été scrapé", "N'a pas été scrapé"],
                                                  'Diagnostic Non Scrapé': [np.nan, np.nan, np.nan, np.nan]})
        # print(self.expected_get_sample_data)
        cls.expected_unscraped_data = cls.expected_raw_data.copy()
        cls.expected_unscraped_data.drop([0], inplace=True)

    @patch('processor.extractor.extractor.get_as_dataframe')
    def test_get_raw_data(self, mocked_dataframe):
        mocked_dataframe.return_value = self.expected_raw_data
        assert_frame_equal(self.SampleExtractor.get_raw_data(), self.expected_raw_data)

    def test_get_unscraped_docs(self):
        assert_frame_equal(self.SampleExtractor.get_unscraped_docs(self.expected_raw_data), self.expected_unscraped_data)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.SampleExtractor = None


class DeniedUrlsExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.DeniedUrlsExtractor = DeniedUrlsExtractor()

    @patch('processor.extractor.extractor.s3')
    def test_get_crawler_deny_config(self, mocked_bucket):
        mocked_bucket.Bucket.download_file.return_value = {'denyDomain': 'https', 'denyPattern': '[0-9].[0-9].[0-9]\\.fr'}
        self.DeniedUrlsExtractor.get_crawler_deny_config()
        mocked_bucket.assert_called_once()

    @patch('processor.extractor.extractor.botocore') ## comment tester code dans except?
    def test_get_crawler_deny_config_with_Error(self, mocked_botocore):
        mocked_botocore.side_effet = ClientError
        with self.assertRaises(ClientError):
            self.DeniedUrlsExtractor.get_crawler_deny_config()
            mocked_botocore.assert_called_once()

    def tearDown(self) -> None:
        self.DeniedUrlsExtractor = None


if __name__ == '__main__':
    unittest.main()
