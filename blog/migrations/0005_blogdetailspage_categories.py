# Generated by Django 3.2 on 2022-05-28 19:43

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogdetailspage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='blog.BlogCategory'),
        ),
    ]
