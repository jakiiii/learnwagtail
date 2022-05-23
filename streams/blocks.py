# StreamFields live in here
from wagtail.core import blocks


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
