import csv

from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ObjectDoesNotExist

from reviews.models import Review
from reviews.models import Titles
from users.models import MyUser


class Command(BaseCommand):
    help = "Load data from review.csv into the database"

    def handle(self, *args, **options):
        csv_file_path = "static/data/review.csv"

        with open(csv_file_path, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                try:
                    title = Titles.objects.get(id=int(row["title_id"]))
                except ObjectDoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Titles with id {row["title_id"]} does not exist. Skipping this row.'
                        )
                    )
                    continue

                try:
                    author = MyUser.objects.get(id=int(row["author"]))
                except ObjectDoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'MyUser with id {row["author"]} does not exist. Skipping this row.'
                        )
                    )
                    continue

                review = Review(
                    text=row["text"],
                    title=title,
                    author=author,
                    score=int(row["score"]),
                    pub_date=parse_datetime(row["pub_date"]),
                )
                review.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully loaded data from {csv_file_path}")
                )
