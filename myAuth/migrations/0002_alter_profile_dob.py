# Generated by Django 4.1.1 on 2022-10-04 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myAuth", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="DOB",
            field=models.DateField(blank=True, null=True),
        ),
    ]
