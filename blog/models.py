from django.db import models
from django.shortcuts import render
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from wagtail.models import Page, Orderable
from wagtail.core.fields import StreamField
from modelcluster.fields import ParentalKey, ParentalManyToManyField
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


@register_snippet
class BlogCategory(models.Model):
    # blog category for a snippet
    name = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        unique=True,
        max_length=255,
        help_text="A slug to identify post by this category"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        db_table = "blog_categories"
        ordering = ("name",)


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
        all_posts = BlogDetailsPage.objects.live().public().order_by('-first_published_at')

        paginator = Paginator(all_posts, 2)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context["posts"] = posts

        context['authors'] = BlogAuthor.objects.all()
        context['categories'] = BlogCategory.objects.all()
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
    # Parental Blog Detail Page
    template = "blog/blog_detail_page.html"

    custom_title = models.CharField(
        max_length=100,
        help_text="Overwrites the default title"
    )
    banner_image = models.ForeignKey(
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
    categories = ParentalManyToManyField(
        "blog.BlogCategory",
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("banner_image"),
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
        MultiFieldPanel(
            [
                FieldPanel(
                    "categories",
                    widget=forms.CheckboxSelectMultiple
                )
            ],
            heading="Categories"
        ),
        StreamFieldPanel("content")
    ]

    def save(self, *args, **kwargs):
        post_cash_key = make_template_fragment_key('blog_post_preview', [self.id])
        cache.delete(post_cash_key)
        return super(BlogDetailsPage, self).save(*args, **kwargs)


# FIRST SUBCLASS BLOG POST PAGE
class ArticleBlogPage(BlogDetailsPage):
    # A subclassed blog post page for articles
    template = "blog/article_blog.html"

    subtitle = models.CharField(
        max_length=100,
        default='',
        blank=True,
        null=True
    )
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Best size for this image will be 1400x400"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("custom_title"),
                FieldPanel("subtitle"),
            ],
            heading="Article Title"
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel("banner_image"),
                ImageChooserPanel("intro_image"),
            ],
            heading="Article Image(s)"
        ),
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
        MultiFieldPanel(
            [
                FieldPanel(
                    "categories",
                    widget=forms.CheckboxSelectMultiple
                )
            ],
            heading="Categories"
        ),
        StreamFieldPanel("content")
    ]


# SECOND SUBCLASS PAGE
class VideoBlogPage(BlogDetailsPage):
    # a video subclass page
    template = "blog/article_video_blog.html"

    youtube_video_id = models.CharField(
        max_length=50
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("custom_title"),
            ],
            heading="Article Title"
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel("banner_image"),
            ],
            heading="Article Image"
        ),
        MultiFieldPanel(
            [
                FieldPanel("youtube_video_id"),
            ],
            heading="Article Video"
        ),
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
        MultiFieldPanel(
            [
                FieldPanel(
                    "categories",
                    widget=forms.CheckboxSelectMultiple
                )
            ],
            heading="Categories"
        ),
        StreamFieldPanel("content")
    ]
