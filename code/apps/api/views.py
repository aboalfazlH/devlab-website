from faker import Faker
from django.utils.text import slugify

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from apps.blog.models import Article
from .permissions import HasValidApiToken
from .serializers import ArticleSerializer, ArticleCreateSerializer


class FrontFakeObjectsApi(APIView):

    def validate_param(self, value, name):
        if value is None:
            return 0, None

        try:
            value = int(value)
        except (TypeError, ValueError):
            return None, f"{name} must be an integer"

        if value < 0:
            return None, f"{name} must be positive"
        if value > 100:
            return None, f"{name} must be <= 100"

        return value, None

    def get(self, request):
        fake = Faker("fa-IR")

        articles, err_articles = self.validate_param(
            request.GET.get("articles"), "articles"
        )
        users, err_users = self.validate_param(request.GET.get("users"), "users")

        if err_articles or err_users:
            return Response(
                {"status": 400, "description": err_articles or err_users},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "status": 200,
            "description": f"Created {articles} articles and {users} users successfully",
            "users": [],
            "articles": [],
        }

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

        return Response(data)


class DevelopLabGetArticlesApi(ListAPIView):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        limit = int(self.kwargs.get("articles", 0)) + 1
        return Article.objects.filter(
            is_active=True, author__public_article=True
        ).order_by("-write_date")[:limit]


class WriteArticle(APIView):

    permission_classes = [HasValidApiToken]

    def post(self, request, token):
        data = request.data.copy()

        if "slug" not in data or not data["slug"]:
            data["slug"] = slugify(data.get("title", ""))

        serializer = ArticleCreateSerializer(
            data=data, context={"author": request.api_entry.user}
        )

        if not serializer.is_valid():
            return Response(
                {
                    "status": 400,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        article = serializer.save()

        return Response(
            {
                "status": 200,
                "description": f"Article '{article.title}' created successfully.",
                "article_id": article.id,
            }
        )
