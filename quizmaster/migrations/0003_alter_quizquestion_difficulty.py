# Generated by Django 5.0.6 on 2024-07-02 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizmaster', '0002_alter_topic_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizquestion',
            name='difficulty',
            field=models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], max_length=100),
        ),
    ]