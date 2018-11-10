# -*- coding: utf-8 -*-

import json

from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from mezaext.models import EditableBlock


def paginator(objects_list, page, per_page=10, to_show=10):
    paginator = Paginator(objects_list, per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    current_idx = data.number - 1
    start_idx = current_idx - (to_show / 2)
    end_idx = current_idx + (to_show / 2)
    if start_idx < 0:
        start_idx = 0
        end_idx = to_show
    if end_idx + 1 > data.paginator.num_pages:
        end_idx = data.paginator.num_pages
        start_idx = end_idx - to_show
    data.sliced_pages = list(data.paginator.page_range)[start_idx:end_idx]
    return data


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def json_response(data):
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_editable_block(slug):
    key = 'editableblock:%s' % slug
    text = cache.get(key, '')
    if not text:
        try:
            text = EditableBlock.objects.get(slug=slug, enabled=True).text
            cache.set(key, text, 60 * 5)
        except EditableBlock.DoesNotExist:
            return ''
    return text
