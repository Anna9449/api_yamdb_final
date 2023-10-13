from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_myuser_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='confirmation_code',
            field=models.CharField(blank=True, default='nJR6Jn', max_length=30),

        ),
    ]
