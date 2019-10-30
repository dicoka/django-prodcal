from django.shortcuts import render
from django.views import generic
from .service import check_locale, get_prodcals, cast, cast_single_date
from prodcal.models import ProdCals
import json
from datetime import datetime, date
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, Http404
from datetime import date
import logging
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from .settings import *

# Create your views here.



logger = logging.getLogger(__name__)

class MyMessageMixin:   # TODO Make one MyMessageMixin and import it
    def success(self, message, fail_silently=True, **kwargs):
        """Notification about successful operation."""
        message = mark_safe(_(message).format(**kwargs))
        messages.add_message(self.request, messages.SUCCESS, message, fail_silently=fail_silently)

    def error(self, message, fail_silently=True, **kwargs):
        """Notification about an error."""
        message = mark_safe(_(message).format(**kwargs))
        messages.add_message(self.request, messages.ERROR, message, fail_silently=fail_silently)

class ProdCalEditView(PermissionRequiredMixin, generic.TemplateView, MyMessageMixin): # PermissionRequiredMixin,
    template_name = 'prodcal.html'
    permission_required = 'prodcal.change_prodcals'
    year_min = 2018
    year_max = 2039
    #years = range(year_min, year_max)
    paginate_by = 10
    localies = dict(LOCALE_SUPPORTING)

    def get_context_data(self, **kwargs):
        context = super(ProdCalEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            raise Http404
        else:
            # GET
            self.locale = check_locale(self.kwargs.get('locale'))
            if not self.locale:
                print("Wrong locale")   # TODO logging
                raise Http404

            context['paginate_by'] = self.paginate_by
            context['locale'] = self.locale
            context['locale_full'] = self.localies[self.locale]
            context['locale_supporting'] = LOCALE_SUPPORTING
            context['year'] = datetime.now().year
            try:
                context['addDates'] = ProdCals.objects.get(locale=self.locale, year=context['year']).dates
            except:
                context['addDates'] = []
            #context['years'] = self.years

            context['year_min'] = self.year_min
            context['year_max'] = self.year_max
            # 'opts' for admin template (breadcrumbs)
            context['opts'] = ProdCals._meta

        return context

    def post(self, request, locale):
        self.locale = check_locale(self.kwargs.get('locale'))
        if not self.locale or not request.is_ajax():
            print("Wrong locale on not ajax")  # TODO logging
            raise Http404
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        try:
            if body['action'] == 'save':
                try:
                    new_dates = [date(int(body['year']), m, d) for m, d in body['dates']]
                except Exception as e:
                    raise ValueError("Даты в Ajax вне пределов допустимых значений (" + str(e) + ")")  # TODO перенаправлять ? TODO - wrong dates
                obj, created = ProdCals.objects.get_or_create(
                    locale=self.locale,
                    year=body['year'],
                )
                obj.dates = new_dates
                obj.save()
                # не работатет
                #return HttpResponseRedirect(reverse('viewflow:prodcal', args=[locale, 'current']))
                return HttpResponse(
                    json.dumps({'result': 'sucess'}),
                    content_type="application/json"
                )
            else:
                try:
                    dates = ProdCals.objects.get(locale=self.locale, year=int(body['year'])).dates
                    addDates = ['{}.{}.{}'.format(d.day, d.month, d.year) for d in dates]
                except:
                    addDates = []
                return HttpResponse(
                    json.dumps({'result': addDates}),
                    content_type="application/json"
                )
        except Exception as e:
            self.error('Ошибка')    # TODO No messages in template
            print('ProdCalEditView Exception: ' + str(e))    # TODO logging
            raise Http404