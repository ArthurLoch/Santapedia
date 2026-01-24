from django.contrib.sitemaps import Sitemap
from django.utils import translation
from articles.models import Article


class ArticleSitemapPT(Sitemap):
    protocol = "https"

    def items(self):
        return Article.objects.all()

    def location(self, obj):
        with translation.override("pt-br"):
            return obj.get_absolute_url()


class ArticleSitemapEN(Sitemap):
    protocol = "https"

    def items(self):
        return Article.objects.all()

    def location(self, obj):
        with translation.override("en"):
            return obj.get_absolute_url()
        