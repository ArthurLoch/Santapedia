from django.db import models
from django.db.models import CharField, SlugField, DateField, DateTimeField, ImageField, TextField, ManyToManyField, ForeignKey
from django.utils.text import slugify

# Create your models here.
class Article(models.Model):
    title = CharField(max_length=100)
    slug = SlugField(unique=True, blank=True)
    content = TextField(blank=True, null=True)
    description = TextField(blank=True, null=True)
    image = ImageField(upload_to='saints/', blank=True, null=True)
    category = CharField(max_length=100)
    country = CharField(max_length=100)

    born_date = DateField(blank=True, null=True)
    death_date = DateField(blank=True, null=True)

    born_date_text = CharField(max_length=100, blank=True, null=True)
    death_date_text = CharField(max_length=100, blank=True, null=True)

    birth_place = CharField(max_length=150, blank=True, null=True)
    death_place = CharField(max_length=150, blank=True, null=True)

    feast_day = DateField(blank=True, null=True)
    canonization_date = DateField(blank=True, null=True)
    canonization_date_text = CharField(max_length=100, blank=True, null=True)

    patronages = TextField(blank=True, null=True)
    patron_of = ManyToManyField('City', related_name='patrons', blank=True)
    
    quotes = TextField(blank=True, null=True)
    sources = TextField(blank=True, null=True)
    
    title_pt = CharField(max_length=100)
    content_pt = TextField()
    description_pt = TextField()
    category_pt = CharField(max_length=100)
    country_pt = CharField(max_length=100)

    born_date_text_pt = CharField(max_length=100, blank=True, null=True)
    death_date_text_pt = CharField(max_length=100, blank=True, null=True)

    birth_place_pt = CharField(max_length=150, blank=True, null=True)
    death_place_pt = CharField(max_length=150, blank=True, null=True)

    canonization_date_text_pt = CharField(max_length=100, blank=True, null=True)

    patronages_pt = TextField(blank=True, null=True)

    quotes_pt = TextField(blank=True, null=True)
    sources_pt = TextField(blank=True, null=True)

    title_en = CharField(max_length=100)
    content_en = TextField()
    description_en = TextField()
    category_en = CharField(max_length=100)
    country_en = CharField(max_length=100)

    born_date_text_en = CharField(max_length=100, blank=True, null=True)
    death_date_text_en = CharField(max_length=100, blank=True, null=True)

    birth_place_en = CharField(max_length=150, blank=True, null=True)
    death_place_en = CharField(max_length=150, blank=True, null=True)

    canonization_date_text_en = CharField(max_length=100, blank=True, null=True)

    patronages_en = TextField(blank=True, null=True)

    quotes_en = TextField(blank=True, null=True)
    sources_en = TextField(blank=True, null=True)

    created_at = DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.title
    

class Prayer(models.Model):
    saint = models.ForeignKey('Article', on_delete=models.CASCADE, null=True, blank=True, related_name='prayers')
    title = CharField(max_length=200)
    content = TextField()
    category = CharField(max_length=200, null=True, blank=True)

    title_pt = CharField(max_length=200)
    content_pt = TextField()
    category_pt = CharField(max_length=200, null=True, blank=True)

    title_en = CharField(max_length=200)
    content_en = TextField()
    category_en = CharField(max_length=200, null=True, blank=True)

    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class City(models.Model):
    name = CharField(max_length=150)
    state = CharField(max_length=150)
    country = CharField(max_length=150)
    country_en = CharField(max_length=150)

    def __str__(self):
        return self.name

class State(models.Model):
    name = CharField(max_length=150)
    abbreviation = CharField(max_length=50)
    country = ForeignKey('Country', on_delete=models.CASCADE, related_name='states')
    patron_saints = ManyToManyField('Article', related_name='patrons_of_state', blank=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = CharField(max_length=150)
    name_pt = CharField(max_length=150)
    name_en = CharField(max_length=150)
    patron_saints = ManyToManyField('Article', related_name='patrons_of_country', blank=True)

    def __str__(self):
        return self.name