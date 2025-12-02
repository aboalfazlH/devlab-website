from rest_framework import serializers
from apps.blog.models import Article
from django.utils.html import strip_tags


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for representing Article objects as JSON."""

    categories = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    author = serializers.CharField(source="author.get_full_name")

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "thumbnail",
            "description",
            "views",
            "author",
            "write_date",
            "is_pin",
            "is_active",
            "categories",
        ]

    def get_categories(self, obj):
        return list(obj.categories.values("id", "name"))

    def get_description(self, obj):
        """Return plain text without HTML tags."""
        return strip_tags(obj.description)

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["title", "description", "slug", "thumbnail", "categories", "is_pin", "is_active"]