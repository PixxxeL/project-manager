# -*- coding: utf-8 -*-

from django import template
from django.utils.safestring import mark_safe

from mezaext.forms import ContactsForm
from mezaext.utils import get_editable_block


register = template.Library()


@register.inclusion_tag('mezaext/contacts_form.html')
def contacts_form(target=None):
    return {
        'form' : ContactsForm(),
        'target' : target,
    }


@register.simple_tag(takes_context=True)
def editableblock(context, slug):
    return mark_safe(get_editable_block(slug))
