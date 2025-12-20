from django.contrib import admin
from .models import Article, Prayer, City, State, Country

# Register your models here.
admin.site.register(Prayer)

class PatronInline(admin.TabularInline):
    model = Article.patron_of.through
    extra = 0

class PatronStateInline(admin.TabularInline):
    model = State.patron_saints.through
    extra = 0

class PatronCountryInline(admin.TabularInline):
    model = Country.patron_saints.through
    extra = 0

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    inlines = [PatronInline]
    list_display = ('name', 'state', 'country')

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    inlines = [PatronStateInline]
    list_display = ('name', 'abbreviation', 'country')

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = [PatronCountryInline]
    list_display = ('name', 'name_pt', 'name_en')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('patron_of',)
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'title_pt', 'title_en', 'created_at')
