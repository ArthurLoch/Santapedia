# sitemaps.py
from django.contrib.sitemaps import Sitemap
from articles.models import Article, Prayer

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class PrayerSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Prayer.objects.all()

    def lastmod(self, obj):
        return obj.created_at
