from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


def currency(dollars):
    dollars = round(float(dollars), 2)
    return "R$%s,%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-2:])


register.filter('currency', currency)
