# -*- coding: utf-8 -*-

from mezzanine.conf import register_setting


register_setting(
    name        = 'CONTACTS_FORM_REDIRECT_SLUG',
    label       = u'Слаг страницы для редиректа',
    description = u'Поле slug из модели Page',
    editable    = True,
    default     = '',
)
