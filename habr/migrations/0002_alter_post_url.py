# Generated by Django 4.0.6 on 2022-07-31 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='url',
            field=models.URLField(db_index=True, unique=True),
        ),
    ]