# Generated by Django 4.0.4 on 2022-05-11 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skilltracker', '0002_tag_remove_post_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(related_name='related_posts', to='skilltracker.tag'),
        ),
    ]