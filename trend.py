import json
import urllib2
import os
import csv
from datetime import date, timedelta as td
import datetime

print "Provide the API Endpoint"
endpoint = raw_input("Endpoint: ")

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

d1 = date(2004, 1, 1)
d2 = date(2013, 12, 31)
delta = d2 - d1

with open(filename, 'wb') as csvfile:
  countwriter = csv.writer(csvfile)
  for i in range (delta.days + 1):
    day = datetime.datetime.strftime(d1 + td(days=i), "%Y%m%d")
    try:
      print day
      print medicinalproducts
      print reactions
      print seriousness
      url = '%s?api_key=nuPx4MMK4OQVVyVzSC7Pf8ah9Or30idKCuVfmUAy&search=patient.drug.medicinalproduct:(%s)+AND+patient.reaction.reactionmeddrapt:(%s)+AND+receivedate:%s%s' % (endpoint, medicinalproducts, reactions, day, seriousness)
      print url
      response = urllib2.urlopen(url)
      data = json.load(response)
      countwriter.writerow((day, data[0]['results']['total']))
      print written
    except:
      print "fail"
      pass
    