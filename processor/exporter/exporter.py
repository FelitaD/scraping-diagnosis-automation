from gspread_dataframe import set_with_dataframe


class Exporter:
    END_INDEX = 5000 # Number of rows estimated in google sheet
    COLS_TO_EXPORT = ['Nom', 'Type', 'URL', 'Scrapé ?', 'Diagnostic Non Scrapé', 'Diagnostic Manuel',
                       'document_domain', 'official_domain', 'Not official URL', 'Denied domain',
                      'Denied pattern', 'timeout_proportion', 'closespider_timeout', 'finished']

    def __init__(self, sheet, raw_data, diagnosed_docs):
        self.sheet = sheet
        self.raw_data = raw_data
        self.diagnosed_docs = diagnosed_docs
        self.diagnosed_raw_data = None

    def format_and_export(self):
        diagnosed_raw_data = self.merge_results()
        formated_sample = self.format_results(diagnosed_raw_data)
        self.clear_google_sheet()
        self.export_results(formated_sample)

    def merge_results(self):
        return self.raw_data.merge(self.diagnosed_docs, on=['Nom', 'URL', 'Scrapé ?'], how='left', suffixes=['_x', ''])

    @classmethod
    def format_results(cls, diagnosed_raw_data):
        formated_sample = diagnosed_raw_data.drop(['Diagnostic Non Scrapé_x'], axis=1)
        formated_sample['Diagnostic Manuel'] = ''
        formated_sample = formated_sample[cls.COLS_TO_EXPORT]
        formated_sample = formated_sample[(formated_sample['Scrapé ?'] == 0) | (formated_sample['Scrapé ?'] == "N'a pas été scrapé")]
        return formated_sample

    def clear_google_sheet(self):
        self.sheet.delete_dimension(dimension='ROWS', start_index=1, end_index=self.END_INDEX)

    def export_results(self, diagnosed_unscraped_docs):
        set_with_dataframe(self.sheet, diagnosed_unscraped_docs)

