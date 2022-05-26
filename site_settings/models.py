from django.db import models

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel


@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(
        null=True,
        blank=True,
        help_text="Facebook URL"
    )
    twitter = models.URLField(
        null=True,
        blank=True,
        help_text="Twitter URL"
    )
    youtube = models.URLField(
        null=True,
        blank=True,
        help_text="Youtube Chanel URL"
    )

    panel = [
        MultiFieldPanel(
            [
                FieldPanel("facebook"),
                FieldPanel("twitter"),
                FieldPanel("youtube"),
            ],
            heading="Social Media Settings"
        )
    ]
