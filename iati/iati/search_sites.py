import haystack
haystack.autodiscover()

from haystack.indexes import *
from haystack import site
from data.models.activity import IATIActivity
import pdb

class IATIActivityIndex(SearchIndex):
    """
    This index is indexing title, country and description in the field text
    """
    text = CharField(document=True)
    title = CharField()
    country = CharField()

    def index_queryset(self):
        return IATIActivity.objects.all()

    def prepare_title(self, obj):
        title = obj.iatiactivitytitle_set.values('title')
        try:
             title = title[0]['title']
             return title
        except IndexError:
            return {'N/A'}

    def prepare_country(self, obj):
        try:
            return obj.iatiactivitycountry_set.all()[0].country.get_iso_display()
        except :
            return {'N/A'}

    def prepare_text(self, obj):

        description = obj.iatiactivitydescription_set.values('description')
        try:
            description = description[0]['description']

            return description
        except IndexError:
            return {'N/A'}

site.register(IATIActivity, IATIActivityIndex)


from haystack.views import SearchView

class PeriodicalSearchView(SearchView):
    def get_results(self):
        """
        This is a test search form. You can access it through __url__/search

        Fetches the results via the form.
        Returns an empty list if there's no query to search with.
        """
        if not (self.form.is_valid() and self.form.cleaned_data['q']):
            return self.form.no_query_found()

        query = self.form.cleaned_data['q']

        words = iter(set(query.split()))
        word = words.next()

        sqs = self.form.searchqueryset.filter(text=word) # actually I have one more field here...
        for word in words:
            sqs = sqs.filter_or(title=word).filter_or(text=word)

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def __call__(self, request, template_name=None):
        """
        Generates the actual response to the search.
        Relies on internal, overridable methods to construct the response.
        """
        if template_name:
            self.template = template_name

        return super(PeriodicalSearchView, self).__call__(request)