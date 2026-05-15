import io
import os
import csv
import zipfile
import requests
import openpyxl
from collections import defaultdict

SOURCE_URL = "https://sdi.eea.europa.eu/datashare/s/b9SGaYerAH3HyX9/download"
COUNTRY_CODES_URL = "https://raw.githubusercontent.com/datasets/country-codes/main/data/country-codes.csv"
ZIP_FILE = "data.zip"

# Activity codes defined in Annex I of EU Directive 2003/87/EC
ACTIVITY_CODES = {
    '10':    '10 Aviation',
    '20':    '20 Combustion of fuels',
    '21':    '21 Refining of mineral oil',
    '22':    '22 Production of coke',
    '23':    '23 Metal ore roasting or sintering',
    '24':    '24 Production of pig iron or steel',
    '25':    '25 Production or processing of ferrous metals',
    '26':    '26 Production of primary aluminium',
    '27':    '27 Production of secondary aluminium',
    '28':    '28 Production or processing of non-ferrous metals',
    '29':    '29 Production of cement clinker',
    '30':    '30 Production of lime, or calcination of dolomite/magnesite',
    '31':    '31 Manufacture of glass',
    '32':    '32 Manufacture of ceramics',
    '33':    '33 Manufacture of mineral wool',
    '34':    '34 Production or processing of gypsum or plasterboard',
    '35':    '35 Production of pulp',
    '36':    '36 Production of paper or cardboard',
    '37':    '37 Production of carbon black',
    '38':    '38 Production of nitric acid',
    '39':    '39 Production of adipic acid',
    '40':    '40 Production of glyoxal and glyoxylic acid',
    '41':    '41 Production of ammonia',
    '42':    '42 Production of bulk chemicals',
    '43':    '43 Production of hydrogen and synthesis gas',
    '44':    '44 Production of soda ash and sodium bicarbonate',
    '45':    '45 Capture of greenhouse gases under Directive 2009/31/EC',
    '99':    '99 Other activity opted-in under Art. 24',
    '20-99': '20-99 All stationary installations',
    '21-99': '21-99 All industrial installations (excl. combustion)',
}

# The 8 sectors included in eu-ets-sector-emissions.csv
TOP_SECTOR_CODES = ['10', '20', '21', '24', '29', '30', '36', '42']

# Names for non-ISO country_code values used in the ETS dataset
FALLBACK_NAMES = {
    'XI': 'Northern Ireland',
    'Innovation fund': 'Innovation fund',
    'Modernisation Fund': 'Modernisation Fund',
    'NER 300 auctions': 'NER 300 auctions',
    'RRF': 'Recovery and Resilience Facility',
}


def build_country_lookup():
    resp = requests.get(COUNTRY_CODES_URL)
    resp.raise_for_status()
    lookup = {}
    for row in csv.DictReader(io.StringIO(resp.text)):
        code = row['ISO3166-1-Alpha-2'].strip()
        name = row['official_name_en'].strip()
        if code and name:
            lookup[code] = name
    lookup.update(FALLBACK_NAMES)
    return lookup


def process():
    print("Downloading EU ETS data...")
    resp = requests.get(SOURCE_URL)
    resp.raise_for_status()
    with open(ZIP_FILE, 'wb') as f:
        f.write(resp.content)

    print("Reading Excel file...")
    with zipfile.ZipFile(ZIP_FILE) as z:
        xlsx_name = next(n for n in z.namelist() if n.endswith('.xlsx') and 'ETS_Database' in n)
        wb = openpyxl.load_workbook(io.BytesIO(z.read(xlsx_name)), read_only=True)
    os.remove(ZIP_FILE)

    ws = wb['Sheet1']
    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    col = {name: idx for idx, name in enumerate(header)}
    data = rows[1:]
    print(f"Read {len(data)} data rows.")

    print("Fetching country names...")
    country_lookup = build_country_lookup()

    print("Writing eu-ets.csv...")
    ets_fields = ['country_code', 'country', 'main_activity_code', 'main_activity_name', 'citl_information', 'year', 'value']
    with open('data/eu-ets.csv', 'w', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=ets_fields, lineterminator='\n')
        writer.writeheader()
        for row in data:
            country_code = row[col['country_code']]
            code = row[col['main_activity_code']]
            writer.writerow({
                'country_code': country_code,
                'country': country_lookup.get(country_code, country_code),
                'main_activity_code': code,
                'main_activity_name': ACTIVITY_CODES.get(code, code),
                'citl_information': row[col['citl_information']],
                'year': row[col['year']],
                'value': row[col['value']],
            })

    print("Writing eu-ets-sector-emissions.csv...")
    sector_emissions = defaultdict(float)
    for row in data:
        code = row[col['main_activity_code']]
        citl = row[col['citl_information']]
        year = row[col['year']]
        value = row[col['value']]
        if citl == '2.1 EU-ETS Verified Emission' and isinstance(year, int) and code in TOP_SECTOR_CODES:
            sector_emissions[(code, year)] += value or 0

    with open('data/eu-ets-sector-emissions.csv', 'w', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=['sector', 'year', 'emissions_mt'], lineterminator='\n')
        writer.writeheader()
        for code in TOP_SECTOR_CODES:
            name = ACTIVITY_CODES[code]
            for year in sorted(y for (c, y) in sector_emissions if c == code):
                writer.writerow({
                    'sector': name,
                    'year': year,
                    'emissions_mt': round(sector_emissions[(code, year)] / 1e6, 2),
                })

    print("Done.")


if __name__ == '__main__':
    process()
