from django.conf.urls import url

from .views import contacts_form

urlpatterns = [
    url(r'^contacts-form/$', contacts_form, name='contacts_form'),
]
