import os
import csv
from django.contrib.gis.geos import GEOSGeometry
from django.db import IntegrityError

from contact.models import Zipcode


zipcode_csv = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'data/US.txt'))

zipcode_fields = ['country', 'code', 'city', 'state', 'point']
file_fields = ['country', 'code', 'city', 'stateFull', 'stateAbr',
               'county', 'countyCode', 'latitude', 'longitude']

def run(verbose=True):
    for row in csv.reader(open(zipcode_csv),delimiter=','):
        row_length = len(row)
        # file has trailing commas
        longitude = row_length -2;
        latitude = row_length -3;
        #print row[0], row[1],row[longitude],row[latitude]
        point = GEOSGeometry('POINT(%s %s)' % (row[longitude],row[latitude]))
        try:
            Zipcode.objects.create(country=row[0], code=row[1], city=row[2], state=row[4], point=point)
        except IntegrityError:
            print row[1]
        except:
            print row[4]

def update(verbose=True):
    for row in csv.reader(open(zipcode_csv),delimiter=','):
        try:
            zipcode = Zipcode.objects.get(code=row[1])
            zipcode.city = row[2]
            zipcode.state = row[4]
            zipcode.save()
        except:
            print row[2]
            print row[4]
