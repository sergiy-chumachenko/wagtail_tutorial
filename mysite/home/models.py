from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (FieldPanel,
                                                InlinePanel,
                                                MultiFieldPanel,
                                                PageChooserPanel)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    body = RichTextField(blank=True)
    disc_t = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('disc_t'),
    ]

    content_panels = Page.content_panels + [
        InlinePanel('slider_items', label="Slider"),
        FieldPanel('body', classname="full"),
        FieldPanel('disc_t', classname="full"),
    ]


class LinkFields(models.Model):
    link_external = models.URLField("URL", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
    ]

    class Meta:
        abstract = True


class SliderItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image')
    ]

    class Meta:
        abstract = True


class HomePageSliderItem(Orderable, SliderItem):
    page = ParentalKey('HomePage', related_name='slider_items')
