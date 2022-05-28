# Generated by Django 3.2 on 2022-05-28 06:53

from django.db import migrations
import streams.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0006_alter_flexpage_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flexpage',
            name='content',
            field=wagtail.fields.StreamField([('title_and_text', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Add your title', required=True)), ('text', wagtail.blocks.TextBlock(help_text='Add additional text', required=True))])), ('full_richtext', streams.blocks.RichTextBlock()), ('simple_richtext', streams.blocks.SimpleRichTextBlock()), ('cards', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Add your title', required=True)), ('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(max_length=40, required=True)), ('text', wagtail.blocks.TextBlock(max_length=200, required=True)), ('button_page', wagtail.blocks.PageChooserBlock(required=False)), ('button_url', wagtail.blocks.URLBlock(help_text='If the button page above is selected, that will be used first.', required=False))])))])), ('cta', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Add your title', required=True)), ('text', wagtail.blocks.RichTextBlock(features=['blog', 'italic'], required=True)), ('button_page', wagtail.blocks.PageChooserBlock(required=False)), ('button_url', wagtail.blocks.URLBlock(required=False)), ('button_text', wagtail.blocks.CharBlock(default='Learn More', max_length=40, required=False))])), ('button', wagtail.blocks.StructBlock([('button_page', wagtail.blocks.PageChooserBlock(help_text='If selected, this url will be used first', required=False)), ('button_url', wagtail.blocks.URLBlock(help_text='If added, this url will be used secondarily to the button page', required=False))]))], blank=True, null=True, use_json_field=None),
        ),
    ]