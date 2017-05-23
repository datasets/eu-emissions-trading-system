#import csv
#import os
import urllib
import zipfile
import csv

version = '19'
source = "http://www.eea.europa.eu/data-and-maps/data/\
european-union-emissions-trading-scheme-eu-ets-data-from-citl-7/\
eu-ets-data-download-latest-version/citl_v"+version+".zip/at_download/file"
zip = 'tmp/citl.zip'
csvfile = 'tmp/CITL_v'+version+'.csv'
out_path = 'data/eu-ets.csv'
def execute():
    print 'Trying to download from path:'
    print source
    urllib.urlretrieve(source, zip)

    with zipfile.ZipFile(zip,'r') as z:
        z.extractall('tmp/')

    with open(csvfile, 'r') as infile, open(out_path,'w') as outfile:
        csvreader = csv.reader(infile, delimiter='\t')
        csvwriter = csv.writer(outfile)
        csvwriter.writerows(csvreader)

execute()
