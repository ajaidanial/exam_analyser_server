# Generated by Django 3.0.10 on 2020-11-09 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("examination", "0011_auto_20201110_0406"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userquestionmarktracker",
            options={
                "default_related_name": "related_mark_trackers",
                "ordering": ["user", "-question"],
            },
        ),
    ]
