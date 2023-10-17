import csv

from django.core.management.base import BaseCommand

from users.models import MyUser


class Command(BaseCommand):
    help = 'Load data from users.csv into the database'

    def handle(self, *args, **options):
        csv_file_path = 'static/data/users.csv'

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                user = MyUser(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully loaded data from {csv_file_path}')
                )
