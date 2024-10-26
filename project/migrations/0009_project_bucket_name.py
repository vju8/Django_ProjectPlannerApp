# Generated by Django 5.1.1 on 2024-10-26 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_projectfile_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='bucket_name',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='active', max_length=9),
        ),
    ]