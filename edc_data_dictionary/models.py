from textwrap import wrap

from django.db import models

from edc_base.model.models import BaseModel


class DataDictionaryModel(BaseModel):

    app_label = models.CharField(
        max_length=50,
        null=True)

    model_name = models.CharField(
        max_length=50,
        null=True)

    db_table = models.CharField(
        max_length=50,
        null=True)

    field = models.CharField(
        max_length=50,
        null=True)

    db_field = models.CharField(
        max_length=50,
        null=True)

    number = models.IntegerField(null=True)

    prompt = models.TextField(
        null=True)

    type = models.CharField(
        max_length=50,
        null=True)

    max_length = models.CharField(
        max_length=50,
        null=True)

    default = models.CharField(
        max_length=50,
        null=True)

    null = models.BooleanField(
        default=False)

    blank = models.BooleanField(
        default=False)

    editable = models.BooleanField(
        default=False)

    help_text = models.CharField(
        max_length=500,
        null=True)

    encrypted = models.BooleanField(
        default=False)

    choices = models.TextField(
        null=True)

    primary_key = models.BooleanField(
        default=False)

    unique = models.BooleanField(
        default=False)

    in_admin = models.BooleanField(
        default=False)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        # don't allow anyone to change these instances once created
        if not self.id:
            super(DataDictionaryModel, self).save(*args, **kwargs)

    def question(self):
        return '<br>'.join(wrap(self.prompt, width=40))
    question.allow_tags = True

    class Meta:
        app_label = 'edc_data_dictionary'
        verbose_name = 'Data Dictionary'
        verbose_name = 'Data Dictionaries'
        ordering = ['model_name', 'number']
