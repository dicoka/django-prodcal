from django.contrib import admin
from .views import ProdCalEditView
from .service import DEFAULT_LOCALE
from .models import ProdCals
# Register your models here.
from .models import ProdCals
from django.urls import re_path
from .settings import *


class ProdcalAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return ProdCalEditView.as_view()(request, locale=DEFAULT_LOCALE)

    def has_add_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            re_path(r'^(?P<locale>[A-Za-z]{2})/$', ProdCalEditView.as_view(), name='prodcal'),
        ]
        return extra_urls + urls

admin.site.register(ProdCals, ProdcalAdmin)

