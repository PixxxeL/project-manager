# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from mezaext.utils import paginator


#def obj(request, slug):
#    try:
#        obj = Obj.objects.get(slug=slug)
#    except:
#        raise Http404
#    return render(request, 'obj.html', {
#        'obj' : obj,
#    })
