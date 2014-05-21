import json
import urllib2
import os
import csv
import calendar

print "Provide the API Endpoint"
endpoint = raw_input("Endpoint: ")

print "Provide an API Key"
api_key = raw_input("API Key: ")

print "Please Enter the Medicinal Products you wish to search for, comma seperated"
medicinalproducts_raw = raw_input("Products: ")
medicinalproducts_list = [x.strip() for x in medicinalproducts_raw.split(',')]
medicinalproducts = '+OR+'.join(medicinalproducts_list)
print medicinalproducts

print "Please enter the reactions you wish to search for, comma seperated"
reactions_raw = raw_input("Reactions: ")
reactions_list = [x.strip() for x in reactions_raw.split(',')]
reactions = '+OR+'.join(reactions_list)

serious = raw_input( "Only limit to serious cases? (Y/n): ")
if serious == "Y":
  seriousness = "+AND+serious:1"
elif serious == "y":
  seriousness = "+AND+serious:1"
else:
  seriousness = ""

filename = raw_input("Please provide an export filename (eg. mytest.csv): ")

# Now we're going to get a list of search dates

years = range(2004, 2014)
months = range(1, 13)

with open(filename, 'wb') as csvfile:
  countwriter = csv.writer(csvfile)
  for year in years:
    for month in months:
      startdate = "%s-%s-01" % (year, month)
      enddate = "%s-%s-%s" % (year, month, calendar.monthrange(year, month)[1])
      try:
        url = '%s?api_key=%s&search=patient.drug.medicinalproduct:(%s)+AND+patient.reaction.reactionmeddrapt:(%s)+AND+receivedate:[%s+TO+%s]%s' % (endpoint, api_key, medicinalproducts, reactions, startdate, enddate, seriousness)
        print url
        response = urllib2.urlopen(url)
        data = json.load(response)
        print "%s Reports Found" % data[0]['results']['total']
        countwriter.writerow((startdate, enddate, data[0]['results']['total']))
      except:
        print "No Reports Found"
        pass
