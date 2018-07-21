# -*- coding: utf-8 -*-

from django import template
from django.utils.safestring import mark_safe

from mezaext.forms import ContactsForm
from mezaext.models import EditableBlock


register = template.Library()


@register.inclusion_tag('mezaext/contacts_form.html')
def contacts_form(target=None):
    return {
        'form' : ContactsForm(),
        'target' : target,
    }


@register.simple_tag(takes_context=True)
def editableblock(context, slug):
    try:
        obj = EditableBlock.objects.get(slug=slug, enabled=True)
    except EditableBlock.DoesNotExist:
        return ''
    return mark_safe(obj.text)
