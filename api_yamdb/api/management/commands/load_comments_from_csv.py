import csv

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from reviews.models import Comment, Review
from users.models import MyUser


class Command(BaseCommand):
    help = "Load data from comments.csv into the database"

    def handle(self, *args, **options):
        csv_file_path = "static/data/comments.csv"

        with open(csv_file_path, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                try:
                    author = MyUser.objects.get(id=int(row["author"]))
                except ObjectDoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'MyUser with id {row["author"]} does not exist. Skipping this row.'
                        )
                    )
                    continue
                try:
                    review = Review.objects.get(id=int(row["review_id"]))
                except ObjectDoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Titles with id {row["review_id"]} does not exist. Skipping this row.'
                        )
                    )
                    continue
                comment = Comment(
                    text=row["text"],
                    review=review,
                    author=author,
                    pub_date=parse_datetime(row["pub_date"]),
                )
                comment.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully loaded data from {csv_file_path}")
                )
