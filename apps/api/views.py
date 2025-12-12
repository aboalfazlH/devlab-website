
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ApiModel
from faker import Faker
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.views.decorators.csrf import csrf_exempt
from apps.blog.models import Article
from .permissions import HasValidApiToken
from .serializers import ArticleSerializer, ArticleCreateSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


@extend_schema(
    summary="ساخت داده‌های تست برای فرانت",
    description="این API تعداد مشخصی کاربر و مقاله را به صورت تصادفی تولید می‌کند.",
    parameters=[
        OpenApiParameter(
            name="lang",
            required=False,
            description="زبان تولید دیتا توسط Faker (پیش‌فرض: fa-IR)",
            type=str,
        ),
        OpenApiParameter(
            name="articles",
            description="تعداد مقالات (0 تا 100)",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="users",
            description="تعداد کاربران (0 تا 100)",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: OpenApiExample(
            "مثال خروجی موفق",
            value={
                "status": 200,
                "description": "Created 3 articles and 2 users successfully",
                "users": [
                    {
                        "username": "u_1",
                        "email": "example@mail.com",
                        "first_name": "Ali",
                        "last_name": "Rezai",
                        "online": True,
                    }
                ],
                "articles": [
                    {
                        "title": "متن تستی",
                        "description": "توضیحات...",
                        "author": "Ali Reza",
                        "write_date": "2025-01-01T12:00:00Z",
                        "pin": False,
                        "active": True,
                        "verify": True,
                    }
                ],
            },
        ),
        400: OpenApiExample(
            "ورودی اشتباه",
            value={"status": 400, "description": "articles must be positive"},
        ),
    },
)
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
        lang = request.GET.get("lang") or "fa-IR"
        fake = Faker(lang)

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


@extend_schema(
    summary="دریافت جدیدترین مقالات",
    parameters=[
        OpenApiParameter(
            name="count",
            location=OpenApiParameter.PATH,
            description="تعداد مقالات مورد نیاز",
            required=True,
            type=int,
        )
    ],
    responses=ArticleSerializer,
)
class DevelopLabGetArticlesApi(ListAPIView):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        limit = int(self.kwargs.get("count", 0)) + 1
        return Article.objects.filter(
            is_active=True, author__public_article=True
        ).order_by("-write_date")[:limit]


@extend_schema(
    summary="نوشتن مقاله جدید",
    description="ساخت مقاله با استفاده از توکن API.",
    request=ArticleCreateSerializer,
    responses={
        200: OpenApiExample(
            "مقاله با موفقیت ساخته شد",
            value={
                "status": 200,
                "description": "Article 'Title' created successfully.",
                "article_id": 12,
            },
        ),
        400: OpenApiExample(
            "خطای اعتبارسنجی",
            value={"status": 400, "errors": {"title": ["This field is required."]}},
        ),
    },
)

@method_decorator(csrf_exempt, name='dispatch')
class WriteArticle(APIView):
    authentication_classes = []
    permission_classes = [HasValidApiToken]

    def post(self, request, token):
        data = request.data.copy()

        if not data.get("title"):
            return Response({"title": ["This field is required."]}, status=400)
        if not data.get("categories"):
            return Response({"categories": ["This field is required."]}, status=400)

        if not data.get("slug"):
            data["slug"] = slugify(data["title"])

        serializer = ArticleCreateSerializer(data=data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)

        article = serializer.save(author=request.api_entry.user)

        return Response({
            "status": 200,
            "description": f"Article '{article.title}' created successfully.",
            "article_id": article.id
        })

class ApiTokenCreateView(LoginRequiredMixin, View):
    template_name = "api/token-create.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        raw_token = ApiModel.generate_token()
        api_instance = ApiModel.objects.create(
            api_name=request.POST.get("api_name", "default_name"),
            key=ApiModel.hash_token(raw_token),
            user=request.user
        )
        return render(request, self.template_name, {
            "api_token": raw_token,
            "api_instance": api_instance
        })
