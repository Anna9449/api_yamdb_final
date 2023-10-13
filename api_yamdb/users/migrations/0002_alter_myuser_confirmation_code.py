from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='confirmation_code',

            field=models.CharField(blank=True, default='WyKsgD', max_length=30),
    ]
