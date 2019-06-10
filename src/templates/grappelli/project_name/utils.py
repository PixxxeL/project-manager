# -*- coding: utf-8 -*-

from copy import deepcopy
import datetime
import hashlib
import json
import logging
import os
import time

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils import timezone
from filebrowser.base import FileObject


logger = logging.getLogger(__name__)


class JsonResponse(HttpResponse):
    '''
    Обобщенный метод ответа на запрос в формате JSON
    '''
    def __init__(self, data, code=0, message='', **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps({
            'code' : code,
            'msg'  : message,
            'data' : data,
        })
        super(JsonResponse, self).__init__(content=data, **kwargs)


def upload_file(post_file, target):
    '''
    Загрузка одного файла из запроса
    '''
    ext = post_file.name.split('.')[-1]
    name = repr(post_file.name) + str(time.time())
    name = hashlib.md5(name.encode('utf-8')).hexdigest()
    name = '{}.{}'.format(name, ext)
    root = getattr(settings, 'FILEBROWSER_DIRECTORY', 'uploads')
    parts = [root, target, name[:2], name[2:4]]
    path = os.path.join(*parts)
    if not os.path.exists(path):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, path))
    path = os.path.join(path, name)
    with open(os.path.join(settings.MEDIA_ROOT, path), 'wb+') as dst:
        for chunk in post_file.chunks():
            dst.write(chunk)
    return path


def normalize_media_path(path):
    '''
    Преобразует строку пути да файла в хранилищу
    в строку URL до файла без домена
    '''
    return '{}{}'.format(settings.MEDIA_URL, path.replace('\\', '/'))


def force_int(value, default=0):
    '''
    Безопасное приведение к int
    '''
    try:
        return int(value)
    except:
        return default


TEXT_FIELD_TYPES = (
    models.CharField, models.TextField, models.URLField,
    models.EmailField, models.SlugField, models.UUIDField,
)

NUMBER_FIELD_TYPES = (
    models.AutoField, models.BigIntegerField,
    models.FloatField, models.IntegerField, models.SmallIntegerField,
    models.PositiveIntegerField, models.PositiveSmallIntegerField,
)

BOOLEAN_FIELD_TYPES = (
    models.BooleanField, models.NullBooleanField,
)

FILE_FIELD_TYPES = (
    models.FileField, models.ImageField,
)

FK_FIELD_TYPES = (
    models.OneToOneField, models.ForeignKey,
)


class AsDictQuerySet(models.QuerySet):

    def as_dict(self, *args, **kwargs):
        return list(map(lambda q: q.as_dict(*args, **kwargs), self))


class ExManager(models.Manager):

    def get_queryset(self):
        return AsDictQuerySet(self.model)

    def as_dict(self, *args, **kwargs):
        return self.get_queryset().as_dict(*args, **kwargs)


class BaseModel(models.Model):
    '''
    Общая функциональность всех моделей проекта
    '''

    objects = ExManager()

    cleaning_keys = []

    def as_dict(self, *args, **kwargs):
        '''
        Сериализация объекта в формат, совместимый с JSON
        '''
        data = deepcopy(self.__dict__)
        for key in self.cleaning_keys + []:
            if key in data:
                del data[key]
        std_types = (str, int, float, bool, list, type(None),)
        for k, v in data.items():
            if isinstance(v, std_types):
                data[k] = v
            elif isinstance(v, (datetime.datetime, datetime.date,)):
                data[k] = v.strftime('%Y-%m-%dT%H-%M-%S')
            else:
                data[k] = str(v)
        return data

    def serialize_json(
        self, processors={}, thumb_sizes={}, excludes=[], only=[]
        ):
        '''
        Сериализует поля модели в JSON-обрабатываемый объект.
        Параметр `processors` служит для задания обработчиков полей
        и должен быть вида:
        {
            'field_name' : pointer_to_function
        }
        Параметр `thumb_sizes` служит для задания миниатюр для полей
        и должен быть вида: 
        {
            'field_name' : thumb_name
        }
        Параметр `excludes` - список имен пропускаемых полей
        Параметр `only` - список имен выбираемых полей
        Некоторые поля (
            models.DurationField, models.FilePathField,
            models.GenericIPAddressField, models.DateField, 
            models.TimeField
        ) не обрабатываются.
        '''
        data = {}
        #for field in self._meta.get_fields(): # check this!
        for field in self._meta.fields + self._meta.many_to_many:
            name = field.name
            if only and name not in only:
                continue
            if name in excludes:
                continue
            value = getattr(self, name)
            processor = processors.get(name)
            if processor:
                data[name] = processor(value)
            elif isinstance(field, TEXT_FIELD_TYPES):
                data[name] = value or ''
            elif isinstance(field, NUMBER_FIELD_TYPES + BOOLEAN_FIELD_TYPES):
                data[name] = value
            elif isinstance(field, FILE_FIELD_TYPES):
                thumb_name = thumb_sizes.get(name)
                data[name] = self.thumb_field(value, thumb_name)\
                if thumb_name\
                else self.__proc_file_field(value)
            elif isinstance(field, models.DecimalField):
                data[name] = float(value or 0)
            elif isinstance(field, models.DateTimeField) and value:
                data[name] = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(field, FK_FIELD_TYPES):
                data[name] = getattr(value, 'pk', None)
            elif isinstance(field, models.ManyToManyField):
                data[name] = list(value.values_list('id', flat=True))
        return data

    def thumb_field(self, field, thumb_name):
        '''
        Делает миниатюру из изображения для поля модели
        '''
        if field and hasattr(field, 'path'):
            img = FileObject(field.path)
            if img.filetype == 'Image':
                return img.version_generate(thumb_name).url

    def __proc_file_field(self, value):
        if value:
            return value.url

    class Meta:
        abstract = True
