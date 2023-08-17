# Outil de pré-diagnostic de la collecte des docs admins

Diagnosis of unscraped administrative documents.

## Objective

Automates the identification of these 3 problems:
- The domain scraped is different than the one in the database 'Pensieve'
- The URL pattern is not authorised
- The crawler job has finished in Timeout

After identification, the diagnosis is held manually.

## Description

processor.extractor.extractor<br>
`SampleExtractor`<br>
    `get_as_dataframe` google sheet 'Grandes Collectivités: diagnostic et correction'<br>
    `get_not_scrapped` 'Scrappé?' = 'Non Scrappé' or 0<br>

processor.transformer.transformer<br>
`SampleTransformer` : creates a datafame containing all pieces of information necessary to perform the pre-diagnosti<br>
    `get_samples_domain` : extracts samples domain name in new column<br>
    `get_pensieve_domain` : extracts territory's domain name in Pensieve<br>
        `get_territory_uid`<br>
            `get_territories_infos` : creates dataframe from file with territories names and codes<br>
            `join_names_with_uids` : joins sample's df with infos df on the territory name<br>
        `request_pensieve` <br>
            `get_samples_uids` : extracts list of samples' unique territories codes from the dataframe<br>
            `request_pensieve` : calls API to get list of jsons containing name, uid and url for each territory<br>
            `normalize_request` : transform list of jsons into dataframe<br>
        `add_samples_pensieve_url` : joins dataframes to obtain a new column with each territory's associated pensieve url<br>
    
processor.diagnoser.domain_comparator<br>
`DomainComparator` : compare le DNS du sample et le DNS du territoire dans Pensieve<br> 

processor.diagnoser.pattern_comparator<br>
`PatternComparator` : compare le pattern du sample et les denied pattern du Scrapper<br>

processor.diagnoser.timeout_identifier<br>
`TimeoutIdentifier` : identifie les sample dont la collecte a finish en Timeout<br>
    
processor.transformer.exporter<br>
`SampleExporter` : Exporte le dataframe avec les diagnostics<br>

    