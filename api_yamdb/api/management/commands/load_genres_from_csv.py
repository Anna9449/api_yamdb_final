import csv

from django.core.management.base import BaseCommand

from genres.models import Genres


class Command(BaseCommand):
    help = 'Load data from genre.csv into the database'

    def handle(self, *args, **options):
        csv_file_path = 'static/data/genre.csv'

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                title = Genres(name=row['name'], slug=row['slug'])
                title.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully loaded data from {csv_file_path}')
                )
