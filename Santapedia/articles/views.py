from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Prayer, City, State, Country
from django.http import JsonResponse
import unicodedata
from random import randint
from django.conf import settings
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.db.models.functions import Lower
from datetime import date, datetime

def home(request):
    articles = Article.objects.all()
    len_saints = len(articles)
    articles = articles.order_by('title')

    saints = []
    for article in articles:
        saints.append(article)
        if len(saints) == 5:
            break

    articles = Prayer.objects.all()
    len_prayers = len(articles)
    articles = articles.order_by('title')

    prayers = []
    for article in articles:
        prayers.append(article)
        if len(prayers) == 5:
            break

    return render(request, 'htmls/home.html', {'saints': saints, 'len_saints': len_saints, 'len_prayers': len_prayers, 'prayers': prayers})

def saints(request):
    
    articles = Article.objects.all()
    countries = []
    categories = []

    for article in articles:
        if request.LANGUAGE_CODE == 'en':
            if article.country_en:
                if article.country_en not in countries:
                    countries.append(article.country_en)

            if article.category_en:
                if article.category_en not in categories:
                    categories.append(article.category_en)

        elif request.LANGUAGE_CODE == 'pt-br':
            if article.country_pt:
                if article.country_pt not in countries:
                    countries.append(article.country_pt)
                    
            if article.category_pt:
                if article.category_pt not in categories:
                    categories.append(article.category_pt)

        

    countries.sort()
    categories.sort()

    if request.method == 'GET':
        order = request.GET.get('order', '')
        category = request.GET.get('category', '')
        country = request.GET.get('country', '')
        title = request.GET.get('title', '')
        q = request.GET.get('q', '')

        if q:
            title = q

        if category:
            if request.LANGUAGE_CODE == 'en':
                articles = articles.filter(category_en=category)
            else:
                articles = articles.filter(category_pt=category)

        if country:
            if request.LANGUAGE_CODE == 'en':
                articles = articles.filter(country_en=country)
            else:
                articles = articles.filter(country_pt=country)

        if title:
            if request.LANGUAGE_CODE == 'en':
                articles = articles.filter(title_en__icontains=title)
            else:
                articles = articles.filter(title_pt__icontains=title)

        if order == 'latest':
            articles = articles.order_by('-created_at')
        elif order == 'oldest':
            articles = articles.order_by('created_at')
        else:
            if request.LANGUAGE_CODE == 'en':
                articles = articles.order_by(Lower('title_en'))
            elif request.LANGUAGE_CODE == 'pt-br':
                articles = articles.order_by(Lower('title_pt'))

        
    return render(request, 'htmls/search.html', {'articles': articles, 'len_articles': len(articles), 'countries': countries, 'categories': categories, 'saints': True})

def prayers(request):
    prayers = Prayer.objects.all()

    saints = []
    categories = []
    for prayer in prayers:
        if request.LANGUAGE_CODE == 'en':
            if prayer.saint:
                if prayer.saint.title_en not in saints:
                    saints.append(prayer.saint.title_en)
            if prayer.category_en:
                if prayer.category_en not in categories:
                    categories.append(prayer.category_en)

        elif request.LANGUAGE_CODE == 'pt-br':
            if prayer.saint:
                if prayer.saint.title_pt not in saints:
                    saints.append(prayer.saint.title_pt)

            if prayer.category_pt:
                if prayer.category_pt not in categories:
                    categories.append(prayer.category_pt)

    saints.sort()
    categories.sort()

    if request.method == 'GET':
        order = request.GET.get('order', '')
        category = request.GET.get('category', '')
        saint = request.GET.get('saint', '')
        title = request.GET.get('title', '')

        if category:
            if request.LANGUAGE_CODE == 'en':
                prayers = prayers.filter(category_en=category)
            elif request.LANGUAGE_CODE == 'pt-br':
                prayers = prayers.filter(category_pt=category)   

        if saint:
            if request.LANGUAGE_CODE == 'en':
                prayers = prayers.filter(saint__title_en = saint)
            elif request.LANGUAGE_CODE == 'pt-br':
                prayers = prayers.filter(saint__title_pt = saint)
        
        if title:
            if request.LANGUAGE_CODE == 'en':
                prayers = prayers.filter(title_en__icontains=title)
            elif request.LANGUAGE_CODE == 'pt-br':
                prayers = prayers.filter(title_pt__icontains=title)

        if order == 'latest':
            prayers = prayers.order_by('-created_at')
        elif order == 'oldest':
            prayers = prayers.order_by('created_at')
        else:
            if request.LANGUAGE_CODE == 'en':
                prayers = prayers.order_by(Lower('title_en'))
            elif request.LANGUAGE_CODE == 'pt-br':
                prayers = prayers.order_by(Lower('title_pt'))

    return render(request, 'htmls/prayers.html', {'prayers': prayers, 'len_prayers': len(prayers), 'saints': saints, 'categories': categories})

def santapedia(request):
    return render(request, 'htmls/santapedia.html')

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    articles = Article.objects.all()
    return render(request, 'htmls/detail.html', {'article': article,
                                                'articles': articles})

def remove_accents(txt):
    if not txt:
        return ""
    
    return ''.join(
        c for c in unicodedata.normalize('NFD', txt)
        if unicodedata.category(c) != 'Mn'
    )

def search_suggestions(request):
    q = request.GET.get('q', '')
    results = []

    if q:
        q_norm = remove_accents(q).lower()
        articles = []

        for a in Article.objects.all():

            if request.LANGUAGE_CODE == 'pt-br':
                title = a.title_pt or ""
                description = a.description_pt or ""

            else:
                title = a.title_en or ""
                description = a.description_en or ""

            if q_norm in remove_accents(title).lower():
                articles.append(a)

            if len(articles) >= 10:
                break

        results = [
            {
                'title': (a.title_pt or "") if request.LANGUAGE_CODE == 'pt-br' else (a.title_en or ""),
                'slug': a.slug,
                'description': (a.description_pt or "") if request.LANGUAGE_CODE == 'pt-br' else (a.description_en or ""),
                'image': a.image.url if a.image else ''
            }
            for a in articles
        ]

    return JsonResponse({'results': results}) 
        

def aleatory(request):
    articles = Article.objects.all()
    number = randint(1, len(articles))
    article = Article.objects.filter(id=number)[0]

    return redirect(f'/articles/{article.slug}')

def patronized_cities(request):

    country_id = request.GET.get("country")
    state_id = request.GET.get("state")
    city_name = request.GET.get("city")

    countries = Country.objects.all().order_by("name")

    states = []
    cities = []
    saints = []

    if country_id:
        states = State.objects.filter(country_id=country_id).order_by("name")
        if not state_id and not city_name:
            saints = Article.objects.filter(
            patrons_of_country=country_id
        ).distinct()

    if state_id:
        country = Country.objects.filter(id=country_id).first()
        cities = City.objects.filter(state=state_id, country=country.name_pt).order_by("name")
        if not city_name:
            id = State.objects.filter(abbreviation=state_id).first()
            saints = Article.objects.filter(
            patrons_of_state=id
        ).distinct()

    if city_name and state_id:
        saints = Article.objects.filter(
            patron_of=city_name
        ).distinct()

    return render(request, "htmls/patronized_cities.html", {
        "countries": countries,
        "states": states,
        "cities": cities,
        "saints": saints,
    })

def get_states_by_country(request):
    country_id = request.GET.get("country")
    if not country_id:
        return JsonResponse({"states": []})

    states = State.objects.filter(country_id=country_id).values("abbreviation", "name").order_by("name")

    return JsonResponse({"states": list(states)})


def get_cities_by_state(request):
    state_id = request.GET.get("state")
    country_id = request.GET.get("country")
    if not state_id:
        return JsonResponse({"cities": []})

    country = Country.objects.filter(id=country_id).first()
    cities = City.objects.filter(state=state_id, country=country.name_pt).values("name", "id").order_by("name")

    return JsonResponse({"cities": list(cities)})

def calendar_data(request):
    """Retorna eventos para o FullCalendar, forçando allDay e anulando o ano para o ano atual."""
    current_year = date.today().year
    saints = Article.objects.exclude(feast_day__isnull=True)
    events = []

    for saint in saints:
        # substitui o ano pelo ano atual (evita anos estranhos como 0001)
        try:
            feast_day = saint.feast_day.replace(year=current_year)
        except Exception:
            # fallback: se algo der errado, usa dia/mês atuais (não ideal, mas evita crash)
            continue

        # formata como ISO date (YYYY-MM-DD) e marca allDay true para evitar shifts de timezone
        events.append({
            "title": saint.title_en if request.LANGUAGE_CODE == 'en' else saint.title_pt,
            "start": feast_day.strftime("%Y-%m-%d"),
            "allDay": True,
            "url": f"/articles/{saint.slug}/"
        })

    return JsonResponse(events, safe=False)

def saints_by_month(request):
    try:
        month = int(request.GET.get("month") or date.today().month)
    except ValueError:
        month = date.today().month

    saints = Article.objects.filter(feast_day__isnull=False, feast_day__month=month).order_by('feast_day')

    data = []
    for s in saints:
        data.append({
            "title_pt": s.title_pt,
            "title_en": s.title_en,
            "slug": s.slug,
            "day": s.feast_day.day,
            "month": s.feast_day.month,
            "image": s.image.url if getattr(s, "image", None) else None,
        })
    return JsonResponse({"saints": data})

def calendar(request):
    today = date.today()
    current_month = today.month

    saints_this_month = Article.objects.filter(
        feast_day__month=current_month
    ).order_by('feast_day')

    context = {
        "saints_this_month": saints_this_month
    }
    return render(request, "htmls/calendar.html", context)

def contact(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"""
            Nova mensagem de contato da Santapédia:

            Nome: {name}
            E-mail: {email}
            Assunto: {subject}

            Mensagem:
            {message}
            """

            email_message = EmailMessage(
                subject = f'[Santapédia] {subject}',
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
    return render(request, 'htmls/privacy_policy.html')