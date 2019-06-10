# -*- coding: utf-8 -*-

import logging

from .utils import JsonResponse


logger = logging.getLogger(__name__)


# def obj(request, slug):
#     try:
#         page = Obj.objects.get(slug=slug)
#     except Obj.DoesNotExist:
#         raise Http404
#     return JsonResponse({
#         'page' : page.as_dict(),
#     })
