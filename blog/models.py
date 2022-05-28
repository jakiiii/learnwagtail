from django.db import models
from django.shortcuts import render

from wagtail.models import Page, Orderable
from wagtail.core.fields import StreamField
from modelcluster.fields import ParentalKey
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet

from streams import blocks


class BlogAuthorsOrderable(Orderable):
    page = ParentalKey(
        "blog.BlogDetailsPage",
        related_name="blog_author"
    )
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.SET_NULL,
        null=True
    )

    panel = [
        SnippetChooserPanel("author")
    ]


@register_snippet
class BlogAuthor(models.Model):
    # blog author for snippets
    name = models.CharField(
        max_length=100,
    )
    website = models.URLField(
        null=True,
        blank=True
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image")
            ],
            heading="Name and Image"
        ),
        MultiFieldPanel(
            [
                FieldPanel("website")
            ]
        )
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"
        db_table = "blog_author"


class BlogListingPage(RoutablePageMixin, Page):
    template = "blog/blog_listing_page.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title"
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BlogListingPage, self).get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailsPage.objects.live().public()
        context['authors'] = BlogAuthor.objects.all()
        return context

    @route(r'^latest/$', name='latest_post')
    def latest_blog_post(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['posts'] = context['posts'][:1]
        return render(request, "blog/latest_posts.html", context)

    def get_sitemap_urls(self, request=None):
        sitemap = super(BlogListingPage, self).get_sitemap_urls(request=request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_post"),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.9
            }
        )
        return sitemap


class BlogDetailsPage(Page):
    template = "blog/blog_detail_page.html"

    custom_title = models.CharField(
        max_length=100,
        help_text="Overwrites the default title"
    )
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
    )

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock())
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("blog_image"),
        MultiFieldPanel(
            [
                InlinePanel(
                    "blog_author",
                    label="Author",
                    min_num=1,
                    max_num=5,
                )
            ],
            heading="Author(s)"
        ),
        StreamFieldPanel("content")
    ]
