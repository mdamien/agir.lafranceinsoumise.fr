import datetime
from django import template
from django.utils.formats import date_format
from django.utils.timezone import utc, is_aware
from django.utils.translation import ugettext as _, ngettext

from ..display import display_price as original_display_price, pretty_time_since as original_pretty_time_since

register = template.Library()


@register.filter(name='display_price')
def display_price(value):
    return original_display_price(value)


@register.filter(name='pretty_time_since')
def pretty_time_since(d, now=None, ):
    return original_pretty_time_since(d, now)
