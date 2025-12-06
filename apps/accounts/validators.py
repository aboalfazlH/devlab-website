from django.core.exceptions import ValidationError
import re

def validate_git_url(value):
    """Validate that the URL is from github.com or gitlab.com"""
    pattern = r"^https?://(www\.)?(github\.com|gitlab\.com)/.+$"
    if not re.match(pattern, value):
        raise ValidationError("لینک باید فقط از github.com یا gitlab.com باشد.")

def validate_facebook_link(value):
    pattern = r"^https?:\/\/(www\.)?facebook\.com\/[A-Za-z0-9_.-]+\/?$"
    if not re.match(pattern, value):
        raise ValidationError("فقط لینک معتبر Facebook وارد کنید.")

def validate_instagram_link(value):
    pattern = r"^https?:\/\/(www\.)?instagram\.com\/[A-Za-z0-9_.-]+\/?$"
    if not re.match(pattern, value):
        raise ValidationError("فقط لینک معتبر Instagram وارد کنید.")

def validate_linkedin_link(value):
    pattern = (
        r"^https?:\/\/(www\.)?linkedin\.com\/(in|company)\/[A-Za-z0-9_.-]+\/?$"
    )
    if not re.match(pattern, value):
        raise ValidationError("فقط لینک معتبر لینکدین وارد کنید.")

def validate_telegram_link(value):
    pattern = r"^https?:\/\/(t\.me)\/[A-Za-z0-9_]{5,32}$"
    if not re.match(pattern, value):
        raise ValidationError(
            "فقط لینک معتبر Telegram وارد کنید. مثال: https://t.me/username"
        )

def validate_phone_number(value):
    pattern = r"^(\+98|0)?9\d{9}$"
    if not re.match(pattern, value):
        raise ValidationError("لطفا یک شماره ایرانی معتبر وارد کند")
