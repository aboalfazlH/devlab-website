from social_core.exceptions import AuthAlreadyAssociated
from social_django.models import UserSocialAuth
from .models import CustomUser

def create_user_if_not_exists(strategy, details, backend, uid, user=None, *args, **kwargs):
    if user:
        UserSocialAuth.objects.get_or_create(user=user, provider=backend.name, uid=uid)
        return {'is_new': False, 'user': user}

    email = details.get('email')
    username = details.get('username') or (email.split('@')[0] if email else None)

    if email:
        try:
            user = CustomUser.objects.get(email=email)
            UserSocialAuth.objects.get_or_create(user=user, provider=backend.name, uid=uid)
            return {'is_new': False, 'user': user}
        except CustomUser.DoesNotExist:
            pass

    user_data = {
        'username': username,
        'email': email,
    }

    try:
        new_user = strategy.create_user(**user_data)
        UserSocialAuth.objects.get_or_create(user=new_user, provider=backend.name, uid=uid)
        return {'is_new': True, 'user': new_user}
    except Exception as e:
        raise AuthAlreadyAssociated(f"This account is already associated: {str(e)}")
