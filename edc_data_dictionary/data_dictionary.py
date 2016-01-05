from collections import OrderedDict

from django.contrib import admin
from django.db.models import get_app, get_models

from .models import DataDictionaryModel


class DataDictionary(object):

    def __init__(self, app_label):
        self.app_label = app_label
        self.app = get_app(app_label)
        self.models = get_models(self.app)

    @property
    def data_dictionaries(self):
        """
        { app_label.model_name:
            {model: {'db_table': '<table_name>', ...},
             fields: {'prompt': verbose_name, ...}
            }
        }

        app_label, model_name, db_table, field, db_field, prompt,
        type, max_length, default, null, blank, editable, help_text,
        encrypted, choices, primary_key, unique

        """
        data_dictionaries = []
        for self.model in self.models:
            self._model_admin = None
            if 'audit' not in self.model._meta.object_name.lower():
                for self.field in self.model._meta.fields:
                    data_dictionaries.append(self.model_fields)
        return data_dictionaries

    def save(self):
        DataDictionaryModel.objects.filter(app_label=self.app_label).delete()
        for model_fields in self.data_dictionaries:
            DataDictionaryModel.objects.create(**model_fields)

    @property
    def model_fields(self):
        model_fields = OrderedDict(
            app_label=self.app_label,
            model_name=self.model._meta.object_name,
            db_table=self.model._meta.db_table)
        model_fields.update(
            blank=self.field.blank,
            choices=self.choices,
            db_field=self.field.attname,
            default=self.default_value,
            editable=self.field.editable,
            encrypted=self.encrypted,
            field=self.field.name,
            help_text=self.field.help_text,
            in_admin=True if self.model_admin else False,
            max_length=self.field.max_length,
            null=self.field.null,
            number=self.question_number,
            primary_key=self.field.primary_key,
            prompt=self.prompt,
            type=self.field.get_internal_type(),
            unique=self.field._unique)
        return model_fields

    @property
    def model_admin(self):
        if not self._model_admin:
            for model_admin in admin.sites.site._registry.itervalues():
                if model_admin.model == self.model:
                    break
            self._model_admin = model_admin
        return self._model_admin

    @property
    def prompt(self):
        prompt = unicode(self.field.verbose_name)
        if not prompt.startswith == '"':
            prompt = '"' + prompt
        if not prompt.endswith == '"':
            prompt = prompt + '"'
        return prompt

    @property
    def question_number(self):
        question_number = None
        try:
            for index, fld in enumerate(self.model_admin.fields):
                if self.field.name == fld:
                    question_number = index + 1
                    break
        except AttributeError:
            pass
        return question_number

    @property
    def default_value(self):
        try:
            default = unicode(self.field.default.func_name)
        except:
            pass
        try:
            default = unicode(self.field.default).split('.')[-1]
        except:
            pass
        try:
            default = unicode(self.field.default)
        except:
            default = self.field.default
        return default

    @property
    def get_encrypted(self):
        try:
            self.field.encrypted
            encrypted = True
        except AttributeError:
            encrypted = False
        return encrypted

    @property
    def choices(self):
        if self.field.choices:
            choices = self.field.choices
        else:
            choices = ''
        return choices
