from django.db import models
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
)

from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )


class ContactPage(WagtailCaptchaEmailForm):  # (AbstractEmailForm):
    template = 'contact/contact_page.html'
    subpage_types = []
    parent_page_types = ['home.HomePage']

    intro = models.CharField(
        max_length=200,
        blank=True
    )
    thank_you_text = RichTextField(
        blank=True
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label='Form Field'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel('from_address', classname="col6"),
                        FieldPanel('to_address', classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            heading="Email Settings"
        ),
    ]

    @cached_property
    def home_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(ContactPage, self).get_context(request, *args, **kwargs)
        context["home_page"] = self.home_page
        return context

    def get_form_fields(self):
        return self.form_fields.all()
