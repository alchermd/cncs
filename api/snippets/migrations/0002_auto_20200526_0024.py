# Generated by Django 3.0.6 on 2020-05-25 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='id',
        ),
        migrations.AddField(
            model_name='snippet',
            name='key',
            field=models.CharField(default='', max_length=4, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
