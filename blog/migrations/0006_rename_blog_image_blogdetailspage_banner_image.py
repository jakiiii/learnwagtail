# Generated by Django 3.2 on 2022-06-01 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogdetailspage_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogdetailspage',
            old_name='blog_image',
            new_name='banner_image',
        ),
    ]
