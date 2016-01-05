from django.contrib import admin

from edc.export.actions import export_as_csv_action

from .models import DataDictionaryModel


class DataDictionaryModelAdmin(admin.ModelAdmin):

    list_display = (
        'field', 'app_label', 'model_name', 'number',
        'question', 'db_table', 'type', 'max_length',
        'null', 'blank', 'encrypted', 'primary_key',
        'unique', 'in_admin')
    list_filter = (
        'app_label', 'type', 'null', 'blank', 'encrypted',
        'primary_key', 'unique', 'editable', 'in_admin',
        'model_name')
    search_fields = ('model_name', 'field', 'prompt')

    actions = (
        export_as_csv_action(
            exclude=[
                'id', 'modified', 'user_created', 'user_modified',
                'hostname_created', 'hostname_modified'],
            delimiter='|'),
        'export_as_csv_action',
        "Export to CSV")
admin.site.register(DataDictionaryModel, DataDictionaryModelAdmin)
