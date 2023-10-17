import csv

from django.core.management.base import BaseCommand

from reviews.models import Genres, Title


class Command(BaseCommand):
    help = 'Load data from genre_title.csv into the database'

    def handle(self, *args, **options):
        csv_file_path = 'static/data/genre_title.csv'

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                title_id = int(row['title_id'])
                genre_id = int(row['genre_id'])
                title = Title.objects.get(id=title_id)
                genre = Genres.objects.get(id=genre_id)
                title.genre.add(genre)

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully loaded data from {csv_file_path}')
                )
