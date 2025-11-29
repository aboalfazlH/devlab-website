from django.utils.html import strip_tags
from django.views.generic import View
from django.http import JsonResponse
from apps.blog.models import Article
import hashlib
from .models import ApiModel
from django.utils.text import slugify

class FrontFakeObjectsApi(View):
    def get(self, request, *args, **kwargs):
        from faker import Faker

        fake = Faker("fa-IR")

        articles = request.GET.get("articles")
        users = request.GET.get("users")

        data = {
            "status": 200,
            "users": [],
            "articles": [],
            "description": "",
        }

        def validate_param(value, name):
            if value is None:
                return 0, None

            try:
                value = int(value)
            except (TypeError, ValueError):
                return None, f"{name} must be an integer"

            if value < 0:
                return None, f"{name} must be a positive number"

            if value > 100:
                return None, f"{name} must be less than or equal to 100"

            return value, None

        articles, err_articles = validate_param(articles, "articles")
        users, err_users = validate_param(users, "users")

        if err_articles or err_users:
            data["status"] = 400
            data["description"] = err_articles or err_users
            return JsonResponse(data, status=400)

        data["description"] = f"create {articles} article and {users} user successfully"

        for i in range(1, users + 1):
            data["users"].append(
                {
                    "username": f"u_{i}",
                    "email": fake.email(),
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "online": fake.boolean(),
                }
            )

        for j in range(1, articles + 1):
            data["articles"].append(
                {
                    "title": fake.text(max_nb_chars=30),
                    "description": fake.text(max_nb_chars=120),
                    "author": f"{fake.first_name()} {fake.last_name()}",
                    "write_date": fake.date_time(),
                    "pin": fake.boolean(),
                    "active": fake.boolean(),
                    "verify": fake.boolean(),
                }
            )

        return JsonResponse(data)


class DevelopLabGetArticlesApi(View):
    def get(self, request, articles=0, *args, **kwargs):
        data = {
            "status": 200,
            "articles": [],
            "description": f"get last {articles} article succesfuly",
        }
        articles = Article.objects.filter(
            is_active=True, author__public_article=True
        ).order_by("-write_date")[: articles + 1]
        for _ in articles:
            data["articles"].append(
                {
                    "title": _.title,
                    "thumbnail": _.thumbnail.url,
                    "description": strip_tags(_.description),
                    "author": _.author.get_full_name(),
                    "write_date": _.write_date.strftime("%Y-%m-%d %H:%M"),
                    "pin": _.is_pin,
                    "active": _.is_active,
                    "verify": _.is_verify,
                    "categories": list(_.categories.values("id", "name")),
                }
            )
        if data["articles"] == []:
            data["status"] = 404
            data["description"] = "query is null"
        return JsonResponse(data, safe=False)



class WriteArticle(View):
    def get(self, request, token, *args, **kwargs):
        hashed_token = hashlib.sha256(token.encode()).hexdigest()

        try:
            api_entry = ApiModel.objects.get(token=hashed_token, is_active=True)
        except ApiModel.DoesNotExist:
            return JsonResponse({"status": 403, "description": "Invalid token."})

        title = request.GET.get("title")
        short_description = request.GET.get("short_description")
        description = request.GET.get("description")
        slug = request.GET.get("slug") or slugify(title or "")

        if not title:
            return JsonResponse({"status": 400, "description": "Title is required."})

        article = Article.objects.create(
            title=title,
            short_description=short_description or "",
            description=description,
            slug=slug,
            author=api_entry.user,
            is_active=True
        )

        return JsonResponse({
            "status": 200,
            "description": f"Article '{article.title}' created successfully.",
            "article_id": article.id,
        })
