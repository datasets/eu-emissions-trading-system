#import csv
#import os
import urllib
import zipfile
#import dataconverters.xls
#from operator import itemgetter
# first run the extract
# os.system('. scripts/constituents.sh')
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
        for line in infile:
            line = line.replace('\t',',')
            outfile.write(line)

    '''
    records = []
    with open(in_path) as f:
        for line in f:
            if len(line.split("\t"))==4 :
                records.append(line.split("\t"))
        #reader = csv.reader(f)
        #records = list(reader)

    #header = records[0]
    #header[0], header[1] = header[1], header[0]
    header = ['Age of Ice', 'CO2 Concentration', 'Age of Air', 'Depth']
    #records = records[21:]
    #print records[0]
    #return
    for i in records:
        i[3] = i[3].strip()
        i[0],i[1] = i[1],i[0] #exchange age of ice with depth
        i[1],i[3] = i[3],i[1] #exchange depth with ppm
    #print records[0]
    #sort in descending order of years BP
    records.reverse()
    #records = sorted(records, key=float(itemgetter(0)))
    #header = ['Date', 'Price (Dollars per million btu)']
    # data begins on row 4
    #records = records[3:]

    #header = [ [ fixsymbol(x[1]) ] for x in header ]

    writer = csv.writer(open(out_path, 'w'), lineterminator='\n')
    writer.writerow(header)
    writer.writerows(records)
'''
execute()
