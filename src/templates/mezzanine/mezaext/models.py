# -*- coding: utf8 -*-

from django.db import models
#from mezzanine.core.fields import RichTextField


class EditableBlock(models.Model):
    title = models.CharField(
        verbose_name=u'Название',
        max_length=255,
    )
    slug = models.SlugField(
        verbose_name=u'Техническое имя',
        max_length=255,
    )
    text = models.TextField(
    #text = RichTextField(
        verbose_name=u'Текст',
    )
    enabled = models.BooleanField(
        verbose_name=u'Включен',
        default=True
    )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Редактируемый блок'
        verbose_name_plural = u'Редактируемые блоки'
