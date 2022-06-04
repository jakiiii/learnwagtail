from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel, PageChooserPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, ObjectList, TabbedInterface
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from streams import blocks


class HomePageCarouselImages(Orderable):
    page = ParentalKey(
        "home.HomePage",
        related_name="carousel_images"
    )
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    panels = [
        ImageChooserPanel("carousel_image")
    ]


class HomePage(RoutablePageMixin, Page):
    template = "home/home_page.html"
    subpage_types = ['blog.BlogListingPage', 'contact.ContactPage', 'flex.FlexPage']
    parent_page_type = [
        'wagtailcore.Page'
    ]
    # max_count = 1

    banner_title = models.CharField(
        max_length=100,
        blank=False,
        null=True
    )
    banner_subtitle = RichTextField(
        features=["bold", "italic"]
    )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    content = StreamField(
        [
            ("cta", blocks.CTABlock())
        ],
        null=True,
        blank=True
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_title"),
                FieldPanel("banner_subtitle"),
                ImageChooserPanel("banner_image"),
                PageChooserPanel("banner_cta"),
            ],
            heading="Banner Options"
        ),
        MultiFieldPanel(
            [
                InlinePanel(
                    "carousel_images",
                    max_num=5,
                    min_num=1,
                    label="Image"
                ),
            ],
            heading="Carousel Images"
        ),
        StreamFieldPanel("content"),
    ]

    # promote_panels = []
    # settings_panels = []

    banner_panels = [
        MultiFieldPanel(
            [
                FieldPanel("banner_title"),
                FieldPanel("banner_subtitle"),
                ImageChooserPanel("banner_image"),
                PageChooserPanel("banner_cta"),
            ],
            heading="Banner Options",
        )
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(banner_panels, heading="Banner Settings"),
            ObjectList(Page.promote_panels, heading="Promotional Staff"),
            ObjectList(Page.settings_panels, heading="Settings Staff"),
        ]
    )

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
        db_table = "home_page"

    @route(r'^subscribe/$')
    def subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        return render(request, "home/subscribe.html", context)
