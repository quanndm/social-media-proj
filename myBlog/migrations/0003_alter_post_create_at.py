# Generated by Django 4.1.1 on 2022-10-08 12:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myBlog", "0002_post_image_url_alter_post_content_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="create_at",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]