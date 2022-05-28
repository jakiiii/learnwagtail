# StreamFields live in here
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        help_text="Add your title"
    )
    text = blocks.TextBlock(
        required=True,
        help_text="Add additional text"
    )

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title and Text"


class CardBlock(blocks.StructBlock):
    # Cards with image and text and button(s)
    title = blocks.CharBlock(
        required=True,
        help_text="Add your title"
    )
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(max_length=40, required=True)),
                ("text", blocks.TextBlock(max_length=200, required=True)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(
                    required=False, help_text="If the button page above is selected, that will be used first."
                ))
            ]
        )
    )

    class Meta:
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Staff Card"


class RichTextBlock(blocks.RichTextBlock):
    # richtext with all the features

    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"


class SimpleRichTextBlock(blocks.RichTextBlock):
    # richtext without (limited) all the features

    def __init__(self, required=True, help_text=None, editor="default", features=None, validators=(), **kwargs):
        self.features = [
            "bold",
            "italic",
            "link"
        ]
        super().__init__(**kwargs)

    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"


class CTABlock(blocks.StructBlock):
    # A simple to action section
    title = blocks.CharBlock(
        required=True,
        help_text="Add your title"
    )
    text = blocks.RichTextBlock(
        required=True, features=["blog", "italic"]
    )
    button_page = blocks.PageChooserBlock(
        required=False
    )
    button_url = blocks.URLBlock(
        required=False
    )
    button_text = blocks.CharBlock(
        max_length=40,
        required=False,
        default="Learn More",
    )

    class Meta:
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"


class LinkStructValue(blocks.StructValue):
    # Additional logic or internal url

    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url
        return None


class ButtonBlock(blocks.StructBlock):
    # External and internal URL
    button_page = blocks.PageChooserBlock(
        required=False,
        help_text="If selected, this url will be used first"
    )
    button_url = blocks.URLBlock(
        required=False,
        help_text="If added, this url will be used secondarily to the button page"
    )

    class Meta:
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue
