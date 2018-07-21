# -*- coding: utf-8 -*-

from django import forms


class ContactsForm(forms.Form):
    name = forms.CharField(
        label=u'Представьтесь',
        max_length=64,
        widget = forms.TextInput(attrs={'autocomplete': 'off'}),
    )
    phone = forms.CharField(
        label=u'Телефон',
        max_length=32,
        widget = forms.TextInput(attrs={'autocomplete': 'off'}),
    )
    agree = forms.BooleanField(
        label=u'Я даю своё согласие на сбор и обработку персональных данных и подтверждаю, что ознакомлен и согласен с политикой обработки персональных данных',
        initial = True,
        required = True,
    )
