from django.db import models
from django.db.models import CharField, SlugField, DateField, DateTimeField, ImageField, TextField, ManyToManyField, ForeignKey
from django.utils.text import slugify
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from cloudinary.models import CloudinaryField
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    title = CharField(max_length=100, db_index=True)
    slug = SlugField(unique=True, blank=True, db_index=True)
    image = CloudinaryField('image', blank=True, null=True, db_index=True)

    born_date = DateField(blank=True, null=True, db_index=True)
    death_date = DateField(blank=True, null=True, db_index=True)

    feast_day = DateField(blank=True, null=True, db_index=True)
    canonization_date = DateField(blank=True, null=True, db_index=True)

    patron_of = ManyToManyField('City', related_name='patrons', blank=True, db_index=True)
    
    
    title_pt = CharField(max_length=100, db_index=True)
    content_pt = TextField()
    description_pt = TextField(db_index=True)
    category_pt = CharField(max_length=100, db_index=True)
    country_pt = CharField(blank=True, null=True, max_length=100, db_index=True)

    born_date_text_pt = CharField(max_length=100, blank=True, null=True, db_index=True)
    death_date_text_pt = CharField(max_length=100, blank=True, null=True, db_index=True)

    birth_place_pt = CharField(max_length=150, blank=True, null=True, db_index=True)
    death_place_pt = CharField(max_length=150, blank=True, null=True, db_index=True)

    canonization_date_text_pt = CharField(max_length=100, blank=True, null=True, db_index=True)

    patronages_pt = TextField(blank=True, null=True, db_index=True)

    quotes_pt = TextField(blank=True, null=True)
    sources_pt = TextField(blank=True, null=True, db_index=True)

    title_en = CharField(max_length=100, db_index=True)
    content_en = TextField()
    description_en = TextField(db_index=True)
    category_en = CharField(max_length=100, db_index=True)
    country_en = CharField(blank=True, null=True, max_length=100, db_index=True)

    born_date_text_en = CharField(max_length=100, blank=True, null=True, db_index=True)
    death_date_text_en = CharField(max_length=100, blank=True, null=True, db_index=True)

    birth_place_en = CharField(max_length=150, blank=True, null=True, db_index=True)
    death_place_en = CharField(max_length=150, blank=True, null=True, db_index=True)

    canonization_date_text_en = CharField(max_length=100, blank=True, null=True, db_index=True)

    patronages_en = TextField(blank=True, null=True, db_index=True)

    quotes_en = TextField(blank=True, null=True)
    sources_en = TextField(blank=True, null=True, db_index=True)

    created_at = DateTimeField(auto_now_add=True, db_index=True)

    search_vector_pt = SearchVectorField(null=True)
    search_vector_en = SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector_pt"]),
            GinIndex(fields=["search_vector_en"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        Article.objects.filter(pk=self.pk).update(
            search_vector_pt=(
                SearchVector("title_pt", weight="A") +
                SearchVector("content_pt", weight="B") +
                SearchVector("quotes_pt", weight="C")
            ),
            search_vector_en=(
                SearchVector("title_en", weight="A") +
                SearchVector("content_en", weight="B") +
                SearchVector("quotes_en", weight="C")
            )
        )

    def get_absolute_url(self):
        return reverse("article_detail", args=[self.slug])
    
    def __str__(self):
        return self.title
    

class Prayer(models.Model):
    saint = models.ForeignKey('Article', on_delete=models.CASCADE, null=True, blank=True, related_name='prayers', db_index=True)
    title = CharField(max_length=200, db_index=True)

    title_pt = CharField(max_length=200, db_index=True)
    content_pt = TextField()
    category_pt = CharField(max_length=200, null=True, blank=True, db_index=True)

    title_en = CharField(max_length=200, db_index=True)
    content_en = TextField()
    category_en = CharField(max_length=200, null=True, blank=True, db_index=True)

    created_at = DateTimeField(auto_now_add=True, db_index=True)

    search_vector_pt = SearchVectorField(null=True)
    search_vector_en = SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector_pt"]),
            GinIndex(fields=["search_vector_en"]),
        ]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # 1️⃣ salva normalmente
        super().save(*args, **kwargs)

        # 2️⃣ atualiza o search_vector no banco
        Prayer.objects.filter(pk=self.pk).update(
            search_vector_pt=(
                SearchVector("title_pt", weight="A") +
                SearchVector("content_pt", weight="B")
            ),
            search_vector_en=(
                SearchVector("title_en", weight="A") +
                SearchVector("content_en", weight="B")
            )
        )


class City(models.Model):
    name = CharField(max_length=150, db_index=True)
    state = CharField(max_length=150, db_index=True)
    country = CharField(max_length=150, db_index=True)
    country_en = CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.name

class State(models.Model):
    name = CharField(max_length=150, db_index=True)
    abbreviation = CharField(max_length=50, db_index=True)
    country = ForeignKey('Country', on_delete=models.CASCADE, related_name='states', db_index=True)
    patron_saints = ManyToManyField('Article', related_name='patrons_of_state', blank=True, db_index=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = CharField(max_length=150, db_index=True)
    name_pt = CharField(max_length=150, db_index=True)
    name_en = CharField(max_length=150, db_index=True)
    patron_saints = ManyToManyField('Article', related_name='patrons_of_country', blank=True, db_index=True)

    def __str__(self):
        return self.name