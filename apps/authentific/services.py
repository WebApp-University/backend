from .models import User
from .passwords import hash_password, check_password
import jwt
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


def generate_jwt(user, lifetime_minutes=60):
    payload = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "exp": timezone.now() + timedelta(minutes = lifetime_minutes),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm = "HS256")
    return token


def register_user(username, email, password):

    hashed_password = hash_password(password)

    user = User.objects.create(
        username = username, email = email, password = hashed_password
    )

    token = generate_jwt(user)
    return user, token


def authenticate_user(email, password):
    try:
        user = User.objects.get(email = email)

        if check_password(password, user.password):
            token = generate_jwt(user)
            return user, token

        return None, None

    except User.DoesNotExist:
        return None, None