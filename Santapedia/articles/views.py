from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Prayer, City, State, Country
from django.http import JsonResponse
import unicodedata
from random import randint
from django.conf import settings
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.db.models.functions import Lower
from datetime import date
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F
from django.views.decorators.cache import cache_page
from django.urls import reverse

@cache_page(60 * 10)
def home(request):
    # Filter 5 articles and 5 prayers to be featured on the homepage
    articles = (Article.objects.only('id','title_pt', 'title_en', 'description_pt', 'description_en', 'content_pt', 'content_en', 'slug', 'image').order_by('title_pt')[:5])

    prayers = (Prayer.objects.select_related('saint').only('id','title_pt', 'title_en', 'content_pt', 'content_en', 'saint__id', 'saint__title_pt', 'saint__title_en', 'saint__image').order_by('title_pt')[:5])

    return render(request, 'htmls/home.html', {'saints': articles, 'len_saints': Article.objects.count(), 'len_prayers': Prayer.objects.count(), 'prayers': prayers})

def redirect_to_home(request):
    # if the URL is empty, redirect to home
    return redirect(reverse('home'))

@cache_page(60 * 10)
def saints(request):
    # Field definition according to language
    lang = request.LANGUAGE_CODE
    title_field = "title_en" if lang == "en" else "title_pt"
    country_field = "country_en" if lang == "en" else "country_pt"
    category_field = "category_en" if lang == "en" else "category_pt"
    vector_field = "search_vector_en" if lang == "en" else "search_vector_pt"

    articles = Article.objects.all()

    # Filters
    order = request.GET.get("order", "")
    category = request.GET.get("category", "")
    country = request.GET.get("country", "")
    title = request.GET.get("q") or request.GET.get("title", "")

    # Filter articles according to the selected filter
    if category:
        articles = articles.filter(**{category_field: category})

    if country:
        articles = articles.filter(**{country_field: country})

    if title:
        # Filter by full-text search
        query = SearchQuery(title)
        articles = (
            articles
            .annotate(rank=SearchRank(F(vector_field), query))
            .filter(rank__gt=0)
            .order_by("-rank")
        )


    # Sort according to the selected option
    if order == "latest":
        articles = articles.order_by("-created_at")
    elif order == "oldest":
        articles = articles.order_by("created_at")
    else:
        articles = articles.order_by(Lower(title_field))

   
   # Display available Countries and Categories in the filter
    countries = (
        Article.objects
        .exclude(**{country_field: ""})
        .values_list(country_field, flat=True)
        .distinct()
        .order_by(country_field)
    )

    categories = (
        Article.objects
        .exclude(**{category_field: ""})
        .values_list(category_field, flat=True)
        .distinct()
        .order_by(category_field)
    )

    return render(
        request,
        "htmls/saints.html",
        {
            "articles": articles,
            "len_articles": articles.count(),
            "countries": countries,
            "categories": categories,
            "saints": True,
        },
    )

@cache_page(60 * 10)
def prayers(request):
    # Field definition according to language
    lang = request.LANGUAGE_CODE
    title_field = "title_en" if lang == "en" else "title_pt"
    saint_field = "saint__title_en" if lang == "en" else "saint__title_pt"
    category_field = "category_en" if lang == "en" else "category_pt"
    vector_field = "search_vector_en" if lang == "en" else "search_vector_pt"

    prayers = (
        Prayer.objects
        .select_related("saint")
        .only(
            "id",
            "title_pt", "title_en",
            "content_pt", "content_en",
            "created_at",
            "category_pt", "category_en",
            "saint_id",
            "saint__title_pt",
            "saint__title_en",
            "saint__image",
        )
    )

    # Filters
    order = request.GET.get("order", "")
    category = request.GET.get("category", "")
    saint = request.GET.get("saint", "")
    title = request.GET.get("q") or request.GET.get("title", "")


    # Filter articles according to the selected filter
    if category:
        prayers = prayers.filter(**{category_field: category})

    if saint:
        prayers = prayers.filter(**{saint_field: saint})

    if title:
        # Filter by full-text search
        query = SearchQuery(title)
        prayers = (
            prayers
            .annotate(rank=SearchRank(F(vector_field), query))
            .filter(rank__gt=0)
            .order_by("-rank")
        )

    # Sort according to the selected option
    if order == "latest":
        prayers = prayers.order_by("-created_at")
    elif order == "oldest":
        prayers = prayers.order_by("created_at")
    else:
        prayers = prayers.order_by(Lower(title_field))

    
    prayers = list(prayers)

    # Display available Saints and Categories in the filter
    saints = (
        Prayer.objects
        .exclude(saint__isnull=True)
        .values_list(saint_field, flat=True)
        .distinct()
        .order_by(saint_field)
    )

    categories = (
        Prayer.objects
        .exclude(**{category_field: ""})
        .values_list(category_field, flat=True)
        .distinct()
        .order_by(category_field)
    )

    return render(
        request,
        "htmls/prayers.html",
        {
            "prayers": prayers,
            "len_prayers": len(prayers),
            "saints": saints,
            "categories": categories,
        }
    )

def santapedia(request):
    # Return the 'About Santapedia' page
    return render(request, 'htmls/santapedia.html')

@cache_page(60 * 10)
def article_detail(request, slug):
    # Return the page of a specific article
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'htmls/detail.html', {'article': article,})


def search_suggestions(request):
    # Suggestion list for the search bar

    # q is what the user is typing
    q = request.GET.get("q", "").strip()

    if not q:
        return JsonResponse({"results": []})

    is_pt = request.LANGUAGE_CODE.startswith("pt")

    # Field definition according to language
    title_field = "title_pt" if is_pt else "title_en"
    description_field = "description_pt" if is_pt else "description_en"

    # Filter articles containing the entered text in the title
    articles = (
        Article.objects
        .filter(**{f"{title_field}__icontains": q})
        .only(title_field, description_field, "slug", "image")[:10]
    )

    results = [
        {
            "title": getattr(a, title_field) or "",
            "description": getattr(a, description_field) or "",
            "slug": a.slug,
            "image": a.image.url if a.image else "",
        }
        for a in articles
    ]

    return JsonResponse({"results": results})
        

def aleatory(request):
    # Redirect to a random article
    number = randint(1, Article.objects.count())
    article = Article.objects.filter(id=number).defer('slug').first()

    return redirect(f'/articles/{article.slug}/')

@cache_page(60 * 10)
def patronized_cities(request):
    # Get filter parameters
    country_id = request.GET.get("country")
    state_abbreviation = request.GET.get("state")
    city_id = request.GET.get("city")

    # Determine state_id from state_abbreviation and country_id
    state_id = State.objects.filter(abbreviation=state_abbreviation, country_id=country_id).values_list("id", flat=True).first() if state_abbreviation else None
    
    # Display available Countries in the filter
    countries = Country.objects.only("id", "name_pt", "name_en").order_by("name_pt")

    # Initialize empty querysets
    states = State.objects.none()
    cities = City.objects.none()
    saints = Article.objects.none()

    # Display States based on selected Country
    if country_id:
        states = (
            State.objects
            .filter(country_id=country_id)
            .only("id", "name", "abbreviation")
            .order_by("name")
        )

    # Display Cities based on selected State
    if state_abbreviation:
        cities = (
            City.objects
            .filter(state=state_abbreviation)
            .only("id", "name")
            .order_by("name")
        )

    # Display Saints based on selected City, State, or Country
    if city_id:
        saints = (
            Article.objects
            .filter(patron_of=city_id)
            .only(
                "id",
                "title_pt", "title_en",
                "description_pt", "description_en",
                "slug", "image"
            )
            .distinct()
        )

    elif state_id:
        saints = (
            Article.objects
            .filter(patrons_of_state=state_id)
            .only(
                "id",
                "title_pt", "title_en",
                "description_pt", "description_en",
                "slug", "image"
            )
            .distinct()
        )

    elif country_id:
        saints = (
            Article.objects
            .filter(patrons_of_country__id=country_id)
            .only(
                "id",
                "title_pt", "title_en",
                "description_pt", "description_en",
                "slug", "image"
            )
            .distinct()
        )

    return render(
        request,
        "htmls/patronized_cities.html",
        {
            "countries": countries,
            "states": states,
            "cities": cities,
            "saints": saints,
        },
    )

def get_states_by_country(request):
    # Get states for a given country (AJAX)
    country_id = request.GET.get("country")
    if not country_id:
        return JsonResponse({"states": []})

    states = State.objects.filter(country_id=country_id).values("abbreviation", "name").order_by("name")

    return JsonResponse({"states": list(states)})


def get_cities_by_state(request):
    # Get cities for a given state and country (AJAX)
    state_id = request.GET.get("state")
    country_id = request.GET.get("country")
    if not state_id:
        return JsonResponse({"cities": []})

    country = Country.objects.filter(id=country_id).first()
    cities = City.objects.filter(state=state_id, country=country.name_pt).values("name", "id").order_by("name")

    return JsonResponse({"cities": list(cities)})

def calendar_data(request):
    # Return JSON data for the calendar of saints' feast days
    current_year = date.today().year
    lang = request.LANGUAGE_CODE

    # Field definition according to language
    title_field = "title_en" if lang == "en" else "title_pt"

    # Get all saints with a feast day
    saints = (
        Article.objects
        .filter(feast_day__isnull=False)
        .values("feast_day", title_field, "slug")
    )

    events = []

    for s in saints:
        # Adjust feast day to the current year
        feast_day = s["feast_day"].replace(year=current_year)

        events.append({
            "title": s[title_field],
            "start": feast_day.strftime("%Y-%m-%d"),
            "allDay": True,
            "url": f"/articles/{s['slug']}/",
        })

    return JsonResponse(events, safe=False)

def saints_by_month(request):
    # Return JSON data of saints for a given month
    lang = request.LANGUAGE_CODE
    month = int(request.GET.get("month", date.today().month))
    title_field = "title_en" if lang == "en" else "title_pt"

    # Get saints with feast days in the specified month
    saints = (
        Article.objects
        .filter(feast_day__isnull=False, feast_day__month=month)
        .only("feast_day", title_field, "slug", "image")
    )

    data = []
    for s in saints:
        if not s.feast_day:
            continue

        data.append({
            "title": getattr(s, title_field),
            "slug": s.slug,
            "day": s.feast_day.day,
            "month": s.feast_day.month,
            "image": s.image.url if s.image else "",
        })

    return JsonResponse({"saints": data})

def calendar(request):
    # Return the calendar page
    return render(request, "htmls/calendar.html")

def contact(request):
    # Contact page

    success = False
    if request.method == 'POST':
        # Create form with Django Forms
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            if request.LANGUAGE_CODE == 'en':
                full_message = f"""
                New contact message from Santapédia:

                Name: {name}
                E-mail: {email}
                Subject: {subject}

                Message:
                {message}
                """
                
            else:
                full_message = f"""
                Nova mensagem de contato da Santapédia:

                Nome: {name}
                E-mail: {email}
                Assunto: {subject}

                Mensagem:
                {message}
                """

            # Send an email to santapedia.contato@gmail.com
            email_message = EmailMessage(
                subject = f'[Santapedia] {subject}' if request.LANGUAGE_CODE == 'en' else f'[Santapédia] {subject}',
                body = full_message,
                from_email = settings.DEFAULT_FROM_EMAIL,
                to=[settings.DEFAULT_FROM_EMAIL],
                reply_to=[email],
            )
            email_message.send()
            success = True
    else:
        form = ContactForm()

    return render(request, 'htmls/contact.html', {'form': form, 'success': success})

def privacy_policy(request):
    # Return the Privacy Policy page
    return render(request, 'htmls/privacy_policy.html')