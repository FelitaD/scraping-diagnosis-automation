import unittest
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from processor.exporter.exporter import Exporter


class ExporterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw_data = pd.DataFrame({'Tour': [1, 1, 2],
                                      'Type collectivité': ['EPCI>100K', 'COMM>100K', 'COMM>100K'],
                                      'Nom': ['Bordeaux Métropole', 'CA du Pays de Saint-Omer', 'Bouzel'],
                                      'Type': np.nan,
                                      'URL': ['http://plan.bordeaux.fr/export/html/pdf',
                                              'http://213.32.116.52/webdelib/files/unzip//seance_21240/1_d1599047276402.pdf',
                                              'http://www.bouzel.fr/reservation-de-salles/tarifs.pdf'],
                                      'En front ?': np.nan,
                                      'Scrapé ?': [0, "N'a pas été scrapé", "N'a pas été scrapé"],
                                      'Diagnostic Non Scrapé': [np.nan, np.nan, np.nan]})

        cls.diagnosed_docs = pd.DataFrame({'Nom': ['Bordeaux Métropole', 'CA du Pays de Saint-Omer', 'Bouzel'],
                                            'URL': ['http://plan.bordeaux.fr/export/html/pdf',
                                                    'http://213.32.116.52/webdelib/files/unzip//seance_21240/1_d1599047276402.pdf',
                                                    'http://www.bouzel.fr/reservation-de-salles/tarifs.pdf'],
                                            'Scrapé ?': [0, "N'a pas été scrapé", "N'a pas été scrapé"],
                                            'Diagnostic Non Scrapé': ['Denied domain', np.nan, 'Denied pattern'],
                                            'document_domain': ['plan.bordeaux.fr', '213.32.116.52', 'www.bouzel.fr'],
                                            'Denied domain': [True, False, False],
                                            'Denied pattern': [False, False, True]})

        cls.Exporter = Exporter(sheet="Resultats diagnostic", raw_data=cls.raw_data, diagnosed_docs=cls.diagnosed_docs)

        cls.merged_results = pd.DataFrame({'Tour': [1, 1, 2],
                                 'Type collectivité': ['EPCI>100K', 'COMM>100K', 'COMM>100K'],
                                'Nom': ['Bordeaux Métropole', 'CA du Pays de Saint-Omer', 'Bouzel'],
                                'Type': np.nan,
                                'URL': ['http://plan.bordeaux.fr/export/html/pdf',
                                        'http://213.32.116.52/webdelib/files/unzip//seance_21240/1_d1599047276402.pdf',
                                        'http://www.bouzel.fr/reservation-de-salles/tarifs.pdf'],
                                'En front ?': np.nan,
                                'Scrapé ?': [0, "N'a pas été scrapé", "N'a pas été scrapé"],
                                'Diagnostic Non Scrapé_x': np.nan,
                                'Diagnostic Non Scrapé': ['Denied domain', np.nan, 'Denied pattern'],
                                'document_domain': ['plan.bordeaux.fr', '213.32.116.52', 'www.bouzel.fr'],
                                'Denied domain': [True, False, False],
                                'Denied pattern': [False, False, True]})

        cls.formatted_results = pd.DataFrame({
                                'Nom': ['Bordeaux Métropole', 'CA du Pays de Saint-Omer', 'Bouzel'],
                                'URL': ['http://plan.bordeaux.fr/export/html/pdf',
                                        'http://213.32.116.52/webdelib/files/unzip//seance_21240/1_d1599047276402.pdf',
                                        'http://www.bouzel.fr/reservation-de-salles/tarifs.pdf'],
                                'document_domain': ['plan.bordeaux.fr', '213.32.116.52', 'www.bouzel.fr'],
                                'Scrapé ?': [0, "N'a pas été scrapé", "N'a pas été scrapé"],
                                'Diagnostic Non Scrapé': ['Denied domain', np.nan, 'Denied pattern'],
                                'Diagnostic Manuel': '',
                                'Denied domain': [True, False, False],
                                'Denied pattern': [False, False, True]})

    def test_format_and_export(self):
        pass

    def test_merge(self):
        assert_frame_equal(self.Exporter.merge_results(), self.merged_results)

    def test_format(self):
        self.Exporter.merge_results()
        assert_frame_equal(self.Exporter.format_results(), self.formatted_results)

    def test_clear_google_sheet(self):
        pass

    def test_export(self):
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        cls.Exporter = None


if __name__ == '__main__':
    unittest.main()
