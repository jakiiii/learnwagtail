from django.db import models

from wagtail.models import Orderable, ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel, PageChooserPanel, InlinePanel, MultiFieldPanel
)
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey

from django_extensions.db.fields import AutoSlugField


class MenuItem(Orderable):
    link_title = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    link_url = models.URLField(
        max_length=255,
        null=True,
        blank=True
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="+"
    )
    open_in_new_tab = models.BooleanField(
        default=False
    )
    page = ParentalKey(
        "Menu",
        related_name="menu_items"
    )

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return "Missing Title"


@register_snippet
class Menu(ClusterableModel):
    # The main menu clusterable model
    title = models.CharField(
        max_length=100
    )
    slug = AutoSlugField(
        populate_from="title",
        editable=True,
        unique=True
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("slug")
            ],
            heading="Menu"
        ),
        InlinePanel("menu_items", label="Menu Item")
    ]

    def __str__(self):
        return self.title
