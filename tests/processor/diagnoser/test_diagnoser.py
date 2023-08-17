import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import unittest

from processor.diagnoser.diagnoser import Diagnoser


class DiagnoserTestCase(unittest.TestCase):
    def setUp(self):
        self.unscraped_docs = pd.DataFrame({'Nom': ['Bordeaux Métropole', 'CA du Pays de Saint-Omer', 'Bouzel'],
                                            'URL': ['http://plan.bordeaux.fr/export/html/pdf',
                                                    'http://213.32.116.52/webdelib/files/unzip//seance_21240/1_d1599047276402.pdf',
                                                    'http://www.bouzel.fr/reservation-de-salles/tarifs.pdf'],
                                            'Scrapé ?': [0, "N'a pas été scrapé", "N'a pas été scrapé"],
                                            'Diagnostic Non Scrapé': np.nan})

        self.denied_urls = {'denyPattern': ['.*/reservation-de-salle[s]?/.*', ".*callto:\\d+.*"],
                            'denyDomain': ['plan.bordeaux.fr', 'fr-fr.facebook.com']}
        self.Diagnoser = Diagnoser()

        self.diagnosed_docs = self.unscraped_docs.copy()
        self.diagnosed_docs['document_domain'] = ['plan.bordeaux.fr', '213.32.116.52', 'www.bouzel.fr']
        self.diagnosed_docs['Denied domain'] = [True, False, False]
        self.diagnosed_docs['Denied pattern'] = [False, False, True]
        self.diagnosed_docs['Diagnostic Non Scrapé'] = ['Denied domain',  np.nan, 'Denied pattern']

    def test_diagnose(self):
        assert_frame_equal(self.Diagnoser.diagnose(self.unscraped_docs, self.denied_urls), self.diagnosed_docs)

    def test_get_domain(self):
        actual = self.Diagnoser.get_domain('http://www.google.com/query')
        self.assertEqual(actual, 'www.google.com')

    def test_check_denied_domain(self):
        x = {'document_domain': 'plan.bordeaux.fr'}
        assert self.Diagnoser.check_denied_domain(x, self.denied_urls)

    def test_check_denied_pattern(self):
        # x = ['213.32.116.52', 'www.213.32.116.52', 'http://213.32.116.52']
        x = 'http://www.bouzel.fr/reservation-de-salles/tarifs.pdf'
        assert self.Diagnoser.check_denied_pattern(x, self.denied_urls)
        y = 'http://213.32.11.664'
        self.assertFalse(self.Diagnoser.check_denied_pattern(y, self.denied_urls))

    def tearDown(self):
        self.Diagnoser = None


if __name__ == '__main__':
    unittest.main()
