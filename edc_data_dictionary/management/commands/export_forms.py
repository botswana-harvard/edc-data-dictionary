from optparse import make_option

from django.contrib import admin
from django.core.management.base import BaseCommand, CommandError

from edc_data_dictionary.form_exporter import FormExporter


class Command(BaseCommand):

    help = 'Export forms in wiki text format given a visit code or app_label.model_name.'

    option_list = BaseCommand.option_list + (
        make_option(
            '--visit',
            action='store',
            dest='by_visit',
            default='',
            help='Export form text by visit code'),
        make_option(
            '--model',
            action='store',
            dest='by_model',
            default='',
            help='Export form text by app_label.model_name'),
        make_option(
            '--app',
            action='store',
            dest='by_app',
            default='',
            help='Export form text by app_label'),
    )

    def handle(self, *args, **options):
        admin.autodiscover()
        try:
            if options['by_visit']:
                self.export_by_visit(options['by_visit'])
            elif options['by_app']:
                self.export_by_app(options['by_app'])
            elif options['by_model']:
                self.export_by_model(options['by_model'])
            else:
                raise CommandError('At least one option is required.')
        except KeyError:
            raise CommandError('Unknown or missing option.')

    def export_by_visit(self, opts):
        try:
            f = FormExporter()
            for form in f.export_by_visit(opts):
                for line in form:
                    print(line)
                print('\n')
        except IndexError:
            raise CommandError('Expected visit code. Got None.')

    def export_by_model(self, opts):
        try:
            f = FormExporter()
            for model in opts.split(','):
                for form in f.export_by_model(*model.split('.')):
                    for line in form:
                        print(line)
                    print('\n')
        except IndexError:
            raise CommandError('Expected visit code. Got None.')

    def export_by_app(self, opts):
        try:
            f = FormExporter()
            for opt in opts.split(','):
                for form in f.export_by_app(opt):
                    for line in form:
                        print(line)
                    print('\n')
        except IndexError:
            raise CommandError('Expected visit code. Got None.')
