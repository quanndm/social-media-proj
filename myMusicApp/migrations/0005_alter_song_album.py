# Generated by Django 4.1.1 on 2022-10-18 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("myMusicApp", "0004_song_image_song"),
    ]

    operations = [
        migrations.AlterField(
            model_name="song",
            name="album",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="songs",
                to="myMusicApp.album",
            ),
        ),
    ]
