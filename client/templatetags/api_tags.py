# -*- coding: UTF-8 -*-
from django import template
from jdatetime import datetime as jdatetime
from datetime import datetime
from dateutil import tz
import json
import locale
from django.urls import reverse
import pytz
register = template.Library()

@register.filter("apiurl")
def apiurl(value):
    return reverse(value)
@register.filter("rial")
def rial(value):
    value=int(value)
    value*=10000
    locale.setlocale(locale.LC_ALL, 'fa_IR')
    return locale.currency( value, grouping=True )
@register.filter("jdate")
def jdate(value,format):
    if type(value)==type(""):
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    value = value.replace(tzinfo=tz.gettz('UTC')).astimezone(pytz.timezone('Asia/Tehran'))
    return jdatetime.fromgregorian(datetime=value).strftime(format)