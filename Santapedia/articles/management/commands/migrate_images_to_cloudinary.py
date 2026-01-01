import cloudinary.api
from articles.models import Article
existing = {
    r["public_id"] for r in cloudinary.api.resources(
        type="upload",
        prefix="saints",
        max_results=500
    )["resources"]
}

for a in Article.objects.all():
    if f"saints/{a.slug}" not in existing:
        print("FALTA:", a.slug)
