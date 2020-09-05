# Generated by Django 3.0.8 on 2020-09-05 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [("cosmos", "0005_committee_board_display_names"), ("cosmos", "0006_auto_20200905_2228")]

    dependencies = [
        ("cosmos", "0004_board_commitee_blank_array"),
    ]

    operations = [
        migrations.AddField(
            model_name="board", name="display_name", field=models.CharField(default="None", max_length=50),
        ),
        migrations.AddField(
            model_name="committee", name="display_name", field=models.CharField(default="None", max_length=50),
        ),
    ]