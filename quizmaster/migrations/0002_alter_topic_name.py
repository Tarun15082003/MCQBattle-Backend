# Generated by Django 5.0.6 on 2024-07-01 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizmaster', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]