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

def test_json_response(request):
    cursor = connection.cursor()
    cursor.execute('SELECT indicator_id, country_id, country_name, value, year, latitude, longitude FROM data_indicatordata id LEFT OUTER JOIN data_country C ON id.country_id=C.iso')
    desc = cursor.description
    results = [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    ]
    return HttpResponse(json.dumps(results), mimetype='application/json')




