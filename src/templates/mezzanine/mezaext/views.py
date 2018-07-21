# -*- coding: utf-8 -*-

import time
import datetime

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .forms import ContactsForm


SITE_TITLE = settings.SITE_TITLE

def contacts_form(request):
    slug = getattr(settings, 'CONTACTS_FORM_REDIRECT_SLUG', '')
    key = 'contacts_form_ts'
    session_ts = float(request.session.get(key, 0))
    now_ts = time.mktime(datetime.datetime.now().timetuple())
    if session_ts + 60 * 15 > now_ts:
        return HttpResponse(u'Можно отправлять не чаще, чем раз в 15 минут')
    if request.method == 'POST':
        form = ContactsForm(request.POST)
        if form.is_valid():
            recipients = getattr(settings, 'CONTACTS_FORM_EMAILS', [])
            if recipients:
                send_mail(
                    u'Сообщение от пользователя сайта %s' % SITE_TITLE,
                    render_to_string('mezaext/contacts_email.txt', {'form' : form}),
                    settings.DEFAULT_FROM_EMAIL,
                    recipients,
                    #fail_silently=False,
                )
            request.session[key] = now_ts
        else:
            request.session[key] = 0
            return HttpResponse(form.errors)
    return HttpResponse(u'Вы отправили заявку')
