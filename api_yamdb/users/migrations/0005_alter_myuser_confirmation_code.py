# Generated by Django 3.2 on 2023-10-14 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_myuser_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='confirmation_code',
            field=models.CharField(blank=True, default='RfnwYR', max_length=30),
        ),
    ]