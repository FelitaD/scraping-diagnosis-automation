from argparse import ArgumentParser

from config import logger
from helpers.interface.gsheet_interface import GoogleSheetInterface
from processor.extractor.extractor import SampleExtractor, AWSExtractor, OfficialUrlsExtractor
from processor.aggregator.aggregator import DeniedUrlsAggregator, SampleAggregator
from processor.diagnoser.diagnoser import Diagnoser
from processor.exporter.exporter import Exporter


def parse_arguments():
    """Parse arguments from console."""
    parser = ArgumentParser()
    parser.add_argument('--gsheet', '-g', type=str, default="Grandes collectivités : diagnostic et correction", help="Name of google sheet.")
    parser.add_argument('--source_sheet', '-s', type=str, default="Echantillonnage et vérification", help="Sheet name to copy data from.")
    parser.add_argument('--destination_sheet', '-d', type=str, default="[Test] Echantillonnage et vérification", help="Sheet name to copy data in.")
    parser.add_argument('--infos_sheet', '-i', type=str, default="Priorisation interne", help="Sheet name to get territories uids from.")
    return parser.parse_args()


def main(args):
    gsheet = GoogleSheetInterface.client.open(args.gsheet)
    source_sheet = gsheet.worksheet(args.source_sheet)
    destination_sheet = gsheet.worksheet(args.destination_sheet)
    infos_sheet = gsheet.worksheet(args.infos_sheet)

    logger.info('-------------- Extracting data --------------------')
    sample_extractor = SampleExtractor(source_sheet)
    raw_data = sample_extractor.get_raw_data()
    unscraped_docs = sample_extractor.get_unscraped_docs(raw_data)

    AWSExtractor().get_crawler_deny_config()
    AWSExtractor().get_structured_collects()

    official_urls_extractor = OfficialUrlsExtractor(infos_sheet)
    official_urls = official_urls_extractor.get_official_urls()

    logger.info('-------------- Aggregating data --------------------')
    sample_aggregator = SampleAggregator(unscraped_docs, official_urls)
    aggregated_docs = sample_aggregator.aggregate()

    denied_urls = DeniedUrlsAggregator().get_denied_urls()

    logger.info('-------------- Diagnosing data --------------------')
    diagnosed_docs = Diagnoser().diagnose(aggregated_docs, denied_urls)

    logger.info('-------------- Exporting data --------------------')
    exporter = Exporter(destination_sheet, raw_data, diagnosed_docs)
    exporter.format_and_export()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
