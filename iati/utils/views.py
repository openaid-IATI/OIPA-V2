# Django specific
import json
from django.db import connection
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from django.views.generic import FormView
from data.models.common import IndicatorData
from utils.forms import UploadForm
from django.core.urlresolvers import reverse

import pdb

class JSONResponse(HttpResponse):
    def __init__(self, data):
        output = simplejson.dumps(data)
        super(JSONResponse, self).__init__(output, mimetype="text/javascript")

def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer


def render_json(func):
    def wrapper(request, *args, **kw):
        data = func(request, *args, **kw)
        if isinstance(data, HttpResponse):
            return data
        return JSONResponse(data)
    return wrapper
class UploadUnHabitatIndicatorCountryCSV(FormView):
    template_name = "upload_csv.html"
    form_class = UploadForm

    def get_success_url(self):
        return reverse('upload_data')

    def get_context_data(self, **kwargs):
        data = super(UploadUnHabitatIndicatorCountryCSV, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        form.save()
        return super(UploadUnHabitatIndicatorCountryCSV, self).form_valid(form=form)
def make_where_query(values, name):
    query = ''
    if not values[0]:
        return None

    for v in values:
        query += '  ' + name + ' = "' + v +'" OR'
    query = query[:-2]
    return query

def test_json_response(request):

    country_filters = request.GET.get('countries', None)
    if country_filters:
        country_q = make_where_query(values=country_filters.split(','), name='iso')
        country_q += ') AND ('
    else:
        country_q = ''

    region_filters = request.GET.get('regions', None)
    if region_filters:
        region_q = make_where_query(values=region_filters.split(','), name='dac_region_code')
        region_q += ') AND ('
    else:
        region_q = ''

    indicator_filters = request.GET.get('indicator', None)
    if indicator_filters:
        indicator_q = make_where_query(values=indicator_filters.split(','), name='indicator_id')
        indicator_q += ') AND ('
    else:
        indicator_q = ''

    if not indicator_q:
        indicator_q = ' indicator_id = "population"'

    filter_string = '  (' + country_q + region_q + indicator_q + ')'

    if 'AND ()' in filter_string:
        filter_string = filter_string[:-6]

    cursor = connection.cursor()

    cursor.execute('SELECT indicator_id, id.country_id,  country_name, dac_region_code, dac_region_name, value, year, latitude, longitude, C.iso '
                   'FROM data_indicatordata id LEFT OUTER JOIN data_country C ON id.country_id=C.iso  '
                   'WHERE %s' % (filter_string))
    #LEFT OUTER JOIN data_city City ON C.iso = City.country_id
    cursor_max = connection.cursor()

    if indicator_filters:
        indicator_q = make_where_query(values=indicator_filters.split(','), name='indicator_id')
#        indicator_q += ' AND '
    else:
        indicator_q = ''

    if not indicator_q:
        indicator_q = ' indicator_id = "population"'

    cursor_max.execute('SELECT max(value) as max_value FROM data_indicatordata WHERE %s' % indicator_q)
    result_max = cursor_max.fetchone()
    desc = cursor.description
    results = [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    ]
    new_results = []
    country = {}
    regions = {}
    countries = {}
    cities = {}
    for r in results:
        years = {}

        year = {}

        #        year[r['year']] = r['value']
#        years.append(year)
#        try:
        #check if it has a result
        if r['value']:
            try:
                years = country[r['country_id']]['years']
            except:
                country[r['country_id']] = {'name' : r['country_name'], 'longitude' : r['longitude'], 'latitude' : r['latitude'], 'max_value' : result_max[0], 'years' : {}}



            years = country[r['country_id']]['years']
            year['y' + str(r['year'])] = r['value']


            country[r['country_id']]['years'].update(year)

            region = {}
            if r['dac_region_code']:
                region[r['dac_region_code']] = r['dac_region_name']
                regions.update(region)

            cntry = {}
            if r['country_id']:
                cntry[r['country_id']] = r['country_name']
                countries.update(cntry)


    country['regions'] = regions
    country['countries'] = countries

#        cit = {}
#        if r['name']:
#            cit[r['name']] = r['name']
#            cities.update(cit)
    #getting all the cpi indicators
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT indicator_id'
                   ' FROM data_indicatordata ')

    desc = cursor.description
    results = [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    ]
    indicators = {}
    for r in results:
        indicator = {}
        indicator[r['indicator_id']] = r['indicator_id']
        indicators.update(indicator)

    country['indicators'] = indicators


    return HttpResponse(json.dumps(country), mimetype='application/json')


def test_json_city_response(request):
    city_filters = request.GET.get('city', None)
    if city_filters:
        city_q = make_where_query(values=city_filters.split(','), name='name')
        city_q += ') AND ('
    else:
        city_q = ''

    country_filters = request.GET.get('countries', None)
    if country_filters:
        country_q = make_where_query(values=country_filters.split(','), name='iso')
        country_q += ') AND ('
    else:
        country_q = ''

    region_filters = request.GET.get('regions', None)
    if region_filters:
        region_q = make_where_query(values=region_filters.split(','), name='dac_region_code')
        region_q += ') AND ('
    else:
        region_q = ''

    indicator_filters = request.GET.get('indicator', None)
    if indicator_filters:
        indicator_q = make_where_query(values=indicator_filters.split(','), name='indicator_id')
        indicator_q += ') AND ('
    else:
        indicator_q = ''

    if not indicator_q:
        indicator_q = ' indicator_id = "cpi_5_dimensions"'
    filter_string = ' AND (' + city_q + country_q + region_q + indicator_q + ')'
    if 'AND ()' in filter_string:
        filter_string = filter_string[:-6]
    cursor = connection.cursor()
    cursor.execute('SELECT indicator_id, city_id, name, country_name, iso, value, year, longitude, latitude, dac_region_code, dac_region_name '
                   'FROM data_indicatorcitydata icd LEFT OUTER JOIN data_city Ci ON icd.city_id=Ci.id, data_country dc where dc.iso = Ci.country_id and year=2012 %s' % (filter_string))

    desc = cursor.description
    results = [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    ]

    cursor_max = connection.cursor()

    if indicator_filters:
        indicator_q = make_where_query(values=indicator_filters.split(','), name='indicator_id')
    #        indicator_q += ' AND '
    else:
        indicator_q = ''

    if not indicator_q:
        indicator_q = ' indicator_id = "cpi_5_dimensions"'

    cursor_max.execute('SELECT max(value) as max_value FROM data_indicatorcitydata WHERE %s' % indicator_q)
    result_max = cursor_max.fetchone()

    country = {}
    regions = {}
    countries = {}
    cities = {}
    for r in results:
        year = {}
        try:
            country[r['city_id']]['years']
        except:
            country[r['city_id']] = {'name' : r['name'], 'longitude' : r['longitude'], 'latitude' : r['latitude'], 'max_value' : result_max[0], 'years' : {}}

#        years = country[r['city_id']]['years']
        year['y' + str(r['year'])] = r['value']

        country[r['city_id']]['years'].update(year)

        region = {}
        if r['dac_region_code']:
            region[r['dac_region_code']] = r['dac_region_name']
            regions.update(region)

        cntry = {}
        if r['iso']:
            cntry[r['iso']] = r['country_name']
            countries.update(cntry)

        cit = {}
        if r['name']:
            cit[r['name']] = r['name']
            cities.update(cit)



    country['regions'] = regions
    country['countries'] = countries
    country['cities'] = cities

    #getting all the cpi indicators
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT indicator_id'
                   ' FROM data_indicatorcitydata ')

    desc = cursor.description
    results = [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    ]
    indicators = {}
    for r in results:
        indicator = {}
        indicator[r['indicator_id']] = r['indicator_id']
        indicators.update(indicator)

    country['indicators'] = indicators
    return HttpResponse(json.dumps(country), mimetype='application/json')

def json_cpi_filter_response(request):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM data_country')
    desc = cursor.description
    results = [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    ]
    result = {}
    regions = {}
    for r in results:
        region = {}
        if r['dac_region_code']:
            region[r['dac_region_code']] = r['dac_region_name']
            regions.update(region)

    result['regions'] = regions

    return HttpResponse(json.dumps(result), mimetype='application/json')


