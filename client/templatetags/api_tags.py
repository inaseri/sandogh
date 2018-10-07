# -*- coding: UTF-8 -*-
from django import template
# from jdatetime import datetime as jdatetime
from datetime import datetime
from dateutil import tz
import json
from django.urls import reverse
register = template.Library()

@register.filter("apiurl")
def apiurl(value):
    return reverse(value)