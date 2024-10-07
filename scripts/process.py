import io
import os
import csv
import zipfile
import requests

source = "https://sdi.eea.europa.eu/datashare/s/SxpWTfMxkZSrpBo/download"
zip_file = "data.zip"

def download_zip(url, output_file):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded ZIP file to {output_file}")
    else:
        raise Exception(f"Failed to download file: {response.status_code}")

def process():
    try:
        download_zip(source, zip_file)
        
        # Open and process the ZIP file
        with zipfile.ZipFile(zip_file, 'r') as archive:
            for elem in archive.namelist():
                if 'CITL' in elem:
                    file_name = elem

            # Open the file from within the ZIP archive
            with archive.open(file_name, 'r') as f: 
                decoded_file = io.TextIOWrapper(f, encoding='utf-8')
                with open('data/eu-ets.csv', 'w', newline='') as f_out:
                    fieldnames = ['country_code','country','main activity sector name','ETS information','year','value','unit']
                    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
                    writer.writeheader()
                    # Use DictReader to read the tab-delimited file
                    for row in csv.DictReader(decoded_file, delimiter='\t'):
                        writer.writerow(row)

        os.remove(zip_file)
        print("Processing complete, ZIP file removed.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__=='__main__':
    process()
